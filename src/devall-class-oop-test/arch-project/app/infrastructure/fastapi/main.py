from fastapi import FastAPI
from app.controller.user import signup
import uvicorn

def create_app():
    app = FastAPI()
    app.add_api_route(
        path='/user',
        methods=['POST'],
        endpoint=signup
    )
    
    return app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # PYTHONPATH=. python src/devall-class-oop-test/arch-project/app/infrastructure/fastapi/main.py
    