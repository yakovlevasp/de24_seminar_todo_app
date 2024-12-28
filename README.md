# TODO API

## Описание

Это простой сервис для управления задачами (TODO) с использованием FastAPI и базы данных SQLite. Сервис предоставляет REST API для создания, обновления, удаления и получения задач.

DockerHub: https://hub.docker.com/r/yakovlevasp/todo-service/tags

## Возможности
- **Создание задач** с заголовком, описанием и статусом выполнения.
- **Получение всех задач** в виде списка.
- **Получение задачи по ID.**
- **Обновление существующих задач.**
- **Удаление задач** по ID.
- **Хранение данных** в SQLite базе данных.

## Стек технологий
- **Backend:** FastAPI
- **База данных:** SQLite
- **ORM:** SQLAlchemy
- **Валидация данных:** Pydantic

## Установка и запуск через Docker

### Шаг 1: Сборка и запуск контейнера
```bash
docker build -t todo-fastapi .
```

### Шаг 2: Запуск контейнера
```bash
docker run -d -p 8000:80 -v todo_data:/app/data todo-fastapi
```

API будет доступно по адресу: http://localhost:8000

### Методы API

- **GET /items** - получить список всех задач.
![get_items.JPG](img%2Fget_items.JPG)
- **GET /items/{item_id}** - получить задачу по ID.
![item_id.JPG](img%2Fitem_id.JPG)
- **POST /items** - создать новую задачу.
![post_items.JPG](img%2Fpost_items.JPG)
- **PUT /items/{item_id}** - обновить задачу по ID.
![put_item.JPG](img%2Fput_item.JPG)
- **DELETE /items/{item_id}** - удалить задачу по ID.
![del_item.JPG](img%2Fdel_item.JPG)