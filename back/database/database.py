from datetime import datetime
from tinydb import TinyDB, Query


db = TinyDB("database/database.json", indent=4)
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

def getUserByEmail(email: str):
    return users.get(query.email == email)

def insertUser(user: dict):
    existingUser = getUserByEmail(user.email)
    if existingUser is not None:
        return existingUser
    return users.insert(user.dict())

def deleteUserByid(id: int):
    return users.remove(query.id == id)

def deleteUserByEmail(email: str):
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

def getHistoryByUserId(user_id: int):
    return history.search(query.user_id == user_id)

def insertHistory(history_item: dict):
    return history.insert(history_item.dict())

def addMessageToHistory(history_id: int, message: dict):
    print('BDD: Adding message to history with id:', history_id)
    print('Message to add:', message)
    history_item = getHistoryById(history_id)
    print('Current history item before adding message:', history_item)
    if history_item is None:
        return None
    messages = history_item.get("messages", [])
    print('Current messages in history item:', messages)
    # Convertir le message en dictionnaire s'il est un objet Pydantic
    message_dict = message.dict() if hasattr(message, 'dict') else message
    # S'assurer que le timestamp est sérialisable en JSON
    if isinstance(message_dict.get("timestamp"), datetime):
        message_dict["timestamp"] = message_dict["timestamp"].isoformat()
    messages.append(message_dict)
    print('Messages in history item after adding new message:', messages)
    history.update({"messages": messages}, query.id == history_id)
    print('History item after update:', getHistoryById(history_id))
    return history_item

def deleteById(id: int):
    return history.remove(query.id == id)
