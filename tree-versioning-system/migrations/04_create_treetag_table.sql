CREATE TABLE TreeTag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tree_id INTEGER NOT NULL,
    tag_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(tree_id) REFERENCES Tree(id)
);

CREATE INDEX idx_treetag_tag_name ON TreeTag (tag_name);
