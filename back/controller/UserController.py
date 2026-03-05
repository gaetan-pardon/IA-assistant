from typing import Annotated
from dotenv import dotenv_values
from fastapi import APIRouter, Depends, Response

from response.UserResponse import UserResponse
from model.user import User
from request.UserRequest import UserRequest
from utils.jwtConfig import create_access_token, get_current_user
from service.UserService import UserService


def get_user_service() -> UserService:
    """Get a UserService instance with the database session"""
    return UserService()


user_router = APIRouter(prefix="/user", tags=["user"])
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

config = dotenv_values(".env")
TOKEN_EXPIRE_MINUTES = int(config["TOKEN_EXPIRE_MINUTES"])

@user_router.post("/register", response_model=UserResponse, status_code=201)
async def registerUser(user_request: UserRequest, user_service: UserServiceDep):
   return await user_service.registerUser(user_request)

@user_router.post("/login", response_model=UserResponse, status_code=200)
async def loginUser(response: Response, user_request: UserRequest, user_service: UserServiceDep):
   user = await user_service.loginUser(user_request)
   if user is None:
      raise Exception("Login failed. Invalid email or password.")

   token = create_access_token(user.email)
   response.set_cookie(
      key = "access_token",
      value = token,
      httponly = True,
      secure = False,
      samesite = "lax",
      max_age = TOKEN_EXPIRE_MINUTES * 60000
   )
   return user

@user_router.post("/logout", status_code=204)
async def logoutUser(response: Response):
   response.delete_cookie(key="access_token")
   return { "message": "Logged out successfully" }

@user_router.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
   return current_user.email