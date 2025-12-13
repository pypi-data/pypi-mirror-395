import sqlite3
from edhelper.infra.config import settings
from pathlib import Path


def init_db():
    conn = sqlite3.connect(settings.DATABASE_URL)

    try:
        # Try to find schema.sql relative to this file first
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            # Fallback to BASE_PATH
            schema_path = Path(settings.BASE_PATH) / "edhelper" / "infra" / "schema.sql"
        
        with open(schema_path, "r") as f:
            sql_script = f.read()

        conn.executescript(sql_script)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()
