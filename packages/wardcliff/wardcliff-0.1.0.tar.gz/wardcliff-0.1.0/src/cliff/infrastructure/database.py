"""
Database Connection and Session Management.

Provides:
- Async database engine and session factory
- Context managers for session handling
- Database initialization utilities
- Migration support via Alembic (optional)

Configuration via environment variables:
- DATABASE_URL: PostgreSQL connection string
- DATABASE_ECHO: Enable SQL logging (default: false)
- DATABASE_POOL_SIZE: Connection pool size (default: 5)
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from models import Base

logger = logging.getLogger(__name__)

# Default to SQLite for development, PostgreSQL for production
DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./trading_simulation.db"


class DatabaseManager:
    """
    Manages database connections and sessions.

    Usage:
        # Initialize
        db = DatabaseManager()
        await db.initialize()

        # Use sessions
        async with db.session() as session:
            project = Project(name="2028 Elections")
            session.add(project)
            await session.commit()

        # Cleanup
        await db.close()
    """

    def __init__(
        self,
        database_url: Optional[str] = None,
        echo: Optional[bool] = None,
        pool_size: Optional[int] = None,
    ):
        """
        Initialize database manager.

        Args:
            database_url: Database connection string (default: env or SQLite)
            echo: Log SQL statements (default: env or False)
            pool_size: Connection pool size (default: env or 5)
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", DEFAULT_DATABASE_URL
        )
        self.echo = echo if echo is not None else os.getenv("DATABASE_ECHO", "").lower() == "true"
        self.pool_size = pool_size or int(os.getenv("DATABASE_POOL_SIZE", "5"))

        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    @property
    def engine(self) -> AsyncEngine:
        """Get the database engine (must call initialize first)."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get the session factory (must call initialize first)."""
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._session_factory

    async def initialize(self, create_tables: bool = True) -> None:
        """
        Initialize database connection and optionally create tables.

        Args:
            create_tables: Create all tables from models (default: True)
        """
        logger.info("Initializing database connection: %s", self._safe_url())

        # Create engine with appropriate settings
        engine_kwargs = {
            "echo": self.echo,
        }

        # SQLite doesn't support pool_size
        if not self.database_url.startswith("sqlite"):
            engine_kwargs["pool_size"] = self.pool_size
            engine_kwargs["max_overflow"] = self.pool_size * 2

        self._engine = create_async_engine(self.database_url, **engine_kwargs)

        # Create session factory
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        # Create tables if requested
        if create_tables:
            await self.create_tables()

        logger.info("Database initialized successfully")

    async def create_tables(self) -> None:
        """Create all tables from SQLAlchemy models."""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

    async def drop_tables(self) -> None:
        """Drop all tables (DANGEROUS - use for testing only)."""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("All database tables dropped")

    async def close(self) -> None:
        """Close database connection."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("Database connection closed")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Context manager for database sessions.

        Automatically commits on success, rolls back on exception.

        Usage:
            async with db.session() as session:
                session.add(model)
                await session.commit()
        """
        session = self.session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def health_check(self) -> bool:
        """Check if database is accessible."""
        try:
            async with self.session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error("Database health check failed: %s", e)
            return False

    def _safe_url(self) -> str:
        """Return URL with password masked for logging."""
        if "@" in self.database_url:
            parts = self.database_url.split("@")
            creds = parts[0].split("://")[-1]
            if ":" in creds:
                user = creds.split(":")[0]
                return self.database_url.replace(creds, f"{user}:****")
        return self.database_url


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


async def get_db() -> DatabaseManager:
    """
    Get the global database manager.

    Initializes on first call.
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
        await _db_manager.initialize()
    return _db_manager


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Convenience function to get a database session.

    Usage:
        async with get_session() as session:
            results = await session.execute(select(Project))
    """
    db = await get_db()
    async with db.session() as session:
        yield session


async def init_db(database_url: Optional[str] = None) -> DatabaseManager:
    """
    Initialize the database (for app startup).

    Args:
        database_url: Optional override for database URL

    Returns:
        Configured DatabaseManager instance
    """
    global _db_manager
    _db_manager = DatabaseManager(database_url=database_url)
    await _db_manager.initialize()
    return _db_manager


async def close_db() -> None:
    """Close the database connection (for app shutdown)."""
    global _db_manager
    if _db_manager:
        await _db_manager.close()
        _db_manager = None


# Repository helpers for common operations
class ProjectRepository:
    """Repository pattern for Project operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, description: Optional[str] = None, **kwargs):
        """Create a new project."""
        from models import Project
        project = Project(name=name, description=description, **kwargs)
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def get(self, project_id):
        """Get project by ID."""
        from models import Project
        from sqlalchemy import select
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self):
        """List all projects."""
        from models import Project
        from sqlalchemy import select
        result = await self.session.execute(select(Project))
        return result.scalars().all()


class MarketRepository:
    """Repository pattern for Market operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        project_id,
        name: str,
        outcomes: list,
        initial_probabilities: Optional[dict] = None,
        **kwargs
    ):
        """Create a new market."""
        from models import Market
        market = Market(
            project_id=project_id,
            name=name,
            outcomes=outcomes,
            initial_probabilities=initial_probabilities,
            current_prices=initial_probabilities,
            **kwargs
        )
        self.session.add(market)
        await self.session.commit()
        await self.session.refresh(market)
        return market

    async def get(self, market_id):
        """Get market by ID."""
        from models import Market
        from sqlalchemy import select
        result = await self.session.execute(
            select(Market).where(Market.id == market_id)
        )
        return result.scalar_one_or_none()

    async def update_prices(self, market_id, prices: dict):
        """Update current prices for a market."""
        from models import Market
        from sqlalchemy import select
        result = await self.session.execute(
            select(Market).where(Market.id == market_id)
        )
        market = result.scalar_one_or_none()
        if market:
            market.current_prices = prices
            await self.session.commit()
        return market


class TradeRepository:
    """Repository pattern for Trade operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def record(
        self,
        agent_id,
        market_id,
        outcome: str,
        direction: str,
        size: float,
        price_before: float,
        price_after: float,
        token_delta: float,
        quote_delta: float,
        rationale: Optional[str] = None,
    ):
        """Record a new trade."""
        from models import Trade
        slippage = abs(price_after - price_before) / price_before if price_before > 0 else 0

        trade = Trade(
            agent_id=agent_id,
            market_id=market_id,
            outcome=outcome,
            direction=direction,
            size=size,
            price_before=price_before,
            price_after=price_after,
            slippage=slippage,
            token_delta=token_delta,
            quote_delta=quote_delta,
            rationale=rationale,
        )
        self.session.add(trade)
        await self.session.commit()
        await self.session.refresh(trade)
        return trade

    async def get_by_agent(self, agent_id, limit: int = 100):
        """Get trades by agent."""
        from models import Trade
        from sqlalchemy import select
        result = await self.session.execute(
            select(Trade)
            .where(Trade.agent_id == agent_id)
            .order_by(Trade.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_market(self, market_id, limit: int = 100):
        """Get trades by market."""
        from models import Trade
        from sqlalchemy import select
        result = await self.session.execute(
            select(Trade)
            .where(Trade.market_id == market_id)
            .order_by(Trade.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()
