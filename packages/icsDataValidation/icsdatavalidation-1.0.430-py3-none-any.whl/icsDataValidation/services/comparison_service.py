import logging
import pandas as pd
import datetime
import numpy as np

from pandas._testing import assert_frame_equal
from decimal import Decimal, InvalidOperation, getcontext

from icsDataValidation.utils.logger_util import configure_dev_ops_logger
from icsDataValidation.utils.pandas_util import get_diff_dataframes, get_diff_dict_from_diff_dataframes
from icsDataValidation.input_parameters.testing_tool_params import TestingToolParams
from icsDataValidation.core.database_objects import DatabaseObject
from icsDataValidation.output_parameters.result_params import ResultParams

#########################################################################################

# Configure Dev Ops Logger

logger = logging.getLogger('ComparisonService')
logger.setLevel(logging.INFO)
configure_dev_ops_logger(logger)

#########################################################################################
#########################################################################################


class ComparisonService(TestingToolParams):
    """
    Class to compare an object between a source and a target system.
    """
    def __init__(self, src_object: DatabaseObject, trgt_object: DatabaseObject, db_service_src, db_service_trgt, src_filter: list, trgt_filter: list, exclude_columns: list, comp_id: int):
        super().__init__()
        self.result_params = ResultParams()
        self.src_object = src_object
        self.trgt_object = trgt_object
        self.db_service_src = db_service_src
        self.db_service_trgt = db_service_trgt
        self.src_filter = src_filter
        self.trgt_filter = trgt_filter
        self.exclude_columns = exclude_columns
        self.comp_id = comp_id

    def _get_group_by_column_by_validation(self, group_by_column_candidates: list, src_column_count_distincts, trgt_column_count_distincts):
        object_group_by_column=None
        for object_group_by_column in group_by_column_candidates:

            src_group_by_column_count_distinct=next((item["COUNT_DISTINCT"] for item in src_column_count_distincts if item["COLUMN_NAME"].upper() == object_group_by_column), None)
            trgt_group_by_column_count_distinct=next((item["COUNT_DISTINCT"] for item in trgt_column_count_distincts if item["COLUMN_NAME"].upper() == object_group_by_column), None)

            if (trgt_group_by_column_count_distinct<=1 or src_group_by_column_count_distinct<=1):
                logger.info(f"[{self.comp_id}] The GROUP_BY_COLUMN {object_group_by_column} does not satisfy the necessary criteria.")
                logger.info(f"[{self.comp_id}] Number of distinct values <= 1 on src or trgt.")
                continue
            elif (trgt_group_by_column_count_distinct==self.result_params.trgt_row_count or src_group_by_column_count_distinct==self.result_params.src_row_count):
                logger.info(f"[{self.comp_id}] The GROUP_BY_COLUMN {object_group_by_column} does not satisfy the necessary criteria.")
                logger.info(f"[{self.comp_id}] Number of distinct values equal to rowcount of object on src or trgt.")
                continue
            elif (trgt_group_by_column_count_distinct<self.min_group_by_count_distinct or src_group_by_column_count_distinct<self.min_group_by_count_distinct):
                logger.info(f"[{self.comp_id}] The GROUP_BY_COLUMN {object_group_by_column} does not satisfy the necessary criteria.")
                logger.info(f"[{self.comp_id}] Number of distinct values falls below the min_group_by_count_distinct {self.min_group_by_count_distinct} on src or trgt.")
                continue
            elif (trgt_group_by_column_count_distinct>self.max_group_by_count_distinct or src_group_by_column_count_distinct>self.max_group_by_count_distinct):
                logger.info(f"[{self.comp_id}] The GROUP_BY_COLUMN {object_group_by_column} does not satisfy the necessary criteria.")
                logger.info(f"[{self.comp_id}] Number of distinct values exceeds the max_group_by_count_distinct {self.max_group_by_count_distinct} on src or trgt.")
                continue
            elif (trgt_group_by_column_count_distinct*len(self.result_params.intersection_columns_trgt_src)>self.max_group_by_size or src_group_by_column_count_distinct*len(self.result_params.intersection_columns_trgt_src)>self.max_group_by_size):
                logger.info(f"[{self.comp_id}] The GROUP_BY_COLUMN {object_group_by_column} does not satisfy the necessary criteria.")
                logger.info(f"[{self.comp_id}] The size of the expected result of the group-by-query exceeds the max_group_by_size {self.max_group_by_size} on src or trgt.")
                continue

            logger.info(f"[{self.comp_id}] USING Column {object_group_by_column} for group by aggregation")
            return object_group_by_column

    def row_count_comparison(self):
        logger.info(f"[{self.comp_id}] START Row-Count-Comparison")
        # row count comparison
        self.result_params.src_row_count, self.result_params.error_list_rows_src = self.db_service_src.get_row_count_from_object(self.src_object, self.src_filter)
        self.result_params.trgt_row_count, self.result_params.error_list_rows_trgt = self.db_service_trgt.get_row_count_from_object(self.trgt_object, self.trgt_filter)
        self.result_params.src_row_count = int(self.result_params.src_row_count)
        self.result_params.trgt_row_count = int(self.result_params.trgt_row_count)
        self.result_params.src_row_count_minus_trgt_row_count = self.result_params.src_row_count-self.result_params.trgt_row_count

        self.result_params.row_counts_equal = True
        if self.result_params.error_list_rows_src or self.result_params.error_list_rows_trgt:
            self.result_params.row_counts_equal = None
        elif self.result_params.src_row_count_minus_trgt_row_count != 0:
            self.result_params.row_counts_equal = False

    def column_names_comparison(self):
        logger.info(f"[{self.comp_id}] START Column-Names-Comparison")
        src_columns = self.db_service_src.get_columns_from_object(self.src_object)
        trgt_columns = self.db_service_trgt.get_columns_from_object(self.trgt_object)
        src_columns.sort()
        trgt_columns.sort()

        src_columns_upper=[src_column.upper() for src_column in src_columns]
        trgt_columns_upper=[trgt_column.upper() for trgt_column in trgt_columns]

        src_columns_minus_trgt_columns = list(set(src_columns_upper) - set(trgt_columns_upper))
        trgt_columns_minus_src_columns = list(set(trgt_columns_upper) - set(src_columns_upper))
        src_columns_minus_trgt_columns.sort()
        trgt_columns_minus_src_columns.sort()

        columns_equal = True
        if src_columns_minus_trgt_columns:
            columns_equal = False

        if trgt_columns_minus_src_columns:
            columns_equal = False

        intersection_columns_trgt_src = list(set(src_columns_upper) & set(trgt_columns_upper))
        intersection_columns_trgt_src.sort()

        all_columns_trgt_src = list(set(src_columns_upper) | set(trgt_columns_upper))
        all_columns_trgt_src.sort()

        #save results
        self.result_params.src_columns = src_columns
        self.result_params.trgt_columns = trgt_columns
        self.result_params.src_columns_upper = src_columns_upper
        self.result_params.trgt_columns_upper = trgt_columns_upper
        self.result_params.src_columns_minus_trgt_columns = src_columns_minus_trgt_columns
        self.result_params.trgt_columns_minus_src_columns = trgt_columns_minus_src_columns
        self.result_params.columns_equal = columns_equal
        self.result_params.intersection_columns_trgt_src = intersection_columns_trgt_src
        self.result_params.all_columns_trgt_src = all_columns_trgt_src

    def aggregation_comparison(self):
        logger.info(f"[{self.comp_id}] START Aggregation-Comparison")
        src_column_datatypes = self.db_service_src.get_data_types_from_object(self.src_object, self.result_params.src_columns)
        src_columns_aggregate = self.db_service_src.create_checksums(self.src_object, self.result_params.src_columns, self.src_filter, self.exclude_columns, self.numeric_scale, self.enclose_column_by_double_quotes)

        trgt_column_datatypes = self.db_service_trgt.get_data_types_from_object(self.trgt_object, self.result_params.trgt_columns)
        trgt_columns_aggregate = self.db_service_trgt.create_checksums(self.trgt_object, self.result_params.trgt_columns, self.trgt_filter, self.exclude_columns, self.numeric_scale, self.enclose_column_by_double_quotes)

        src_aggregations_error = src_columns_aggregate['TESTATM_ERRORS']
        trgt_aggregations_error = trgt_columns_aggregate['TESTATM_ERRORS']

        if self.result_params.error_list_rows_src != []:
            src_error_dict = {
                'QUERY': self.result_params.error_list_rows_src[1]
                , 'ERROR': self.result_params.error_list_rows_src[0]
            }
        elif src_aggregations_error!= []:
            src_error_dict = {
                'QUERY': src_aggregations_error[0][1]
                , 'ERROR': src_aggregations_error[0][2]
            }
        else:
            src_error_dict = {'QUERY': None, 'ERROR': None}

        if self.result_params.error_list_rows_trgt != []:
            trgt_error_dict = {
                'QUERY': self.result_params.error_list_rows_trgt[1]
                , 'ERROR': self.result_params.error_list_rows_trgt[0]
            }
        elif trgt_aggregations_error!= []:
            trgt_error_dict = {
                'QUERY': trgt_aggregations_error[0][1]
                , 'ERROR': trgt_aggregations_error[0][2]
            }
        else:
            trgt_error_dict = {'QUERY': None, 'ERROR': None}

        del src_columns_aggregate['TESTATM_ERRORS']
        del trgt_columns_aggregate['TESTATM_ERRORS']

        if self.result_params.src_row_count != 0 and self.result_params.trgt_row_count != 0:
            try:
                aggregation_differences_trgt_minus_src_not_boolean = {
                                                                        k:  round(Decimal(trgt_columns_aggregate[k][1])
                                                                            - Decimal(src_columns_aggregate[k][1]), self.numeric_scale)
                                                                        for k in src_columns_aggregate.keys()
                                                                            if k in trgt_columns_aggregate
                                                                            and str(src_columns_aggregate[k][1]) != str(trgt_columns_aggregate[k][1])
                                                                            and src_columns_aggregate[k][1] != trgt_columns_aggregate[k][1]
                                                                            and src_columns_aggregate[k][0].upper() != 'AGGREGATEBOOLEAN'
                                                                            and trgt_columns_aggregate[k][0].upper() != 'AGGREGATEBOOLEAN'
                                                                    }
            except InvalidOperation as e:
                getcontext().prec = 100 # sets the precision of Decimal to a higher value - due to the limitations of the decimal module when handling such large numbers with high precision
                aggregation_differences_trgt_minus_src_not_boolean = {
                                                                        k:  round(Decimal(trgt_columns_aggregate[k][1])
                                                                            - Decimal(src_columns_aggregate[k][1]), self.numeric_scale)
                                                                        for k in src_columns_aggregate.keys()
                                                                            if k in trgt_columns_aggregate
                                                                            and str(src_columns_aggregate[k][1]) != str(trgt_columns_aggregate[k][1])
                                                                            and src_columns_aggregate[k][1] != trgt_columns_aggregate[k][1]
                                                                            and src_columns_aggregate[k][0].upper() != 'AGGREGATEBOOLEAN'
                                                                            and trgt_columns_aggregate[k][0].upper() != 'AGGREGATEBOOLEAN'
                                                                    }


            aggregation_differences_trgt_minus_src_boolean = {
                                                                k:  str(
                                                                        int(trgt_columns_aggregate[k][1].split('_',1)[0])
                                                                        - int(src_columns_aggregate[k][1].split('_',1)[0])
                                                                    )
                                                                    + '_'
                                                                    + str(
                                                                        int(trgt_columns_aggregate[k][1].split('_',1)[1])
                                                                        - int(src_columns_aggregate[k][1].split('_',1)[1])
                                                                    )
                                                                for k in src_columns_aggregate.keys()
                                                                    if k in trgt_columns_aggregate
                                                                    and str(src_columns_aggregate[k][1]) != str(trgt_columns_aggregate[k][1])
                                                                    and src_columns_aggregate[k][1] != trgt_columns_aggregate[k][1]
                                                                    and src_columns_aggregate[k][0].upper() == 'AGGREGATEBOOLEAN'
                                                                    and trgt_columns_aggregate[k][0].upper() == 'AGGREGATEBOOLEAN'
                                                            }
            aggregation_differences_trgt_minus_src=aggregation_differences_trgt_minus_src_not_boolean
            aggregation_differences_trgt_minus_src.update(aggregation_differences_trgt_minus_src_boolean)
        elif self.result_params.src_row_count != 0 and self.result_params.trgt_row_count == 0:
            aggregation_differences_trgt_minus_src_not_boolean = {
                                                        k: -src_columns_aggregate[k][1]
                                                        for k in src_columns_aggregate.keys()
                                                            if k in trgt_columns_aggregate
                                                            and str(src_columns_aggregate[k][1]) != str(trgt_columns_aggregate[k][1])
                                                            and src_columns_aggregate[k][1] != trgt_columns_aggregate[k][1]
                                                            and src_columns_aggregate[k][0].upper() != 'AGGREGATEBOOLEAN'
                                                            and trgt_columns_aggregate[k][0].upper() != 'AGGREGATEBOOLEAN'
                                                    }
            aggregation_differences_trgt_minus_src_boolean = {
                                                                k:  str(
                                                                        - int(src_columns_aggregate[k][1].split('_',1)[0])
                                                                    )
                                                                    + '_'
                                                                    + str(
                                                                        - int(src_columns_aggregate[k][1].split('_',1)[1])
                                                                    )
                                                                for k in src_columns_aggregate.keys()
                                                                    if k in trgt_columns_aggregate
                                                                    and str(src_columns_aggregate[k][1]) != str(trgt_columns_aggregate[k][1])
                                                                    and src_columns_aggregate[k][1] != trgt_columns_aggregate[k][1]
                                                                    and src_columns_aggregate[k][0].upper() == 'AGGREGATEBOOLEAN'
                                                                    and trgt_columns_aggregate[k][0].upper() == 'AGGREGATEBOOLEAN'
                                                            }
            aggregation_differences_trgt_minus_src=aggregation_differences_trgt_minus_src_not_boolean
            aggregation_differences_trgt_minus_src.update(aggregation_differences_trgt_minus_src_boolean)
        elif self.result_params.src_row_count == 0 and self.result_params.trgt_row_count != 0:
            aggregation_differences_trgt_minus_src = {
                                                        k: trgt_columns_aggregate[k][1]
                                                        for k in src_columns_aggregate.keys()
                                                            if k in trgt_columns_aggregate
                                                            and str(src_columns_aggregate[k][1]) != str(trgt_columns_aggregate[k][1])
                                                    }

        else:
            aggregation_differences_trgt_minus_src = {}

        aggregations_compared = True
        aggregations_equal = True
        if src_aggregations_error or trgt_aggregations_error:
            aggregations_equal = None
            aggregations_compared = False
        else:
            for aggregation_diff in aggregation_differences_trgt_minus_src.values():
                if aggregation_diff and not aggregation_diff == 0.0:
                    aggregations_equal = False
                    break

        # save results
        self.result_params.src_column_datatypes = src_column_datatypes
        self.result_params.src_columns_aggregate = src_columns_aggregate
        self.result_params.trgt_column_datatypes = trgt_column_datatypes
        self.result_params.trgt_columns_aggregate = trgt_columns_aggregate
        self.result_params.src_aggregations_error = src_aggregations_error
        self.result_params.trgt_aggregations_error = trgt_aggregations_error
        self.result_params.aggregation_differences_trgt_minus_src  = aggregation_differences_trgt_minus_src
        self.result_params.src_error_dict = src_error_dict
        self.result_params.trgt_error_dict = trgt_error_dict
        self.result_params.aggregations_compared = aggregations_compared
        self.result_params.aggregations_equal = aggregations_equal


    def group_by_comparison(self):

        object_group_by_columns=[]
        group_by_columns_src=[]
        group_by_columns_trgt=[]
        src_group_by_error = {}
        trgt_group_by_error = {}
        src_group_by_query_aggregation_string = ''
        src_group_by_query_columns_string = ''
        trgt_group_by_query_aggregation_string = ''
        trgt_group_by_query_columns_string = ''
        group_by_values_with_mismatches = {}
        group_by_query_where_filter = ''
        columns_with_mismatch = []
        group_by_diff_dict = {}
        src_group_by_query = ''
        trgt_group_by_query = ''

        src_pdf_from_group_by_sorted = None
        trgt_pdf_from_group_by_sorted = None
        diff_src_pdf_from_group_by_sorted = None
        diff_trgt_pdf_from_group_by_sorted = None
        pandas_df_from_group_by_is_equal = None

        if not "GROUP_BY_AGGREGATION" in self.migration_config:
            raise ValueError(f"The GROUP_BY_AGGREGATION key is missing in the migration_config.json. Please add the key and the parameters GROUP_BY_COLUMNS and GROUP_BY_COLUMNS_PER_TABLE to the config or disable the execute_group_by_comparison parameter.")
        elif self.use_group_by_columns :
            if not "GROUP_BY_COLUMNS" in  self.migration_config["GROUP_BY_AGGREGATION"]:
                raise ValueError(f"The GROUP_BY_COLUMNS key is missing in the migration_config.json. Please add the key to the config under GROUP_BY_AGGREGATION or disable the use_group_by_columns parameter or the execute_group_by_comparison parameter.")
            if not "GROUP_BY_COLUMNS_PER_TABLE" in  self.migration_config["GROUP_BY_AGGREGATION"]:
                raise ValueError(f"The GROUP_BY_COLUMNS_PER_TABLE key is missing in the migration_config.json. Please add the key to the config under GROUP_BY_AGGREGATION or disable the use_group_by_columns parameter or the execute_group_by_comparison parameter.")

        # group-by only if tables not empty
        if self.result_params.src_row_count == 0 :
            logger.info(f"[{self.comp_id}] Source table  {self.src_object.database}.{self.src_object.schema}.{self.src_object.name} is empty, Group-By-Comparison will be skipped")
        elif self.result_params.trgt_row_count == 0:
            logger.info(f"[{self.comp_id}] Target table {self.trgt_object.database}.{self.trgt_object.schema}.{self.trgt_object.name}  is empty, Group-By-Comparison will be skipped")

        # group-by option 1 - group_by_columns defined as multiple lists for specific tables
        elif self.use_group_by_columns and f"{self.src_object.database}.{self.src_object.schema}.{self.src_object.name}" in self.migration_config["GROUP_BY_AGGREGATION"]["GROUP_BY_COLUMNS_PER_TABLE"].keys():
            logger.info(f"[{self.comp_id}] START Group-By-Comparison - with option 1 (group_by_columns defined for specific object)")
            group_by_configuration_current_object = self.migration_config["GROUP_BY_AGGREGATION"]["GROUP_BY_COLUMNS_PER_TABLE"][f"{self.src_object.database}.{self.src_object.schema}.{self.src_object.name}"]
            object_group_by_columns = group_by_configuration_current_object["GROUP_BY_COLUMNS"]
            object_group_by_aggregation_columns = group_by_configuration_current_object["GROUP_BY_AGGREGATION_COLUMNS"]
            object_group_by_aggregation_type = group_by_configuration_current_object["GROUP_BY_AGGREGATION_TYPE"]

        # group-by option 2 - group_by_columns defined as one list for all tables
        elif self.use_group_by_columns and self.migration_config["GROUP_BY_AGGREGATION"]["GROUP_BY_COLUMNS"]:
            logger.info(f"[{self.comp_id}] START Group-By-Comparison - with option 2 (group_by_columns defined as a list for all objects)")
            global_group_by_columns=self.migration_config["GROUP_BY_AGGREGATION"]["GROUP_BY_COLUMNS"]
            object_group_by_columns=[group_by_column for group_by_column in global_group_by_columns if group_by_column in self.result_params.intersection_columns_trgt_src]
            if object_group_by_columns:
                object_group_by_aggregation_columns=["all"]
                object_group_by_aggregation_type='various'

        # group-by option 3 - group_by_columns NOT defined as a list
        elif (not self.use_group_by_columns or not object_group_by_columns):
            logger.info(f"[{self.comp_id}] START Group-By-Comparison - with option 3 (group_by_columns NOT defined -> retrieve group_by_columns by defined criteria)")
            src_column_count_distincts, error_list = self.db_service_src.get_count_distincts_from_object(self.src_object, self.result_params.src_columns, enclose_column_by_double_quotes=self.enclose_column_by_double_quotes)
            trgt_column_count_distincts, error_list = self.db_service_trgt.get_count_distincts_from_object(self.trgt_object, self.result_params.trgt_columns, enclose_column_by_double_quotes=self.enclose_column_by_double_quotes)
            if src_column_count_distincts and trgt_column_count_distincts:
                object_group_by_column=self._get_group_by_column_by_validation(self.result_params.intersection_columns_trgt_src, src_column_count_distincts, trgt_column_count_distincts)
                if object_group_by_column:
                    object_group_by_columns=[object_group_by_column]
                    object_group_by_aggregation_columns=["all"]
                    object_group_by_aggregation_type='various'

        if not object_group_by_columns:
            logger.info(f"[{self.comp_id}] No Group-By-Columns found")
        else:
            logger.info(f"[{self.comp_id}] USING Column(s) {str(object_group_by_columns)} for Group-By-Comparison")
            src_pdf_from_group_by, src_group_by_query_aggregation_string, src_group_by_query_columns_string, group_by_columns_src, src_group_by_error = self.db_service_src.create_pandas_df_from_group_by(self.src_object, self.result_params.intersection_columns_trgt_src, object_group_by_columns, object_group_by_aggregation_columns, object_group_by_aggregation_type, False, self.src_filter, self.exclude_columns, self.numeric_scale, self.enclose_column_by_double_quotes)
            trgt_pdf_from_group_by, trgt_group_by_query_aggregation_string, trgt_group_by_query_columns_string, group_by_columns_trgt, trgt_group_by_error = self.db_service_trgt.create_pandas_df_from_group_by(self.trgt_object, self.result_params.intersection_columns_trgt_src, object_group_by_columns, object_group_by_aggregation_columns, object_group_by_aggregation_type, False, self.trgt_filter, self.exclude_columns, self.numeric_scale, self.enclose_column_by_double_quotes)

             # check if Group-By-Aggregation was actually performed
            if src_group_by_error == {} and trgt_group_by_error == {}:
                diff_src_pdf_from_group_by_sorted, diff_trgt_pdf_from_group_by_sorted, src_pdf_from_group_by_sorted, trgt_pdf_from_group_by_sorted = get_diff_dataframes(src_pdf_from_group_by, trgt_pdf_from_group_by, group_by_columns_src, group_by_columns_trgt)
                if not diff_src_pdf_from_group_by_sorted.empty:
                    logger.debug(f"[{self.comp_id}] diff_src_pdf_from_group_by_sorted:\n {diff_src_pdf_from_group_by_sorted}")
                    logger.debug(f"[{self.comp_id}] diff_trgt_pdf_from_group_by_sorted:\n {diff_trgt_pdf_from_group_by_sorted}")

                for object_group_by_column in object_group_by_columns:
                    # creating Group-By-Values with mismatches
                    if object_group_by_column in diff_src_pdf_from_group_by_sorted and object_group_by_column in diff_trgt_pdf_from_group_by_sorted:
                        group_by_values_with_mismatches [object_group_by_column] = list(set(diff_src_pdf_from_group_by_sorted[object_group_by_column].tolist()).union(set(diff_trgt_pdf_from_group_by_sorted[object_group_by_column].tolist())))
                    elif object_group_by_column in diff_src_pdf_from_group_by_sorted:
                        group_by_values_with_mismatches [object_group_by_column] = diff_src_pdf_from_group_by_sorted[object_group_by_column].tolist()
                    elif object_group_by_column in diff_trgt_pdf_from_group_by_sorted:
                        group_by_values_with_mismatches [object_group_by_column] = diff_trgt_pdf_from_group_by_sorted[object_group_by_column].tolist()
                    else:
                        continue

                    if len(group_by_values_with_mismatches) > self.max_group_by_values_with_mismatches:
                        group_by_values_with_mismatches = [f"Warning: There are more than {self.max_group_by_values_with_mismatches} entries."]
                    else:
                        # creating Group-By-Query where filter
                        group_by_values_with_mismatches_string = ', '.join(f"'{c}'" for c in group_by_values_with_mismatches[object_group_by_column])
                        group_by_query_where_filter+=f" AND {object_group_by_column} IN ({group_by_values_with_mismatches_string})"

                # creating list of columns with mismatches
                for column in diff_src_pdf_from_group_by_sorted.columns:
                    if column in diff_trgt_pdf_from_group_by_sorted.columns and column not in object_group_by_columns:
                        if (diff_src_pdf_from_group_by_sorted[column].equals(diff_trgt_pdf_from_group_by_sorted[column])):
                            continue
                        try:
                            pd.testing.assert_series_equal(diff_src_pdf_from_group_by_sorted[column],diff_trgt_pdf_from_group_by_sorted[column], check_dtype = False, check_index_type= False, check_series_type= False, check_names= False)
                            continue
                        except Exception:
                            columns_with_mismatch.append(column)
                    elif column not in diff_trgt_pdf_from_group_by_sorted.columns and column not in object_group_by_columns:
                        columns_with_mismatch.append(column)
                for column in diff_trgt_pdf_from_group_by_sorted.columns:
                    if column not in diff_src_pdf_from_group_by_sorted.columns and column not in object_group_by_columns:
                        columns_with_mismatch.append(column)


                if group_by_columns_src and group_by_columns_trgt and diff_src_pdf_from_group_by_sorted is not None and diff_trgt_pdf_from_group_by_sorted is not None:
                    group_by_diff_dict = get_diff_dict_from_diff_dataframes(diff_src_pdf_from_group_by_sorted, diff_trgt_pdf_from_group_by_sorted, group_by_columns_src, group_by_columns_trgt, group_by_values_with_mismatches, self.numeric_scale)

            # creating final Group-By-Queries TODO write as function
            if src_group_by_query_columns_string and src_group_by_query_aggregation_string and group_by_query_where_filter and not len(group_by_values_with_mismatches) > self.max_group_by_values_with_mismatches:
                src_group_by_query = f"SELECT {src_group_by_query_columns_string}, COUNT(*) AS COUNT_OF_GROUP_BY_VALUE, {src_group_by_query_aggregation_string} FROM {self.src_object.database}.{self.src_object.schema}.{self.src_object.name} WHERE 1=1 {group_by_query_where_filter} GROUP BY {src_group_by_query_columns_string};"

            if trgt_group_by_query_columns_string and trgt_group_by_query_aggregation_string and group_by_query_where_filter and not len(group_by_values_with_mismatches) > self.max_group_by_values_with_mismatches:
                trgt_group_by_query = f"SELECT {trgt_group_by_query_columns_string}, COUNT(*) AS COUNT_OF_GROUP_BY_VALUE, {trgt_group_by_query_aggregation_string} FROM {self.trgt_object.database}.{self.trgt_object.schema}.{self.trgt_object.name} WHERE 1=1 {group_by_query_where_filter} GROUP BY {trgt_group_by_query_columns_string};"

            # additional evaluation of the pandas_df_from_group_by TODO check if this is really necessary and write as a function
            if src_pdf_from_group_by_sorted is not None and trgt_pdf_from_group_by_sorted is not None:
                try:
                    pandas_df_from_group_by_is_equal = src_pdf_from_group_by_sorted.equals(trgt_pdf_from_group_by_sorted)
                except:
                    pandas_df_from_group_by_is_equal = False

            ## RE-EVALUATE
            if src_group_by_error == {} and trgt_group_by_error == {} and src_pdf_from_group_by_sorted is not None and trgt_pdf_from_group_by_sorted is not None:

                eq_frame = src_pdf_from_group_by_sorted.eq(trgt_pdf_from_group_by_sorted)
                if not pandas_df_from_group_by_is_equal:
                    all_equal_columns = eq_frame.all()
                    if all_equal_columns.all():
                        pandas_df_from_group_by_is_equal = True
                    else:
                        pandas_df_from_group_by_is_equal = False

                src_number_of_rows = len(src_pdf_from_group_by_sorted.index)
                trgt_number_of_rows = len(trgt_pdf_from_group_by_sorted.index)
                logger.info(f"[{self.comp_id}] ROWS src_pdf_from_group_by_sorted: {str(src_number_of_rows)}")
                logger.info(f"[{self.comp_id}] ROWS trgt_pdf_from_group_by_sorted: {str(trgt_number_of_rows)}")
                diff_rows = abs(trgt_number_of_rows - src_number_of_rows)
                logger.info(f"[{self.comp_id}] ROW DIFF: {str(diff_rows)}")

                src_number_of_columns = len(src_pdf_from_group_by_sorted.columns)
                trgt_number_of_columns = len(trgt_pdf_from_group_by_sorted.columns)
                logger.info(f"[{self.comp_id}] COLUMNS src_pdf_from_group_by_sorted: {str(src_number_of_columns)}")
                logger.info(f"[{self.comp_id}] COLUMNS trgt_pdf_from_group_by_sorted: {str(trgt_number_of_columns)}")

                if set(src_pdf_from_group_by_sorted.columns.values) == set(trgt_pdf_from_group_by_sorted.columns.values):
                    src_delta_pdf_pre = src_pdf_from_group_by_sorted.merge(trgt_pdf_from_group_by_sorted, indicator=True, how='outer').query('_merge not in ("both", "right_only")')

                    trgt_delta_pdf_pre = trgt_pdf_from_group_by_sorted.merge(src_pdf_from_group_by_sorted, indicator=True, how='outer').query('_merge not in ("both", "right_only")')

                    ## RE-EVALUATE
                    eq_frame = src_pdf_from_group_by_sorted.eq(trgt_pdf_from_group_by_sorted)
                    if not pandas_df_from_group_by_is_equal:
                        if src_delta_pdf_pre.empty and trgt_delta_pdf_pre.empty:
                            pandas_df_from_group_by_is_equal = True
                        else:
                            pandas_df_from_group_by_is_equal = False

        #### save self.result_params data
        self.result_params.src_group_by_query = src_group_by_query
        self.result_params.trgt_group_by_query = trgt_group_by_query
        self.result_params.src_group_by_error = src_group_by_error
        self.result_params.trgt_group_by_error = trgt_group_by_error
        self.result_params.object_group_by_columns = object_group_by_columns
        self.result_params.group_by_equal = pandas_df_from_group_by_is_equal
        self.result_params.group_by_values_with_mismatches= group_by_values_with_mismatches
        self.result_params.columns_with_mismatch= columns_with_mismatch
        self.result_params.group_by_diff_dict = group_by_diff_dict

    def pandas_dataframe_comparison(self):

        if self.max_object_size > -1:

            if self.src_object.type=='view':
                    src_tbl_size=-1
            else:
                src_tbl_size = self.db_service_src.get_table_size(self.src_object)

            if self.trgt_object.type=='view':
                trgt_tbl_size=-1
            else:
                trgt_tbl_size = self.db_service_trgt.get_table_size(self.trgt_object)
        else:
            src_tbl_size = None
            trgt_tbl_size = None

        if (
            src_tbl_size is None
            or trgt_tbl_size is None
            or src_tbl_size == 0
            or trgt_tbl_size == 0
            or src_tbl_size > self.max_object_size
            or trgt_tbl_size > self.max_object_size
            or self.result_params.src_row_count > self.max_row_number
            or self.result_params.trgt_row_count > self.max_row_number
        ):
            pandas_df_compared = False
            pandas_df_is_equal = None
            pandas_df_mismatch = f"Pandas Dataframes not compared!"
            if src_tbl_size == 0:
                logger.info(f"[{self.comp_id}] Pandas Dataframes not compared -> Source table empty")
            elif trgt_tbl_size == 0:
                logger.info(f"[{self.comp_id}] Pandas Dataframes not compared -> Target table empty")
            else:
                logger.info(f"[{self.comp_id}] Pandas Dataframes not compared -> restricted by input parameters MAX_OBJECT_SIZE and MAX_ROW_NUMBER")
        else:
            logger.info(f"[{self.comp_id}] START Pandas-Dataframe-Comparison")
            src_pdf = self.db_service_src.create_pandas_df(self.src_object, self.result_params.intersection_columns_trgt_src, self.src_filter, self.exclude_columns, self.enclose_column_by_double_quotes)
            trgt_pdf = self.db_service_trgt.create_pandas_df(self.trgt_object, self.result_params.intersection_columns_trgt_src, self.trgt_filter, self.exclude_columns, self.enclose_column_by_double_quotes)

            # sorting the dataframes using the intersecting columns minus excluded columns
            src_pdf_sorted  =  src_pdf.sort_values(by=list(set(self.result_params.intersection_columns_trgt_src) - set(self.exclude_columns))).reset_index(drop=True)
            trgt_pdf_sorted = trgt_pdf.sort_values(by=list(set(self.result_params.intersection_columns_trgt_src) - set(self.exclude_columns))).reset_index(drop=True)

            pandas_df_compared = True
            pandas_df_is_equal = True
            pandas_df_mismatch = ""

            try:
                assert_frame_equal(src_pdf_sorted,trgt_pdf_sorted, check_dtype = False, check_names = False, check_index_type = False, check_column_type = False, check_exact = False)
            except Exception as err:
                pandas_df_is_equal = False
                pandas_df_mismatch =  err

        self.result_params.pandas_df_compared = pandas_df_compared
        self.result_params.pandas_df_is_equal = pandas_df_is_equal
        self.result_params.pandas_df_mismatch = pandas_df_mismatch
        self.result_params.src_tbl_size = src_tbl_size
        self.result_params.trgt_tbl_size = trgt_tbl_size

    def sample_comparison(self):
        logger.info(f"[{self.comp_id}] START Sample-Comparison")
        samples_compared = False
        trgt_key_filters = {}
        trgt_used_columns = []
        src_sample_query = None
        trgt_sample_query = None

        src_sample_pdf = [pd.DataFrame(), {}]
        trgt_sample_pdf = [pd.DataFrame(), {}]
        samples_equal = None
        src_sample_dict  = {}
        trgt_sample_dict = {}
        src_sample_error_dict = {}
        trgt_sample_error_dict = {}
        if "SAMPLE_KEYS" in self.migration_config.keys():
            sample_comparison_config=self.migration_config["SAMPLE_KEYS"]
            if f"{self.src_object.database}.{self.src_object.schema}.{self.src_object.name}" in  sample_comparison_config.keys():
                logger.info(f"[{self.comp_id}] START Sample-Check for: {self.src_object.database}.{self.src_object.schema}.{self.src_object.name}")
                samples_compared = True
                key_columns = sample_comparison_config[f"{self.src_object.database}.{self.src_object.schema}.{self.src_object.name}"]
                trgt_sample_pdf, trgt_key_filters, trgt_used_columns, trgt_sample_query = self.db_service_trgt.create_pandas_df_from_sample(
                                                                                                                                object = self.trgt_object,
                                                                                                                                column_intersections=self.result_params.intersection_columns_trgt_src,
                                                                                                                                key_columns=key_columns,
                                                                                                                                where_clause=self.trgt_filter,
                                                                                                                                exclude_columns=self.exclude_columns,
                                                                                                                                numeric_scale=self.numeric_scale,
                                                                                                                                enclose_column_by_double_quotes=self.enclose_column_by_double_quotes
                                                                                                                                )
                src_sample_pdf, src_key_filters, src_used_columns, src_sample_query = self.db_service_src.create_pandas_df_from_sample(
                                                                                                                            object = self.src_object,
                                                                                                                            column_intersections=self.result_params.intersection_columns_trgt_src,
                                                                                                                            key_columns=key_columns,
                                                                                                                            where_clause=self.src_filter,
                                                                                                                            exclude_columns=self.exclude_columns,
                                                                                                                            key_filters=trgt_key_filters,
                                                                                                                            dedicated_columns=trgt_used_columns,
                                                                                                                            numeric_scale=self.numeric_scale,
                                                                                                                            enclose_column_by_double_quotes=self.enclose_column_by_double_quotes
                                                                                                                            )
                ## Handle Datetime Datatypes -> transform into readable string
                for key in trgt_key_filters:
                    if any((isinstance(x, datetime.date) for x in trgt_key_filters[key]) or (isinstance(x, datetime.datetime) for x in trgt_key_filters[key])):
                        new_value = []
                        for element in trgt_key_filters[key]:
                            new_value.append(str(element))
                        trgt_key_filters[key] = new_value

            # TODO Runden erst hier - vorher create_pandas_df_from_sample ohne Runden zurückgeben und dann hier eine Extra Funktion zum Runden
                if trgt_key_filters:
                    logger.info(f"[{self.comp_id}] Sample-Check Keys: {trgt_key_filters}")
                else:
                    logger.info(f"[{self.comp_id}] Sample-Check Keys not found in column intersection or excluded in ADDITIONAL_CONFIGURATION.")

            src_sample_error_dict   = src_sample_pdf[1]
            trgt_sample_error_dict  = trgt_sample_pdf[1]
            if samples_compared and src_sample_error_dict == {} and trgt_sample_error_dict == {}:
                # sorting the dataframes using the intersecting columns
                src_sample_pdf_sorted  = src_sample_pdf[0] #.sort_values(by=intersection_columns_trgt_src).reset_index(drop=True)
                src_sample_pdf_sorted  = src_sample_pdf_sorted.replace(np.nan, None)
                src_sample_pdf_sorted  = src_sample_pdf_sorted.astype(str)

                trgt_sample_pdf_sorted = trgt_sample_pdf[0] #.sort_values(by=intersection_columns_trgt_src).reset_index(drop=True)
                trgt_sample_pdf_sorted = trgt_sample_pdf_sorted.replace(np.nan, None)
                trgt_sample_pdf_sorted = trgt_sample_pdf_sorted.astype(str)

                src_sample_dict  = src_sample_pdf_sorted.to_dict()
                trgt_sample_dict = trgt_sample_pdf_sorted.to_dict()

                try:
                    pd.testing.assert_frame_equal(src_sample_pdf_sorted,trgt_sample_pdf_sorted,check_dtype = False, check_names = False, check_index_type = False, check_column_type = False, check_exact = False)
                    samples_equal = True
                except:
                    samples_equal = False
            else:
                samples_compared = False
        # save results
        self.result_params.src_sample_query = src_sample_query
        self.result_params.trgt_sample_query = trgt_sample_query
        self.result_params.src_sample_dict = src_sample_dict
        self.result_params.trgt_sample_dict  = trgt_sample_dict
        self.result_params.samples_equal = samples_equal
        self.result_params.src_sample_error_dict= src_sample_error_dict
        self.result_params.trgt_sample_error_dict= trgt_sample_error_dict
        self.result_params.samples_compared = samples_compared
        self.result_params.samples_equal = samples_equal
        self.result_params.trgt_key_filters = trgt_key_filters
