## build
```bash
docker build -t drive_reader .
```

<br>

## run
```bash
docker run -it --rm --env-file .env drive_reader uvicorn app.api:app --host 0.0.0.0 --port 8000
```