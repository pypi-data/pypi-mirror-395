# models/user_team.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from dataflow.db import Base

class RoleServer(Base):

    """TABLE 'ROLE_SERVER'

    Attributes:
        role_id (int): Foreign key referencing the ROLE table, also part of the primary key.
        custom_server_id (int): Foreign key referencing the CUSTOM_SERVER table, also part of the primary key.
    """
    
    __tablename__ = 'ROLE_SERVER'
    __table_args__ = (UniqueConstraint('role_id', 'custom_server_id', name='_role_server_uc'),)

    role_id = Column(Integer, ForeignKey('ROLE.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    custom_server_id = Column(Integer, ForeignKey('CUSTOM_SERVER.id', ondelete="CASCADE"), nullable=False, primary_key=True)