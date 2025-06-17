from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from chatbot_logic import get_factual_answer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Basic context (can be extended or dynamic later)
CONTEXT = """
The current President of India is Droupadi Murmu. India is a country in South Asia.
The capital of India is New Delhi. The currency is Indian Rupee. Prime Minister is Narendra Modi.
The Taj Mahal is located in Agra. The national animal of India is the Bengal tiger.
"""

# SQLite setup
conn = sqlite3.connect("chat_logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_response TEXT
    )
""")
conn.commit()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    form = await request.form()
    user_msg = form["message"]
    try:
        bot_reply = get_factual_answer(user_msg, CONTEXT)
    except Exception as e:
        bot_reply = "Sorry, I couldn't find an answer."

    cursor.execute("INSERT INTO chat_logs (user_message, bot_response) VALUES (?, ?)", (user_msg, bot_reply))
    conn.commit()

    return JSONResponse({"reply": bot_reply})
