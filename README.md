# 🤖 Eva – Your Voice Assistant

Eva is a smart, voice-enabled assistant built with Python and Flask. She can chat, tell jokes, fetch weather updates, answer questions using GPT, and even remind you to drink water — all through a sleek web interface or terminal mode.

<p align="center">
  <img src="https://github.com/MSRamya9/Eva_Voice_Assistant/edit/main/README.md" alt="Eva Voice Assistant Demo" width="600"/>
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

<pre>
Eva_Voice_Assistant/
├── assistant.py         # Core assistant logic
├── server.py            # Flask web server and API endpoints
├── main.py              # Entry point (web or terminal)
├── templates/           # HTML templates (index.html, etc.)
├── static/              # CSS, JavaScript, and assets
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed)
└── README.md
</pre>
---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Eva_Voice_Assistant.git
cd Eva_Voice_Assistant
```
###  2: Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Up Environment Variables
Create a .env file in the root directory
```bash
OPENAI_API_KEY=your_openai_key
OPENWEATHER_KEY=your_openweather_key
NEWSAPI_KEY=your_newsapi_key
```
---
## 🧪 Usage
### ▶️ Run in Terminal Mode
```bash
python server.py
```
Eva will respond via terminal and speak using pyttsx3.
### 🌐 Run in Web Mode
```bash
python main.py web
```
Then open http://localhost:5000 in your browser.

---
## 💬 Example Commands
- “Tell me a joke”

- “What’s the weather in New York?”

- “Who is Ada Lovelace?”

- “Remind me to drink water in 30 minutes”

- “Play a game”

- "Open To-do List" 

- “Thank you”

---

## 🔐 API Keys Required

| API             | Purpose                | Get Key From                                               |
|------------------|-------------------------|-------------------------------------------------------------|
| OpenAI API       | GPT-based responses     | [OpenAI API Keys](https://platform.openai.com/account/api-keys) |
| OpenWeatherMap   | Weather updates         | [OpenWeatherMap](https://openweathermap.org/api)           |
| NewsAPI          | News headlines          | [NewsAPI](https://newsapi.org)                             |


---
## 🤝 Contributing
Pull requests are welcome! If you have ideas for new features or improvements, feel free to fork the repo and submit a PR.

---
## 📜 License
This project is licensed under the MIT License.

---
## 🙌 Acknowledgments
- OpenAI

- OpenWeatherMap

- NewsAPI

- Wikipedia API

- pyttsx3

- Flask

---
## Built with 💡 and a lot of curiosity by Sai
