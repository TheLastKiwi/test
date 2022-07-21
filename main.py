from fastapi import FastAPI
from database.connector import get_database
from database.models import TestTable
from database.connector import Base, engine


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/test")
def test():
    db = next(get_database())
    t = TestTable(name="test")
    db.add(t)
    db.commit()
    return t


@app.get("/test")
def get_test_data():
    db = next(get_database())
    return db.query(TestTable).all()


def populate_test_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = next(get_database())
    test_row = TestTable(name="TestData")
    db.add(test_row)
    db.commit()


populate_test_data()
