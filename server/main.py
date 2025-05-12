from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import LargeBinary, create_engine, Column, TEXT, VARCHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import bcrypt

app = FastAPI()

DATABASE_URL = 'postgresql://postgres:0000@localhost:5432/fluttermusicapp'

# Setup database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

Base = declarative_base()

# Pydantic model for input validation
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# SQLAlchemy model for the User table
class User(Base):
    __tablename__ = 'users'

    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    oaswird = Column(LargeBinary)  # Store the hashed password

# Route for user signup
@app.post('/signup')
def signup_user(user: UserCreate):
    # Check if user with the same email already exists
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User with the same email already exists!")
    
    # Hash the password before storing
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Create a new user instance
    new_user = User(
        id=str(uuid.uuid4()),  # Unique ID for the user
        email=user.email,
        oaswird=hashed_pw,  # Store the hashed password
        name=user.name
    )

    # Add and commit the new user to the database
    db.add(new_user)
    db.commit()
    
    # Refresh to get the ID and other auto-generated fields if needed
    db.refresh(new_user)

    # Return the user data (excluding the password)
    return new_user

# Create tables in the database
Base.metadata.create_all(engine)
