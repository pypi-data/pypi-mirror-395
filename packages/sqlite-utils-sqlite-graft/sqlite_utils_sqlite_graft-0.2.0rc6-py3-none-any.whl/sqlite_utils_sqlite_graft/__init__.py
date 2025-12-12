
from sqlite_utils import hookimpl
import sqlite_graft

__version__ = "0.2.0rc6"
__version_info__ = tuple(__version__.split("."))

@hookimpl
def prepare_connection(conn):
  conn.enable_load_extension(True)
  sqlite_graft.load(conn)
  conn.enable_load_extension(False)
