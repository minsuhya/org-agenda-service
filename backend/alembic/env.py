from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context
from models.base import Base

config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    # ... 마이그레이션 설정 ... 