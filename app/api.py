from fastapi import FastAPI
from app.drive_loader import DriveReader
from app.parser import parse

app = FastAPI()


@app.get("/{dir_id}")
async def root(dir_id: str):
    reader = DriveReader()
    print("File fetching started")
    transcripts = reader.read_transcripts(dir_id)
    print("File parsing started")
    dashboard = parse(transcripts)
    print(dashboard)
