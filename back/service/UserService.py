from utils.jwtConfig import create_access_token
from response.UserResponse import UserResponse
from database.database import get_next_user_id
from model.user import User
from request.UserRequest import UserRequest
from utils.registrationManagement import hash_password, verify_password

from database.database import insertUser, getUserByEmail



class UserService:

    def __init__(self):
        pass

    async def registerUser(self, user_request: UserRequest):
        if getUserByEmail(user_request.email) is not None:      
            raise Exception("Email already registered. You must log in instead.")
            
        hashed_password = hash_password(user_request.password)
        user_to_create = User(
            id = get_next_user_id(),
            email = user_request.email,
            hashed_password = hashed_password,
        )

        inserted_user_id = insertUser(user_to_create)
        if inserted_user_id is None:
            raise Exception("Failed to create user")
        return UserResponse(id=inserted_user_id, email=user_request.email)


    async def loginUser(self, user_request: UserRequest):
        dbUser = getUserByEmail(user_request.email)
        if dbUser is None:
            raise Exception("User not found. You must create an account first.")
        if verify_password(user_request.password, dbUser["hashed_password"]) == False:
            raise Exception("Login failed. Wrong password.")

        return UserResponse(id=dbUser["id"], email=dbUser["email"])