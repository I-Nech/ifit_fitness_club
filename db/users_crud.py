import aiosqlite
import asyncio


async def create_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        await conn.execute(f'INSERT INTO users (id_tg) VALUES (?)', (id_tg,))
        await conn.commit()
    return True

async def get_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        cursor = await conn.execute('SELECT * FROM users WHERE id_tg = ?', (id_tg,))
        return await cursor.fetchone() # fetchmany/ fetchall

# async def update_user(id_tg: int, param: str,  value):
#     async with aiosqlite.connect('lead.db') as conn:
#         await conn.execute(f'UPDATE users SET {param} = ? WHERE id_tg = ?', (value, id_tg))
#         await conn.commit()   

async def update_user(id_tg: int, **kwargs):
    async with aiosqlite.connect('lead.db') as conn:
        for key in kwargs: 
            try: 
                await conn.execute(f'UPDATE users SET {key} = ? WHERE id_tg = ?', (kwargs[key], id_tg))
            except Exception as e:
                print('ошибка', e)
        await conn.commit() 

if __name__ == '__main__':

    # asyncio.run(create_user(123))
    asyncio.run(update_user(123, nam='Leha', number='3759434343243243'))
    