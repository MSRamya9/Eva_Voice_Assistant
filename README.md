# 🤖 Eva – Your Voice Assistant

Eva is a smart, voice-enabled assistant built with Python and Flask. She can chat, tell jokes, fetch weather updates, answer questions using GPT, and even remind you to drink water — all through a sleek web interface or terminal mode.

<p align="center">
  <img src="https://your-demo-gif-or-image-link.gif" alt="Eva Voice Assistant Demo" width="600"/>
</p>

---

## ✨ Features

- 🎤 Voice and text input support
- 💬 GPT-powered conversational responses
- 🌦️ Real-time weather updates via OpenWeatherMap API
- 📰 News headlines via NewsAPI
- 😂 Jokes with PyJokes
- 📚 Wikipedia summaries
- ⏰ Smart reminders (e.g., “Remind me to stretch in 10 minutes”)
- 🕹️ Number guessing game
- 🧠 Web and terminal modes
- 🗣️ Text-to-speech using Web Speech API (browser) or pyttsx3 (terminal)

---

## 🛠️ Tech Stack

| Layer         | Tools Used                                      |
|---------------|--------------------------------------------------|
| Backend       | Python, Flask, APScheduler, OpenAI API          |
| Frontend      | HTML, CSS, JavaScript, Web Speech API           |
| Voice Engine  | pyttsx3 (terminal), SpeechSynthesis (browser)   |
| APIs          | OpenWeatherMap, NewsAPI, Wikipedia, OpenAI      |

---

## 📁 Project Structure

```plaintext
Eva_Voice_Assistant/
├── assistant.py         # Core assistant logic
├── server.py            # Flask web server and API endpoints
├── main.py              # Entry point (web or terminal)
├── templates/           # HTML templates (index.html, etc.)
├── static/              # CSS, JavaScript, and assets
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed)
└── README.md


