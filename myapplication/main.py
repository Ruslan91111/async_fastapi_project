"""Main module, contains instance of Fastapi and main_api_router."""
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from myapplication.api.user_routes import user_router


app = FastAPI(title="Ruslan's app")

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
