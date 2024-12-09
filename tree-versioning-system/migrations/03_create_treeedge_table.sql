CREATE TABLE TreeEdge (
    id INTEGER PRIMARY KEY,
    incoming_node_id INTEGER NOT NULL,
    outgoing_node_id INTEGER NOT NULL,
    data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incoming_node_id) REFERENCES TreeNode(id),
    FOREIGN KEY (outgoing_node_id) REFERENCES TreeNode(id)
);
