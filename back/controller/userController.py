import json
from dotenv import dotenv_values
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.database import get_next_user_id
from model.user import User
from request.UserRequest import UserRequest
from utils.registrationManagement import hash_password, verify_password

from database.database import insertUser, getUserByEmail

from utils.jwtConfig import create_access_token, get_current_user, verify_access_token

config = dotenv_values(".env")

TOKEN_EXPIRE_MINUTES = int(config["TOKEN_EXPIRE_MINUTES"])


app = FastAPI()

origins= [
   "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
   return JSONResponse(
      status_code=exc.status_code,
      content={
         "status": exc.status_code,
         "message": getattr(exc, "detail", "HTTP error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(FileNotFoundError)
async def file_not_found_exception_handler(request: Request, exc: FileNotFoundError):
   return JSONResponse(
      status_code=404,
      content={
         "status": 404,
         "message": getattr(exc, "detail", "File not found"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "JSON decode error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(PermissionError)
async def permission_exception_handler(request: Request, exc: PermissionError):
   return JSONResponse(
      status_code=403,
      content={
         "status": 403,
         "message": getattr(exc, "detail", "Permission denied"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(TypeError)
async def type_error_handler(request: Request, exc: TypeError):
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "Type error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "Value error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": getattr(exc, "detail", "Internal server error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )



@app.post("/register")
async def registerUser(user_request: UserRequest):
    if getUserByEmail(user_request.email) is not None:
        return JSONResponse(status_code=400, content={
            "status": 400,
            "message": "Invalid request",
            "details": "Email already registered. You must log in instead."
         })
    
    hashed_password = hash_password(user_request.password)
    user_to_create = User(
        id = get_next_user_id(),
        email = user_request.email,
        hashed_password = hashed_password,
    )

    inserted_user_id = insertUser(user_to_create)
    if inserted_user_id is None:
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": "Internal server error",
            "details": "Failed to create user"
         })
    return JSONResponse(status_code=201, content={ "status": 201, "message": "User created successfully", "data": {"id": inserted_user_id, "email": user_to_create.email} })


@app.post("/login")
async def loginUser(user_request: UserRequest):
   user = User(**dict(getUserByEmail(user_request.email)))
   if user is None:
      return JSONResponse(status_code=404, content={
            "status": 404,
            "message": "User not found",
            "details": "You must create an account first."
         })
   
   if verify_password(user_request.password, user.hashed_password) == False:
      return JSONResponse(status_code=401, content={ "status": 401, "message": "Login failed", "details": "Wrong password" })

   token = create_access_token(user.email)
   response = JSONResponse(status_code=200, content={ "status": 200, "message": "Login successful", "data": {"email": user.email, "access_token": token} })
   response.set_cookie(
      key = "access_token",
      value = token,
      httponly = True,
      secure = False,
      samesite = "lax",
      max_age = TOKEN_EXPIRE_MINUTES * 60000
   )
   return response

@app.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return JSONResponse(status_code=200, content={ "status": 200, "message": "Protected route accessed successfully", "data": {"email": current_user.email} })