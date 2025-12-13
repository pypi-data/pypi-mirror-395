from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from dataflow.db import Base

class ServerConfig(Base):

    """TABLE 'SERVER_CONFIG'

    Attributes:
        id (int): Primary key for the server configuration.
        display_name (str): Human-readable name for the server configuration.
        slug (str): URL-friendly unique identifier for the server configuration.
        price (str): Pricing information for the server configuration.
        ram (str): Amount of RAM allocated to the server configuration.
        cpu (str): Number of CPU cores allocated to the server configuration.
        gpu (str): GPU specifications for the server configuration, if any.
        default (bool): Indicates if this is the default server configuration.
        tags (JSONB): JSON array of tags associated with the server configuration.
        description (str): Detailed description of the server configuration.
        kubespawner_override (JSONB): JSON object for custom KubeSpawner settings.

    Relationships:
        organizations: Many-to-many relationship with Organization model via ORGANIZATION_SERVER association table.
    """

    __tablename__ = "SERVER_CONFIG"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_name = Column(String, nullable=False, unique=True)
    slug = Column(String, unique=True, nullable=False)
    price = Column(String, nullable=False)
    ram = Column(String, nullable=False)
    cpu = Column(String, nullable=False)
    gpu = Column(String)
    default = Column(Boolean, default=False, server_default='false')
    tags = Column(JSONB, default=func.json([]), server_default=text("'[]'::jsonb"))
    description = Column(Text, nullable=True)
    kubespawner_override = Column(JSONB, default=func.json({}), server_default=text("'{}'::jsonb"))

    # Relationships
    organizations = relationship("Organization", secondary="ORGANIZATION_SERVER", back_populates="servers")

class CustomServerConfig(Base):

    """TABLE 'CUSTOM_SERVER'.

    Attributes:
        id (int): Primary key for the custom server configuration.
        base_server_id (int): Foreign key referencing the ServerConfig table.
        org_id (int): Foreign key referencing the ORGANIZATION table.
        display_name (str): Human-readable name for the custom server configuration.
        description (str): Detailed description of the custom server configuration.

    Relationships:
        server_config: Many-to-one relationship with ServerConfig model.
        organization: Many-to-one relationship with Organization model.
        roles: Many-to-many relationship with Role model via ROLE_SERVER association table.
    """
    
    __tablename__ = "CUSTOM_SERVER"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_server_id = Column(Integer, ForeignKey(ServerConfig.id, ondelete="CASCADE"), nullable=False)
    org_id = Column(Integer, ForeignKey('ORGANIZATION.id', ondelete="CASCADE"), nullable=False)
    display_name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    server_config = relationship(ServerConfig)
    organization = relationship("Organization", back_populates="custom_servers")
    roles = relationship("Role", secondary="ROLE_SERVER", back_populates="servers")

    __table_args__ = (
        UniqueConstraint('display_name', 'org_id', name='uq_display_name_org'),
    )