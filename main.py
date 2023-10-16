from fastapi import FastAPI
from routers import sports_router, sport_router, medals_router, medal_router, audient_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sports_router.router)
app.include_router(sport_router.router)
app.include_router(medals_router.router)
app.include_router(medal_router.router)
app.include_router(audient_router.router)


@app.get("/")
def root():
    return {"msg": "welcome to root page"}
