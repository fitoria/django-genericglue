from django.db import connections, DEFAULT_DB_ALIAS


def table_exists(table_name, database=DEFAULT_DB_ALIAS):
    """
    Determines if the given table_name exists in the specified database.
    """
    connection = connections[database]
    return table_name in connection.introspection.table_names()
