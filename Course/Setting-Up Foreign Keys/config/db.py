from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DB_Url = "postgresql://neondb_owner:npg_zO6s5HngmDCh@ep-super-wind-a8ltjh1f-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DB_Url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()