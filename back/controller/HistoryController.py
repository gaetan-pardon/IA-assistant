from datetime import datetime
from pyexpat.errors import messages
from fastapi import Depends
from utils.AIModelresponse import get_ai_response_distant, get_max_id
from database.database import getHistoryById, insertHistory, getHistoryByUserId
from model.history import History
from model.user import User
from controller.ControllerConfig import app
from fastapi.responses import JSONResponse
from utils.jwtConfig import get_current_user
from model.message import Message


@app.get("/history")
async def getHistoryByUserIdRoute(current_user: User = Depends(get_current_user)):
    history_items = getHistoryByUserId(current_user.id)
    if history_items is None:
        return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "History not found for user",
            "details": f"No history items found for user with id {current_user.id}"
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "History retrieved successfully",
        "data": history_items
    })

@app.post("/history")
async def createHistory(history_item: History, current_user: User = Depends(get_current_user)):
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
async def addMessageToHistory(history_id: int, message: str, current_user: User = Depends(get_current_user)):
    history_item = getHistoryById(history_id)
    if history_item is None:
        return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "History item not found",
            "details": f"No history item found with id {history_id}"
        })

    if history_item.user_id != current_user.id:
        return JSONResponse(status_code=403, content={
            "status": 403,
            "message": "Forbidden",
            "details": "You do not have permission to modify this history item"
        })

    message_to_insert = Message(
        id = get_max_id() + 1,
        role = "user",
        content = message,
        timestamp = datetime.now().isoformat()
    )

    updated_history_item = addMessageToHistory(history_id, message_to_insert)
    aiResponse = get_ai_response_distant(updated_history_item["messages"])
    updated_history_item = addMessageToHistory(history_id, aiResponse)

    if updated_history_item is None:
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": "Internal server error",
            "details": "Failed to add message to history item"
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Message added to history item successfully",
        "data": updated_history_item
    })