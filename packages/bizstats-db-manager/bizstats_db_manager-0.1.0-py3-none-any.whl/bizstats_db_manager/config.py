"""
Database configuration management.

Supports configuration via:
- Direct parameters
- Environment variables
- Kubernetes service discovery
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pydantic_settings import BaseSettings


@dataclass
class TimeoutConfig:
    """Database timeout configuration (in seconds)."""

    query_timeout: int = 30
    """Timeout for individual queries."""

    command_timeout: int = 60
    """Timeout for asyncpg commands."""

    pool_timeout: int = 30
    """Timeout waiting for pool connection."""

    @classmethod
    def from_env(cls) -> "TimeoutConfig":
        """Create timeout config from environment variables."""
        return cls(
            query_timeout=int(os.getenv("DB_QUERY_TIMEOUT", "30")),
            command_timeout=int(os.getenv("DB_COMMAND_TIMEOUT", "60")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
        )


@dataclass
class PoolConfig:
    """Connection pool configuration."""

    min_size: int = 5
    """Minimum number of connections in the pool."""

    max_size: int = 20
    """Maximum number of connections in the pool."""

    max_overflow: int = 20
    """SQLAlchemy max overflow connections."""

    pool_recycle: int = 1800
    """Connection recycle time in seconds (30 minutes)."""

    pool_pre_ping: bool = True
    """Enable connection health check before use."""

    @classmethod
    def from_env(cls) -> "PoolConfig":
        """Create pool config from environment variables."""
        return cls(
            min_size=int(os.getenv("DB_POOL_MIN_SIZE", "5")),
            max_size=int(os.getenv("DB_POOL_MAX_SIZE", "20")),
            max_overflow=int(os.getenv("DB_POOL_MAX_OVERFLOW", "20")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "1800")),
            pool_pre_ping=os.getenv("DB_POOL_PRE_PING", "true").lower() == "true",
        )


@dataclass
class DatabaseConfig:
    """
    Database connection configuration.

    Supports multiple configuration methods:
    1. Direct URL: DATABASE_URL environment variable
    2. Component parts: POSTGRES_HOST, POSTGRES_PORT, etc.
    3. Kubernetes service discovery: POSTGRES_SERVICE_SERVICE_HOST

    Example:
        # From environment
        config = DatabaseConfig.from_env()

        # Direct configuration
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="mydb"
        )

        # Get connection URL
        url = config.get_url()
    """

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"
    schema: Optional[str] = None

    # Pool and timeout config
    pool: PoolConfig = field(default_factory=PoolConfig)
    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)

    # Debug settings
    echo_sql: bool = False
    """Echo SQL statements to logs."""

    application_name: str = "bizstats_db_manager"
    """Application name for PostgreSQL connection."""

    # Connection retry settings
    max_retries: int = 5
    """Maximum connection retry attempts."""

    retry_backoff_base: int = 2
    """Base for exponential backoff (seconds)."""

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """
        Create configuration from environment variables.

        Supports Kubernetes service discovery patterns:
        - POSTGRES_SERVICE_SERVICE_HOST (K8s)
        - POSTGRES_SERVICE_HOST (Docker Compose)
        - POSTGRES_HOST (Custom)
        """
        # Check for direct DATABASE_URL first
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return cls.from_url(database_url)

        # Build from component environment variables
        host = (
            os.getenv("POSTGRES_SERVICE_SERVICE_HOST")  # Kubernetes
            or os.getenv("POSTGRES_SERVICE_HOST")  # Docker Compose
            or os.getenv("POSTGRES_HOST")  # Custom
            or "localhost"
        )

        port = int(
            os.getenv("POSTGRES_SERVICE_SERVICE_PORT")  # Kubernetes
            or os.getenv("POSTGRES_SERVICE_PORT")  # Docker Compose
            or os.getenv("POSTGRES_PORT")  # Custom
            or "5432"
        )

        return cls(
            host=host,
            port=port,
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            database=os.getenv("POSTGRES_DB", "postgres"),
            schema=os.getenv("POSTGRES_SCHEMA"),
            pool=PoolConfig.from_env(),
            timeouts=TimeoutConfig.from_env(),
            echo_sql=os.getenv("DEBUG_SQL", "false").lower() == "true",
            application_name=os.getenv("DB_APPLICATION_NAME", "bizstats_db_manager"),
            max_retries=int(os.getenv("DB_MAX_RETRIES", "5")),
            retry_backoff_base=int(os.getenv("DB_RETRY_BACKOFF_BASE", "2")),
        )

    @classmethod
    def from_url(cls, url: str) -> "DatabaseConfig":
        """Parse configuration from database URL."""
        from urllib.parse import urlparse, parse_qs

        # Handle both postgresql:// and postgresql+asyncpg://
        clean_url = url.replace("postgresql+asyncpg://", "postgresql://")
        parsed = urlparse(clean_url)

        config = cls(
            host=parsed.hostname or "localhost",
            port=parsed.port or 5432,
            user=parsed.username or "postgres",
            password=parsed.password or "postgres",
            database=parsed.path.lstrip("/") if parsed.path else "postgres",
            pool=PoolConfig.from_env(),
            timeouts=TimeoutConfig.from_env(),
        )

        # Parse query parameters
        if parsed.query:
            params = parse_qs(parsed.query)
            if "schema" in params:
                config.schema = params["schema"][0]

        return config

    def get_url(self, async_driver: bool = False) -> str:
        """
        Get database connection URL.

        Args:
            async_driver: If True, use postgresql+asyncpg:// prefix

        Returns:
            Database connection URL
        """
        prefix = "postgresql+asyncpg://" if async_driver else "postgresql://"
        url = f"{prefix}{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

        if self.schema:
            url += f"?options=-csearch_path={self.schema}"

        return url

    def get_asyncpg_url(self) -> str:
        """Get URL formatted for asyncpg (without driver prefix)."""
        return self.get_url(async_driver=False)

    def get_sqlalchemy_url(self) -> str:
        """Get URL formatted for SQLAlchemy async."""
        return self.get_url(async_driver=True)

    def get_masked_url(self) -> str:
        """Get URL with password masked for logging."""
        return self.get_url().replace(f":{self.password}@", ":***@")

    def get_server_settings(self) -> dict:
        """Get PostgreSQL server settings for connection."""
        return {
            "jit": "off",
            "application_name": self.application_name,
            "statement_timeout": f"{self.timeouts.query_timeout * 1000}",  # ms
        }
