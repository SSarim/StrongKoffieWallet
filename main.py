import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import router as blockchain_router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="BobbyShmurda:TheKingOfNY")

app.include_router(blockchain_router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# For testing, running on uvicorn
# uvicorn main:app --reload or uvicorn main:app --port 8001