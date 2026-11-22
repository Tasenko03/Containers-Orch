FROM python:3.13-slim-bookworm

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TASKS_DB=/data/tasks.sqlite3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --gid 10001 tasks \
    && useradd --uid 10001 --gid tasks --no-create-home tasks \
    && install -d -o tasks -g tasks /data

COPY app.py storage.py ./

USER tasks
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
