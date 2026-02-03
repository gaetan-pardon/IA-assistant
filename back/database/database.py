from tinydb import TinyDB, Query
from model.user import User
from model.history import History, Message
from pydantic import EmailStr


db = TinyDB("database/database.json")
users = db.table("users")
history = db.table("history")
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
    return users.insert(user.dict())

def deleteUserByid(id: int):
    return users.remove(query.id == id)

def deleteUserByEmail(email: EmailStr):
    return users.remove(query.email == email)


# Requêtes SQL pour la table history

def get_next_history_id():
    all_history = getHistory()
    if not all_history:
        return 1
    return max(history["id"] for history in all_history) + 1

def getHistory():
    return history.all()

def getHistoryById(id: int):
    return history.get(query.id == id)

def insertHistory(history_item: History):
    return history.insert(history_item.dict())

def deleteById(id: int):
    return history.remove(query.id == id)

def addMessageToHistory(history_id: int, message: Message):
    history_item = getHistoryById(history_id)
    if history_item is None:
        return None
    messages = history_item.get("messages", [])
    messages.append(message.dict())
    history.update({"messages": messages}, query.id == history_id)
    return history_item