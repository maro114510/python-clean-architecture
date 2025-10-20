"""
Pytest configuration and fixtures for datastore layer tests.

This module provides fixtures for database setup and cleanup specific to
datastore unit tests. It uses the same DatabaseConfig and TransactionManager
from the application layer, ensuring tests use the actual connection implementations.
"""

import pytest
from pytest_asyncio import fixture as async_fixture
from pathlib import Path
from typing import AsyncGenerator

from app.config.database_config import DatabaseConfig
from app.datastore.database import DatabaseFactory
from app.datastore.database.transaction_factory import TransactionManagerFactory


@pytest.fixture(scope="function")
def db_config() -> DatabaseConfig:
    """Load database configuration from environment variables.

    Uses existing DatabaseConfig.from_env() to respect app's DB settings.
    Environment variables (DB_TYPE, MYSQL_*, FIRESTORE_*, etc.) control
    which database is tested.
    """
    return DatabaseConfig.from_env()


@async_fixture(scope="function")
async def db_connection(db_config: DatabaseConfig):
    """Create database connection based on configuration.

    Yields the raw connection object that can be used to create
    TransactionManagers for test transactions.
    """
    connection = DatabaseFactory.create_connection(db_config)
    db_conn = await connection.connect()
    try:
        yield connection
    finally:
        await connection.disconnect()


@async_fixture(scope="function")
async def setup_test_db(db_config: DatabaseConfig, db_connection):
    """Setup test database schema by executing DDL.

    Runs once per test function to create fresh schema.
    For SQLite: creates in-memory DB
    For MySQL/Firestore: uses environment-configured DB
    """
    # Load DDL from file
    ddl_path = Path(__file__).parent.parent.parent.parent / "db" / "ddl.sql"
    if not ddl_path.exists():
        raise FileNotFoundError(f"DDL file not found: {ddl_path}")

    ddl_content = ddl_path.read_text()

    # Execute DDL statements
    # Split by semicolon and filter empty statements
    statements = [s.strip() for s in ddl_content.split(";") if s.strip()]

    # Create TransactionManager to execute DDL
    transaction_manager = TransactionManagerFactory.create_manager(
        db_connection, db_config
    )
    await transaction_manager.begin()

    try:
        for statement in statements:
            await transaction_manager.execute(statement)
        await transaction_manager.commit()
    except Exception as e:
        await transaction_manager.rollback()
        raise RuntimeError(f"Failed to setup test database: {e}") from e

    yield

    # Cleanup: truncate tables (function scope teardown)
    transaction_manager = TransactionManagerFactory.create_manager(
        db_connection, db_config
    )
    await transaction_manager.begin()
    try:
        if db_config.db_type == DatabaseConfig.SQLITE:
            # SQLite: drop tables
            await transaction_manager.execute("DROP TABLE IF EXISTS item")
        elif db_config.db_type == DatabaseConfig.MYSQL:
            # MySQL: truncate table
            await transaction_manager.execute("TRUNCATE TABLE item")
        # Note: Firestore requires different cleanup logic (not implemented here)
        await transaction_manager.commit()
    except Exception as e:
        await transaction_manager.rollback()
        # Don't raise during cleanup to avoid masking test failures


@async_fixture(scope="function")
async def test_transaction(
    db_config: DatabaseConfig, db_connection
) -> AsyncGenerator:
    """Provide a transaction for each test function.

    Automatically begins transaction at start and rolls back after test.
    This ensures test isolation and cleans up any data modifications.

    Usage:
        async def test_something(test_transaction):
            result = await test_transaction.execute(sql, params)
            # Automatically rolled back after test
    """
    transaction_manager = TransactionManagerFactory.create_manager(
        db_connection, db_config
    )
    await transaction_manager.begin()

    try:
        yield transaction_manager
    finally:
        # Automatic rollback after test
        if transaction_manager.is_transaction_active:
            await transaction_manager.rollback()
