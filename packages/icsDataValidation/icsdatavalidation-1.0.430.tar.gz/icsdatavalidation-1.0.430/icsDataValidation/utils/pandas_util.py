import numpy as np
from decimal import Decimal



def get_diff_dataframes(df_1, df_2, key_columns_1, key_columns_2):
    """
    Get the the difference between two Pandas Dataframes by sorting over specific key-columns.
    Returns the two dataframes containing only the rows with differences from the input dataframes and the sorted dataframes.
    """
    df_1_sorted = df_1.sort_values(by=key_columns_1).reset_index(drop=True)
    df_2_sorted = df_2.sort_values(by=key_columns_2).reset_index(drop=True)

    diff_1 = df_1_sorted[~df_1_sorted.apply(tuple,1).isin(df_2_sorted.apply(tuple,1))]
    diff_2 = df_2_sorted[~df_2_sorted.apply(tuple,1).isin(df_1_sorted.apply(tuple,1))]

    diff_1 = diff_1.reset_index(drop=True)
    diff_2 = diff_2.reset_index(drop=True)

    return diff_1, diff_2, df_1_sorted, df_2_sorted


def get_diff_dict_from_diff_dataframes(diff_1, diff_2, key_columns_1, key_columns_2, key_column_values_with_mismatches, numeric_scale):
    """
    Get the 
    """
    diff_dict = {}

    #TODO support a list of key_columns_1 (and key_columns_2) and a dictionary of key_column_values_with_mismatches
    key_column_1=key_columns_1[0]
    key_column_2=key_columns_2[0]
    key_column_values_with_mismatches=key_column_values_with_mismatches[key_column_1]

    for value_with_mismatch in key_column_values_with_mismatches:
        
        if value_with_mismatch is None:
            row_1_with_mismatch = diff_1.loc[diff_1[key_column_1].isnull()]
            row_2_with_mismatch = diff_2.loc[diff_2[key_column_2].isnull()]
            value_with_mismatch = 'NULL'
        else:
            row_1_with_mismatch = diff_1.loc[diff_1[key_column_1] == value_with_mismatch]
            row_2_with_mismatch = diff_2.loc[diff_2[key_column_2] == value_with_mismatch]
            value_with_mismatch = str(value_with_mismatch)

        diff_dict[value_with_mismatch] = {}

        for column in row_1_with_mismatch:
            if column == 'group_by_column' or column not in row_2_with_mismatch or column in key_columns_1:
                continue

            if row_1_with_mismatch[column].values.size > 0:
                src_value=row_1_with_mismatch[column].values[0]
            elif column=='COUNT_OF_GROUP_BY_VALUE':
                src_value=0
            else:
                src_value= None

            if row_2_with_mismatch[column].values.size > 0:
                trgt_value=row_2_with_mismatch[column].values[0]
            elif column=='COUNT_OF_GROUP_BY_VALUE':
                trgt_value=0
            else:
                trgt_value= None
            
            try:
                src_value= src_value.item()
            except Exception:
                pass

            try:
                trgt_value= trgt_value.item()
            except Exception:
                pass
            
            if src_value != trgt_value: 
                if src_value is None:
                    diff_trgt_minus_src = trgt_value
                elif trgt_value is None:
                    if isinstance(src_value, str) or isinstance(trgt_value, str):
                        diff_trgt_minus_src = f"{-int(src_value.split('_',1)[0])}_{-int(src_value.split('_',1)[1])}"
                    else:
                        diff_trgt_minus_src = -round(float(src_value), numeric_scale)
                else:
                    if isinstance(src_value, str) or isinstance(trgt_value, str):
                        diff_trgt_minus_src = f"{int(trgt_value.split('_',1)[0])-int(src_value.split('_',1)[0])}_{int(trgt_value.split('_',1)[1])-int(src_value.split('_',1)[1])}"
                    else:
                        diff_trgt_minus_src = round(float(trgt_value)-float(src_value), numeric_scale)
                
                if diff_trgt_minus_src:
                    diff_dict[value_with_mismatch][column] = {
                        "SRC_VALUE": src_value,
                        "TRGT_VALUE": trgt_value,
                        "DIFF_TRGT_MINUS_SRC": diff_trgt_minus_src
                        }
        if not diff_dict[value_with_mismatch]:
            diff_dict.pop(value_with_mismatch)

    if not diff_dict:
        diff_dict = None

    return diff_dict



#########################################################################################################
#TODO write as pytest
# Test Space 
import pandas as pd

# *** TEST 1 ***
#df1 = pd.DataFrame({'group_by_column': [1, 2,3,6], 'A': [1, 1,9,2], 'B': [1, 3,9,2], 'C': [1, 4,9,2],'D': ['1_1', '1_1','8_3','1_1']})
#df2 = pd.DataFrame({'group_by_column': [2, 1,3,5], 'A': [2, 1,9,1], 'B': [3, 1,5,1], 'C': [5, 1,9,1],'D': ['1_1', '1_1','5_5','1_1']})
#key_column_values_with_mismatches={'group_by_column':[None,3,5,6]}
#numeric_scale=2

#########

# *** TEST 2 ***
#df1 = pd.DataFrame({'group_by_column': [1, None,3,6], 'A': [1, 1,9,2], 'B': [1, 3,9,2], 'C': [1, 4,9,2],'D': ['1_1', '1_1','8_3','1_1']})
#df2 = pd.DataFrame({'group_by_column': [None, 1,3,5], 'A': [2, 1,9,1], 'B': [3, 1,5,1], 'C': [5, 1,9,1],'D': ['1_1', '1_1','5_5','1_1']})
#key_column_values_with_mismatches={'group_by_column':[None,3,5,6]}
#numeric_scale=2

#########

# *** TEST 3 ***
#df1 = pd.DataFrame({'group_by_column': [1, 2,3,4], 'A': [1, 1,9,2.001], 'B': [1, 3,9,2.0004], 'C': [1, 4,9,2.00000000001],'D': ['1_1', '1_1','8_3','1_1']})
#df2 = pd.DataFrame({'group_by_column': [1, 2,3,4], 'A': [2, 1,9,Decimal(2.001)], 'B': [3, 3,9,2.0005], 'C': [1, 4,9,2.00000000004],'D': ['1_1', '1_1','8_3','1_1']})
#key_column_values_with_mismatches={'group_by_column':[1,2,3,4]}
#numeric_scale=7
#
##########
#
#diff_1, diff_2, df_1_sorted, df_2_sorted =get_diff_dataframes(df1, df2, ['group_by_column'], ['group_by_column'])
#diff_dict = get_diff_dict_from_diff_dataframes(df1, df2, ['group_by_column'], ['group_by_column'], key_column_values_with_mismatches, numeric_scale)
#import json
#import decimal
#import numpy as np
#
#class CustomJSONEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            return str(o)
#        if isinstance(o, np.integer):
#            return int(o)
#        if isinstance(o, np.floating):
#            return float(o)
#        if isinstance(o, np.ndarray):
#            return o.tolist()
#        try:
#            super(CustomJSONEncoder, self).default(o)
#        except:
#            return str(o)
#
#        return super(CustomJSONEncoder, self).default(o)
#
#diff_json = json.dumps(diff_dict, indent=4, cls=CustomJSONEncoder)
#
#print(diff_json)