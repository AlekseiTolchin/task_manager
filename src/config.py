import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql+asyncpg://postgres_user:postgres_password@postgres:5432/postgres_db'
)
SYNC_DATABASE_URL = os.getenv(
    'SYNC_DATABASE_URL', 'postgresql://postgres_user:postgres_password@postgres:5432/postgres_db'
)
