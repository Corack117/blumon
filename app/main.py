from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.appliactions.users.views import router as user_router
from app.appliactions.users import models
from app.config.database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
testclient = TestClient(app)


@app.get('/')
def root():
    return {'data': 'Ruta'}