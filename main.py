import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from core.settings import settings

from api_v1 import router as router_v1


app = FastAPI()

origins = ['http://localhost','http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def start_test():
    return {"message": "1, 2, 3 Start!"}


if __name__ == "__main__":
<<<<<<< HEAD
    uvicorn.run("main:app", port=8001, reload=True)
=======
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=False)
>>>>>>> ba81d64 (Разрешил CORS для работы с API)
