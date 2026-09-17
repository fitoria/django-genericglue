from django.db import connections, DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate


# introspection.table_names() lists every table in the database to answer a
# question about one. Cache the set per connection for the life of the process.
_table_names = {}


def clear_table_names_cache(**kwargs):
    """Drop the cached table names. Wired to post_migrate, so a process that
    creates tables (migrate, or a test runner building its database) sees them
    straight away."""
    _table_names.clear()


post_migrate.connect(
    clear_table_names_cache,
    dispatch_uid="genericglue.utils.clear_table_names_cache",
)


def table_exists(table_name, database=DEFAULT_DB_ALIAS):
    """
    Determines if the given table_name exists in the specified database.
    """
    names = _table_names.get(database)
    if names is None:
        names = _table_names[database] = frozenset(
            connections[database].introspection.table_names()
        )
    return table_name in names
