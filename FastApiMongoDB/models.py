
from mongoengine import Document, StringField, IntField, ListField, ReferenceField, DateTimeField, BooleanField
from pydantic import BaseModel
from fastapi import Body


class Employee(Document):
    emp_id=IntField(required=True)
    name = StringField(required=True, max_length=50)
    age = IntField(required=True, max_length=50)
    teams=ListField()

    # salary = IntField(required=True)
    # department = ReferenceField('Department', required=True)
    # created_at = DateTimeField(required=True)
    # updated_at = DateTimeField(required=True)
    # is_active = BooleanField(required=True)
    # meta = {'collection': 'employee'}

class User(Document):
    username = StringField(required=True, max_length=50)
    password = StringField(required=True, max_length=150)
    meta = {'collection': 'user'}


class NewEmployee(BaseModel):
    emp_id: int
    name: str
    age: int = Body(None, gt=18)
    teams: list
    # salary: int
    # department: str
    # created_at: str
    # updated_at: str
    # is_active: bool

class NewUser(BaseModel):
    username: str
    password: str