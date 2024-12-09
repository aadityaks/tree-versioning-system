from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Tree(Base):
    __tablename__ = 'tree'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_tree_id = Column(Integer, ForeignKey('tree.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship('Tree', remote_side=[id])
    nodes = relationship('TreeNode', back_populates='tree', cascade="all, delete-orphan")
    tags = relationship('TreeTag', back_populates='tree')  # Relationship to TreeTag
