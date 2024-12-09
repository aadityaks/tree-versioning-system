import pytest
from src.database import create_connection, initialize_db
from src.traversal import traverse_tree
from src.models.tree import Tree
from src.models.treenode import TreeNode
from src.models.treeedge import TreeEdge
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO
import sys

@pytest.fixture
def session():
    initialize_db()
    engine = create_engine('sqlite:///tree_versioning.db')
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    engine.dispose()

def test_traverse_single_node_tree(session, capsys):
    # Create a single node tree
    tree = Tree(name="Single Node Tree")
    session.add(tree)
    session.commit()

    root_node = TreeNode(tree_id=tree.id, data={"root": True})
    session.add(root_node)
    session.commit()

    traverse_tree(session, tree.id, root_node.id) # Capture output
    captured = capsys.readouterr()
    assert "Node" in captured.out
    assert "data: {'root': True}" in captured.out

def test_traverse_multiple_nodes(session, capsys):
    tree = Tree(name="Multi Node Tree") # Create a tree with multiple nodes and edges
    session.add(tree)
    session.commit()

    root_node = TreeNode(tree_id=tree.id, data={"root": "value"})
    child_node = TreeNode(tree_id=tree.id, data={"child": "value"})
    session.add(root_node)
    session.add(child_node)
    session.commit()

    edge = TreeEdge(incoming_node_id=root_node.id, outgoing_node_id=child_node.id, data={"relationship": "parent-child"})
    session.add(edge)
    session.commit()

    traverse_tree(session, tree.id, root_node.id)
    captured = capsys.readouterr()
    assert "Node" in captured.out
    assert "data: {'root': 'value'}" in captured.out
    assert "data: {'child': 'value'}" in captured.out

def test_traverse_invalid_node(session, capsys):
    tree = Tree(name="Empty Tree") # Tree doesn't have edges
    session.add(tree)
    session.commit()

    traverse_tree(session, tree.id, 999) # Try traversing a node that doesn't exist
    captured = capsys.readouterr()
    assert "Node not found." in captured.out

def test_traverse_branching(session, capsys):
    tree = Tree(name="Branching Tree")  # Create a branching tree
    session.add(tree)
    session.commit()

    root = TreeNode(tree_id=tree.id, data={"node": "root"})
    child1 = TreeNode(tree_id=tree.id, data={"node": "child1"})
    child2 = TreeNode(tree_id=tree.id, data={"node": "child2"})
    session.add_all([root, child1, child2])
    session.commit()

    # Add edges
    edge1 = TreeEdge(incoming_node_id=root.id, outgoing_node_id=child1.id, data={"edge": "root->child1"})
    edge2 = TreeEdge(incoming_node_id=root.id, outgoing_node_id=child2.id, data={"edge": "root->child2"})
    session.add_all([edge1, edge2])
    session.commit()

    traverse_tree(session, tree.id, root.id)
    captured = capsys.readouterr()

    # Should see root, child1, and child2 in output
    assert "data: {'node': 'root'}" in captured.out
    assert "data: {'node': 'child1'}" in captured.out
    assert "data: {'node': 'child2'}" in captured.out
    # Check edges printed
    assert "Edge" in captured.out
    assert "root->child1" in captured.out
    assert "root->child2" in captured.out
