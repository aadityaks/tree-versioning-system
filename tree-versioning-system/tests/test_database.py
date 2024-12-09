import os
import pytest
import sqlite3
from src.database import DATABASE_PATH, create_connection, initialize_db

@pytest.fixture
def setup_db():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    initialize_db()
    yield
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

def test_database_connection(setup_db):
    conn = create_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

def test_tables_exist(setup_db):
    # Check if table exists
    conn = create_connection()
    cursor = conn.cursor()

    tables = {"Tree", "TreeNode", "TreeEdge", "TreeTag"}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    db_tables = {row[0] for row in cursor.fetchall()}

    for table in tables:
        assert table in db_tables, f"Table '{table}' should exist in the database."

    conn.close()

def test_insert_data(setup_db):
    # Basic test to ensure we can insert a tree and query it
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Tree (name) VALUES ('Test Tree')")
    conn.commit()

    cursor.execute("SELECT id, name FROM Tree WHERE name='Test Tree'")
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == 'Test Tree'
    conn.close()

def test_tag_index(setup_db):
    conn = create_connection() # Does tag name exists ? 
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('TreeTag')")
    indexes = cursor.fetchall()
    index_names = {idx[1] for idx in indexes}  # idx[1] is the index name
    assert 'idx_treetag_tag_name' in index_names
    conn.close()
