from dataclasses import dataclass

@dataclass
class ResultParams():
        """
        Class to store an object level comparison result for inherent use.
        """

        # last altered
        last_altered_src = None
        last_altered_trgt = None
        not_altered_during_comparison_src = None
        not_altered_during_comparison_trgt = None

        # data types
        datatypes_equal = None

        # row count
        src_row_count = None
        error_list_rows_src = None
        trgt_row_count = None
        error_list_rows_trgt = None
        row_counts_equal = None
        src_row_count_minus_trgt_row_count = None

        # column-names-comparison (for further calculation)
        src_columns = None
        trgt_columns = None
        src_columns_upper = None
        trgt_columns_upper = None

        # column-names-comparison (to save)
        src_columns_minus_trgt_columns = None
        trgt_columns_minus_src_columns = None
        column_level_comparison_result = None
        all_columns_trgt_src = None
        intersection_columns_trgt_src = None
        columns_equal = None

        # aggregation-comparison
        src_column_datatypes = None
        src_columns_aggregate = None
        trgt_column_datatypes = None
        trgt_columns_aggregate = None
        src_aggregations_error = None
        trgt_aggregations_error = None
        aggregations_compared = None
        aggregation_differences_trgt_minus_src = None

        # aggregation-comparison (to save)
        aggregations_equal = None
        all_count_nulls_equal = None

        # error handling (row-count-comparison and aggregation-comparison)
        src_error_dict = None
        trgt_error_dict = None

        # group-by-comparison (to save)
        src_group_by_query = None
        trgt_group_by_query = None
        src_group_by_error = None
        trgt_group_by_error = None
        object_group_by_columns = None
        group_by_equal = None
        group_by_values_with_mismatches = None
        columns_with_mismatch = None
        group_by_diff_dict = None

        # sample-check (to save)
        src_sample_query = None
        trgt_sample_query = None
        src_sample_dict = None
        trgt_sample_dict = None
        src_sample_error_dict = None
        trgt_sample_error_dict = None
        samples_compared = None
        samples_equal = None
        trgt_key_filters = None

        # pandas-dataframe-comparison (for further calculation)
        pandas_df_mismatch = None
        src_tbl_size = None
        trgt_tbl_size = None


        # pandas-dataframe-comparison (to save)
        pandas_df_compared = None
        pandas_df_is_equal = None

        # not part of result class:
        # global_iflter
        # exclude_columns
        # trgt_key_filters= None
        # additional_configuration_per_table = None
