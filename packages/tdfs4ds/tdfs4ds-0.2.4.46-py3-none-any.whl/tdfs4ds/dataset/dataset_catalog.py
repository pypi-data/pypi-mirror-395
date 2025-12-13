from tdfs4ds import logger
import uuid
from tdfs4ds.dataset.dataset import Dataset
import teradataml as tdml
import json

class DatasetCatalog:

    def __init__(self, schema_name = None, name = 'DATASET'):
        if schema_name is None:
            self.schema_name = tdml.context.context._get_current_databasename()
        else:
            self.schema_name = schema_name
        self.name        = name

        self.catalog_table_name = f"{self.schema_name}.FS_{self.name}_CATALOG"
        self.catalog_view_name  = f"{self.schema_name}.FS_V_{self.name}_CATALOG"
        self.entity_table_name = f"{self.schema_name}.FS_{self.name}_ENTITY"
        self.entity_view_name  = f"{self.schema_name}.FS_V_{self.name}_ENTITY"
        self.feature_table_name = f"{self.schema_name}.FS_{self.name}_FEATURES"
        self.feature_view_name  = f"{self.schema_name}.FS_V_{self.name}_FEATURES"

        self.creation_queries = self._creation_query()
        if not self._exists():
            self.create_catalog()

        self.catalog = tdml.DataFrame(tdml.in_schema(self.catalog_view_name.split('.')[0],self.catalog_view_name.split('.')[1]))
        self.entity = tdml.DataFrame(tdml.in_schema(self.entity_view_name.split('.')[0],self.entity_view_name.split('.')[1]))
        self.features = tdml.DataFrame(tdml.in_schema(self.feature_view_name.split('.')[0],self.feature_view_name.split('.')[1]))

    def __repr__(self):
        return f"DatasetCatalog(catalog_view={self.catalog_view_name}, entity_view={self.entity_view_name}, feature_view={self.feature_view_name})"
    
    def __getattr__(self, item):
        if self.catalog is not None:
            return getattr(self.catalog, item)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def _creation_query(self):

        if self.schema_name is not None and self.name is not None:

            query_dataset_catalog = f"""
            CREATE MULTISET TABLE {self.catalog_table_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                DATASET_ID VARCHAR(36) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                DATASET_NAME VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                DATASET_DATABASE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                DATASET_TYPE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                DATASET_VALIDTIME VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                METADATA JSON(32000) CHARACTER SET LATIN,
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX (DATASET_ID);
            """

            query_dataset_catalog_view = f"""
                        CREATE VIEW {self.catalog_view_name} AS
                        LOCK ROW FOR ACCESS
                        CURRENT VALIDTIME
                        SELECT *
                        FROM {self.catalog_table_name}
            """
            
            query_dataset_entity = f"""
            CREATE MULTISET TABLE {self.entity_table_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                DATASET_ID VARCHAR(36) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ENTITY VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ENTITY_TYPE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX (DATASET_ID);
            """

            query_dataset_entity_view = f"""
                        CREATE VIEW {self.entity_view_name} AS
                        LOCK ROW FOR ACCESS
                        CURRENT VALIDTIME
                        SELECT *
                        FROM {self.entity_table_name}
            """

            query_dataset_features = f"""
            CREATE MULTISET TABLE {self.feature_table_name},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                DATASET_ID VARCHAR(36) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_ID VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_NAME VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_TYPE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_DATABASE VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                FEATURE_VIEW VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME
            )
            PRIMARY INDEX (DATASET_ID);
            """

            query_dataset_feature_view = f"""
                        CREATE VIEW {self.feature_view_name} AS
                        LOCK ROW FOR ACCESS
                        CURRENT VALIDTIME
                        SELECT *
                        FROM {self.feature_table_name}
            """

            queries = [
                {'name' : f'{self.catalog_table_name}', 'type': 'table', 'query': query_dataset_catalog},
                {'name' : f'{self.entity_table_name}', 'type': 'table', 'query': query_dataset_entity},
                {'name' : f'{self.feature_table_name}', 'type': 'table', 'query': query_dataset_features},
                {'name' : f'{self.catalog_view_name}', 'type': 'view', 'query': query_dataset_catalog_view},
                {'name' : f'{self.entity_view_name}', 'type': 'view', 'query': query_dataset_entity_view},
                {'name' : f'{self.feature_view_name}', 'type': 'view', 'query': query_dataset_feature_view}
            ]

            return queries
        else:
            logger.error('the schema name is not defined')
            raise ValueError("the schema name is not defined")
        
    def _get_list_objects(self):
        return [self.catalog_table_name, self.entity_table_name, self.feature_table_name, self.catalog_view_name, self.entity_view_name, self.feature_view_name]
        
    def create_catalog(self, schema_name = None):

        if schema_name is not None:
            self.schema_name = schema_name
            self.catalog_table_name = f"{self.schema_name}.{self.name}_CATALOG"
            self.catalog_view_name  = f"{self.schema_name}.V_{self.name}_CATALOG"
            self.entity_table_name = f"{self.schema_name}.{self.name}_ENTITY"
            self.entity_view_name  = f"{self.schema_name}.V_{self.name}_ENTITY"
            self.feature_table_name = f"{self.schema_name}.{self.name}_FEATURES"
            self.feature_view_name  = f"{self.schema_name}.V_{self.name}_FEATURES"

        
        self.creation_queries = self._creation_query()
        already_exists = [v for v in self._get_list_objects() if v.lower().split('.')[1] in map(str.lower, tdml.db_list_tables(schema_name = self.schema_name).TableName.values)]

        if len(already_exists) > 0:
            msg = f"The dataset catalog cannot be created because these tables already exist : {already_exists}"
            logger.error(msg)
            raise ValueError(msg)
        else:
            for query in self.creation_queries:
                logger.info(f"creation of {query['name']}")
                tdml.execute_sql(query['query'])

    def drop_catalog(self):

        for query in self.creation_queries:
            logger.info(f"drop {query['name']}")
            if query['type'] == 'table':
                tdml.execute_sql(f"DROP TABLE {query['name']}")
            elif query['type'] == 'view':
                tdml.execute_sql(f"DROP VIEW {query['name']}")

    def _exists(self):
        not_exists = [v for v in self._get_list_objects() if v.lower().split('.')[1] not in map(str.lower, tdml.db_list_tables(schema_name = self.schema_name).TableName.values)]
        return not_exists == []
    
    def add_dataset(self, dataset, metadata = {}):

        # if dataset exists:
        res = self.catalog[(self.catalog.DATASET_NAME == dataset.view_name.upper())&(self.catalog.DATASET_DATABASE == dataset.schema_name.upper())]
        if res.shape[0] == 1:
            logger.info('this dataset is already present and will be updated')
            print(res[['DATASET_ID', 'DATASET_NAME', 'DATASET_DATABASE']])
            dataset_id = res[['DATASET_ID']].to_pandas().DATASET_ID.values[0]

            entity = tdml.DataFrame(tdml.in_schema(self.entity_view_name.split('.')[0],self.entity_view_name.split('.')[1]))
            existing_entity = entity[entity.DATASET_ID == dataset_id].to_pandas()

            features = tdml.DataFrame(tdml.in_schema(self.feature_view_name.split('.')[0],self.feature_view_name.split('.')[1]))
            existing_features = features[features.DATASET_ID == dataset_id].to_pandas()

        elif res.shape[0] == 0:
            dataset_id = str(uuid.uuid4())
            existing_entity = None
            existing_features = None
            logger.info('the dataset is new and will be registered')
        else:
            logger.error('there are more that one dataset with the same id')
            raise
        logger.info(f'dataset is : {dataset_id}')

        query_insert_catalog =  f"""
        CURRENT VALIDTIME
        MERGE INTO {self.catalog_table_name} EXISTING
        USING (
            SEL 
                '{dataset_id}' AS DATASET_ID
            ,   '{dataset.view_name}' AS DATASET_NAME
            ,   '{dataset.schema_name}' AS DATASET_DATABASE
            ,   '{dataset.dataset_type}' AS DATASET_TYPE
            ,   '{dataset.valid_time}' AS DATASET_VALIDTIME
            ,   '{json.dumps(metadata).replace("'", '"')}' AS METADATA
        ) UPDATED
        ON EXISTING.DATASET_ID = UPDATED.DATASET_ID
        WHEN MATCHED THEN
            UPDATE
            SET
                DATASET_NAME      = UPDATED.DATASET_NAME 
            ,   DATASET_DATABASE  = UPDATED.DATASET_DATABASE 
            ,   DATASET_TYPE      = UPDATED.DATASET_TYPE
            ,   DATASET_VALIDTIME = UPDATED.DATASET_VALIDTIME
            ,   METADATA          = UPDATED.METADATA
        WHEN NOT MATCHED THEN
        INSERT (
            UPDATED.DATASET_ID,
            UPDATED.DATASET_NAME,
            UPDATED.DATASET_DATABASE,
            UPDATED.DATASET_TYPE,
            UPDATED.DATASET_VALIDTIME,
            UPDATED.METADATA
            )   
        """

        updated_entity = dataset.entity
        if existing_entity is not None:
            dropped_entity = [e for e in existing_entity.ENTITY.values if e.lower() not in map(str.lower, updated_entity.keys())]
        else:
            dropped_entity = []
            
        logger.info(f"entity to update : {list(updated_entity.keys())}")
        logger.info(f"entity to drop : {dropped_entity}")

        query_insert_entity = []
        for k,v in updated_entity.items():
            query_insert_entity_ =  f"""
            CURRENT VALIDTIME
            MERGE INTO {self.entity_table_name} EXISTING
            USING (
                SEL 
                    '{dataset_id}' AS DATASET_ID
                ,   '{k}' AS ENTITY
                ,   '{v}' AS ENTITY_TYPE
            ) UPDATED
            ON EXISTING.DATASET_ID = UPDATED.DATASET_ID
            AND EXISTING.ENTITY = UPDATED.ENTITY
            WHEN MATCHED THEN
                UPDATE
                SET
                    ENTITY_TYPE = UPDATED.ENTITY_TYPE 

            WHEN NOT MATCHED THEN
            INSERT (
                UPDATED.DATASET_ID,
                UPDATED.ENTITY,
                UPDATED.ENTITY_TYPE
                )   
            """
            query_insert_entity.append(query_insert_entity_)

        for k in dropped_entity:
            query_insert_entity_ = f"""
            CURRENT VALIDTIME
            DELETE {self.entity_table_name} WHERE DATASET_ID = '{dataset_id}' AND ENTITY = '{k}'
            """
            query_insert_entity.append(query_insert_entity_)

        updated_features = dataset.features
            
        if existing_features is not None:
            dropped_features = [f for f in existing_features.FEATURE_NAME.values if f.lower() not in map(str.lower, updated_features.keys())]
        else:
            dropped_features = []
            
        logger.info(f"features to update : {list(updated_features.keys())}")
        logger.info(f"features to drop : {dropped_features}")

        query_insert_features = []
        for k,v in updated_features.items():
            query_insert_feature_ =  f"""
            CURRENT VALIDTIME
            MERGE INTO {self.feature_table_name} EXISTING
            USING (
                SEL 
                    '{dataset_id}' AS DATASET_ID
                ,   {v['id']} AS FEATURE_ID
                ,   '{k}' AS FEATURE_NAME
                ,   '{v['type']}' AS FEATURE_TYPE
                ,   '{v['database']}' AS FEATURE_DATABASE
                ,   '{v['view']}' AS FEATURE_VIEW
            ) UPDATED
            ON EXISTING.DATASET_ID = UPDATED.DATASET_ID
            AND EXISTING.FEATURE_NAME = UPDATED.FEATURE_NAME
            WHEN MATCHED THEN
                UPDATE
                SET
                    FEATURE_ID       = UPDATED.FEATURE_ID 
                ,   FEATURE_TYPE     = UPDATED.FEATURE_TYPE 
                ,   FEATURE_DATABASE = UPDATED.FEATURE_DATABASE 
                ,   FEATURE_VIEW     = UPDATED.FEATURE_VIEW 
            WHEN NOT MATCHED THEN
            INSERT (
                UPDATED.DATASET_ID,
                UPDATED.FEATURE_ID,
                UPDATED.FEATURE_NAME,
                UPDATED.FEATURE_TYPE,
                UPDATED.FEATURE_DATABASE,
                UPDATED.FEATURE_VIEW
            )   
            """
            query_insert_features.append(query_insert_feature_)

        for k in dropped_entity:
            query_insert_feature_ = f"""
            CURRENT VALIDTIME
            DELETE {self.feature_table_name} WHERE DATASET_ID = '{dataset_id}' AND FEATURE_NAME = '{k}'
            """
            query_insert_features.append(query_insert_feature_)

        queries = [query_insert_catalog] + query_insert_entity + query_insert_features
        for query in queries:
            logger.info(query.split('\n')[2].strip())
            tdml.execute_sql(query)

    def drop_dataset(self, dataset_id):
        if self.catalog[self.catalog.DATASET_ID == dataset_id].shape[0] == 1:
            query_drop_feature = f"""
            CURRENT VALIDTIME
            DELETE {self.feature_table_name} WHERE DATASET_ID = '{dataset_id}'
            """
            query_drop_entity = f"""
            CURRENT VALIDTIME
            DELETE {self.entity_table_name} WHERE DATASET_ID = '{dataset_id}'
            """
            query_drop_catalog = f"""
            CURRENT VALIDTIME
            DELETE {self.catalog_table_name} WHERE DATASET_ID = '{dataset_id}'
            """

            for query in [query_drop_feature, query_drop_entity, query_drop_catalog]:
                logger.info(query.split('\n')[2].strip())
                tdml.execute_sql(query)
            
    def get_dataset_entity(self, dataset_id = None):

        if dataset_id is None:
            return self.entity
        else:
            return self.entity[self.entity.DATASET_ID == dataset_id]
        

    def get_dataset_features(self, dataset_id = None):

        if dataset_id is None:
            return self.features
        else:
            return self.features[self.features.DATASET_ID == dataset_id]