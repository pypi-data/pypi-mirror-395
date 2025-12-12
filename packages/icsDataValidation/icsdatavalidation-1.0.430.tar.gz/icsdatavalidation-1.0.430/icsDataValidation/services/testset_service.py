import logging

from icsDataValidation.utils.file_util import load_json
from icsDataValidation.utils.logger_util import configure_dev_ops_logger

#########################################################################################
# Configure Dev Ops Logger

logger = logging.getLogger('TestsetService')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

#########################################################################################
#########################################################################################

class TestsetService:
    """
    Class to prepare the set of objects for the comparison.
    Maps schemas and objects between source and target.
    Handles blacklists and whitelists.
    """

    def __init__(self, testset_mapping:dict, testset_blacklist: dict, testset_file_paths: list=None):
        self.testset_mapping = testset_mapping
        self.testset_blacklist = testset_blacklist

        if testset_file_paths:
            self.testset_whitelist = self._load_testset(testset_file_paths)
        else:
            self.testset_whitelist = None

    @staticmethod
    def _load_testset(testset_file_paths):
        """
        Load the testset files from a list of file paths.
        Configure the whitelist of databases, schemas, and objects.
        """
        logger.info(f"++++++++++++++++ LOAD testset/whitelist")
        try:
            testset_whitelist={
                "WHITELIST_OBJECTS_SRC":[],
                "WHITELIST_SCHEMAS_SRC":[],
                "WHITELIST_DATABASES_SRC":[],
                "WHITELIST_OBJECTS_TRGT":[],
                "WHITELIST_SCHEMAS_TRGT":[],
                "WHITELIST_DATABASES_TRGT":[]
            }

            for testset_file_path in testset_file_paths:
                testset_=load_json(testset_file_path)
                for key, value in testset_.items():
                    testset_whitelist[key]= list(set(testset_whitelist[key]) | set(value))
        except FileNotFoundError as file_not_found_err:
            logger.error(f"Not able to load testset from {testset_file_path}!")
            raise file_not_found_err
        except Exception as exc:
            logger.error("Unexpected exception while trying to load testset and/or defining the whitelist:\n", exc_info=exc)
            raise exc

        return testset_whitelist

    def handle_database_mapping(self, source_database_name: str = None) -> str:
        """
        Map the source and the target database.
        Note: Case-Insensitive and returns upper-case target database name.
        """
        target_database_name=source_database_name.upper()

        if self.testset_mapping and "DATABASE_MAPPING" in self.testset_mapping:
            for database_mapping in self.testset_mapping["DATABASE_MAPPING"]:
                if source_database_name.upper() == database_mapping["src_database_name"].upper():
                    target_database_name = database_mapping["trgt_database_name"].upper()

        return target_database_name

    def handle_schema_mapping(self, source_schema_name: str = None, source_database_name: str = None) -> str:
        """
        Map the source and the target schema.
        Note: Case-Insensitive and returns upper-case target schema name.
        """
        target_schema_name=source_schema_name.upper()
        found_schema_mapping = False

        if self.testset_mapping and "SCHEMA_MAPPING" in self.testset_mapping:
            for schema_mapping in self.testset_mapping["SCHEMA_MAPPING"]:

                if f"{source_database_name.upper()}.{source_schema_name.upper()}" == schema_mapping["src_schema_identifier"].upper():
                    target_schema_name = schema_mapping["trgt_schema_name"].upper()
                    found_schema_mapping = True

        return target_schema_name, found_schema_mapping

    def handle_schema_replace_mapping(self, source_schema_name: str = None) -> str:
        """
        Map the source and the target schema by replacing a subset of the target schema string.
        Note: Case-Insensitive and returns upper-case target schema name.
        """

        if self.testset_mapping and "SCHEMA_REPLACE_MAPPING" in self.testset_mapping:
            replace_mapping = self.testset_mapping["SCHEMA_REPLACE_MAPPING"]
            for replace_object in replace_mapping:
                target_schema_name = source_schema_name.upper().replace(
                    replace_object["src_replace_value"].upper(),
                    replace_object["trgt_replace_value"].upper(),
                )
        else:
            target_schema_name=source_schema_name.upper()

        return target_schema_name

    def handle_blacklist(self, database_objects: dict, src_trgt: str)-> dict:
        """
        Handle the blacklist from the migration_config to restrict database objects.
        Use src_trgt="SRC" for source and src_trgt="TRGT" for target.
        """
        blacklist_objects=[object_blacklisted.upper() for object_blacklisted in self.testset_blacklist[f"BLACKLIST_OBJECTS_{src_trgt}"]]
        blacklist_schemas=[schema_blacklisted.upper() for schema_blacklisted in self.testset_blacklist[f"BLACKLIST_SCHEMAS_{src_trgt}"]]
        blacklist_databases=[database_blacklisted.upper() for database_blacklisted in self.testset_blacklist[f"BLACKLIST_DATABASES_{src_trgt}"]]

        database_objects_=database_objects.copy()

        for db_object in database_objects_:
            database_name = db_object["object_identifier"].split(".",1)[0]
            schema_identifier = ".".join(db_object["object_identifier"].split(".",2)[:2])
            if database_name in blacklist_databases:
                database_objects.remove(db_object)
            elif schema_identifier in blacklist_schemas:
                database_objects.remove(db_object)
            elif db_object["object_identifier"] in blacklist_objects:
                database_objects.remove(db_object)

        return database_objects

    def handle_whitelist(self, database_objects: dict, src_trgt: str)-> dict:
        """
        Handle the whitelist which is defined as a testset to restrict database objects.
        Use src_trgt="SRC"  for source and src_trgt="TRGT" for target.
        """
        whitelist_objects=[object_whitelisted.upper() for object_whitelisted in self.testset_whitelist[f"WHITELIST_OBJECTS_{src_trgt}"]]
        whitelist_schemas=[schema_whitelisted.upper() for schema_whitelisted in self.testset_whitelist[f"WHITELIST_SCHEMAS_{src_trgt}"]]
        whitelist_databases=[database_whitelisted.upper() for database_whitelisted in self.testset_whitelist[f"WHITELIST_DATABASES_{src_trgt}"]]

        database_objects_=database_objects.copy()

        for db_object in database_objects_:
            database_name = db_object["object_identifier"].split(".",1)[0]
            schema_identifier = ".".join(db_object["object_identifier"].split(".",2)[:2])
            if not db_object["object_identifier"].upper() in whitelist_objects and schema_identifier.upper() not in whitelist_schemas and database_name.upper() not in whitelist_databases:
                database_objects.remove(db_object)

        return database_objects

    def map_objects(self, database_objects_src: list, database_objects_trgt: list):
        """
        Maps objects between source and target by using the mapping defined in the migration_config.json.
        Handles object "1:1"-mapping  and object "replace"-mapping.
        Returns remaining_mapping_objects which differ between source and target and can not be mapped.
        Returns a flag all_objects_matching which indicates if there exist remaining_mapping_objects.
        """
        intersection_objects_mapped_trgt_src = []
        remaining_mapping_objects = []
        src_objects_minus_trgt_objects = [object for object in database_objects_src if object not in database_objects_trgt]
        trgt_objects_minus_src_objects = [object for object in database_objects_trgt if object not in database_objects_src]


        trgt_objects_minus_src_table_identifiers = [object["object_identifier"] for object in database_objects_trgt if object not in database_objects_src and object["object_type"] == 'table']
        trgt_objects_minus_src_view_identifiers = [object["object_identifier"] for object in database_objects_trgt if object not in database_objects_src and object["object_type"] == 'view']


        if database_objects_src != database_objects_trgt and self.testset_mapping:

            src_objects_minus_trgt_objects_ = src_objects_minus_trgt_objects.copy()

            trgt_objects_minus_src_object_identifiers=[object["object_identifier"] for object in trgt_objects_minus_src_objects]

            for n_db_object, db_object in enumerate(src_objects_minus_trgt_objects_):
                logger.info(f"Object {n_db_object+1} of {len(src_objects_minus_trgt_objects_)}: {db_object}")
                continue_flag = True

                #########################################################################################
                # Object-Mapping
                for mapping in self.testset_mapping["OBJECT_MAPPING"]:

                    if (
                        db_object["object_identifier"] == mapping["src_object_identifier"].upper()
                        and db_object["object_type"] == mapping["src_object_type"]
                        and mapping['trgt_object_identifier'].upper() in trgt_objects_minus_src_object_identifiers
                    ):
                        logger.info(f" -> mapping object found: {mapping}")
                        intersection_objects_mapped_trgt_src.append({"src_object_identifier": db_object["object_identifier"],"src_object_type": db_object["object_type"], "trgt_object_identifier": mapping["trgt_object_identifier"],"trgt_object_type": mapping["trgt_object_type"]})
                        src_objects_minus_trgt_objects.remove(db_object)

                        for trgt_object in trgt_objects_minus_src_objects:
                            if trgt_object["object_identifier"] == mapping["trgt_object_identifier"].upper():
                                trgt_objects_minus_src_objects.remove(trgt_object)
                        logger.info(" -> added by 1:1 mapping")

                        # set continue_flag to false because this object has been covered by the mapping
                        continue_flag = False
                        break

                ##########################################################################################
                # Database-Mapping, and Schema-Mapping

                if continue_flag == True:

                    src_database_name = db_object["object_identifier"].split(".",1)[0]
                    src_schema_name = db_object["object_identifier"].split(".",2)[1]
                    src_object_name = db_object["object_identifier"].split(".",2)[2]

                    trgt_database_name=self.handle_database_mapping(src_database_name)
                    trgt_schema_name, _ =self.handle_schema_mapping(src_schema_name,src_database_name)

                    trgt_object_identifier=f"{trgt_database_name}.{trgt_schema_name}.{src_object_name}".upper()

                    if (db_object["object_type"] == 'table' and trgt_object_identifier in trgt_objects_minus_src_table_identifiers) or (db_object["object_type"] == 'view' and trgt_object_identifier in trgt_objects_minus_src_view_identifiers):
                        intersection_objects_mapped_trgt_src.append({"src_object_identifier": db_object["object_identifier"],"src_object_type": db_object["object_type"], "trgt_object_identifier": trgt_object_identifier,"trgt_object_type": db_object["object_type"]})
                        src_objects_minus_trgt_objects.remove(db_object)

                        for trgt_object in trgt_objects_minus_src_objects:
                            if trgt_object["object_identifier"] == trgt_object_identifier:
                                trgt_objects_minus_src_objects.remove(trgt_object)

                        logger.info(" -> added by database/schema-mapping")

                        # set continue_flag to false because this object has been covered by the replacements
                        continue_flag = False

                ##########################################################################################
                # Replace-Mapping

                if continue_flag == True:


                        src_database_name = db_object["object_identifier"].split(".",1)[0]
                        src_schema_name = db_object["object_identifier"].split(".",2)[1]
                        src_object_name = db_object["object_identifier"].split(".",2)[2]

                        #TODO rework!!!!

                        ## replace the values from the migration_config.json to create a potential_match which can be looked for the trgt_objects_minus_src_objects list
                        #potential_match = db_object["object_identifier"].upper().replace(f'{substitute["src_replace_value"].upper()}',f'{substitute["trgt_replace_value"].upper()}')
