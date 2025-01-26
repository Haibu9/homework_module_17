from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalars(select(User)).all()
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")



@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_: CreateUser):

    db.execute(insert(User).values(username=create_user_.username,
                                       firstname=create_user_.firstname,
                                       lastname=create_user_.lastname,
                                       age=create_user_.age,
                                       slug=slugify(create_user_.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)],
                      user_id: int,
                      update_user_: UpdateUser):
    users = db.scalars(select(User)).all()
    for user in users:
        if user.id == user_id:
            db.execute(update(User).where(User.id == user_id).values(firstname=update_user_.firstname,
                                                                     lastname=update_user_.lastname,
                                                                     age=update_user_.age))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalars(select(User)).all()
    for user in users:
        if user.id == user_id:
            db.execute(delete(User).where(User.id == user_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted is successful!'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")