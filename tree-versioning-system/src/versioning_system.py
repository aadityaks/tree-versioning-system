from sqlalchemy.orm import Session
from .models.tree import Tree
from .models.treenode import TreeNode
from .models.treeedge import TreeEdge
from .models.treetag import TreeTag

def create_tag(session: Session, tree_id: int, tag_name: str, description: str = ""):
    """Create a tag for a specific tree configuration."""
    tag = TreeTag(tree_id=tree_id, tag_name=tag_name, description=description)
    session.add(tag)
    session.commit()
    return tag

def create_new_version_from_tag(session: Session, tag_name: str):
    """Create a new tree version from an existing tagged configuration."""
    tag = session.query(TreeTag).filter_by(tag_name=tag_name).first()
    if not tag:
        raise ValueError(f"Tag '{tag_name}' not found.")

    new_tree = Tree(name=f"New version from {tag_name}", parent_tree_id=tag.tree_id)
    session.add(new_tree)
    session.commit()

    old_to_new_id_map = {}

    # Copy all the nodes from the tagged Tree to the new Tree.
    for node in tag.tree.nodes:
        new_node = TreeNode(tree_id=new_tree.id, data=node.data)
        session.add(new_node)
        session.commit()
        old_to_new_id_map[node.id] = new_node.id # Record the mapping of old node ID to new node ID.

    for node in tag.tree.nodes:
        for edge in node.edges:
            new_incoming_id = old_to_new_id_map[node.id]
            new_outgoing_id = old_to_new_id_map[edge.outgoing_node.id]

            new_edge = TreeEdge(
                incoming_node_id=new_incoming_id,
                outgoing_node_id=new_outgoing_id,
                data=edge.data
            )
            session.add(new_edge)

    session.commit()  # make sure all changes are committed
    return new_tree, old_to_new_id_map

def get_tree_by_tag(session: Session, tag_name: str) -> Tree:
    """Retrieve the tree associated with a given tag name without creating a new version."""
    tag = session.query(TreeTag).filter_by(tag_name=tag_name).first()
    if not tag:
        raise ValueError(f"Tag '{tag_name}' not found.")
    return tag.tree

def get_child_versions(session: Session, tree_id: int):
    """Get all direct child versions of a given tree."""
    children = session.query(Tree).filter_by(parent_tree_id=tree_id).all()
    return children
