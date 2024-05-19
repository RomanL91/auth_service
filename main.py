import uvicorn

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def start_test():
    return {"message": "1, 2, 3 Start!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
