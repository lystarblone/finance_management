from fastapi import FastAPI
from database import engine, Base
from routers import transactions, categories, statistics
from models import Transaction, Category
import uvicorn

app = FastAPI(title="Finance Tracker API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Finance Tracker API! Try /docs for API documentation."}

Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(statistics.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)