import aiosqlite
from config.config import TAGS
from logs import logger

async def create_user_tag(user_id_tg:int, tag_name:str):
    
    if tag_name in TAGS:
        
        async with aiosqlite.connect('lead.db') as conn:
            cursor = await conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
            tag_id = await cursor.fetchone()
            cursor = await conn.execute('SELECT id FROM users WHERE id_tg = ?', (user_id_tg,))
            user_id = await cursor.fetchone()
            await conn.execute ('INSERT INTO user_tags (user_id, tag_id) VALUES (?, ?)', (user_id[0], tag_id[0]))
            await conn.commit()
            
            return True
    return False

async def rename_user_tag(user_id_tg:int, tag_name_old:str, tag_name_new:str):
    '''Функция чтобы менять тэг "новый" на "не новый"'''
    async with aiosqlite.connect('lead.db') as conn:
        cursor = await conn.execute ('SELECT id FROM users WHERE id_tg = ?', (user_id_tg,))
        user_id = await cursor.fetchone()
        cursor = await conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name_old,))
        tag_id = await cursor.fetchone()
        cursor = await conn.execute ('SELECT id FROM user_tags WHERE user_id = ? AND tag_id = ?', (user_id[0], tag_id[0]))
        user_tags_data = await cursor.fetchone()
        if user_tags_data:
            cursor = await conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name_new,))
            tag_id = await cursor.fetchone()
            # await conn.execute('UPDATE user_tags SET tag_id = ? WHERE id = ?', (tag_id[0], user_tags_data[0]))
            await conn.execute('UPDATE user_tags SET tag_id = ? WHERE id = ?', (tag_id, user_tags_data[0]))
            logger.info('ОШИБКА после обновления  ТУТ 🤡')
            await conn.commit()
            return True
        return False
        
async def get_users_by_tag(tag_name:str,):
    async with aiosqlite.connect('lead.db') as conn:
        cursor = await conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        tag_id = await cursor.fetchone()
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute ('SELECT * FROM user_tags JOIN users ON user_tags.user_id = users.id WHERE  tag_id = ?', (tag_id[0],))
        user_tags_data = await cursor.fetchall()
        

        return [dict(user) for user in user_tags_data]

