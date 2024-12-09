CREATE TABLE Tree (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    parent_tree_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_tree_id) REFERENCES Tree(id)
);
