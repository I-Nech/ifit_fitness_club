import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN= os.getenv("TOKEN")
ADMIN_ID = os.getenv('ADMIN_ID')