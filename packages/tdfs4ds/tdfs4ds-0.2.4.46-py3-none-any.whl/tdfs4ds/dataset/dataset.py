import teradataml as tdml
from tdfs4ds.utils.info import get_feature_types_sql_format
from tdfs4ds import logger

class Dataset:

    def __init__(self, view_name=None, schema_name=None, df=None):

        if df is not None:
            self.df          = df
            df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)
            view_name = df._table_name
            if '.' in view_name:            
                self.view_name   = view_name.split('.')[1]
                self.schema_name = view_name.split('.')[0]
            else:
                self.view_name   = view_name
                self.schema_name = tdml.context.context._get_current_databasename()
        elif view_name is not None and schema_name is not None:
            self.view_name   = view_name
            self.schema_name = schema_name
            if view_name.lower() in  map(str.lower, tdml.db_list_tables(object_type='view', schema_name=self.schema_name).TableName.values):
                self.df      = tdml.DataFrame(tdml.in_schema(schema_name, view_name))
            else:
                print(f"{self.view_name} not found in {self.schema_name} database")
                self.df      = None
        else:
            raise ValueError("Either df or both view_name and schema_name must be provided.")
        
        self.valid_time   = self._get_validtime()
        self.dataset_type = self._get_dataset_type()
        self.entity, self.features     = self._retrieve_entities_and_features()
        
    
    def get_dataframe(self):
        return self.df
    
    def __repr__(self):
        return f"Dataset(view_name={self.view_name}, schema_name={self.schema_name}, df={type(self.df)})"
    
    def __getattr__(self, item):
        if self.df is not None:
            return getattr(self.df, item)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")
    
    def _retrieve_entities_and_features_old(self):

        if self._get_dataset_type() == 'snapshot':

            blocks = [x.split(')')[0] for x in self._get_ddl().split('(')]
            feature_names    = [blocks[i].replace('\n','').split('AS ')[1].split('FROM')[0].strip() for i in range(1,len(blocks)) if i % 2 == 1]
            feature_ids      = [int(blocks[i].replace('\n','').split('=')[1].split('AND')[0].strip()) for i in range(1,len(blocks)) if i % 2 == 0]
            feature_versions = [blocks[i].replace('\n','').split('=')[2].replace("'",'').strip() for i in range(1,len(blocks)) if i % 2 == 0]
            
            feature_database = [blocks[i].replace('\n','').split('"')[1].strip() for i in range(1,len(blocks)) if i % 2 == 1]
            feature_view     = [blocks[i].replace('\n','').split('"')[3].strip() for i in range(1,len(blocks)) if i % 2 == 1]

            columns_types    = get_feature_types_sql_format(self.df)
            feature_types    = [columns_types[f] for f in feature_names]

            features = {}
            for n,i,v,t,d,vv in zip(feature_names, feature_ids, feature_versions, feature_types, feature_database, feature_view):
                features[n.upper()] = {'id' : i, 'version': v, 'type': t.upper(), 'database' : d.upper(), 'view' : vv.upper()}

            
            entity_names     = [x.strip().split('.')[1] for x in blocks[0].split('SELECT')[1].split('FROM')[0].replace('\n','').split(',') if x.strip().startswith('A1') if x.strip().split('.')[1] not in feature_names]
            entity_types     = [columns_types[e] for e in entity_names]

            entity = {}
            for n,t in zip(entity_names, entity_types):
                entity[n] = t

            return entity, features
        else:
            logger.error(f"not implemented yet for dataset type: {self._get_dataset_type()}")
            raise
    
    def _retrieve_entities_and_features(self):
        if self._get_dataset_type() != 'snapshot':
            logger.error(f"not implemented yet for dataset type: {self._get_dataset_type()}")
            raise

        import re

        ddl = self._get_ddl()

        # Column types from the materialized dataframe
        columns_types = get_feature_types_sql_format(self.df)

        # Regex to capture each feature subquery:
        #  - grabs feature name alias, FEATURE_ID, FEATURE_VERSION
        #  - grabs database and view/table (quoted or unquoted)
        pattern = re.compile(
            r"""
            SEQUENCED\s+VALIDTIME\s+SELECT
            .*?                               # anything before the feature value
            B1\.FEATURE_VALUE\s+AS\s+(?P<fname>[A-Za-z_][\w]*)   # AS <feature_name>
            \s+FROM\s+
            (?:
                "(?P<dbq>[^"]+)"\."(?P<viewq>[^"]+)"             # "DB"."VIEW"
                |
                (?P<db>[A-Za-z_]\w*)\.(?P<view>[A-Za-z_]\w*)     # DB.VIEW
            )
            \s+B1\s+WHERE\s*\(
                \s*FEATURE_ID\s*=\s*(?P<fid>\d+)\s+
                AND\s+FEATURE_VERSION\s*=\s*'(?P<fver>[^']+)'
            \s*\)
            """,
            re.IGNORECASE | re.DOTALL | re.VERBOSE
        )

        features = {}
        for m in pattern.finditer(ddl):
            fname = m.group('fname')
            fid   = int(m.group('fid'))
            fver  = m.group('fver')
            db    = (m.group('dbq') or m.group('db') or '').upper()
            view  = (m.group('viewq') or m.group('view') or '').upper()
            ftype = columns_types[fname].upper()
            features[fname.upper()] = {
                'id': fid,
                'version': fver,
                'type': ftype,
                'database': db,
                'view': view
            }

        # Anything in the dataframe that isn't a feature column is an entity column.
        feature_names_upper = set(features.keys())
        entity_names = [c for c in self.df.columns if c.upper() not in feature_names_upper]
        entity = {n: columns_types[n] for n in entity_names}

        return entity, features
    
    def _get_dataset_type(self):
        return 'snapshot'
    
    def _get_validtime(self):
        if self._get_dataset_type() == 'snapshot':
            return self._get_ddl().split('\n')[4].strip()
        else:
            logger.error(f"not implemented yet for dataset type: {self._get_dataset_type()}")
        return ''

    def _get_feature_store_database(self):

        databases = [self.features[k]['database'] for k in self.features.keys()]
        databases = list(set(databases))
        if len(databases) == 1:
            self.feature_store_database = databases[0]
        elif len(databases) > 1:
            logger.warning(f"features are stored in multiple databases: {databases}")
        else:
            logger.error(f"unable to identify the feature store database")
            raise
        
    
    def _get_ddl(self):
        return tdml.execute_sql(f"SHOW VIEW {self.schema_name}.{self.view_name}").fetchall()[0][0].replace('\r','\n')
    
    def show_query(self):
        if self.df is not None:
            print(self._get_ddl())

    def info(self):
        print("\nEntities:")
        for key, value in self.entity.items():
            print(f"  - {key}: {value}")

        print("\nFeatures:")
        for feature, details in self.features.items():
            print(f"  - {feature}:")
            for detail_key, detail_value in details.items():
                print(f"      {detail_key}: {detail_value}")
