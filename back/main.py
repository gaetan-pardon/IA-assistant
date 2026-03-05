from email.policy import default
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi


from controller.UserController import user_router
from controller.HistoryController import history_router

app = FastAPI()

origins= [
   "http://localhost:5173",
   "http://localhost:5173/"
]

# En-têtes CORS à inclure dans toutes les réponses
cors_headers = {
   "Access-Control-Allow-Origin": "http://localhost:5173",
   "Access-Control-Allow-Credentials": "true",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(history_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
   return JSONResponse(
      status_code=exc.status_code,
      content={
         "status": exc.status_code,
         "message": getattr(exc, "detail", "HTTP error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      },
      headers=cors_headers
   )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
   return JSONResponse(
      status_code=422,
      content={
         "status": 422,
         "message": "Validation error",
         "details": exc.errors()
      },
      headers=cors_headers
   )

@app.exception_handler(FileNotFoundError)
async def file_not_found_exception_handler(request: Request, exc: FileNotFoundError):
   return JSONResponse(
      status_code=404,
      content={
         "status": 404,
         "message": getattr(exc, "detail", "File not found"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      },
      headers=cors_headers
   )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "JSON decode error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      },
      headers=cors_headers
   )


@app.exception_handler(PermissionError)
async def permission_exception_handler(request: Request, exc: PermissionError):
   return JSONResponse(
      status_code=403,
      content={
         "status": 403,
         "message": getattr(exc, "detail", "Permission denied"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      },
      headers=cors_headers
   )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
   """Gère toutes les autres exceptions non capturées"""
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": str(exc),
         "details": None
      },
      headers=cors_headers
   )

# Configuration de la documentation OpenAPI pour inclure l'authentification par cookie (Swagger)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {})["CookieAuth"] = {
        "type": "apiKey",
        "in": "cookie",
        "name": "access_token",
    }
    for path in schema.get("paths", {}).values():
        for operation in path.values():
            operation.setdefault("security", [{"CookieAuth": []}])
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
