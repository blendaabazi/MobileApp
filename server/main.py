# from fastapi import FastAPI
# from routes import auth
# from models.base import Base
# from database import engine
# app = FastAPI()

# app.include_router(auth.router, prefix='/auth')


# Base.metadata.create_all(engine)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routes import auth
from models.base import Base
from database import engine

app = FastAPI()

app.include_router(auth.router, prefix='/auth')

Base.metadata.create_all(engine)

# ✅ Shto këtë për ta trajtuar GET /
@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Welcome to the API</h1>"
