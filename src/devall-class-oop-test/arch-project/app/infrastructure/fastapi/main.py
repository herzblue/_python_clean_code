from fastapi import FastAPI
from app.controller.user import signup
from app.infrastructure.database.orm import db, UserModel
import uvicorn

def create_app():
    app = FastAPI()
    app.add_api_route(
        path='/user',
        methods=['POST'],
        endpoint=signup
    )
    
    return app

def init_db():
    db.connect()
    UserModel.create_table()

if __name__ == "__main__":
    init_db()
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # PYTHONPATH=. python src/devall-class-oop-test/arch-project/app/infrastructure/fastapi/main.py
    