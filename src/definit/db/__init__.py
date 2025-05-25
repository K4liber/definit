from definit.db.interface import DatabaseAbstract
from definit.db.md import DatabaseMd

_DATABASE = DatabaseMd()


def get_database() -> DatabaseAbstract:
    """
    Get the database instance.
    """
    return _DATABASE
