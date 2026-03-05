from typing import Annotated
from fastapi import APIRouter, Depends
from service.HistoryService import HistoryService
from request.NewMessageRequest import NewMessageRequest
from utils.jwtConfig import get_current_user
from model.user import User


def get_history_service() -> HistoryService:
    """Get a HistoryService instance"""
    return HistoryService()


HistoryServiceDep = Annotated[HistoryService, Depends(get_history_service)]

history_router = APIRouter(prefix="/history", tags=["history"])

@history_router.get("")
async def getHistoryByUserIdRoute(history_service: HistoryServiceDep, current_user: User = Depends(get_current_user)):
    return await history_service.getHistoryByUserIdRoute(current_user)


@history_router.get("/{history_id}")
async def getHistoryByIdRoute(history_id: int, history_service: HistoryServiceDep, current_user: User = Depends(get_current_user)):
    return await history_service.getHistoryByIdRoute(history_id, current_user)


@history_router.post("", status_code=201)
async def createHistoryRoute(history_service: HistoryServiceDep, current_user: User = Depends(get_current_user)):
    return await history_service.createHistoryRoute(current_user)


@history_router.post("/{history_id}/message")
async def addMessageToHistoryRoute(history_id: int, newMessageRequest: NewMessageRequest, history_service: HistoryServiceDep, current_user: User = Depends(get_current_user)):
    return await history_service.addMessageToHistoryRoute(history_id, newMessageRequest, current_user)


@history_router.delete("/{history_id}")
async def deleteHistoryRoute(history_id: int, history_service: HistoryServiceDep, current_user: User = Depends(get_current_user)):
    return await history_service.deleteHistoryRoute(history_id, current_user)