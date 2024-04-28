from app.drive_loader import DriveReader
from app.parser import parse


def load_data(dir_id: str):
    reader = DriveReader()
    print("File fetching started")
    transcripts = reader.read_transcripts(dir_id)
    print("File parsing started")
    dashboard = parse(transcripts)
    return dashboard
