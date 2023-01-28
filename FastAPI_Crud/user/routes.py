from fastapi.templating import Jinja2Templates
from http.client import HTTPResponse, HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi import APIRouter, Request, Form,status,Depends
# from .models import Category, SubCategory,Product,Admin
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,UploadFile,File
from user.pydantic_models import *
import os
from slugify import slugify
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
import json
import jwt
from passlib.context import CryptContext

from configs import appinfo
from functools import lru_cache

router=APIRouter()


templates= Jinja2Templates(directory="user/templates")

@router.get("/", response_class=HTMLResponse )
async def read_item(request:Request):
    return templates.TemplateResponse("uregs.html",{
        "request":request,
    })

@router.get("/ulogin/", response_class=HTMLResponse )
async def read_item(request:Request):
    return templates.TemplateResponse("ulogin.html",{
        "request":request,
    })

@router.get("/webpage/", response_class=HTMLResponse )
async def read_item(request:Request):
    return templates.TemplateResponse("webpage.html",{
        "request":request,
    })        