import os
from schemas.session import engine, Base
from schemas.models import Album, Songs

def test_connection():
    try:
        with engine.connect() as conn:
            print("database success!")
    except Exception as e:
        print("database failed..")
        
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    test_connection()
    create_tables()