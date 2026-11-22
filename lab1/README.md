# ЛР 1. Dockerfile

HTTP API списка задач. SQLite хранит данные в `/data/tasks.sqlite3`. Код работы с БД находится в `storage.py`.

## Сборка и проверка

Команды выполняются из корня репозитория. Для каждого образа используется отдельный именованный volume.

```bash
docker build -t lab1-tasks:good lab1
docker build -t lab1-tasks:bad -f lab1/Dockerfile.bad lab1

variant=good
volume="lab1-tasks-$variant-$$"
docker run -d --name lab1-tasks -p 127.0.0.1:8000:8000 \
  --mount "type=volume,source=$volume,target=/data" "lab1-tasks:$variant"

curl -fsS --retry 10 --retry-all-errors --retry-delay 1 http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' -d '{"title":"Проверить volume"}'
curl -fsS -X PATCH http://127.0.0.1:8000/tasks/1/complete
docker rm -f lab1-tasks

docker run -d --name lab1-tasks -p 127.0.0.1:8000:8000 \
  --mount "type=volume,source=$volume,target=/data" "lab1-tasks:$variant"

curl -fsS --retry 10 --retry-all-errors --retry-delay 1 http://127.0.0.1:8000/tasks
docker rm -f lab1-tasks
docker volume rm "$volume"
```

На свежем volume первая задача получает `id=1`. После пересоздания контейнера `GET /tasks` возвращает её с `completed: true`. Для второго образа повторить запуск и проверку с `variant=bad`.

## Практики в Dockerfile

| Плохой вариант | Последствие | Исправление | Источник |
| --- | --- | --- | --- |
| Процесс от `root` | Приложение получает лишние права внутри контейнера | `USER tasks`, каталог `/data` доступен этому пользователю для записи. | [Docker Docs — USER](https://docs.docker.com/build/building/best-practices/#user) |
| Установка `vim` | Растут размер образа и число пакетов | Убрать редактор из образа. | [Docker Docs — лишние пакеты](https://docs.docker.com/build/building/best-practices/#dont-install-unnecessary-packages) |
| Копирование кода до `pip install` | Изменение кода сбрасывает кеш установки зависимостей | Скопировать `requirements.txt`, установить зависимости, затем скопировать код. | [Docker Docs — порядок слоёв](https://docs.docker.com/build/cache/optimize/#order-your-layers) |

При локальной проверке оба образа сохранили задачу после пересоздания контейнера. Размеры образов по `docker image inspect` составили 46,4 МБ для хорошего и 60,2 МБ для плохого. После изменения `app.py` шаг `pip install` взялся из кеша только в хорошем образе.

## Плохие практики эксплуатации

- Хранить БД в записываемом слое контейнера. При удалении контейнера данные пропадут. Подключать volume к `/data`.
- Устанавливать зависимости через `docker exec`. Ручные изменения пропадут при пересоздании контейнера из исходного образа. Добавлять зависимости в сборку образа.

## Когда контейнеры не подходят

- Проверка нового ядра Linux или драйвера. Контейнер использует ядро хоста. Для проверки под другим ядром нужна виртуальная машина или отдельный компьютер.
- Разовый запуск локального Python-скрипта для обработки CSV. Для изоляции зависимостей достаточно `venv`. Сборка образа и подключение папки с данными добавят лишние шаги.
