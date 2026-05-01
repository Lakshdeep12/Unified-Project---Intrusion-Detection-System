import uvicorn
from src.Database.models import create_tables

if __name__ == "__main__":
    create_tables()
    uvicorn.run("backend.main:app", host="127.0.0.0", port=8000, reload=True)
