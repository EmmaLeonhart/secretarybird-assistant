"""Tests for the database connector module."""
import os
import pytest
import pandas as pd

from backend.integrations.databases import DatabaseConnector, ConnectionConfig


@pytest.fixture
def connector():
    """Create a DatabaseConnector instance."""
    return DatabaseConnector()


@pytest.fixture
def sqlite_db(tmp_path):
    """Create a temporary SQLite database for testing."""
    import sqlite3
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            salary REAL
        )
    """)
    cursor.executemany(
        "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
        [
            ("Alice", "Engineering", 75000),
            ("Bob", "Sales", 65000),
            ("Charlie", "Engineering", 80000),
            ("Diana", "Marketing", 60000),
        ],
    )
    conn.commit()
    conn.close()
    return db_path


class TestConnectionConfig:
    """Test ConnectionConfig creation."""

    def test_sqlite_config(self):
        """Test creating SQLite connection config."""
        config = ConnectionConfig(
            type="sqlite",
            database="/path/to/db.sqlite",
        )
        assert config.type == "sqlite"
        assert "sqlite" in config.connection_string

    def test_postgres_config(self):
        """Test creating PostgreSQL connection config."""
        config = ConnectionConfig(
            type="postgresql",
            host="localhost",
            port=5432,
            database="mydb",
            username="user",
            password="pass",
        )
        assert config.type == "postgresql"
        assert "postgresql" in config.connection_string

    def test_mysql_config(self):
        """Test creating MySQL connection config."""
        config = ConnectionConfig(
            type="mysql",
            host="localhost",
            port=3306,
            database="mydb",
            username="user",
            password="pass",
        )
        assert config.type == "mysql"
        assert "mysql" in config.connection_string


class TestDatabaseConnector:
    """Test DatabaseConnector with SQLite."""

    def test_init(self, connector):
        """Test connector initialization."""
        assert connector is not None

    def test_connect_sqlite(self, connector, sqlite_db):
        """Test connecting to SQLite database."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connection = connector.connect(config)
        assert connection is not None
        connector.disconnect(config)

    def test_query_to_dataframe(self, connector, sqlite_db):
        """Test querying data and returning a DataFrame."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connector.connect(config)
        df = connector.query(config, "SELECT * FROM employees")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert "name" in df.columns
        connector.disconnect(config)

    def test_query_with_filter(self, connector, sqlite_db):
        """Test querying with WHERE clause."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connector.connect(config)
        df = connector.query(
            config, "SELECT * FROM employees WHERE department = 'Engineering'"
        )
        assert len(df) == 2
        connector.disconnect(config)

    def test_list_tables(self, connector, sqlite_db):
        """Test listing tables in database."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connector.connect(config)
        tables = connector.list_tables(config)
        assert "employees" in tables
        connector.disconnect(config)

    def test_describe_table(self, connector, sqlite_db):
        """Test describing a table's columns."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connector.connect(config)
        columns = connector.describe_table(config, "employees")
        assert isinstance(columns, list)
        col_names = [c["name"] for c in columns]
        assert "id" in col_names
        assert "name" in col_names
        assert "salary" in col_names
        connector.disconnect(config)

    def test_execute_insert(self, connector, sqlite_db):
        """Test executing an insert statement."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connector.connect(config)
        connector.execute(
            config,
            "INSERT INTO employees (name, department, salary) VALUES ('Eve', 'Sales', 70000)",
        )
        df = connector.query(config, "SELECT * FROM employees")
        assert len(df) == 5
        connector.disconnect(config)

    def test_disconnect(self, connector, sqlite_db):
        """Test disconnecting from database."""
        config = ConnectionConfig(type="sqlite", database=sqlite_db)
        connector.connect(config)
        connector.disconnect(config)
        # After disconnect, operations should fail or reconnect
        assert config not in connector.active_connections or connector.active_connections[config] is None
