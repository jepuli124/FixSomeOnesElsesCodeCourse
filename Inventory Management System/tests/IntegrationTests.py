import sqlite3
import sys
from pathlib import Path

import pytest

# Something to fix importing, found on https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import create_db, directoryHandler


# monkeypatch will used to edit directoryHandler base_path value to temp path used for testing.
def setMonkeypatch(tmp_path, monkeypatch):
    monkeypatch.setattr(directoryHandler, "base_path", lambda: str(tmp_path))

@pytest.fixture() #makes isolated_db into a variable used later.
def isolated_db(tmp_path, monkeypatch):
    setMonkeypatch(tmp_path, monkeypatch)
    db_dir = Path(directoryHandler.database_path())
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "ims.db"



def test_integration_insert_and_query_active_products(isolated_db):
    create_db.create_db()

    con = sqlite3.connect(isolated_db)
    cur = con.cursor()
    try:

        cur.execute("INSERT INTO category(name) VALUES (?)", ("Electronics",))
        cur.execute(
            "INSERT INTO supplier(invoice,name,contact,desc) VALUES (?,?,?,?)",
            (1, "ACME Supplies", "9999999999", "Test supplier"),
        )
        
        cur.execute(
            """
            INSERT INTO product(Category,Supplier,name,price,qty,status)
            VALUES (?,?,?,?,?,?)
            """,
            ("Electronics", "ACME Supplies", "Phone", "1000", "10", "Active"),
        )
        con.commit()

        active = cur.execute(
            "SELECT pid,name,price,qty,status FROM product WHERE status='Active'"
        ).fetchall()
        assert len(active) == 1
        pid, name, price, qty, status = active[0]
        assert name == "Phone"
        assert price == "1000"
        assert qty == "10"
        assert status == "Active"

        # Mimic the billing logic update: qty -> 0, status -> Inactive.
        cur.execute("UPDATE product SET qty=?, status=? WHERE pid=?", ("0", "Inactive", pid))
        con.commit()

        inactive = cur.execute(
            "SELECT pid,name,qty,status FROM product WHERE status='Inactive'"
        ).fetchall()
        assert len(inactive) == 1
        assert inactive[0][2] == "0"
        assert inactive[0][3] == "Inactive"
    finally:
        con.close()


def test_integration_create_db_does_not_drop_existing_rows(isolated_db):
    create_db.create_db()

    con = sqlite3.connect(isolated_db)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO category(name) VALUES (?)", ("Gadgets",))
        con.commit()

        # Re-run schema creation; IF NOT EXISTS should keep data intact.
        create_db.create_db()

        rows = cur.execute("SELECT name FROM category WHERE name=?", ("Gadgets",)).fetchall()
        assert len(rows) == 1
    finally:
        con.close()