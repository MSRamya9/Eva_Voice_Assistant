import os, json, datetime, webbrowser
from flask      import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv     import load_dotenv
import pyjokes, wikipedia, requests, openai, random
from flask_apscheduler import APScheduler
import re


# ─── Load secrets ───────────────────────────────
load_dotenv()
OPENAI_KEY      = os.getenv("OPENAI_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
NEWSAPI_KEY     = os.getenv("NEWSAPI_KEY")
openai.api_key  = OPENAI_KEY


# ─── Flask Config & Scheduler Setup ─────────────
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__,
            static_folder="static",
            template_folder="templates")
app.config.from_object(Config)
CORS(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# ─── Flask app ───────────────────────────────────
# ─── 1) Import & adapt your real assistant ─────────────────
from assistant import EvaTerminalAssistant

class EvaWebAdapter(EvaTerminalAssistant):
    def __init__(self):
        super().__init__()
        self.responses = []
    
    def load_todos(self):
        # override base to avoid missing-method error
        self.todos = []

    def save_todos(self):
        # no-op
        pass

    def __init__(self):
        super().__init__()
        self.responses = []

    # override speak() so it buffers replies instead of printing/TTS
    def speak(self, text: str):
        self.responses.append(text)

    # after running process_command, call this to grab & clear the buffer
    def pop_responses(self):
        out, self.responses = self.responses, []
        return out

# instantiate one adapter
eva = EvaWebAdapter()

# ─── Reminder Scheduling Function ───────────────
def schedule_reminder(task, delay):
    job_id = f"reminder_{datetime.datetime.now().timestamp()}"

    def send_reminder():
        message = f"⏰ Reminder: {task}"
        eva.chat_history.append({"eva": message})
        print(f"[Reminder Fired] {message}")  


    run_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
    scheduler.add_job(id=job_id, func=send_reminder, trigger='date', run_date=run_time)

# ─── 2) Flask setup ───────────────────────────────────────
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__,
            static_folder="static",
            template_folder="templates")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ─── 3) Your real /api/chat endpoint ───────────────────────
@app.route("/api/chat", methods=["POST"])
def chat_api():
    data     = request.get_json(force=True)
    msg      = data.get("message","")
    # Detect natural reminder
    if "remind me to" in msg and "in" in msg:
        match = re.search(r"remind me to (.+?) in (\d+)\s*(seconds?|minutes?|hours?)", msg)
        if match:
            task = match.group(1).strip()
            amount = int(match.group(2))
            unit = match.group(3).lower()
            multiplier = {"second": 1, "seconds": 1, "minute": 60, "minutes": 60, "hour": 3600, "hours": 3600}
            delay = amount * multiplier.get(unit, 0)
            schedule_reminder(task, delay)
            eva.responses.append(f"Reminder set: {task} in {amount} {unit}")
        else:
            eva.responses.append("❌ I couldn't understand the reminder format.")
    else:
        eva.process_command(msg)          # run YOUR assistant logic
    replies  = eva.pop_responses()     # grab everything it spoke
    return jsonify(replies)           # send back a raw array

@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(eva.chat_history)

if __name__ == "__main__":
    # Only open the browser if this is the main process, not the reloader
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://localhost:5000")

    app.run(debug=True)


