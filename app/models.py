from xmlrpc.client import Boolean
from sqlalchemy import Column, String, Integer, TIMESTAMP, text, Boolean, ForeignKey
from .database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=30), nullable=False, unique=True)
    email = Column(String(length=100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    @property
    def password_hashed(self):
        return self.password
    
    @password_hashed.setter
    def password_hashed(self, password_plain_text):
        self.password = pwd_context.hash(password_plain_text)

    def check_password(password_hashed, password_plain_text):
        return pwd_context.verify(password_plain_text, password_hashed)


# task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_name = Column(String, nullable=False, unique=True)
    completed = Column(Boolean, nullable=False, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    