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
async def get_users():
    async with aiosqlite.connect('lead.db') as conn:
        cursor = await conn.execute('SELECT * FROM users WHERE agreement = 0 ') # ТУТ ПРАВИЛЬНО? ЕСЛИ ЮЗЕР СОГЛАСЕН НА ОПД?
        return await cursor.fetchall()

# async def update_user(id_tg: int, param: str,  value):
#     async with aiosqlite.connect('lead.db') as conn:
#         await conn.execute(f'UPDATE users SET {param} = ? WHERE id_tg = ?', (value, id_tg))
#         await conn.commit()   

async def update_user(id_tg: int, **kwargs):
    # print(kwargs.items())
    async with aiosqlite.connect('lead.db') as conn:
        # for parameter, value in kwargs.items():
        for parameter, value in kwargs.items(): 
            try: 
                await conn.execute(f'UPDATE users SET {parameter} = ? WHERE id_tg = ?', (value, id_tg))
            except Exception as e:
                print('ошибка', e)
        await conn.commit() 

if __name__ == '__main__':

    # asyncio.run(create_user(123))
    asyncio.run(update_user(123, name='Leha', number='3759434343243243'))
    