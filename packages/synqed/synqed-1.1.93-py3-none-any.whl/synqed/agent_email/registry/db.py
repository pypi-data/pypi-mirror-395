"""
postgres backend for agent registry.

provides persistent storage for agent registry entries.
drop-in replacement for in-memory AgentRegistry.

usage:
    # set environment variable
    export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/agentdb"
    
    # registry api will automatically use postgres if DATABASE_URL is set
"""

from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from pydantic import HttpUrl

from synqed.agent_email.registry.models import AgentRegistryEntry

Base = declarative_base()


class AgentRegistryDB(Base):
    """sqlalchemy model for agent registry table."""
    
    __tablename__ = "agent_registry"
    
    # primary key is agent_id (canonical uri)
    agent_id = Column(String, primary_key=True)
    email_like = Column(String, unique=True, nullable=False, index=True)
    inbox_url = Column(String, nullable=False)
    public_key = Column(String, nullable=True)
    capabilities = Column(JSON, nullable=False, default=list)
    metadata = Column(JSON, nullable=False, default=dict)
    
    # audit fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # indexes for fast lookups
    __table_args__ = (
        Index('idx_email_like', 'email_like'),
        Index('idx_created_at', 'created_at'),
    )


class PostgresAgentRegistry:
    """
    postgres-backed agent registry.
    
    compatible with in-memory AgentRegistry interface.
    all methods are async and use sqlalchemy async engine.
    
    example:
        >>> registry = PostgresAgentRegistry("postgresql+asyncpg://...")
        >>> await registry.init_db()
        >>> entry = AgentRegistryEntry(...)
        >>> await registry.register(entry)
    """
    
    def __init__(self, database_url: str):
        """
        initialize postgres registry.
        
        args:
            database_url: async postgres connection string
                format: "postgresql+asyncpg://user:pass@host:port/dbname"
                example: "postgresql+asyncpg://postgres:password@localhost/agentdb"
        """
        self.engine = create_async_engine(
            database_url,
            echo=False,  # set to True for sql query logging
            pool_size=5,
            max_overflow=10,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def init_db(self) -> None:
        """
        create tables if they don't exist.
        
        call this once on startup before using the registry.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def register(self, entry: AgentRegistryEntry) -> None:
        """
        register or update an agent entry.
        
        if agent_id already exists, updates the entry (upsert).
        
        args:
            entry: the registry entry to register
        """
        async with self.async_session() as session:
            # create db model from pydantic model
            db_entry = AgentRegistryDB(
                agent_id=entry.agent_id,
                email_like=entry.email_like,
                inbox_url=str(entry.inbox_url),
                public_key=entry.public_key,
                capabilities=entry.capabilities,
                metadata=entry.metadata,
            )
            
            # merge does upsert: insert if new, update if exists
            await session.merge(db_entry)
            await session.commit()
    
    async def get_by_uri(self, agent_uri: str) -> AgentRegistryEntry:
        """
        lookup agent by canonical uri.
        
        args:
            agent_uri: canonical agent uri (e.g., agent://futurehouse/cosmos)
            
        returns:
            registry entry
            
        raises:
            KeyError: if agent not found
        """
        async with self.async_session() as session:
            result = await session.get(AgentRegistryDB, agent_uri)
            
            if result is None:
                raise KeyError(f"agent not found: {agent_uri}")
            
            # convert db model to pydantic model
            return self._db_to_pydantic(result)
    
    async def get_by_email(self, email_like: str) -> AgentRegistryEntry:
        """
        lookup agent by email-like address.
        
        args:
            email_like: email-like address (e.g., cosmos@futurehouse)
            
        returns:
            registry entry
            
        raises:
            KeyError: if agent not found
        """
        from sqlalchemy import select
        
        async with self.async_session() as session:
            stmt = select(AgentRegistryDB).where(
                AgentRegistryDB.email_like == email_like
            )
            result = await session.execute(stmt)
            db_entry = result.scalar_one_or_none()
            
            if db_entry is None:
                raise KeyError(f"agent not found: {email_like}")
            
            return self._db_to_pydantic(db_entry)
    
    async def list_all(self) -> List[AgentRegistryEntry]:
        """
        get all registered agents.
        
        returns entries ordered by creation time (newest first).
        
        returns:
            list of all registry entries
        """
        from sqlalchemy import select
        
        async with self.async_session() as session:
            stmt = select(AgentRegistryDB).order_by(
                AgentRegistryDB.created_at.desc()
            )
            result = await session.execute(stmt)
            db_entries = result.scalars().all()
            
            return [self._db_to_pydantic(e) for e in db_entries]
    
    async def clear(self) -> None:
        """
        remove all entries (useful for testing).
        
        warning: this deletes all data!
        """
        from sqlalchemy import delete
        
        async with self.async_session() as session:
            stmt = delete(AgentRegistryDB)
            await session.execute(stmt)
            await session.commit()
    
    def _db_to_pydantic(self, db_entry: AgentRegistryDB) -> AgentRegistryEntry:
        """convert sqlalchemy model to pydantic model."""
        return AgentRegistryEntry(
            agent_id=db_entry.agent_id,
            email_like=db_entry.email_like,
            inbox_url=HttpUrl(db_entry.inbox_url),
            public_key=db_entry.public_key,
            capabilities=db_entry.capabilities or [],
            metadata=db_entry.metadata or {},
        )
    
    async def close(self) -> None:
        """close database connections."""
        await self.engine.dispose()

