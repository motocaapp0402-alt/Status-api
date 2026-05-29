from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json, os

app = FastAPI(title="Meu Status API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"]
)

STATUS_FILE = "status.json"

def get_status():
    if not os.path.exists(STATUS_FILE):
        return {"status": "offline", "emoji": "💤", "ultima_atualizacao": None}
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

@app.get("/")
def root():
    return {"msg": "API de Status online. Use /status"}

@app.get("/status")
def ler_status():
    return get_status()

@app.post("/status/{novo_status}")
def atualizar_status(novo_status: str):
    emojis = {
        "trabalhando": "💻",
        "livre": "🎮",
        "dormindo": "😴",
        "estudando": "📚",
        "offline": "💤"
    }
    status_data = {
        "status": novo_status,
        "emoji": emojis.get(novo_status, "❓"),
        "ultima_atualizacao": datetime.now().strftime("%d/%m %H:%M")
    }
    save_status(status_data)
    return status_data
