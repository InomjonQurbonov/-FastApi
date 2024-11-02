from sqlalchemy.orm import Session
from todo import model, schemas
from fastapi import HTTPException


def get_todos(db: Session, skip: int = 0, limit: int = 10, status: str = None):
    query = db.query(model.Todo)
    if status:
        query = query.filter(model.Todo.task_status == status)
    return query.offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int):
    return db.query(model.Todo).filter(model.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = model.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate, user_id: int):
    db_todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if db_todo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")

    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if db_todo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")

    db.delete(db_todo)
    db.commit()
    return db_todo