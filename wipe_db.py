import os
import dj_database_url
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load .env from current directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL found in .env")
    exit(1)

config = dj_database_url.parse(db_url)

try:
    print(f"Connecting to {config['HOST']}...")
    conn = psycopg2.connect(
        dbname=config['NAME'],
        user=config['USER'],
        password=config['PASSWORD'],
        host=config['HOST'],
        port=config['PORT'],
        sslmode='require'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Resetting 'public' schema...")
    # Drop all tables in the public schema
    cur.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
    """)
    print("Database schema 'public' has been reset successfully.")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error resetting database: {e}")
