from fastapi import FastAPI, HTTPException,Depends
import uuid
import bcrypt
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from database import get_db
from sqlalchemy.orm import Session
from models.user import User


from pydantic_schemas.user_login import UserLogin

router = APIRouter()


@router.post('/signup', status_code=201)
def signup_user(user: UserCreate, db: Session=Depends(get_db)):
    # Check if user with the same email already exists
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User with the same email already exists!")
    
    # Hash the password before storing
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Create a new user instance
    # user_db = User(
    #     id=str(uuid.uuid4()),  # Unique ID for the user
    #     email=user.email,
    #     password=hashed_pw,  # Store the hashed password
    #     name=user.name
    # )
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hashed_pw, name=user.name)



    # Add and commit the new user to the database
    db.add(user_db)
    db.commit()
    
    # Refresh to get the ID and other auto-generated fields if needed
    db.refresh(user_db)

    # Return the user data (excluding the password)
    return user_db



@router.post('/login')

def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # check if a user with same email already exist
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400, 'User with this email does not exist!')
    
    # password matching or not
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    
    
    if not is_match:
        raise HTTPException(400, 'Incorrect password!')
    
    return user_db