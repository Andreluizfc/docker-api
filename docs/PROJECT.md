#### Project Structure:
```
docker-api/
│
├── app/
│   ├── __init__.py
│   └── main.py
├── poetry.lock
├── pyproject.toml
├── Dockerfile
└── README.md
```
### **Step 1: Create the FastAPI App**

#### 1.1 Create Project Structure
```bash
mkdir app
touch app/main.py Dockerfile
```

#### 1.2 Create the `app/main.py` File
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/add-data")
async def add_data():
    return {"message": "Endpoint for adding data is live!"}
```

#### 1.3 Set Up Poetry
Initialize the project with Poetry:
```bash
poetry init --name fastapi-docker --description "A simple FastAPI project" \
  --author "Your Name" --license MIT --python "^3.12" --dependency fastapi --dependency uvicorn
```

#### 1.4 Create the FastAPI `Dockerfile`
```dockerfile
FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY app ./app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 1.5 Build and Run the FastAPI Container
Build the FastAPI Docker image:
```bash
docker build -t fastapi-app .
```

Run the container:
```bash
docker run -d --name fastapi-container -p 8000:8000 fastapi-app
```

---

### **Step 2: Create the PostgreSQL Container**

#### 2.1 Create a Directory for PostgreSQL
```bash
mkdir db && cd db
touch Dockerfile init.sql
```

#### 2.2 Write the `db/Dockerfile`
```dockerfile
FROM postgres:15

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=fastapi_db

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/
```

#### 2.3 Write the `db/init.sql`
```sql
CREATE TABLE IF NOT EXISTS people (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    sex TEXT NOT NULL,
    age INT NOT NULL,
    cryptos JSONB NOT NULL
);
```

#### 2.4 Build and Run the PostgreSQL Container
Navigate to the `db` folder and build the PostgreSQL image:
```bash
docker build -t postgres-db .
```

Run the PostgreSQL container with a persistent volume:
```bash
docker volume create pgdata
docker run -d --name postgres-container -p 5432:5432 \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=fastapi_db \
  -v pgdata:/var/lib/postgresql/data postgres-db
```

#### 2.5 Verify the PostgreSQL Container
Check logs to ensure it started successfully:
```bash
docker logs postgres-container
```

Connect to the database for verification:
```bash
docker exec -it postgres-container psql -U user -d fastapi_db
```

---

### **Step 3: Link the FastAPI App to PostgreSQL**

#### Update `app/main.py` in the FastAPI container to connect to PostgreSQL:
```python
from fastapi import FastAPI, HTTPException
from databases import Database
import os

DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "fastapi_db")
DB_HOST = os.getenv("DB_HOST", "localhost")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
database = Database(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
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

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/add-data")
async def add_data(name: str, sex: str, age: int, cryptos: dict):
    query = """
    INSERT INTO people (name, sex, age, cryptos)
    VALUES (:name, :sex, :age, :cryptos);
    """
    try:
        await database.execute(query, {"name": name, "sex": sex, "age": age, "cryptos": cryptos})
        return {"message": f"Data for {name} has been added!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Rebuild the FastAPI container with the database connection:
```bash
docker build -t fastapi-app .
docker run -d --name fastapi-container -p 8000:8000 fastapi-app
```

#### 3.1 Test the API
Rebuild and bring up the containers:
```bash
docker-compose down && docker-compose up --build
```

Use a tool like `Postman` or `curl` to test the API:
```bash
curl -X POST "http://localhost:8000/add-data" \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "sex": "male", "age": 30, "cryptos": {"BTC": 2, "ETH": 5}}'
```


---

### **Step 4: Add PostgreSQL Container with Persistent Storage**

#### 4.1 Create a `docker-compose.yml` File
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

#### 4.2 Create a `.env` File
```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=fastapi_db
```

#### 4.3 Update the `Dockerfile` for the App
Ensure the `app` can access PostgreSQL by including the dependency:
```bash
poetry add asyncpg databases
```

Rebuild and bring up containers:
```bash
docker-compose up --build
```

---