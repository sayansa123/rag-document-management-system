from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

db_name = 'DMS2'


# ===============================
# CREATING DATABASE if not EXISTS
# ===============================
# For creating the database if not exists
# mysql+pymysql://username:password@host:port/
ROOT_DATABASE_URL = f"mysql+pymysql://root:root@localhost:3306/"
root_engine = create_engine(ROOT_DATABASE_URL)      # Engine WITHOUT database


# Create database if not exists
def create_database_if_not_exists():
    with root_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()


# =================
# AS USUAL
# =================
# Create database url
# mysql+pymysql://username:password@host:port/db_name
DATABASE_URL = f"mysql+pymysql://root:root@localhost:3306/{db_name}"
# Create Engine
engine = create_engine(DATABASE_URL)

# Make Session Factory
Local_session = sessionmaker(bind=engine, autoflush=False)

# Declare Base Class
Base = declarative_base()


# Provide Session
def get_db():
    db = Local_session()
    try:
        yield db
    finally:
        db.close()