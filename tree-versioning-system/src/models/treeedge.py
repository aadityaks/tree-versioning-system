from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class TreeEdge(Base):
    __tablename__ = 'treeedge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    incoming_node_id = Column(Integer, ForeignKey('treenode.id'), nullable=False)
    outgoing_node_id = Column(Integer, ForeignKey('treenode.id'), nullable=False)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    incoming_node = relationship('TreeNode', foreign_keys=[incoming_node_id], back_populates='edges')
    outgoing_node = relationship('TreeNode', foreign_keys=[outgoing_node_id])  # Fixed relationship for outgoing node
