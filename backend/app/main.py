"""FastAPI main application entry point"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import download, logs, parse, pipeline, run_full, settings

app = FastAPI(title="HomeStock API", version="1.0.0")

# CORS middleware to allow Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(download.router, prefix="/download", tags=["download"])
app.include_router(parse.router, prefix="/parse", tags=["parse"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])
app.include_router(run_full.router, prefix="/run-full", tags=["run-full"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5001)
