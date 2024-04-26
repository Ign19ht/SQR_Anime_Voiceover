## build
```bash
docker build -t drive_reader .
```

<br>

## run
```bash
docker run --env-file .env --rm -it --network host drive_reader
```