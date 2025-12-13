from tinydb import TinyDB
from platformdirs import user_data_dir
from pathlib import Path

_db_instance = None


def get_db():
    global _db_instance
    if _db_instance is None:
        app_data_dir = Path(user_data_dir("algoflex"))
        app_data_dir.mkdir(parents=True, exist_ok=True)
        path = Path(app_data_dir, "stats.json")
        _db_instance = TinyDB(path=path)
    return _db_instance
