from datetime import datetime
from fastapi import Depends
from request.NewMessageRequest import NewMessageRequest
from utils.AIModelresponse import get_ai_response_distant, get_max_id
from database.database import deleteById, getHistoryById, insertHistory, getHistoryByUserId, get_next_history_id, addMessageToHistory, cleanDatabase
from utils.jwtConfig import get_current_user
from model.history import History
from model.user import User
from controller.ControllerConfig import app
from fastapi.responses import JSONResponse
from utils.jwtConfig import get_current_user
from model.message import Message


@app.get("/history")
async def getHistoryByUserIdRoute(current_user: User = Depends(get_current_user)):
    cleanDatabase()
    history_items = getHistoryByUserId(current_user.id)
    if history_items is None:
        return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "History not found for user",
            "details": f"No history items found for user with id {current_user.id}"
        })
    
    # On retourne seulement les champs name et id de chaque history_item dont le tableau messages n'est pas vide et dont le champ name n'est pas vide ou composé uniquement d'espaces
    not_empty = [item for item in history_items if len(item["messages"]) != 0 and item["name"].strip() != ""]
    id_names = [{"id": item["id"], "name": item["name"]} for item in not_empty]
    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "History retrieved successfully",
        "data": id_names
    })

@app.get("/history/{history_id}")
async def getHistoryByIdRoute(history_id: int, current_user: User = Depends(get_current_user)):
    history_item = getHistoryById(history_id)
    if history_item is None:
        return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "History item not found",
            "details": f"No history item found with id {history_id}"
        })

    if history_item["user_id"] != current_user.id:
        return JSONResponse(status_code=403, content={
            "status": 403,
            "message": "Forbidden",
            "details": "You do not have permission to access this history item"
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "History item retrieved successfully",
        "data": history_item
    })

@app.post("/history")
async def createHistoryRoute(current_user: User = Depends(get_current_user)):
    next_id = get_next_history_id()
    history_item = History(
        id = next_id,
        user_id = current_user.id,
        name = f"Conversation {next_id}",
        messages = []
    )
    inserted_history_id = insertHistory(history_item)
    if inserted_history_id is None:
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": "Internal server error",
            "details": "Failed to create history item"
        })

    return JSONResponse(status_code=201, content={
        "status": 201,
        "message": "History item created successfully",
        "data": {"id": inserted_history_id}
    })

@app.post("/history/{history_id}/message")
async def addMessageToHistoryRoute(history_id: int, newMessageRequest: NewMessageRequest, current_user: User = Depends(get_current_user)):
    history_item = getHistoryById(history_id)

    if history_item is None:
        return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "History item not found",
            "details": f"No history item found with id {history_id}"
        })

    if history_item["user_id"] != current_user.id:
        return JSONResponse(status_code=403, content={
            "status": 403,
            "message": "Forbidden",
            "details": "You do not have permission to modify this history item"
        })

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
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": "Internal server error",
            "details": "Failed to retrieve updated history"
        })

    # Obtenir la réponse de l'IA
    aiResponse = get_ai_response_distant(updated_history["messages"])
    
    # Ajouter la réponse de l'IA
    addMessageToHistory(history_id, aiResponse)
    
    # Récupérer l'historique final
    final_history = getHistoryById(history_id)

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Message added to history item successfully",
        "data": final_history
    })

@app.delete("/history/{history_id}")
async def deleteHistoryRoute(history_id: int, current_user: User = Depends(get_current_user)):
    history_item = getHistoryById(history_id)

    if history_item is None:
        return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "History item not found",
            "details": f"No history item found with id {history_id}"
        })

    if history_item["user_id"] != current_user.id:
        return JSONResponse(status_code=403, content={
            "status": 403,
            "message": "Forbidden",
            "details": "You do not have permission to delete this history item"
        })

    deleteById(history_id)
    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "History item deleted successfully",
        "details": f"History item with id {history_id} has been deleted"
    })