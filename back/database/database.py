from tinydb import TinyDB, Query
from user import User
from pydantic import EmailStr


db = TinyDB("database.json")
users = db.table("users")
messages = db.table("messages")
query = Query()

# Requêtes SQL pour la table users
def get_next_user_id():
    all_users = getUsers()
    if not all_users:
        return 1
    return max(user["id"] for user in all_users) + 1

def getUsers():
    return users.all()

def getUserById(id: int):
    return users.get(query.id == id)

def getUserByEmail(email: EmailStr):
    return users.get(query.email == email)

def insertUser(user: User):
    existingUser = getUserByEmail(user.email)
    if existingUser is not None:
        return existingUser
    return users.insert(user)

def deleteUserByid(id: int):
    return users.remove(query.id == id)

def deleteUserByEmail(email: EmailStr):
    return users.remove(query.email == email)

# Requêtes SQL pour la table messages
def get_next_message_id():
    all_messages = getMessages()
    if not all_messages:
        return 1
    return max(message["id"] for message in all_messages) + 1

def getMessages():
    return messages.all()