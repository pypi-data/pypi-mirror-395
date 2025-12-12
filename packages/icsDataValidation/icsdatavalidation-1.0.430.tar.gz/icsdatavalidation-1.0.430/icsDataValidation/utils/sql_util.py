

def parse_filter(filter_list:list)->str:
    """
    Retrieve a where-filter in SQL-Syntax from a list of defined conditions.
    """
    if filter_list != []:
        where_clause = "WHERE "
        for filter_condition in filter_list:
            where_clause += f"({filter_condition}) AND "
        where_clause = where_clause[:-4]
    else:
        where_clause = ""
    return where_clause