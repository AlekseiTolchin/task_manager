import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:user@localhost:5432/tasks')
SYNC_DATABASE_URL = os.getenv('SYNC_DATABASE_URL', 'sqlite:///posts.db')