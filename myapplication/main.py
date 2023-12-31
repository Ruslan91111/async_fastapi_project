"""Main module, contains instance of Fastapi and main_api_router."""
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from myapplication.api.handlers.user_handlers import user_router
from myapplication.api.handlers.login_handlers import login_router


app = FastAPI(title="Ruslan's app")

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
