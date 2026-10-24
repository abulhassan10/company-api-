from fastapi import FastAPI
from sqlalchemy import text
from database import Base, engine
from routers import company, employee, users

# Ensure database tables exist
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Company API",
    description="API for Company and Employee management with dual authentication (Password & Security PIN).",
    version="1.0.0"
)

# Mount routers
app.include_router(users.router)
app.include_router(company.router)
app.include_router(employee.router)


@app.get("/", )
def root():
    return {
        "message": "Welcome to Company API",
        
        
    }

