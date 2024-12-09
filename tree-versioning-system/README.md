# Tree Versioning System

## Introduction

Tree Versioning System is an application to versioning and managing hierarchical trees with the SQL Database. The tree has nodes (all storage configuration data) and edges (form the relationships between those nodes). With this application, you could do the following things:

- Tag specific tree states with meaningful labels.
- Create new versions (or branches) of a tree from any tagged configuration.
- Traverse and inspect the state of the tree at any point in time.
- Manage and navigate between multiple versions of the same tree lineage.

## Features

1. **Tagging System:**
   - Assign user-defined tags to a particular state of the tree.
   - Store metadata (description, creation time) about tags.
   - Retrieve the tree as it was when a given tag was created.

2. **Version Management:**
   - Create new versions of a tree from an existing tagged configuration.
   - Maintain parent-child relationships between versions.
   - Easily navigate from a tree to its derived versions.

3. **Tree Traversal and Inspection:**
   - Traverse the tree starting from any node to inspect its nodes and edges.
   - Access nodes and edges for both the original and newly created versions at any tagged point in time.

4. **Efficiency and Indexing:**
   - Uses a simple SQLite database for storage.
   - Includes indexing on the `tag_name` column in the `TreeTag` table for efficient retrieval by tags.

## Repository Structure
├── README.md
├── demo.py
├── migrations
│   ├── 01_create_tree_table.sql
│   ├── 02_create_treenode_table.sql
│   ├── 03_create_treeedge_table.sql
│   └── 04_create_treetag_table.sql
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── database.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── tree.py
│   │   ├── treeedge.py
│   │   ├── treenode.py
│   │   └── treetag.py
│   ├── traversal.py
│   └── versioning_system.py
├── tests
│   ├── test_database.py
│   ├── test_traversal.py
│   └── test_versioning.py
└── tree_versioning.db

### Key Files

- **`demo.py`**: A script demonstrating the full workflow of creating a tree, tagging it, creating new versions from tags, and traversing the trees.
- **`migrations/`**: Contains SQL files to set up the necessary database tables.
- **`src/database.py`**: Handles database initialization and connection.
- **`src/models/`**: Contains SQLAlchemy ORM models for `Tree`, `TreeNode`, `TreeEdge`, and `TreeTag`.
- **`src/versioning_system.py`**: Implements functionalities to tag trees, create new versions from tags, and retrieve trees by tags.
- **`src/traversal.py`**: Provides a function to traverse a given tree from a starting node.
- **`tests/`**: Contains test files to validate database operations, versioning, and traversal logic.

## Installation and Setup Guide

### Prerequisites

- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/) for managing Python packages.
- SQLite (comes pre-installed on most systems).

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/tree-versioning-system.git
   cd tree-versioning-system
2. **Create and Activate a Virtual Environment (Optional but Recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Run Demo:**
    ```bash
    python demo.py
    
## Usage Scenarios

The `demo.py` file provides a full demonstration of the workflow:

### Creating a Tree and Adding Data
- A new tree is created.
- Nodes and edges are added to represent configuration data and relationships.

### Tagging a Tree State
- Assign a tag (like `v1.0`) to the current configuration of the tree.
- This allows you to return to this exact state later.

### Creating a New Version from a Tag
- Using `create_new_version_from_tag("v1.0")`, a new tree version is created.
- The nodes and edges from the original tagged state are copied into the new version.
- This simulates branching in feature development—e.g., creating a feature branch from a stable release tag.

### Retrieving and Traversing a Tree by Tag
- `get_tree_by_tag("v1.0")` retrieves the original tree as it was at `v1.0`.
- Traverse the retrieved tree or the new version at any time to inspect data.

### Navigating Between Versions
- `get_child_versions(tree_id)` returns all direct children of a tree.
- Traverse child versions to understand their structure or continue to evolve them by adding nodes, edges, or tags.

## Design Decisions and Tradeoffs

**SQLite as the Database:**
- **Decision**: Chose SQLite for simplicity and portability.
- **Tradeoff**: SQLite is file-based and may not scale well for very large datasets or high concurrency. For large-scale production environments, a more robust DB (e.g., Postgres) may be needed.

**SQLAlchemy ORM vs. Raw SQL:**
- **Decision**: Used SQLAlchemy ORM for better maintainability, readability, and easier schema evolution.
- **Tradeoff**: Direct SQL can sometimes be faster and more explicit. However, ORM improves development speed and code clarity.

**Schema Design:**
- **Tree Table**: Stores the identity and optional `parent_tree_id` for versioning lineage.
- **TreeNode Table**: Holds node-specific data (JSON field for flexibility in storing configuration).
- **TreeEdge Table**: Defines relationships between nodes. Foreign keys maintain referential integrity.
- **TreeTag Table**: Allows tagging any tree version and quickly retrieving it.
- **Tradeoff**: Using JSON columns for node/edge data provides flexibility but no strict schema for configuration data. For more complex use cases, consider structured fields or separate tables.

**Indexing for Performance:**
- **Decision**: Indexed `tag_name` in `TreeTag` to make lookups by tag efficient.
- **Tradeoff**: Additional indexes mean more storage and slightly slower writes, but the benefit of faster reads is worth it for a common operation.

**Versioning Approach:**
- **Decision**: Fully copy nodes and edges to a new version. This ensures each version is self-contained.
- **Tradeoff**: Copying can lead to data duplication. An alternative is a more complicated approach using references and deltas. For simplicity and clarity, full copying is chosen.

