from tinydb import TinyDB, Query
from model.user import User
from pydantic import EmailStr


db = TinyDB("message.json")
users = db.table("users")
query = Query()

def getUsers():
    return users.all()

def getUserById(id: int):
    return users.get(query.id == id)

def getUserByEmail(email: EmailStr):
    return users.get(query.email == email)

def insertUser(user: User):
    return users.insert(user)

def deleteUserByid(id: int):
    return users.remove(query.id == id)

def deleteUserByEmail(email: EmailStr):
    return users.remove(query.email == email)