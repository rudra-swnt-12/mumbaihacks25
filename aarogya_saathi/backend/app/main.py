from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers.websocket import router as browser_router
from app.routers.portal import router as portal_router
from app.routers.call_socket import router as phone_router
from app.core.scheduler import start_scheduler
from app.core.exceptions import AarogyaException
from app.routers.community import router as community_router
from app.routers.analytics import router as analytics_router
from app.routers.patient_actions import router as patient_actions_router

app = FastAPI(
    title="Aarogya Saathi Backend",
    description="Autonomous AI Health System for MumbaiHacks 2025",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(phone_router)
app.include_router(browser_router)
app.include_router(portal_router)
app.include_router(community_router)
app.include_router(analytics_router)
app.include_router(patient_actions_router)


@app.exception_handler(AarogyaException)
async def aarogya_exception_handler(request, exc: AarogyaException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "error",
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.on_event("startup")
async def startup_event():
    print("Server Starting...")
    # start_scheduler()


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Aarogya Saathi Agentic Swarm is Running 🚀",
        "docs": "/docs",
    }
