import uvicorn

from fastapi import FastAPI

from core.settings import settings

from api_v1 import router as router_v1


app = FastAPI()

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def start_test():
    return {"message": "1, 2, 3 Start!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=False)
