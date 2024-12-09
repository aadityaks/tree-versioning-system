import os
import sqlite3
from contextlib import closing

DATABASE_PATH = "tree_versioning.db"

def create_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def initialize_db():
    """Initialize the database schema."""

    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    with closing(create_connection()) as conn:
        with open('migrations/01_create_tree_table.sql', 'r') as f:
            conn.executescript(f.read())
        with open('migrations/02_create_treenode_table.sql', 'r') as f:
            conn.executescript(f.read())
        with open('migrations/03_create_treeedge_table.sql', 'r') as f:
            conn.executescript(f.read())
        with open('migrations/04_create_treetag_table.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()

