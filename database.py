import sqlite3

conn = sqlite3.connect('chatbot.db')
c = conn.cursor()

# Table to store keyword-based Q&A
c.execute('''
CREATE TABLE IF NOT EXISTS chatbot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    answer TEXT NOT NULL
)
''')

# Recreate logs table with phone column
c.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
