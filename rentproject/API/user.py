from fastapi import APIRouter, Form
import hashlib
import json
from pymongo import MongoClient
import os
from typing import Annotated
from rentproject.primitives.user import User

router = APIRouter()

client = MongoClient(os.environ["RentProjectMongo"])
db = client["main"]
users = db["Users"]


@router.post("/create_user")
def create_user(user_data: Annotated[User, Form()]):
    hashword = hashlib.sha256()
    hashword.update(user_data.password.encode())
    user_data.password = hashword
    users.insert_one(json.loads(user_data.json()))

@router.post("/update_user")
def update_user(user_id: str, user_password: str, user_data: User):
    hashword = hashlib.sha256()
    hashword.update(user_password.encode())
    user = {"user_id": hashword.hexdigest()}
    users.update_one(user, {
        "user_id": user_id,
        "user_password": hashword.hexdigest(),
        "user_data": json.loads(user_data.json())
    })

def get_user(user_id: str, user_password: str) -> User:
    hashword = hashlib.sha256()
    hashword.update(user_password.encode())
    user = users.find({"user_id": user_id})