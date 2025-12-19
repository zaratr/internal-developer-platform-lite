from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from platform.api.routers import services

app = FastAPI(title="IDP-Lite Control Plane")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router, prefix="/api/v1/services", tags=["services"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
