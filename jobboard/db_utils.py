from django.db import connection
from django.db import OperationalError
import time

def test_database_connection():
    """Test if database connection is working"""
    try:
        connection.ensure_connection()
        return True
    except OperationalError:
        return False

def wait_for_database(max_retries=5, delay=2):
    """Wait for database to become available"""
    for i in range(max_retries):
        if test_database_connection():
            return True
        print(f"Database not ready, retrying in {delay} seconds... (Attempt {i+1}/{max_retries})")
        time.sleep(delay)
    return False