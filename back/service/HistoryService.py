from datetime import datetime
from fastapi import HTTPException
from request.NewMessageRequest import NewMessageRequest
from utils.AIModelresponse import get_ai_response_distant, get_max_id
from database.database import deleteById, getHistoryById, insertHistory, getHistoryByUserId, get_next_history_id, addMessageToHistory, cleanDatabase
from model.history import History
from model.user import User
from model.message import Message

class HistoryService:
    def __init__(self):
        pass



    async def getHistoryByUserIdRoute(self, current_user: User):
        cleanDatabase()
        history_items = getHistoryByUserId(current_user.id)
        if history_items is None:
            raise HTTPException(status_code=404, detail=f"No history items found for user with id {current_user.id}")
        
        # On retourne seulement les champs name et id de chaque history_item dont le tableau messages n'est pas vide et dont le champ name n'est pas vide ou composé uniquement d'espaces
        not_empty = [item for item in history_items if len(item["messages"]) != 0 and item["name"].strip() != ""]
        id_names = [{"id": item["id"], "name": item["name"]} for item in not_empty]
        return id_names


    async def getHistoryByIdRoute(self, history_id: int, current_user: User):
        history_item = getHistoryById(history_id)
        if history_item is None:
            raise HTTPException(status_code=404, detail=f"No history item found with id {history_id}")

        if history_item["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to access this history item")

        return history_item


    async def createHistoryRoute(self, current_user: User):
        next_id = get_next_history_id()
        history_item = History(
            id = next_id,
            user_id = current_user.id,
            name = f"Conversation {next_id}",
            messages = []
        )
        inserted_history_id = insertHistory(history_item)
        if inserted_history_id is None:
            raise HTTPException(status_code=500, detail="Failed to create history item")

        return history_item


    async def addMessageToHistoryRoute(self, history_id: int, newMessageRequest: NewMessageRequest, current_user: User):
        history_item = getHistoryById(history_id)

        if history_item is None:
            raise HTTPException(status_code=404, detail=f"No history item found with id {history_id}")

        if history_item["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to modify this history item")

        # Calculer le prochain ID de message
        messages = history_item.get("messages", [])
        if len(messages) == 0:
            next_message_id = 1
        else:
            next_message_id = get_max_id(messages) + 1

        message_to_insert = Message(
            id = next_message_id,
            role = "user",
            content = newMessageRequest.message,
            timestamp = datetime.now().isoformat()
        )

        # Ajouter le message de l'utilisateur
        addMessageToHistory(history_id, message_to_insert)
        
        # Récupérer l'historique mis à jour pour obtenir la réponse IA
        updated_history = getHistoryById(history_id)
        if updated_history is None:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve updated history item with id {history_id} after adding user message")
        
        # Obtenir la réponse de l'IA
        aiResponse = get_ai_response_distant(updated_history["messages"])
        
        # Ajouter la réponse de l'IA
        addMessageToHistory(history_id, aiResponse)
        
        # Récupérer l'historique final
        final_history = getHistoryById(history_id)

        return final_history


    async def deleteHistoryRoute(self, history_id: int, current_user: User):
        history_item = getHistoryById(history_id)

        if history_item is None:
            raise HTTPException(status_code=404, detail=f"No history item found with id {history_id}")

        if history_item["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this history item")

        return deleteById(history_id)