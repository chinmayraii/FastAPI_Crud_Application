from fastapi.templating import Jinja2Templates
from http.client import HTTPResponse, HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.middleware.sessions import SessionMiddleware
from fastapi import APIRouter, Request, Form,status,Depends
from .models import User
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
import typing
from configs import appinfo
from functools import lru_cache




router=APIRouter()
SECRET = 'your-secret-key'
manager = LoginManager(SECRET, token_url='/auth/token')
templates = Jinja2Templates(directory="user/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []

templates= Jinja2Templates(directory="user/templates")
templates.env.globals['get_flashed_messages'] = get_flashed_messages    




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get("/", response_class=HTMLResponse )
async def read_item(request:Request):
    return templates.TemplateResponse("uregs.html",{
        "request":request,
    })

@router.post('/add_registration/',)
async def create_user(request: Request,name: str = Form(...),
                      email: str = Form(...),
                      password: str = Form(...)):
        
    if "_messages" in request.session:
        print(request.session["_messages"][0]['username']) 
        email = request.session["_messages"][0]['username']
        flash(request, "Registered Successful", "success")
        return templates.TemplateResponse("ulogin.html", {"request": request})
        
    else:
        user_obj = await User.create(name=name,email=email,password= get_password_hash(password))
        flash(request, "Registered Successful", "success")
        return templates.TemplateResponse("ulogin.html", {"request": request})


@router.get("/ulogin/", response_class=HTMLResponse )
async def read_item(request:Request):
    return templates.TemplateResponse("ulogin.html",{
        "request":request,
    })     


@manager.user_loader()
async def load_user(email:str):
    if await User.exists(email=email):
        newapi=await User.get(email=email)
        return newapi

@router.post('/ulogin/')
async def login(request:Request,email: str = Form(...)
                , password: str = Form(...)):

    email = email
   
    user = await load_user(email)
    
    if not User:
        flash(request, "Invalid Username", "danger")
        return templates.TemplateResponse("ulogin.html",{'request':request})
    elif not verify_password(password,user.password):
        flash(request, "Password incorect", "danger")
        return templates.TemplateResponse("ulogin.html",{'request':request})

    else:
        # request.session['id']=user.id
        request.session['name']=user.name  
        flash(request, "Login Successful", "success")
        return templates.TemplateResponse("webpage.html",{'request':request})
        

@router.get("/webpage/", response_class=HTMLResponse )
async def read_item(request:Request):
    return templates.TemplateResponse("webpage.html",{
        "request":request,
    })        