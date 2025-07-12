import os
import re
import webbrowser
import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
import pyjokes
import wikipedia
import requests
import openai
import random

from assistant import EvaTerminalAssistant

# ─── Load environment variables ─────────────────────
load_dotenv()
OPENAI_KEY      = os.getenv("OPENAI_API_KEY")
WEATHER_KEY     = os.getenv("OPENWEATHER_KEY")
NEWSAPI_KEY     = os.getenv("NEWSAPI_KEY")
BING_API_KEY    = os.getenv("BING_API_KEY")
BING_ENDPOINT   = os.getenv("BING_ENDPOINT")

openai.api_key = OPENAI_KEY

# ─── Flask & Scheduler Configuration ───────────────
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
app.config.from_object(Config)
CORS(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# ─── Adapter to buffer Eva’s responses ──────────────
class EvaWebAdapter(EvaTerminalAssistant):
    def __init__(self):
        super().__init__()
        self.responses = []

    def speak(self, text: str):
        # Buffer instead of printing/TTS
        self.responses.append(text)

    def pop_responses(self):
        out, self.responses = self.responses, []
        return out

eva = EvaWebAdapter()


# ─── Reminder Scheduler ────────────────────────────
def schedule_reminder(task: str, delay: int):
    job_id = f"reminder_{datetime.datetime.now().timestamp()}"

    def send_reminder():
        message = f"⏰ Reminder: {task}"
        eva.chat_history.append({"eva": message})
        print(f"[Reminder Fired] {message}")

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=delay)
    scheduler.add_job(
        id=job_id,
        func=send_reminder,
        trigger='date',
        run_date=run_date
    )


# ─── Routes ────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(force=True)
    msg  = data.get("message", "").strip()

    # Log user message
    eva.chat_history.append({"user": msg})

    # Natural-language reminder?
    if "remind me to" in msg and " in " in msg:
        match = re.search(
            r"remind me to (.+?) in (\d+)\s*(seconds?|minutes?|hours?)",
            msg
        )
        if match:
            task   = match.group(1).strip()
            amount = int(match.group(2))
            unit   = match.group(3).lower()
            multiplier = {
                "second": 1, "seconds": 1,
                "minute": 60, "minutes": 60,
                "hour": 3600, "hours": 3600
            }
            delay = amount * multiplier.get(unit, 0)
            schedule_reminder(task, delay)
            eva.responses.append(f"Reminder set: {task} in {amount} {unit}")
        else:
            eva.responses.append("❌ I couldn't understand that reminder format.")
    else:
        # Delegate to Eva’s logic
        eva.process_command(msg)

    # Return all buffered replies
    replies = eva.pop_responses()
    return jsonify(replies)


@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(eva.chat_history)


# ─── Run the App ───────────────────────────────────
if __name__ == "__main__":
    # Open browser once, not on reload
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://localhost:5000")

    app.run(debug=True)
