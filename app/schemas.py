from pydantic import BaseModel, EmailStr, validator

class UserCreated(BaseModel):
    username : str
    email : EmailStr
    password : str

    @validator('username')
    def check_username(cls, v):
        if v.strip() == '' or v.strip() is None:
            raise ValueError('You didnt enter a username')
        return v

    @validator('password')
    def check_password(cls, v):
        if v.strip() == '' or v.strip() is None:
            raise ValueError('You didnt enter a password')
        if len(v) < 6:
            raise ValueError('Use a least 6 characters')
        return v


# user login schema
class UserLogin(BaseModel):
    username : str
    password : str

    @validator('username')
    def check_username(cls, v):
        if v.strip() == '' or v.strip() is None:
            raise ValueError('You didnt enter a username')
        return v

    @validator('password')
    def check_password(cls, v):
        if v.strip() == '' or v.strip() is None:
            raise ValueError('You didnt enter a password')
        if len(v) < 6:
            raise ValueError('Use a least 6 characters')
        return v


class Token(BaseModel):
    access_token : str
    type_token : str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : int

# tasks

# create task
class CreateTask(BaseModel):
    task_name : str
    completed : bool = False

    @validator('task_name')
    def check_username(cls, v):
        if v.strip() == '' or v.strip() is None:
            raise ValueError('You didnt enter a task name')
        return v

class UpdateTask(CreateTask):
    pass

# tasks


