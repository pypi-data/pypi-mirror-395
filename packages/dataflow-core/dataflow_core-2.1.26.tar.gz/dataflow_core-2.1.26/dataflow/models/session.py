"""models.py"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from dataflow.db import Base

class Session(Base):
    """Table SESSION

    Attributes:
        id (int): Primary key for the session entry.
        session_id (str): Unique identifier for the session.
        jupyterhub_token (str): Token associated with the JupyterHub session.
        jupyterhub_token_id (str): Identifier for the JupyterHub token.
        user_id (int): Foreign key referencing the USER table.
    """

    __tablename__='SESSION'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    session_id = Column(String, unique=True, nullable=False)
    jupyterhub_token = Column(String)
    jupyterhub_token_id = Column(String)
    user_id = Column(Integer, ForeignKey('USER.user_id', ondelete="CASCADE"), nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)


