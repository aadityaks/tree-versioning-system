from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import initialize_db, create_connection
from src.versioning_system import create_tag, create_new_version_from_tag, get_tree_by_tag, get_child_versions
from src.traversal import traverse_tree
from src.models.tree import Tree
from src.models.treenode import TreeNode
from src.models.treeedge import TreeEdge
from src.models.treetag import TreeTag

# Initialize the database
initialize_db()

engine = create_engine('sqlite:///tree_versioning.db')
Session = sessionmaker(bind=engine)
session = Session()

def demo_create_tree():
    """Create a new tree."""
    tree = Tree(name="Demo Tree for Versioning")
    session.add(tree)
    session.commit()
    print(f"Created tree: {tree.name} (ID: {tree.id})")
    return tree

def demo_create_tag(tree):
    """Create a new tag for the given tree."""
    tag = create_tag(session, tree.id, "v1.0", "Initial version of the tree")
    print(f"Created tag: {tag.tag_name} for tree ID: {tree.id}")
    return tag

def demo_create_new_version_from_tag(tag_name):
    """Create a new version of the tree based on a tag."""
    new_tree, old_to_new_id_map = create_new_version_from_tag(session, tag_name)
    print(f"Created new tree version: {new_tree.name} (Parent Tree ID: {new_tree.parent_tree_id})")
    return new_tree, old_to_new_id_map

def demo_add_nodes_and_edges(tree):
    """Add nodes and edges to the tree."""
    root_node = TreeNode(tree_id=tree.id, data={"root": "value"})
    session.add(root_node)
    session.commit()

    child_node = TreeNode(tree_id=tree.id, data={"child": "value"}) # Create a child node
    session.add(child_node)
    session.commit()

    # Create an edge between the root node and child node
    edge = TreeEdge(incoming_node_id=root_node.id, outgoing_node_id=child_node.id, data={"relationship": "parent-child"})
    session.add(edge)
    session.commit()

    print(f"Added root node (ID: {root_node.id}) and child node (ID: {child_node.id}) with edge ID: {edge.id}")
    return root_node, child_node

def demo_traversal(tree, start_node_id):
    """Traverse the tree starting from a given node."""
    print(f"Traversing tree {tree.name} starting from node ID: {start_node_id}")
    traverse_tree(session, tree.id, start_node_id)

def run_demo():
    tree = demo_create_tree()

    # Add nodes and edges to the tree
    root_node, child_node = demo_add_nodes_and_edges(tree)

    # Usecase: Create a tag for the tree
    tag = demo_create_tag(tree)

    # Usecase: Create a new version from the tag, get the mapping
    new_tree, old_to_new_id_map = demo_create_new_version_from_tag(tag.tag_name)

    # Usecase: Traverse the original tree
    demo_traversal(tree, root_node.id)

    # Usecase: Traverse the new tree version using the mapped root node ID
    new_root_node_id = old_to_new_id_map[root_node.id]
    demo_traversal(new_tree, new_root_node_id)

    # ********** New Usecases **********

    # Usecase: Retrieve the original tree by tag without creating a new version
    tagged_tree = get_tree_by_tag(session, "v1.0")
    print(f"Retrieved tree {tagged_tree.name} by tag 'v1.0' without creating a new version.")

    demo_traversal(tagged_tree, root_node.id) # Traverse it from the original root node (id=1)

    # Usecase: List child versions of the original tree
    children = get_child_versions(session, tree.id)
    for child_version in children:
        print(f"Child version of Tree {tree.id}: {child_version.name} (ID: {child_version.id})")

    # If there's a child version, we can also traverse it from its root
    if children:
        # Assuming the root node of a child version is also structured similarly
        # In a real scenario, we would query for the root node of the child version.
        # For simplicity: let's pick the first child's first node
        child_version_tree = children[0]
        first_node_of_child = session.query(TreeNode).filter_by(tree_id=child_version_tree.id).first()
        if first_node_of_child:
            demo_traversal(child_version_tree, first_node_of_child.id)

if __name__ == "__main__":
    run_demo()
