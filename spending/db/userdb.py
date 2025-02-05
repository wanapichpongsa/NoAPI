import sqlite3

class UserDatabase:
  def __init__(self):
      pass
  
  def init_user_db(self):
      with sqlite3.connect('role.db') as conn:
          cursor = conn.cursor()
          # This code is for a 100% local app so we don't have admins etc.
          # Can create multiple accounts and associated data incase user wants multiple accounts (for any reason)
          # Since this db is the 'last resort' db, no read access as password is not encrypted.
          cursor.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  user_index INTEGER AUTOINCREMENT,
                  user_id UUID DEFAULT RANDOMUUID(),
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (user_index, user_id)
              )
          ''')
          conn.commit()

  def check_user_exists(self, username: str) -> bool:
      with sqlite3.connect('role.db') as conn:
          cursor = conn.cursor()
          cursor.execute('''
              SELECT COUNT(*) FROM users WHERE username = ?
          ''', (username))
          return cursor.fetchone()[0]

  def verify_password(self, username: str, password: str) -> bool:
      with sqlite3.connect('role.db') as conn:
          cursor = conn.cursor()
          cursor.execute('''
              SELECT password FROM users WHERE username = ?
          ''', (username))
          return cursor.fetchone()[0] == password