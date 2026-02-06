import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError, ProgrammingError, NoSuchColumnError, NoSuchTableError, DBAPIError


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

@app.exception_handler(RequestValidationError)
async def bad_request_exception_handler(request: Request, exc: RequestValidationError):
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": "Bad Request",
         "details": exc.errors()
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

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": "Database error",
         "details": str(exc)
      }
   )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": "Database integrity error",
         "details": str(exc)
      }
   )

@app.exception_handler(OperationalError)
async def operational_exception_handler(request: Request, exc: OperationalError):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": "Database operational error",
         "details": str(exc)
      }
   )

@app.exception_handler(ProgrammingError)
async def programming_exception_handler(request: Request, exc: ProgrammingError):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": "Database programming error",
         "details": str(exc)
      }
   )

@app.exception_handler(NoSuchColumnError)
async def no_such_column_exception_handler(request: Request, exc: NoSuchColumnError):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": "Database column not found",
         "details": str(exc)
      }
   )

@app.exception_handler(NoSuchTableError)
async def no_such_table_exception_handler(request: Request, exc: NoSuchTableError):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": "Database table not found",
         "details": str(exc)
      }
   )

@app.exception_handler(DBAPIError)
async def dbapi_exception_handler(request: Request, exc: DBAPIError):
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": "Database API error",
         "details": str(exc)
      }
   )