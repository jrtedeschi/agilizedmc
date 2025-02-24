import pytest
from agilizedmc.db import DB
import mysql.connector

@pytest.fixture
def mysql_params():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'test_password',
        'port': '3306',
        'database': 'test_db'
    }

@pytest.fixture
def test_db(mysql_params):
    """Create a test database connection"""
    try:
        db = DB(**mysql_params)
        db.connection  # Test connection
        
        # Create test table
        db.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255)
            )
        """)
        
        yield db
        
        # Cleanup
        db.execute("DROP TABLE IF EXISTS test_table")
        db.close()
    except Exception as e:
        pytest.skip(f"MySQL not available: {str(e)}")

class TestDB:
    def test_attributes(self, mysql_params):
        """Test DB instance attributes"""
        db = DB(**mysql_params)
        for key, value in mysql_params.items():
            assert getattr(db, key) == value

    @pytest.mark.integration
    def test_connection(self, test_db):
        """Test basic connection"""
        assert test_db.connection.is_connected()

    @pytest.mark.integration
    def test_execute_and_query(self, test_db):
        """Test basic query execution and retrieval"""
        # Insert data
        test_db.execute(
            "INSERT INTO test_table (name) VALUES (%s)",
            ('Test Name',)
        )
        
        # Query data
        results = test_db.query("SELECT name FROM test_table")
        assert len(results) == 1
        assert results[0][0] == 'Test Name' 