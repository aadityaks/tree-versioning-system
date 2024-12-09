import pytest
from src.database import create_connection, initialize_db
from src.versioning_system import create_tag, create_new_version_from_tag, get_tree_by_tag, get_child_versions
from src.models.tree import Tree
from src.models.treenode import TreeNode

@pytest.fixture
def session():
    # Fresh DB for each test
    initialize_db()
    conn = create_connection()
    # In a real scenario, we'd likely use SQLAlchemy sessions directly. 
    # For these tests, let's just simulate a session using SQLAlchemy directly if possible.
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('sqlite:///tree_versioning.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()

def test_create_tag(session):
    tree = Tree(name="Test Tree")
    session.add(tree)
    session.commit()

    tag = create_tag(session, tree.id, "v1.0", "Initial version")
    assert tag is not None
    assert tag.tag_name == "v1.0"
    assert tag.description == "Initial version"
    assert tag.tree_id == tree.id

def test_create_new_version_from_tag(session):
    tree = Tree(name="Original Tree")
    session.add(tree)
    session.commit()

    node1 = TreeNode(tree_id=tree.id, data={"root": True})
    session.add(node1)
    session.commit()

    # Tag the original tree
    create_tag(session, tree.id, "orig-tag", "Base version")

    # Create a new version from the tag
    new_tree, mapping = create_new_version_from_tag(session, "orig-tag")
    assert new_tree.parent_tree_id == tree.id
    assert isinstance(mapping, dict)
    # The new tree should have a copied node
    new_nodes = session.query(TreeNode).filter_by(tree_id=new_tree.id).all()
    assert len(new_nodes) == 1
    assert new_nodes[0].data == {"root": True}
    # mapping should map old node id to new node id
    assert node1.id in mapping

def test_get_tree_by_tag(session):
    tree = Tree(name="Tree for Tag Retrieval")
    session.add(tree)
    session.commit()

    # Add and tag
    create_tag(session, tree.id, "retrieval-tag", "Snapshot")
    tagged_tree = get_tree_by_tag(session, "retrieval-tag")
    assert tagged_tree.id == tree.id

def test_get_tree_by_invalid_tag(session):
    with pytest.raises(ValueError):
        get_tree_by_tag(session, "non-existent-tag")

def test_child_versions(session):
    # Create a parent tree
    parent_tree = Tree(name="Parent Tree")
    session.add(parent_tree)
    session.commit()
    create_tag(session, parent_tree.id, "parent-tag", "Base") # Tag parent tree
    child_tree, _ = create_new_version_from_tag(session, "parent-tag") # Create child version

    children = get_child_versions(session, parent_tree.id)
    assert len(children) == 1
    assert children[0].id == child_tree.id
    
    no_children = get_child_versions(session, child_tree.id) #A tree with no children returns an empty list
    assert no_children == []
