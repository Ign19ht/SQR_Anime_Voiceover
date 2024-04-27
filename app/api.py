from fastapi import FastAPI
import uvicorn
from drive_loader import DriveReader
from parser import parse

app = FastAPI()


@app.get("/{dir_id}")
async def root(dir_id: str):
    reader = DriveReader()
    print("File fetching started")
    transcripts = reader.read_transcripts(dir_id)
    print("File parsing started")
    dashboard = parse(transcripts)
    print(dashboard)


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
