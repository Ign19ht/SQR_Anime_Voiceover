from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/{dir_id}")
async def root(dir_id: str):
    return {"message": "Hello World"}


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
