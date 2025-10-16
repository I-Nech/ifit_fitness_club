import aiosqlite

async def create_tables(app):
    conn = await aiosqlite.connect('lead.db')
    await conn.execute('''CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_tg INTEGER UNIQUE,
                            name TEXT NULL,
                            number TEXT NULL UNIQUE,
                            email TEXT NULL UNIQUE,
                            agreement INTEGER DEFAULT 0,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    await conn.commit()
    await conn.close()

