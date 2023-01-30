import uuid
from fastapi import FastAPI
from tortoise.models import Model
from tortoise import Tortoise,fields



class User(Model):
    id=fields.UUIDField(pk=True)
    name=fields.CharField(20, unique=True)
    email=fields.CharField(30 )
    password=fields.CharField(500 )




