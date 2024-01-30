# Attendance-System-fastapi


Run server

```
uvicorn main:app --reload
```

Docker build
```
sudo docker build -t <image_name>:<tag> .
```

Docker run

```
docker run --name test -p 8000:8000 test
```
Run test
```
python -m pytest
```

Auto generate migration
```
alembic revision --autogenerate -m "migration message"
```

Do migration
```
alembic upgrade head
```

docker compose
```
sudo docker-compose up -d --build 
```