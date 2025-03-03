from context_manager import get_db_connection
from tabulate import tabulate
import os

import logging
import psycopg2
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_database(db_name: str):
  conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
  )
  conn.autocommit=True # So CREATE DATABASE not in transaction block
  cur = conn.cursor()
  # Check if database already exists
  cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
  if cur.fetchone():
      print(f"Database {db_name} already exists")
      return

  cur = conn.cursor()
  cur.execute(f"CREATE DATABASE {db_name}")
  logging.info(f"Database {db_name} created successfully")

def drop_tables():
  """Drop all tables if they exist"""
  with get_db_connection() as conn:
      cur = conn.cursor()
      # drop tables in descending hierarchical order.
      cur.execute("""
          DROP TABLE IF EXISTS table_format_edge_cases;
          DROP TABLE IF EXISTS table_formats;
          DROP TABLE IF EXISTS documents;
      """)
      conn.commit()
      logging.info("Tables dropped successfully")

def create_tables():
  """Initialize database tables if they don't exist"""
  with get_db_connection() as conn:
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    # Create documents table
    cur.execute("""
      CREATE TABLE IF NOT EXISTS documents (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        index BIGSERIAL,
        filename VARCHAR(255) NOT NULL,
        filetype VARCHAR(50) NOT NULL,
        byte_encoding BYTEA NOT NULL,
        sha256_hash VARCHAR(128) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      """)
    cur.execute("""
      CREATE TABLE IF NOT EXISTS table_formats(
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        index BIGSERIAL,
        document_id UUID NOT NULL,
        column_name VARCHAR(255) NOT NULL,
        column_type VARCHAR(50) NOT NULL,
        example_value VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
      );
      """)
    cur.execute("""
      CREATE TABLE IF NOT EXISTS table_format_edge_cases(
        table_id UUID PRIMARY KEY,
        edge_case VARCHAR(255) NOT NULL,
        edge_case_response VARCHAR(255) NOT NULL,
        FOREIGN KEY (table_id) REFERENCES table_formats(id)
      );
      """)
    
    conn.commit()
    logging.info("Tables created successfully")

def migrate_documents():
  """Migrate fs documents to database"""
  with get_db_connection() as conn:
     cur = conn.cursor()
     for file in os.listdir("./documents"):
        split = file.split(".")
        filename = "".join(split[:-1])
        filetype = split[-1]
        byte_encoding = open(f"./documents/{file}", "rb").read()
        sha256_hash = hashlib.sha256(byte_encoding).hexdigest()
        
        cur.execute("""
          INSERT INTO documents (filename, filetype, byte_encoding, sha256_hash)
          VALUES (%s, %s, %s, %s)
          """, (filename, filetype, byte_encoding, sha256_hash))
     conn.commit()
     logging.info("Documents migrated successfully")

def show_documents_table():
   with get_db_connection() as conn:
        cur = conn.cursor()
        
        # Show documents table
        print("\n=== Documents Table ===")
        cur.execute("""
            SELECT id, index, filename, filetype, 
                   LEFT(sha256_hash, 8) as hash_preview, 
                   created_at 
            FROM documents 
            ORDER BY index
        """)
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        print(tabulate(results, headers=columns, tablefmt='psql'))
   

def main():
  try:
    init_database("now")
    drop_tables()
    create_tables()
    migrate_documents()
  except psycopg2.Error as e:
    logging.error(f"DB ERROR: {e}")

if __name__ == "__main__":
   show_documents_table()