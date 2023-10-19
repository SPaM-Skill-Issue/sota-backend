from fastapi import FastAPI
from routers import sports_router, sport_router, medals_router, medal_router, audient_router, apikeygen_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from decouple import config, Csv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config("ALLOWED_ORIGINS", cast=Csv()),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

authentication = FastAPI()
authentication.add_middleware(
    CORSMiddleware,
    allow_origins=config("ALLOWED_AUTH_ORIGINS", cast=Csv()),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
authentication.add_middleware(
    
)

app.mount("/apigenkey", authentication)

app.include_router(sports_router.router)
app.include_router(sport_router.router)
app.include_router(medals_router.router)
app.include_router(medal_router.router)
app.include_router(audient_router.router)

# to be separated into another CORS configuration
app.include_router(apikeygen_router.router)


@app.get("/")
def root():
    return {"msg": "welcome to root page"}
