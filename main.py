"""
API для управления задачами
"""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import TodoItem as TodoItemModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TODO API Service", description="API для управления задачами (TODO)", version="1.0")


class TodoCreate(BaseModel):
    title: str = Field(..., example="Организовать конференцию")
    description: Optional[str] = Field(None, example="Организовать международную конференцию по климату")
    completed: bool = Field(False, example=False)

    class Config:
        schema_extra = {
            "example": {
                "title": "Организовать конференцию",
                "description": "Организовать международную конференцию по климату",
                "completed": False
            }
        }


class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Организовать конференцию",
                "description": "Организовать международную конференцию по климату",
                "completed": False
            }
        }


def get_db():
    """
    Функция для получения сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items", response_model=List[TodoItem], summary="Получить все задачи")
def get_items(db: Session = Depends(get_db)):
    """
    Получить список всех задач.

    **Пример ответа:**
    ```json
    [
      {
        "id": 1,
        "title": "Организовать конференцию",
        "description": "Организовать международную конференцию по климату",
        "completed": False
      }
    ]
    ```
    """
    items = db.query(TodoItemModel).all()
    return items


@app.get("/items/{item_id}", response_model=TodoItem, summary="Получить задачу по ID")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Получить задачу по её ID.

    **Пример ответа:**
    ```json
    {
      "id": 1,
      "title": "Организовать конференцию",
      "description": "Организовать международную конференцию по климату",
      "completed": False
    }
    ```

    **Ошибки:**
    - 404: Задача не найдена
    """
    item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=TodoItem, summary="Создать новую задачу")
def create_item(item: TodoCreate, db: Session = Depends(get_db)):
    """
    Создать новую задачу.

    **Пример тела запроса:**
    ```json
    {
      "title": "Организовать конференцию",
      "description": "Организовать международную конференцию по климату",
      "completed": False
    }
    ```
    """
    new_item = TodoItemModel(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=TodoItem, summary="Обновить задачу по ID")
def update_item(item_id: int, item: TodoCreate, db: Session = Depends(get_db)):
    """
    Обновить существующую задачу по её ID.

    **Ошибки:**
    - 404: Задача не найдена
    """
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db_item.completed = item.completed
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", summary="Удалить задачу по ID")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Удалить задачу по её ID.

    **Ошибки:**
    - 404: Задача не найдена
    """
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}
