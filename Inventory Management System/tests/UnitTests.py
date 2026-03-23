import sqlite3
import sys
from pathlib import Path

import pytest

# Something to fix importing, found on https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import create_db, databaseHandler, directoryHandler

# monkeypatch will used to edit directoryHandler base_path value to temp path used for testing.
def setMonkeypatch(tmp_path, monkeypatch):
    monkeypatch.setattr(directoryHandler, "base_path", lambda: str(tmp_path))

@pytest.fixture() #makes isolated_db into a variable used later.
def isolated_db(tmp_path, monkeypatch):
    setMonkeypatch(tmp_path, monkeypatch)
    db_dir = Path(directoryHandler.database_path())
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "ims.db"


def test_directoryHandler_path_helpers(tmp_path, monkeypatch):
    setMonkeypatch(tmp_path, monkeypatch)

    image_dir = Path(directoryHandler.image_path())
    bill_dir = Path(directoryHandler.bill_path())
    db_dir = Path(directoryHandler.database_path())

    assert image_dir.name == "images"
    assert image_dir.exists()

    assert bill_dir.name == "bill"
    assert bill_dir.exists()

    assert db_dir.name == "database"


def test_create_db_creates_expected_tables(isolated_db):
    create_db.create_db()

    con = sqlite3.connect(isolated_db)
    cur = con.cursor()
    try:
        tables = {
            row[0]
            for row in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

        expected = {"employee", "supplier", "category", "product"}
        assert expected.issubset(tables)
    finally:
        con.close()


def test_databaseHandler_connects_to_expected_db_file(isolated_db):
    cur, con = databaseHandler.get_con_and_cursor()
    try:
        cur.execute("SELECT 1")
        assert cur.fetchone()[0] == 1
    finally:
        con.close()

    assert isolated_db.exists()