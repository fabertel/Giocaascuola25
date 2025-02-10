from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

app = FastAPI()

# Database configuration
DATABASE_URL = "mysql+mysqlconnector://'tigeruser':'5y]nKt84!OYjIvm'@195.231.81.175/dbtiger"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

# Create tables
Base.metadata.create_all(bind=engine)

# HTML form
REGISTER_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>User Registration</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        form { display: flex; flex-direction: column; gap: 10px; }
        input[type="text"] { padding: 8px; }
        button { padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>User Registration</h1>
    <form action="/register" method="post">
        <input type="text" name="name" placeholder="Enter your name" required>
        <button type="submit">Register</button>
    </form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return REGISTER_FORM

@app.post("/register")
async def register(name: str = Form(...)):
    db = SessionLocal()
    try:
        user = User(name=name)
        db.add(user)
        db.commit()
        return {"message": f"User {name} registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)