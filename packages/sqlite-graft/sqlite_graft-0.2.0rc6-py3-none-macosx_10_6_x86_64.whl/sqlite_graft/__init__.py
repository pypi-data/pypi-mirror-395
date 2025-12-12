
from os import path
import sqlite3

__version__ = "0.2.0rc6"
__version_info__ = tuple(__version__.split("."))

def loadable_path():
  """ Returns the full path to the sqlite-graft loadable SQLite extension bundled with this package """

  loadable_path = path.join(path.dirname(__file__), "libgraft_sqlite_extension")
  return path.normpath(loadable_path)

def load(conn: sqlite3.Connection)  -> None:
  """ Load the sqlite-graft SQLite extension into the given database connection. """

  conn.load_extension(loadable_path())

