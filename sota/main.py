from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .routers import (
    sports_router,
    sport_router,
    medals_router,
    medal_router,
    audient_router,
    apikeygen_router,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from decouple import config, Csv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config("ALLOWED_ORIGINS", cast=Csv()),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_origins = config("ALLOWED_AUTH_ORIGINS", cast=Csv())
authentication = FastAPI()
authentication.add_middleware(
    CORSMiddleware,
    allow_origins=auth_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
authentication.add_middleware(TrustedHostMiddleware, allowed_hosts=auth_origins)

app.mount("/apikeygen", authentication)

app.include_router(sports_router.router)
app.include_router(sport_router.router)
app.include_router(medals_router.router)
app.include_router(medal_router.router)
app.include_router(audient_router.router)

# to be separated into another CORS configuration
authentication.include_router(apikeygen_router.router)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/")
def root():
    return {"msg": "welcome to root page"}
