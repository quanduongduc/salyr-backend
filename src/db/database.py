from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query

DATABASE_URL = settings.mysql_dsn

engine = create_engine(DATABASE_URL)

print(settings.mysql_dsn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def paginate(db: Session, query : Query, page_number: int, page_limit: int) -> Query:
    offset = (page_number - 1) * page_limit
    return query.offset(offset).limit(page_limit)