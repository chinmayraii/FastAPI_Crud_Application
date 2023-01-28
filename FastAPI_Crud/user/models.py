import uuid
from fastapi import FastAPI
from tortoise.models import Model
from tortoise import Tortoise,fields



class User(Model):
    id=fields.UUIDField(pk=True)
    user_name=fields.CharField(50, unique=True)
    first_name=fields.CharField(50,)
    last_name=fields.CharField(50, )
    email=fields.CharField(50, )
    password=fields.CharField(50, )




