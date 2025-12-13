"""
Database session management with auto-migration
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

logger = logging.getLogger(__name__)


class DatabaseSession:
    _instance = None
    _engine = None
    _session_factory = None
    
    def __new__(cls, database_url: str = None):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            if database_url:
                cls._instance._initialize(database_url)
        return cls._instance
    
    def _initialize(self, database_url: str):
        if self._engine is not None:
            return
        
        self.database_url = database_url
        self._engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"check_same_thread": False, "timeout": 30.0} if "sqlite" in database_url else {},
            echo=False
        )
        self._session_factory = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        )
        self._auto_migrate()
        logger.info(f"📦 Database initialized: {database_url}")
    
    def _auto_migrate(self):
        from .base import Base
        Base.metadata.create_all(bind=self._engine)
        logger.info("✅ Database schema migrated")
    
    def get_session(self) -> Session:
        return self._session_factory()
    
    def remove_session(self):
        self._session_factory.remove()
