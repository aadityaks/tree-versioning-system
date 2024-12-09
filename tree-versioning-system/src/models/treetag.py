from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class TreeTag(Base):
    __tablename__ = 'treetag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tree_id = Column(Integer, ForeignKey('tree.id'), nullable=False)
    tag_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tree = relationship('Tree', back_populates='tags')  # Relationship back to Tree
