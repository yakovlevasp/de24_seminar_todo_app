"""
Модель для представления задач
"""
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class TodoItem(Base):
    """
    Модель TodoItem для представления задач в списке дел.

    Атрибуты:
        id (int): Уникальный идентификатор задачи (primary key).
        title (str): Заголовок задачи.
        description (str, optional): Описание задачи. Может быть пустым (nullable).
        completed (bool): Статус выполнения задачи. По умолчанию False (не выполнена).

    Таблица:
        todo_items: Содержит все задачи, где каждая задача имеет уникальный id, заголовок, описание и статус выполнения.
    """
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
