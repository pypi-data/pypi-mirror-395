import teradataml as tdml
import datetime
from tdfs4ds import logger, logger_safe
import re

import tdfs4ds
import numpy as np
import pandas as pd


def get_hidden_table_name(schema_name, view_name):
    """
    Return the backing 'hidden' table name for a public view/table.

    Args:
        table_name (str): Public-facing table/view name.

    Returns:
        str: The corresponding hidden table name (suffix '_HIDDEN').
    """

    try:
        view_name = tdfs4ds.utils.lineage.get_ddl(schema_name=schema_name, view_name=view_name).split('\n')[-2].split('.')[1]
        return view_name
    except Exception as e:
        logger_safe("warning", "Failed to extract hidden table name from DDL; defaulting to suffix method.", str(e).split('\n')[0])
        return view_name + "_HIDDEN"


class TimeManager:
    """
    Manage versioned business time steps behind a Teradata-backed public view.

    `TimeManager` stores a sequence of time “snapshots” in a hidden physical
    table (`<view_name>_HIDDEN`) with two columns:
    - `TIME_ID` (1..N): the step index, assigned deterministically via
      `ROW_NUMBER()` over the input time column.
    - `BUSINESS_DATE`: the business date/time associated with each step. When
      loading, the SQL type is inferred and upcast to `TIMESTAMP WITH TIME ZONE`
      when needed to preserve offsets.

    A companion public view (`<view_name>`) always exposes the *current* business
    date by filtering the hidden table on a single `TIME_ID`. Changing the
    current step only rewrites the view definition—no data is mutated.

    Key capabilities
    - Load/replace the hidden table from a pandas DataFrame (`load_time_steps`).
    - Switch the active time step by `TIME_ID` (`update`).
    - Inspect the current date/time (`display`, `get_date_in_the_past`).
    - Generate a timeline view up to (or strictly before) the current step
      (`generate_timeline`).
    - Prune older steps and renumber so the earliest remaining step becomes 1
      (`prune_time`).
    - Clone from another `TimeManager` (soft link or hard copy) and optionally
      take ownership of the hidden table (`clone_timer`, `take_ownership`).
    - Introspect the active step by parsing the view DDL (`get_current_timeid`,
      `print_view_ddl`).

    Workflow overview
      1) Instantiate `TimeManager` with a target `view_name` and `schema_name`.
      2) Call `load_time_steps(df, time_column)` to (re)create the hidden table and
         point the public view at `TIME_ID = 1`.
      3) Use `update(time_id)` to switch the active business date.
      4) (Optional) Create derivative timeline views, prune older steps, or clone.

    Parameters
        table_name (str): Base public view name to manage (e.g., "MY_VIEW").
        schema_name (str): Teradata schema/database that holds the artifacts.

    Attributes
        schema_name (str): Target schema for the view and hidden table.
        table_name (str): Hidden table name (`<view_name>_HIDDEN`).
        view_name (str): Public view name (`<view_name>`).
        time_id (str): Name of the step identifier column (default: "time_id").
        nb_time_steps (int | None): Number of steps detected after load/inspection.
        data_type (str | None): SQL data type of `BUSINESS_DATE` (e.g., `DATE`,
            `TIMESTAMP WITH TIME ZONE`), inferred during load/inspection.

    Notes
        - On initialization, if the hidden table already exists, metadata
          (`data_type`, `nb_time_steps`) is auto-detected.
        - `load_time_steps` will drop and recreate the hidden table to match the
          inferred schema, then rebuild the public view.
        - “Soft” cloning points this manager’s view at the source hidden table;
          “hard” cloning copies the table into this schema and marks it owned.
        - Ownership controls whether `_drop()` is allowed to remove the hidden
          table (use `take_ownership` to promote ownership when appropriate).
    """

    def __init__(self, table_name: str, schema_name: str) -> None:
        """Initialize a TimeManager for an existing or future hidden table/view.

        On initialization, if the hidden table already exists, the instance
        inspects it to populate ``data_type`` and ``nb_time_steps``.

        Args:
            table_name: Base public view name to manage (e.g., ``"MY_VIEW"``).
            schema_name: Schema that contains/should contain the objects.
        """
        self.schema_name   = schema_name
        self.table_name    = get_hidden_table_name(schema_name=schema_name,view_name=table_name)
        self.view_name     = table_name
        self.time_id       = 'time_id'
        self.nb_time_steps = None
        self.data_type     = None

        logger.debug(
            "Initializing TimeManager for schema=%s, view=%s, table=%s",
            self.schema_name, self.view_name, self.table_name
        )

        if self._exists():
            logger.debug("Hidden table %s.%s exists; inspecting metadata.", self.schema_name, self.table_name)
            df = tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))
            d_ = {x[0]: x[1] for x in df._td_column_names_and_types}
            self.data_type = d_.get('BUSINESS_DATE')
            self.nb_time_steps = tdml.execute_sql(
                f"SEL MAX(TIME_ID) AS nb_time_steps FROM {self.schema_name}.{self.table_name}"
            ).fetchall()[0][0]
            logger.info(
                "Detected BUSINESS_DATE data_type=%s with nb_time_steps=%s",
                self.data_type, self.nb_time_steps
            )

    def load_time_steps(self, df: pd.DataFrame, time_column: str) -> None:
        """Load/replace the hidden table and (re)point the public view to step 1.

        Workflow:
          1) Build a DataFrame with sequential ``TIME_ID`` and ``BUSINESS_DATE``.
          2) Infer SQL types and upcast to ``TIMESTAMP WITH TIME ZONE`` when
             needed (to preserve offsets).
          3) Drop and recreate the hidden table with inferred schema.
          4) Append the rows.
          5) Replace the public view to expose ``TIME_ID = 1``.
          6) Store ``nb_time_steps``.

        Args:
            df: Input pandas DataFrame with a time column.
            time_column: Name of the time column in ``df`` to use as ``BUSINESS_DATE``.
        """
        logger.info("Loading time steps into %s.%s from column '%s'.",
                    self.schema_name, self.table_name, time_column)

        # Step 1: Build DataFrame with TIME_ID and BUSINESS_DATE
        df_ = df.assign(
            time_id=tdml.sqlalchemy.literal_column(
                f"ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY {time_column})",
                tdml.BIGINT()
            ),
            BUSINESS_DATE=df[time_column]
        )[["time_id", "BUSINESS_DATE"]]
        logger.debug("Constructed intermediate DataFrame with TIME_ID and BUSINESS_DATE.")

        # Step 2: Get SQL types and adjust BUSINESS_DATE if necessary
        sql_types = tdfs4ds.utils.info.get_feature_types_sql_format(df_)
        type_business_date = sql_types["BUSINESS_DATE"]

        if "TIMESTAMP" in type_business_date.upper() and "ZONE" not in type_business_date.upper():
            new_type = f"{type_business_date} WITH TIME ZONE"
            logger.info(
                "Upcasting BUSINESS_DATE from %s to %s to preserve timezone.",
                type_business_date, new_type
            )
            type_business_date = new_type
            sql_types["BUSINESS_DATE"] = new_type

            df_ = df_.assign(
                BUSINESS_DATE=tdml.sqlalchemy.literal_column(
                    f"CAST(BUSINESS_DATE AS {new_type})"
                )
            )

        self.data_type = type_business_date
        logger.debug("Final BUSINESS_DATE SQL type: %s", self.data_type)

        # Step 3: Drop table if it exists
        try:
            tdml.execute_sql(f"DROP TABLE {self.schema_name}.{self.table_name}")
            logger.debug("Dropped existing table %s.%s (if existed).", self.schema_name, self.table_name)
        except Exception as e:
            # Not fatal; the table might not exist. Log at debug when in dev, warning otherwise.
            e_str = str(e).split('\n')[0]
            msg = f"Error dropping table {self.schema_name}.{self.table_name}: {e_str}"
            if tdfs4ds.DEBUG_MODE:
                logger.debug(msg)
            else:
                logger.warning(msg)

        # Step 4: Recreate table
        ddl = ",\n".join([f"{col} {dtype}" for col, dtype in sql_types.items()])
        create_table_sql = f"""
            CREATE TABLE {self.schema_name}.{self.table_name} (
                {ddl}
            )
            PRIMARY INDEX (time_id)
        """
        tdml.execute_sql(create_table_sql)
        logger.info("Created table %s.%s with schema: %s", self.schema_name, self.table_name, sql_types)

        # Step 5: Insert data
        df_[list(sql_types.keys())].to_sql(
            table_name=self.table_name,
            schema_name=self.schema_name,
            if_exists="append"
        )
        logger.info("Inserted %s time steps into %s.%s.", df_.shape[0], self.schema_name, self.table_name)

        # Step 6: Update view
        create_view_sql = f"""
            REPLACE VIEW {self.schema_name}.{self.view_name} AS
            SELECT BUSINESS_DATE
            FROM {self.schema_name}.{self.table_name}
            WHERE time_id = 1
        """
        tdml.execute_sql(create_view_sql)
        logger.debug("Replaced view %s.%s to point at TIME_ID=1.", self.schema_name, self.view_name)

        # Step 7: Store number of time steps
        result = tdml.execute_sql(
            f"SELECT MAX(time_id) AS nb_filters FROM {self.schema_name}.{self.table_name}"
        ).fetchall()
        self.nb_time_steps = result[0][0]
        logger.info("Time steps loaded. nb_time_steps=%s", self.nb_time_steps)

    def _exists(self) -> bool:
        """Check if the hidden table exists in the schema.

        Returns:
            True if the hidden table exists; False otherwise.
        """
        exists = len([
            x for x in tdml.db_list_tables(schema_name=self.schema_name).TableName.values
            if x.lower().replace('"', '') == self.table_name.lower()
        ]) > 0
        logger.debug("Hidden table %s.%s exists? %s", self.schema_name, self.table_name, exists)
        return exists

    def _drop(self, drop_view: bool = False, force: bool = False) -> None:
        """Drop the hidden table if we own it, and optionally the public view.

        Args:
            drop_view: If True, also drop the public view.
            force: If True, drop the hidden table even if we don't own it.

        Notes:
            - The hidden table is dropped only if:
                * self._owns_hidden is True, or
                * force is True.
            - The view can be dropped regardless of ownership when drop_view=True.
        """
        # Drop hidden table
        if self._exists():
            if getattr(self, "_owns_hidden", False) or force:
                logger.info(
                    "Dropping hidden table %s.%s (force=%s).",
                    self.schema_name, self.table_name, force
                )
                tdml.db_drop_table(schema_name=self.schema_name, table_name=self.table_name)
            else:
                logger.warning(
                    "Refusing to drop hidden table %s.%s because this manager does not own it. "
                    "Use force=True to override.",
                    self.schema_name, self.table_name
                )
        else:
            logger.debug("Hidden table %s.%s does not exist.", self.schema_name, self.table_name)

        # Optionally drop view
        if drop_view:
            try:
                logger.info("Dropping view %s.%s.", self.schema_name, self.view_name)
                tdml.execute_sql(f"DROP VIEW {self.schema_name}.{self.view_name}")
            except Exception as e:
                logger.warning("Error dropping view %s.%s: %s", self.schema_name, self.view_name, e)


    def update(self, time_id: int) -> None:
        """Point the public view at a specific ``TIME_ID``.

        Args:
            time_id: The time step identifier to expose via the public view.
        """
        if self._exists():
            query = f"""
            REPLACE VIEW {self.schema_name}.{self.view_name} AS
            SEL BUSINESS_DATE
            FROM {self.schema_name}.{self.table_name}
            WHERE TIME_ID = {time_id}
            """
            if getattr(tdfs4ds, "DEBUG_MODE", False):
                logger_safe("debug", "Executing view update:\n%s", query)

            tdml.execute_sql(query)
            logger_safe("info", "Updated view %s.%s to TIME_ID=%s.", self.schema_name, self.view_name, time_id)

        else:
            logger_safe(
                "warning",
                "Cannot update view: hidden table %s.%s does not exist.",
                self.schema_name, self.table_name
            )

    def display(self) -> pd.DataFrame:
        """Return the current public view (one row: current BUSINESS_DATE).

        Returns:
            A pandas DataFrame with the current ``BUSINESS_DATE`` exposed by the view.
        """
        logger.debug("Reading current BUSINESS_DATE from %s.%s.", self.schema_name, self.view_name)
        cols = tdml.DataFrame(tdml.in_schema(self.schema_name, self.view_name)).columns
        return pd.DataFrame(
            tdml.execute_sql(f"SEL * FROM {self.schema_name}.{self.view_name}").fetchall(),
            columns=cols
        )

    def get_date_in_the_past(self) -> str | None:
        """Return the earliest BUSINESS_DATE from the public view as a string.

        The format includes timezone offset when applicable:
        - ``YYYY-MM-DD HH:MM:SS±HH:MM`` if timezone info is present;
        - otherwise ``YYYY-MM-DD HH:MM:SS``.

        Returns:
            The formatted earliest date/time string, or ``None`` if parsing fails.
        """
        date_obj = self.display().BUSINESS_DATE.iloc[0]
        logger.debug("Raw earliest BUSINESS_DATE value read: %r (%s)", date_obj, type(date_obj))

        if isinstance(date_obj, pd.Timestamp):
            datetime_obj = date_obj.to_pydatetime()
        elif isinstance(date_obj, datetime.datetime):
            datetime_obj = date_obj
        elif isinstance(date_obj, datetime.date):
            datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        elif isinstance(date_obj, np.datetime64):
            datetime_obj = pd.to_datetime(date_obj).to_pydatetime()
        else:
            logger.warning("Unrecognized BUSINESS_DATE type: %s; value=%r", type(date_obj), date_obj)
            return None

        if datetime_obj.tzinfo is not None and datetime_obj.tzinfo.utcoffset(datetime_obj) is not None:
            output_string = datetime_obj.isoformat(sep=' ', timespec='seconds')
        else:
            output_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

        logger.debug("Formatted earliest BUSINESS_DATE: %s", output_string)
        return output_string

    def get_list_date(self) -> tdml.DataFrame:
        """Return the full list of time steps from the hidden table.

        Returns:
            A Teradata DataFrame over ``schema.table`` (hidden table) with
            ``TIME_ID`` and ``BUSINESS_DATE``.
        """
        logger.debug("Returning Teradata DataFrame for %s.%s.", self.schema_name, self.table_name)
        return tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))

    def generate_timeline(self, schema_name: str, view_name: str, current_included: bool = True) -> tdml.DataFrame:
        """Create a timeline view filtered relative to the current business date.

        The new view (``schema_name.view_name``) selects dates from the hidden
        source (``self.view_name + '_HIDDEN'``) up to the current business date
        exposed by the public view (``self.view_name``).

        Args:
            schema_name: Schema where the new timeline view will be created.
            view_name: Name of the new timeline view.
            current_included: If True, include the current business date;
                otherwise, exclude it.

        Returns:
            A Teradata DataFrame bound to the newly replaced timeline view.
        """
        logger.info(
            "Generating timeline view %s.%s (current_included=%s).",
            schema_name, view_name, current_included
        )
        query = f"""
        REPLACE VIEW {schema_name}.{view_name} AS
        SEL BUSINESS_DATE
        FROM {self.schema_name}.{self.view_name + '_HIDDEN'} A
        """
        if current_included:
            query += f"WHERE BUSINESS_DATE <= (SELECT BUSINESS_DATE FROM {self.schema_name}.{self.view_name})"
        else:
            query += f"WHERE BUSINESS_DATE < (SELECT BUSINESS_DATE FROM {self.schema_name}.{self.view_name})"

        tdml.execute_sql(query)
        logger.debug("Replaced timeline view with query:\n%s", query.strip())
        return tdml.DataFrame(tdml.in_schema(schema_name, view_name))

    def get_current_step(self) -> int | None:
        """Return the TIME_ID corresponding to the current BUSINESS_DATE in the view.

        Returns:
            The current ``TIME_ID`` if exactly one match is found; otherwise ``None``.
        """
        # Note: original code omits schema qualifiers here; kept intentionally.
        logger.debug("Fetching current TIME_ID from %s and %s.", self.table_name, self.view_name)
        res = tdml.execute_sql(
            f"SELECT TIME_ID FROM {self.table_name} "
            f"WHERE BUSINESS_DATE = (SELECT BUSINESS_DATE FROM {self.view_name})"
        ).fetchall()

        if len(res) == 1:
            logger.info("Current TIME_ID resolved to %s.", res[0][0])
            return res[0][0]

        logger.warning("Could not resolve a unique current TIME_ID (rows returned: %s).", len(res))
        return None

    def clone_timer(
        self,
        source_timemanager,
        time_id_to_apply: int = 1,
        take_ownership: bool = False,
        clone_mode: str = "soft",
        if_exists: str = "error",
    ):
        """
        Clone time-step definitions from another TimeManager.

        Supports:
        - soft clone (default): point this manager's view to the source _HIDDEN table
        - hard clone: copy the source _HIDDEN table into this schema and own the copy

        Args:
            source_timemanager (TimeManager): Source manager to clone from.
            time_id_to_apply (int, optional): TIME_ID to activate in the public view. Default: 1.
            take_ownership (bool, optional): For soft clones only, whether this
                manager should consider itself the owner of the hidden table.
                (Hard clones always own their copy.) Default: False.
            clone_mode (str, optional): "soft" or "hard". Default: "soft".
            if_exists (str, optional): What to do if the destination hidden table already exists
                - "error" (default): raise an exception
                - "replace": drop and recreate
                - "skip": reuse existing table

        Returns:
            TimeManager: self

        Raises:
            ValueError: On invalid clone_mode/if_exists or missing source table.
            RuntimeError: If destination exists and if_exists="error".
        """
        if clone_mode not in ("soft", "hard"):
            raise ValueError("clone_mode must be 'soft' or 'hard'")
        if if_exists not in ("error", "replace", "skip"):
            raise ValueError("if_exists must be 'error', 'replace', or 'skip'")

        src_schema = source_timemanager.schema_name
        src_hidden = source_timemanager.table_name

        logger.info(
            "Cloning timer",
            extra={
                "mode": clone_mode,
                "source": f"{src_schema}.{src_hidden}",
                "target_view": f"{self.schema_name}.{self.view_name}",
            },
        )

        # Validate source existence
        existing_src = [t.lower() for t in tdml.db_list_tables(schema_name=src_schema).TableName.values]
        if src_hidden.lower() not in existing_src:
            raise ValueError(f"Source hidden timer table {src_schema}.{src_hidden} does not exist.")

        if clone_mode == "hard":
            # Hard clone → create (or reuse) a NEW hidden table in this schema
            self.table_name = get_hidden_table_name(schema_name=self.schema_name, view_name=self.view_name)
            existing_dest = [t.lower() for t in tdml.db_list_tables(schema_name=self.schema_name).TableName.values]

            if self.table_name.lower() in existing_dest:
                if if_exists == "error":
                    raise RuntimeError(f"Target table {self.schema_name}.{self.table_name} already exists.")
                elif if_exists == "replace":
                    logger.warning("Replacing existing table %s.%s", self.schema_name, self.table_name)
                    tdml.db_drop_table(schema_name=self.schema_name, table_name=self.table_name)
                elif if_exists == "skip":
                    logger.info("Skipping clone, using existing %s.%s", self.schema_name, self.table_name)

            if self.table_name.lower() not in existing_dest or if_exists == "replace":
                logger.info("Creating cloned table %s.%s", self.schema_name, self.table_name)
                create_sql = f"""
                CREATE TABLE {self.schema_name}.{self.table_name} AS
                    (SELECT * FROM {src_schema}.{src_hidden})
                WITH DATA
                """
                tdml.execute_sql(create_sql)

            self._owns_hidden = True
            target_schema = self.schema_name

        else:
            # Soft clone → just point to the source hidden table
            logger.info("Soft clone: linking view to source hidden table")
            self.table_name = src_hidden
            self._owns_hidden = bool(take_ownership)
            target_schema = src_schema  # view will select from the source schema

        # Load metadata from the target hidden table
        df_meta = tdml.DataFrame(tdml.in_schema(target_schema, self.table_name))
        # Get data type for BUSINESS_DATE (if present)
        try:
            dtypes = {c: t for c, t in df_meta._td_column_names_and_types}
            self.data_type = dtypes.get("BUSINESS_DATE")
        except Exception:
            self.data_type = None

        self.nb_time_steps = tdml.execute_sql(
            f"SEL MAX(TIME_ID) FROM {target_schema}.{self.table_name}"
        ).fetchall()[0][0]

        # Rebuild the public view to the requested TIME_ID
        view_sql = f"""
        REPLACE VIEW {self.schema_name}.{self.view_name} AS
        SELECT BUSINESS_DATE
        FROM {target_schema}.{self.table_name}
        WHERE TIME_ID = {int(time_id_to_apply)}
        """
        tdml.execute_sql(view_sql)

        logger.info(
            "Timer clone complete → Active TIME_ID=%s; nb_time_steps=%s; data_type=%s",
            time_id_to_apply, self.nb_time_steps, self.data_type
        )
        return self

    def take_ownership(
        self,
        create_copy: bool = True,
        if_exists: str = "error",
    ) -> "TimeManager":
        """Promote this manager to OWN the hidden table.

        Two modes:
        - create_copy=True (default): Hard-promote by copying the current source
            hidden table into this manager's schema as <view>_HIDDEN, repoint the
            view, and set ownership.
        - create_copy=False: Only mark as owned if the current hidden table is
            already <schema=self.schema_name, table=<view>_HIDDEN>. Otherwise, warn.

        Args:
            create_copy: If True, copy data into this schema and repoint view.
            if_exists: Behavior when the destination <view>_HIDDEN already exists:
                - "error" (default): raise
                - "replace": drop & recreate
                - "skip": reuse existing

        Returns:
            TimeManager: self
        """
        if if_exists not in ("error", "replace", "skip"):
            raise ValueError("if_exists must be 'error', 'replace', or 'skip'")

        # Figure out current active TIME_ID to preserve selection after repointing
        try:
            current_time_id = self.get_current_step()
        except Exception:
            current_time_id = None
        if current_time_id is None:
            current_time_id = 1

        dest_table = get_hidden_table_name(schema_name=self.schema_name, view_name=self.view_name)

        if not create_copy:
            # Only mark as owned if we already match <schema, view_HIDDEN>
            if self.schema_name and self.table_name == dest_table:
                logger.info(
                    "Marking existing hidden table %s.%s as owned (no copy).",
                    self.schema_name, self.table_name
                )
                self._owns_hidden = True
                return self
            logger.warning(
                "Cannot take ownership without copying: current table is %s (expected %s). "
                "Re-run with create_copy=True to copy into %s.%s.",
                self.table_name, dest_table, self.schema_name, dest_table
            )
            return self

        # We will copy data into <self.schema_name>.<view>_HIDDEN
        dest_exists = [
            t.lower() for t in tdml.db_list_tables(schema_name=self.schema_name).TableName.values
        ]
        need_create = True

        if dest_table.lower() in dest_exists:
            if if_exists == "error":
                raise RuntimeError(f"Destination table {self.schema_name}.{dest_table} already exists.")
            elif if_exists == "replace":
                logger.warning("Replacing existing table %s.%s", self.schema_name, dest_table)
                tdml.db_drop_table(schema_name=self.schema_name, table_name=dest_table)
            elif if_exists == "skip":
                logger.info("Reusing existing destination table %s.%s", self.schema_name, dest_table)
                need_create = False

        if need_create:
            logger.info(
                "Creating owned copy %s.%s from current source %s.%s",
                self.schema_name, dest_table, self.schema_name, self.table_name
            )
            # The current table might be in another schema; qualify from the DataFrame binding
            # Derive the true source schema for safety
            # (If you know it's always schema-qualified in self.table_name, keep as-is.)
            src_schema = self.schema_name if self._exists() else None
            # Fallback to probing the DataFrame binding for schema
            if src_schema is None:
                logger.debug("Could not verify source schema via _exists(); defaulting to self.schema_name.")
                src_schema = self.schema_name

            create_sql = f"""
            CREATE TABLE {self.schema_name}.{dest_table} AS
                (SELECT * FROM {src_schema}.{self.table_name})
            WITH DATA
            """
            tdml.execute_sql(create_sql)

        # Repoint this manager to the new owned table and rebuild the view
        self.table_name = dest_table
        self._owns_hidden = True

        view_sql = f"""
        REPLACE VIEW {self.schema_name}.{self.view_name} AS
        SELECT BUSINESS_DATE
        FROM {self.schema_name}.{self.table_name}
        WHERE TIME_ID = {int(current_time_id)}
        """
        tdml.execute_sql(view_sql)

        # Refresh metadata
        try:
            df_meta = tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))
            dtypes = {c: t for c, t in df_meta._td_column_names_and_types}
            self.data_type = dtypes.get("BUSINESS_DATE")
        except Exception:
            pass
        self.nb_time_steps = tdml.execute_sql(
            f"SEL MAX(TIME_ID) FROM {self.schema_name}.{self.table_name}"
        ).fetchall()[0][0]

        logger.info(
            "Ownership taken for %s.%s. Active TIME_ID=%s; nb_time_steps=%s; data_type=%s",
            self.schema_name, self.table_name, current_time_id, self.nb_time_steps, self.data_type
        )
        return self

    def get_current_timeid(self) -> int:
        """
        Extract the currently active TIME_ID from the public view's DDL.

        Returns:
            int: TIME_ID parsed from the view definition.

        Raises:
            ValueError: If the TIME_ID cannot be parsed from the DDL.
        """
        logger.debug("Reading view DDL to extract current TIME_ID")
        txt = tdfs4ds.utils.lineage.get_ddl(schema_name=self.schema_name, view_name=self.view_name)

        # Look for "WHERE TIME_ID = <number>" (allow whitespace/case variations)
        m = re.search(r"WHERE\s+TIME_ID\s*=\s*(\d+)", txt, flags=re.IGNORECASE)
        if not m:
            logger.exception("Failed to parse TIME_ID from view DDL")
            raise ValueError("Unable to parse current TIME_ID from view DDL.")
        current = int(m.group(1))
        logger.info("Current TIME_ID extracted", extra={"time_id": current})
        return current


    def print_view_ddl(self) -> None:
        """
        Log the view definition (DDL) for troubleshooting/traceability.
        """
        ddl = tdfs4ds.utils.lineage.get_ddl(schema_name=self.schema_name, view_name=self.view_name)
        logger.info("View DDL:\n%s", ddl)


    def prune_time(self, time_id: int | None = None):
        """
        Remove all time steps with TIME_ID lower than `time_id` and renumber remaining ones.

        If `time_id` is omitted, the method uses the current TIME_ID from the view.
        After pruning, TIME_ID values are normalized so the smallest remaining id becomes 1,
        and the public view is repointed to TIME_ID=1.

        Args:
            time_id (int, optional): Threshold id; rows with TIME_ID < time_id are deleted.

        Returns:
            TimeManager: Self, to allow method chaining.
        """
        if time_id is None:
            time_id = self.get_current_timeid()

        logger.info("Pruning time steps", extra={"threshold_time_id": time_id})

        delete_sql = f"""
            DELETE {self.schema_name}.{self.table_name}
            WHERE TIME_ID < {int(time_id)}
        """
        update_sql = f"""
            UPDATE {self.schema_name}.{self.table_name}
            SET TIME_ID = TIME_ID - {int(time_id)} + 1
        """

        logger.debug("Executing prune delete", extra={"sql": delete_sql})
        tdml.execute_sql(delete_sql)

        logger.debug("Executing prune renumber", extra={"sql": update_sql})
        tdml.execute_sql(update_sql)

        # Refresh metadata and repoint view to TIME_ID=1
        self.update(1)
        self.nb_time_steps = tdml.execute_sql(
            f"SEL MAX(TIME_ID) FROM {self.schema_name}.{self.table_name}"
        ).fetchall()[0][0]

        logger.info(
            "Prune complete; active TIME_ID set to 1; nb_time_steps=%s",
            self.nb_time_steps
        )
        return self
