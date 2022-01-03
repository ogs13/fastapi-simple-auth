import uuid
from fastapi import APIRouter,Body, Depends, HTTPException
from starlette import status

from app.forms import UserLoginForm, UserCreateForm
from app.models import connect_db, User,AuthToken
from app.utils import get_password_hash
from app.auth import check_auth_token

router = APIRouter()


#@router.post('/login',name='user:login')
@router.post('/login')
def login(user_form: UserLoginForm = Body(..., embed=True), 
            database=Depends(connect_db)):
    queryset = database.query(User)
    filtered = queryset.filter(User.email == user_form.email)
    user = filtered.one_or_none()
    
    if not user or get_password_hash(user_form.password)!=user.password:
        return {
            'status':status.HTTP_400_BAD_REQUEST,
            'error':'Email or password invalid'
        }
    
    auth_token = AuthToken(token=str(uuid.uuid4()),user_id=user.id)
    database.add(auth_token)
    database.commit()
    return {
        'status':status.HTTP_200_OK,
        'auth_token':auth_token.token
    }

#@router.post('/user', name='user:create')
@router.post('/user')
def create_user(user:UserCreateForm=Body(...,embed=True),
                database=Depends(connect_db)):
    
    queryset = database.query(User.id)
    filtered = queryset.filter(User.email==user.email)
    exists_user = filtered.one_or_none()
    if exists_user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists'
        )
    
    new_user = User(
        email = user.email,
        password = get_password_hash(user.password),
        first_name = user.first_name,
        last_name = user.last_name,
        nick_name = user.nick_name,
    )
    database.add(new_user)
    database.commit()
    return {
        'status':status.HTTP_200_OK,
        'user_id':new_user.id
    }


#@router.get('/user', name='user:get')
@router.get('/user')
def user_get(token:AuthToken=Depends(check_auth_token), database=Depends(connect_db)):
    queryset = database.query(User)
    filtered = queryset.filter(User.id == token.user_id)
    user = filtered.one_or_none()    

    return {
        'status':status.HTTP_200_OK,
        'id':user.id,
        'email':user.email,
        'nick_name':user.nick_name
    }

