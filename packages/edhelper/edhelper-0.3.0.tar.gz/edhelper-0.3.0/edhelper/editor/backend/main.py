from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from edhelper.editor.backend.app.routers.deck import router as deck_router
from edhelper.editor.backend.app.routers.card import router as card_router
from edhelper.editor.backend.app.routers.commander import router as commander_router
from edhelper.infra.config import settings
import os

app = FastAPI(
    title="MTG Commanders App",
    version="0.1.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:3839",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(card_router)
app.include_router(deck_router)
app.include_router(commander_router)

# Mount static files only if dist/ exists
frontend_dist_path = os.path.join(settings.BASE_PATH, "editor", "frontend", "dist")
if os.path.exists(frontend_dist_path) and os.path.isdir(frontend_dist_path):
    app.mount(
        "/",
        StaticFiles(directory=frontend_dist_path, html=True),
        name="Deck Editor",
    )
else:
    # If dist/ doesn't exist, provide a message
    @app.get("/")
    def frontend_missing():
        return {
            "error": "Frontend not built",
            "message": "Please build the frontend first.",
        }
