from sqlalchemy.ext.asyncio import AsyncSession
from todo import model, schemas
from fastapi import HTTPException


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 10, status: str = None):
    query = db.query(model.Todo)
    if status:
        query = query.filter(model.Todo.task_status == status)
    result = await query.offset(skip).limit(limit).all()
    return result


async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    return result


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate, user_id: int):
    db_todo = model.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def update_todo(db: AsyncSession, todo_id: int, todo: schemas.TodoUpdate, user_id: int):
    db_todo = await db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if db_todo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")

    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def delete_todo(db: AsyncSession, todo_id: int, user_id: int):
    db_todo = await db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if db_todo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")

    await db.delete(db_todo)
    await db.commit()
    return db_todo
