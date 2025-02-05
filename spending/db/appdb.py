import sqlite3

class AppDatabase:
  def __init__(self):
    pass
  
  def init_app_db(self):
      with sqlite3.connect('app.db') as conn:
          cursor = conn.cursor() # cursor executes SQL commands
          """
          When creating tables to represent nested attributes, use composite primary keys because...
          1. index: {1,2,3} is better for relative search
          2. uuid: 853deca8-e3e6-11ef-ac60-f683b11e0f59 is unique, thus better for absolute search
          """
          # requests table is the parent of all tables hence it doesn't need uuid for composite key
          # It will; however, have day indexes to know which no request of the day it is
          cursor.execute('''
              CREATE TABLE IF NOT EXISTS requests (
                  request_index INTEGER PRIMARY KEY AUTOINCREMENT,
                  day DATE NOT NULL DEFAULT CURRENT_DATE,
                  day_index INTEGER,
                  month TEXT NOT NULL,
                  year INTEGER NOT NULL,
                  request_type TEXT NOT NULL,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              )
          ''')
          # request_type has to be array-checked in python. sub-tables based on request_types can made :) e.g., db_search, chatbot

          cursor.execute('''
              CREATE TABLE IF NOT EXISTS chatbot (
                  message_index INTEGER AUTOINCREMENT,
                  message_id UUID DEFAULT RANDOMUUID(),
                  user_messages TEXT NOT NULL,
                  ai_response TEXT NOT NULL,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (message_index, message_id),
                  FOREIGN KEY (request_index) REFERENCES requests(request_index)
              )
          ''')
          conn.commit()