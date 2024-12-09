from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class TreeNode(Base):
    __tablename__ = 'treenode'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tree_id = Column(Integer, ForeignKey('tree.id'), nullable=False)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    tree = relationship('Tree', back_populates='nodes')
    edges = relationship(
        'TreeEdge',
        back_populates='incoming_node',
        cascade="all, delete-orphan",
        foreign_keys='TreeEdge.incoming_node_id'
    )

