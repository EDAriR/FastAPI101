from pydantic import BaseModel, Field
from typing import Optional

from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField
import datetime


class UserModel(BaseModel):
    user_id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    father_name: Optional[str] = Field(
        None, title="The father name of the User", max_length=300
    )
    age: float = Field(..., gt=0,
                       description="The age must be greater than zero")


class User(Document):
    _id = IntField()
    username = StringField(max_length=250, required=True)
    password = StringField(max_length=250, required=True)
    disabled = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
