from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Task

from app.schemas import CreateTask, UpdateTask
from ..database import get_db
from ..onauth2 import get_current_user

router = APIRouter(prefix='/tasks', tags=['Task'])

@router.get('/')
def get_tasks(db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).order_by(Task.created_at.desc()).all()

    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Tasks...')

    return tasks


@router.get('/{id}')
def create_task(id:int, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'not exist any task by this ID => {id}')

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')

    return task

@router.post('/', status_code=status.HTTP_201_CREATED )
def create_task(task_data : CreateTask,db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = Task(**task_data.dict(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch('/{id}')
def update_task(id : int, task_data : UpdateTask, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'not exist any task by this ID => {id}')

    if task.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    task.update(dict(task_data), synchronize_session=False)
    db.commit()
    return task.first()

@router.delete('/{id}')
def delete_task(id:int, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'not exist any task by this ID => {id}')

    if task.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    
    task.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)