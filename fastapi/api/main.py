from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth
from .database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Add middleware to bypass CORS from NEXTJS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'], # Default nextjs port
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
    # with these middlewares we can consume anything from the port 3000
)

@app.get("/")
def health_check():
    return 'Health Check Complete'

app.include_router(auth.router)
