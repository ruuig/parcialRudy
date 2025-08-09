# app/db.py
from psycopg2.pool import SimpleConnectionPool
import psycopg2.extras

pool = None

def init_db_pool(dsn, sslmode='disable', minconn=1, maxconn=10):
    global pool
    pool = SimpleConnectionPool(minconn, maxconn, dsn=dsn, sslmode=sslmode)

def get_conn():
    conn = pool.getconn()
    conn.autocommit = True
    return conn

def put_conn(conn):
    pool.putconn(conn)

def query(sql, params=None, fetch='all'):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, params or [])
            if fetch == 'one':
                return cur.fetchone()
            if fetch == 'all':
                return cur.fetchall()
            return None
    finally:
        put_conn(conn)
