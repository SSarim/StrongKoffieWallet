from fastapi import FastAPI
from app.routes import router as blockchain_router
import uvicorn

app = FastAPI()
app.include_router(blockchain_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# For testing, running on uvicorn
# uvicorn main:app --reload
