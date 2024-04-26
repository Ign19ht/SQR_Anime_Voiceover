from drive_loader import DriveReader

def main():
    reader = DriveReader()
    print("File fetching started")
    transcripts = reader.read_transcripts("1O_lS_3AwnHUzH0TfwzSZ_PbHVIEq5PMC")
    print(transcripts.keys())

if __name__ == '__main__':
    main()