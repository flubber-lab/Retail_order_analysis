import psycopg2
from psycopg2 import pool

# Connection pool setup
def create_connection_pool():
    return psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user='postgres',
        password='roottoor',
        host='awsdb.c9agcyo0i9j6.ap-south-1.rds.amazonaws.com',
        port='5432',
        database='project'
    )

# Create the connection pool
connection_pool = create_connection_pool()

def get_connection():
    """Retrieve a database connection from the pool."""
    if connection_pool:
        return connection_pool.getconn()

def release_connection(conn):
    """Release a database connection back to the pool."""
    if connection_pool and conn:
        connection_pool.putconn(conn)

def close_all_connections():
    """Close all connections in the pool."""
    if connection_pool:
        connection_pool.closeall()