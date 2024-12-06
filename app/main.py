from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
import os
import uvicorn
import json

DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "fastapi_db")
DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}?connect_timeout=10"
database = Database(DATABASE_URL)

app = FastAPI()

class Person(BaseModel):
    name: str
    sex: str
    age: int
    cryptos: dict

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        await database.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            sex TEXT NOT NULL,
            age INT NOT NULL,
            cryptos JSONB NOT NULL
        );
        """)
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
    except Exception as e:
        print(f"Error during shutdown: {e}")

@app.post("/add-data")
async def add_data(person: Person):
    query = """
    INSERT INTO people (name, sex, age, cryptos)
    VALUES (:name, :sex, :age, :cryptos);
    """
    try:
        # Ensure cryptos is a JSON string if it's a dict
        cryptos_json = json.dumps(person.cryptos) if isinstance(person.cryptos, dict) else person.cryptos
        await database.execute(query, {"name": person.name, "sex": person.sex, "age": person.age, "cryptos": cryptos_json})
        return {"message": f"Data for {person.name} has been added!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)