#
                        ## the potential_match is contained within the trgt_objects_minus_src_objects list
                        #if potential_match in trgt_objects_minus_src_object_identifiers:
                        #    logger.info(f" -> replace mapping found: {substitute}")
                        #    intersection_objects_mapped_trgt_src.append({"src_object_identifier": db_object["object_identifier"],"src_object_type": db_object["object_type"], "trgt_object_identifier": potential_match,"trgt_object_type": db_object["object_type"]})
                        #    src_objects_minus_trgt_objects.remove(db_object)
#
                        #    for trgt_object in trgt_objects_minus_src_objects:
                        #        if trgt_object["object_identifier"] == potential_match:
                        #            trgt_objects_minus_src_objects.remove(trgt_object)
                        #    logger.info(" -> added by replace mapping")
#
                        #    # set continue_flag to false because this object has been covered by the replacements
                        #    continue_flag = False
                        #    break

                #####################################################################
                # Remaining objects
                if continue_flag == True:
                    remaining_mapping_objects.append({"src_object_identifier": db_object["object_identifier"],"trgt_object_identifier": '',"src_object_type": db_object["object_type"],"trgt_object_type": ''})
                    logger.info(" -> no mapping found -> added to remaining_mapping_objects")

        object_identifiers_src_minus_trgt= [object["object_identifier"] for object in src_objects_minus_trgt_objects]
        object_identifiers_trgt_minus_src= [object["object_identifier"] for object in trgt_objects_minus_src_objects]

        if src_objects_minus_trgt_objects:
            logger.warning('There are database objects in the source db that are not in the target db and for which no mapping exists:')
            logger.warning(f"{object_identifiers_src_minus_trgt}")
        if trgt_objects_minus_src_objects:
            logger.warning('There are database objects in the target db that are not in the source db and for which no mapping exists:')
            logger.warning(f"{object_identifiers_trgt_minus_src}")

        if not (src_objects_minus_trgt_objects and trgt_objects_minus_src_objects):
            all_objects_matching=True
        else:
            all_objects_matching=False

        return intersection_objects_mapped_trgt_src, object_identifiers_src_minus_trgt, object_identifiers_trgt_minus_src, remaining_mapping_objects, all_objects_matching

    @staticmethod
    def get_intersection_objects_trgt_src(database_objects_src: list, database_objects_trgt: list, intersection_objects_mapped_trgt_src:list):
        """
        Get intersection of all database objects from source db and target db - including mapped objects.
        """

        intersection_objects_trgt_src_without_mapping =[{"src_object_identifier": object["object_identifier"],"src_object_type": object["object_type"],"trgt_object_identifier": object["object_identifier"],"trgt_object_type": object["object_type"]} for object in database_objects_src if object in database_objects_trgt]

        intersection_objects_trgt_src= intersection_objects_trgt_src_without_mapping + intersection_objects_mapped_trgt_src

        return intersection_objects_trgt_src
