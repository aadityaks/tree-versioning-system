from sqlalchemy.orm import Session
from .models.tree import Tree
from .models.treenode import TreeNode
from .models.treeedge import TreeEdge

def traverse_tree(session: Session, tree_id: int, node_id: int):
    """Traverse and print the tree from a specific node."""
    node = session.query(TreeNode).filter_by(id=node_id, tree_id=tree_id).first()
    if not node:
        print("Node not found.")
        return

    print(f"Node {node.id} data: {node.data}")
    edges = session.query(TreeEdge).filter_by(incoming_node_id=node.id).all()
    for edge in edges:
        print(f"Edge {edge.id}: {edge.data}")
        traverse_tree(session, tree_id, edge.outgoing_node_id)
