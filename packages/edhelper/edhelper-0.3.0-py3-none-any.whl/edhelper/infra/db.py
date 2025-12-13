from contextlib import contextmanager
from edhelper.infra.config import settings
import sqlite3


@contextmanager
def transaction(cursor=None):
    if cursor is not None:
        yield cursor
        return

    conn = sqlite3.connect(settings.DATABASE_URL)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
