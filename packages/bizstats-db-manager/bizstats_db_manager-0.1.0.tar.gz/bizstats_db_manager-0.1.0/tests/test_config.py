"""Tests for database configuration."""

import os
import pytest
from bizstats_db_manager.config import (
    DatabaseConfig,
    TimeoutConfig,
    PoolConfig,
)


class TestTimeoutConfig:
    """Tests for TimeoutConfig."""

    def test_default_values(self):
        """Test default timeout values."""
        config = TimeoutConfig()
        assert config.query_timeout == 30
        assert config.command_timeout == 60
        assert config.pool_timeout == 30

    def test_custom_values(self):
        """Test custom timeout values."""
        config = TimeoutConfig(
            query_timeout=10,
            command_timeout=30,
            pool_timeout=15,
        )
        assert config.query_timeout == 10
        assert config.command_timeout == 30
        assert config.pool_timeout == 15

    def test_from_env(self, monkeypatch):
        """Test loading from environment variables."""
        monkeypatch.setenv("DB_QUERY_TIMEOUT", "45")
        monkeypatch.setenv("DB_COMMAND_TIMEOUT", "90")
        monkeypatch.setenv("DB_POOL_TIMEOUT", "60")

        config = TimeoutConfig.from_env()
        assert config.query_timeout == 45
        assert config.command_timeout == 90
        assert config.pool_timeout == 60


class TestPoolConfig:
    """Tests for PoolConfig."""

    def test_default_values(self):
        """Test default pool values."""
        config = PoolConfig()
        assert config.min_size == 5
        assert config.max_size == 20
        assert config.max_overflow == 20
        assert config.pool_recycle == 1800
        assert config.pool_pre_ping is True

    def test_from_env(self, monkeypatch):
        """Test loading from environment variables."""
        monkeypatch.setenv("DB_POOL_MIN_SIZE", "10")
        monkeypatch.setenv("DB_POOL_MAX_SIZE", "50")
        monkeypatch.setenv("DB_POOL_MAX_OVERFLOW", "30")
        monkeypatch.setenv("DB_POOL_RECYCLE", "3600")
        monkeypatch.setenv("DB_POOL_PRE_PING", "false")

        config = PoolConfig.from_env()
        assert config.min_size == 10
        assert config.max_size == 50
        assert config.max_overflow == 30
        assert config.pool_recycle == 3600
        assert config.pool_pre_ping is False


class TestDatabaseConfig:
    """Tests for DatabaseConfig."""

    def test_default_values(self):
        """Test default database values."""
        config = DatabaseConfig()
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.user == "postgres"
        assert config.password == "postgres"
        assert config.database == "postgres"

    def test_get_url(self):
        """Test URL generation."""
        config = DatabaseConfig(
            host="myhost",
            port=5433,
            user="myuser",
            password="mypass",
            database="mydb",
        )

        url = config.get_url()
        assert url == "postgresql://myuser:mypass@myhost:5433/mydb"

        async_url = config.get_url(async_driver=True)
        assert async_url == "postgresql+asyncpg://myuser:mypass@myhost:5433/mydb"

    def test_get_url_with_schema(self):
        """Test URL generation with schema."""
        config = DatabaseConfig(
            host="localhost",
            database="mydb",
            schema="myschema",
        )

        url = config.get_url()
        assert "myschema" in url

    def test_get_masked_url(self):
        """Test masked URL for logging."""
        config = DatabaseConfig(
            host="localhost",
            user="myuser",
            password="supersecret",
        )

        masked = config.get_masked_url()
        assert "supersecret" not in masked
        assert "***" in masked

    def test_from_url(self):
        """Test parsing from URL."""
        url = "postgresql://user:pass@host:5433/database"
        config = DatabaseConfig.from_url(url)

        assert config.host == "host"
        assert config.port == 5433
        assert config.user == "user"
        assert config.password == "pass"
        assert config.database == "database"

    def test_from_url_with_asyncpg(self):
        """Test parsing from asyncpg URL."""
        url = "postgresql+asyncpg://user:pass@host:5433/database"
        config = DatabaseConfig.from_url(url)

        assert config.host == "host"
        assert config.user == "user"

    def test_from_env_with_database_url(self, monkeypatch):
        """Test loading from DATABASE_URL environment variable."""
        monkeypatch.setenv("DATABASE_URL", "postgresql://envuser:envpass@envhost:5434/envdb")

        config = DatabaseConfig.from_env()
        assert config.host == "envhost"
        assert config.port == 5434
        assert config.user == "envuser"
        assert config.database == "envdb"

    def test_from_env_kubernetes_discovery(self, monkeypatch):
        """Test Kubernetes service discovery."""
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.setenv("POSTGRES_SERVICE_SERVICE_HOST", "k8s-host")
        monkeypatch.setenv("POSTGRES_SERVICE_SERVICE_PORT", "5436")

        config = DatabaseConfig.from_env()
        assert config.host == "k8s-host"
        assert config.port == 5436

    def test_from_env_docker_compose(self, monkeypatch):
        """Test Docker Compose environment."""
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.delenv("POSTGRES_SERVICE_SERVICE_HOST", raising=False)
        monkeypatch.setenv("POSTGRES_SERVICE_HOST", "docker-host")
        monkeypatch.setenv("POSTGRES_SERVICE_PORT", "5437")

        config = DatabaseConfig.from_env()
        assert config.host == "docker-host"
        assert config.port == 5437

    def test_from_env_custom(self, monkeypatch):
        """Test custom environment variables."""
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.delenv("POSTGRES_SERVICE_SERVICE_HOST", raising=False)
        monkeypatch.delenv("POSTGRES_SERVICE_HOST", raising=False)
        monkeypatch.setenv("POSTGRES_HOST", "custom-host")
        monkeypatch.setenv("POSTGRES_PORT", "5438")
        monkeypatch.setenv("POSTGRES_USER", "customuser")
        monkeypatch.setenv("POSTGRES_PASSWORD", "custompass")
        monkeypatch.setenv("POSTGRES_DB", "customdb")

        config = DatabaseConfig.from_env()
        assert config.host == "custom-host"
        assert config.port == 5438
        assert config.user == "customuser"
        assert config.password == "custompass"
        assert config.database == "customdb"

    def test_get_server_settings(self):
        """Test server settings generation."""
        config = DatabaseConfig(application_name="test_app")
        settings = config.get_server_settings()

        assert settings["application_name"] == "test_app"
        assert settings["jit"] == "off"
        assert "statement_timeout" in settings

    def test_get_asyncpg_url(self):
        """Test asyncpg URL getter."""
        config = DatabaseConfig(host="localhost", database="mydb")
        url = config.get_asyncpg_url()
        assert url.startswith("postgresql://")
        assert "asyncpg" not in url

    def test_get_sqlalchemy_url(self):
        """Test SQLAlchemy URL getter."""
        config = DatabaseConfig(host="localhost", database="mydb")
        url = config.get_sqlalchemy_url()
        assert "postgresql+asyncpg://" in url
