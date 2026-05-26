import sqlite3

conn = sqlite3.connect("data/memory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        role TEXT,
        content TEXT
    )
    '''
)

conn.commit()

def save_memory(user_id, role, content):
    cursor.execute(
        '''
        INSERT INTO memory (user_id, role, content)
        VALUES (?, ?, ?)
        ''',
        (user_id, role, content)
    )
    conn.commit()

def load_memory(user_id, limit=10):
    cursor.execute(
        '''
        SELECT role, content
        FROM memory
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        ''',
        (user_id, limit)
    )

    rows = cursor.fetchall()
    rows.reverse()

    return [
        {
            "role": row[0],
            "content": row[1]
        }
        for row in rows
    ]
