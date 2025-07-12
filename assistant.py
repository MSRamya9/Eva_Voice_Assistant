import speech_recognition as sr
import pyttsx3
import pyjokes
import webbrowser
import json
import os
from typing import Optional
import wikipedia
import requests
import openai
import random 
import re
from typing import Optional
import pywhatkit
import datetime  # for datetime.datetime.now()
from datetime import datetime as dt, timedelta  # for dt.now() and timedelta
from utils import todo
import threading
import time
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")




class EvaTerminalAssistant:
    def __init__(self):
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Use female voice
        self.game_active   = False
        self.secret_number = None
        self.guess_count   = 0
        self.todo_mode = False
        self.responses = []
        self.number_words  = {
            "one":1,"two":2,"three":3,"four":4,"five":5,
            "six":6,"seven":7,"eight":8,"nine":9,"ten":10}
        self.chat_history = []
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

        
        # Command mappings
        self.commands = {
            'exit': self.handle_exit,
            'how are you': self.handle_how_are_you,
            'play': self.handle_play,
            'time': self.handle_time,
            'who is': self.handle_who_is,
            'joke': self.handle_joke,
            'weather': self.handle_weather,
            'play game':       self.handle_game,
            'guessing game':   self.handle_game,
            'play a game':     self.handle_game,
            'game':          self.handle_game,
            'reminder': self.handle_reminder,
            'set reminder': self.handle_reminder

        }

    def handle_greeting(self, _):
        greetings = [
            "Hi! I'm Eva – your personal voice assistant. How can I help you today?",
            "Hi there! How can I help you today?",
            "Hello! I'm here and ready to assist.",
            "Hey! Great to hear from you. What can I do for you?"
        ]
        
        self.speak(greetings[datetime.datetime.now().second % len(greetings)])
        return True


    def speak(self, text: str):
        """Convert text to speech"""
        print(f"Eva: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        self.responses.append(text)
        self.chat_history.append(("Eva", text))

    def listen(self) -> Optional[str]:
        """Listen to microphone input and return recognized text"""
        with sr.Microphone() as source:
            print("\nListening... (press Ctrl+C to stop)")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You: {command}")
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
                return None
            except sr.RequestError:
                self.speak("There was an issue with the speech service.")
                return None
            except KeyboardInterrupt:
                return "exit"
            except Exception as e:
                print(f"Error: {e}")
                return None
    

    def listen_game(self):
        """Listen for voice input"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
        
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return None
            except sr.RequestError:
                self.speak("Sorry, my speech service is down. Please type your guess.")
                return input("Type your guess: ").lower()
            except Exception as e:
                print(f"Error: {e}")
                return None
        
    def handle_game(self, command: str):
    # Start the game if not already active
        if not self.game_active:
            self.secret_number = random.randint(1, 10)
            self.guess_attempts = 0
            self.game_active = True
            self.speak("Welcome to the Voice Guessing Game!")
            self.speak("I'm thinking of a number between 1 and 10. Try to guess it!")
            return True

        # If game is active, treat input as a guess
        guess = self.extract_number(command)
        if guess is None:
            self.speak("Please enter a number between 1 and 10.")
            return True

        self.guess_attempts += 1

        if guess < self.secret_number:
            self.speak("Too low! Try again.")
        elif guess > self.secret_number:
            self.speak("Too high! Try again.")
        else:
            self.speak(f"Congratulations! You guessed the number in {self.guess_attempts} attempts!")
            self.game_active = False  # Reset game state

        return True
    
    def extract_number(self, text):
        # Try to extract a digit first
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())

        # Try to match a number word
        words = text.lower().split()
        for word in words:
            if word in self.number_words:
                return self.number_words[word]

        return None

    def handle_todo_list(self, command):
        command = command.lower()

        if ("to-do list" in command or 'todo list' in command) and not self.todo_mode:
            self.todo_mode = True
            self.speak("Entering To-Do List mode. You can say add task, view tasks, remove task, or exit to-do list.")
            return True

        if self.todo_mode:
            if "exit to-do list" in command or 'exit todo list' in command or 'exit to do list' in command:
                self.todo_mode = False
                self.speak("Exiting To-Do List mode.")

            elif "add" in command:
                task = command.replace("add", "").replace("task", "").strip()
                # Extract priority
                priority = "normal"
                if "high priority" in command:
                    priority = "high"
                elif "low priority" in command:
                    priority = "low"

                # Extract due date
                due_date = None
                if "due today" in command:
                    due_date = dt.now().strftime("%Y-%m-%d")
                    task = re.sub(r"due today( evening| morning| afternoon)?", "", task).strip()
                elif "due tomorrow" in command:
                    due_date = (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                    task = re.sub(r"due tomorrow( evening| morning| afternoon)?", "", task).strip()
                elif "due" in command:
                    match = re.search(r"due (\w+ \d+)", command)
                    if match:
                        try:
                            parsed = datetime.strptime(match.group(1), "%B %d")
                            due_date = parsed.replace(year=datetime.now().year).strftime("%Y-%m-%d")
                            task = task.replace(match.group(0), "").strip()
                        except:
                            pass

                self.speak(todo.add_task(task, priority, due_date))


            elif "view" in command or "show" in command:
                if "priority" in command:
                    tasks_text = todo.view_tasks(sort_by="priority")
                elif "due" in command or "date" in command:
                    tasks_text = todo.view_tasks(sort_by="due")
                else:
                    tasks_text = todo.view_tasks()

                for line in tasks_text.split("\n"):
                    self.speak(line)
            elif "due today" in command or "remind me" in command:
                tasks_text = todo.tasks_due_today()
                for line in tasks_text.split("\n"):
                    self.speak(line)


            elif "remove" in command or "delete" in command or "completed" in command:
                index = self.extract_number(command)
                if "all" in command:
                    self.speak(todo.clear_tasks())
                elif index:
                    self.speak(todo.remove_task(index))
                else:
                    index = self.extract_number(command)
                
                
                

            else:
                self.speak("In To-Do List mode, you can say add, view, remove, or exit to-do list.")

            return True

        return False

    def handle_exit(self, _):
        """Handle exit command"""
        self.speak("Goodbye! Have a great day!")
        return False  # Stop the main loop

    def handle_how_are_you(self, _):
        """Respond to how are you"""
        responses = [
            "I'm doing great, thank you for asking!",
            "I'm fantastic! Ready to help you with anything.",
            "Doing well! Just enjoying our conversation."
        ]
        self.speak(responses[datetime.datetime.now().second % len(responses)])
        return True

    def handle_play(self, command: str):
        """Handle play command"""
        song = command.replace('play', '').strip()
        if song:
            self.speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            self.speak("What would you like me to play?")
        return True

    def handle_time(self, _):
        """Tell current time"""
        time = datetime.datetime.now().strftime('%I:%M %p')
        self.speak(f"The current time is {time}")
        return True


    def handle_who_is(self, command: str):
        # Extract the person's name from various phrasings
        triggers = ['who is', 'tell me about', 'what do you know about']
        person = command
        for trigger in triggers:
            if trigger in command:
                person = command.replace(trigger, '').strip()
                break

        if person:
            try:
                summary = wikipedia.summary(person, sentences=2)
                self.speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                self.speak(f"There are multiple results for {person}. Can you be more specific?")
            except wikipedia.exceptions.PageError:
                self.speak(f"Sorry, I couldn’t find any information about {person}.")
            except Exception as e:
                self.speak("Something went wrong while looking that up.")
        else:
            self.speak("Who would you like me to look up?")
        return True



    def handle_joke(self, _):
        """Tell a joke"""
        self.speak(pyjokes.get_joke())
        return True


    

    def handle_weather(self, _):
        city = "Marietta"  # or make it dynamic with input
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

        try:
            response = requests.get(url).json()
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            self.speak(f"It's currently {temp}°F with {desc} in {city}.")
        except:
            self.speak("Sorry, I couldn't get the weather data.")
        return True
    

    def handle_reminder(self, command):
    
        match = re.search(r"remind me to (.+?) in (\d+)\s*(seconds?|minutes?|hours?)", command)
        if not match:
            self.speak("Sorry, I couldn't understand the reminder format.")
            return

        task = match.group(1).strip()
        amount = int(match.group(2))
        unit = match.group(3).lower()

        multiplier = {
            "second": 1, "seconds": 1,
            "minute": 60, "minutes": 60,
            "hour": 3600, "hours": 3600
        }

        delay = amount * multiplier.get(unit, 0)
        if delay == 0:
            self.speak("I couldn't understand the time unit.")
            return

        self.speak(f"Okay, I’ll remind you to {task} in {amount} {unit}.")
        print(f"[DEBUG] Setting reminder for {delay} seconds...")

    def send_reminder():
        print(f"[DEBUG] Reminder triggered: {task}")
        self.speak(f"⏰ Reminder: {task}")

        threading.Timer(delay, send_reminder).start()
    
    def handle_news(self, _):
        api_key = os.getenv("NEWS_API_KEY")
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        try:
            response = requests.get(url).json()
            top_articles = response['articles'][:3]
            for article in top_articles:
                self.speak(article['title'])
        except:
            self.speak("Couldn't fetch the news right now.")
        return True
    

    def handle_chat(self, command: str):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = command.replace("chat", "").strip()

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            self.speak(answer)
        except Exception as e:
            print("🧠 GPT error:", e)
            self.speak("I'm having trouble reaching my brain. Let me search the web instead.")
            fallback = self.search_web("capital of India")
            self.speak("Here's a quick summary from the web.")

            lines = fallback.split('\n')
            if len(lines) > 1:
                self.speak(lines[1])  # Speak the first snippet
            else:
                self.speak(fallback)  # Just speak the whole fallback message

        return True
    
    def search_web(self, query):
        try:
            headers = {"Ocp-Apim-Subscription-Key": os.getenv("BING_API_KEY")}
            params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
            endpoint = os.getenv("BING_ENDPOINT")
            response = requests.get(endpoint, headers=headers, params=params)
            data = response.json()
            response = requests.get(endpoint, headers=headers, params=params)
            data = response.json()


            if "webPages" in data and data["webPages"]["value"]:
                results = data["webPages"]["value"][:3]  # Top 3 results
                snippets = [f"- {item['snippet']}" for item in results]
                summary = "Here's what I found:\n" + "\n".join(snippets)
                return summary
            else:
                return "I searched the web but couldn't find anything useful."
        except Exception as e:
            print("🔍 Web search error:", e)
            return "Sorry, I couldn't search the web right now."



    
    def process_command(self, command: str) -> bool:
        if not command.strip():
            return self.handle_greeting()

        command = command.lower().strip()

         
        
        if (command == "exit" or command=="bye" or command=="ok bye") and not self.todo_mode:
            return self.handle_exit(command)
        if self.game_active:
            return self.handle_game(command)


        # Flexible matching
        if any(greet in command for greet in ['hi', 'hello', 'hey']):
            return self.handle_greeting(command)
        if any(phrase in command for phrase in ["how are you", "how's it going", "what's up"]):
            return self.handle_how_are_you(command)
        # 📋 Route to To-Do List handler
        if self.todo_mode or "to-do list" in command or 'todo' in command or'todo list' in command or any(word in command for word in ["add", "remove", "view"]):
            return self.handle_todo_list(command)

        elif 'who is' in command or 'tell me about' in command or 'what do you know about' in command:
         return self.handle_who_is(command)
        elif 'chat' in command or 'talk to me' in command  or "what is" in command:
            return self.handle_chat(command)
        elif 'game' in command or' play a game' in command or 'lets play a game' in command or 'guessing game' in command:
            return self.handle_game(command)
        elif 'tell me a joke' in command or 'say joke' in command:
            return self.handle_joke(command)
        elif 'tell me about weather' in command or 'how is the weather' in command or 'what is the temperature' in command or 'climate' in command or 'how is the climate' in command:
            return self.handle_weather(command)
        elif 'what is the time' in command or 'time' in command or 'what time is it' in command or 'tell me the time' in command:
            return self.handle_time(command)
        elif "remind me" in command or 'set a reminder for' in command or "remind me to" in command:
            return self.handle_reminder(command)
        elif 'news' in command:
            return self.handle_news(command)
       
    
        # Check defined commands
        for cmd, handler in self.commands.items():
            if command.startswith(cmd):
                return handler(command)

        self.speak("Hmm, I’m not sure how to help with that yet.")
        return True

                
        # Default response for unknown commands
        responses = [
            "I'm not sure I understand that command yet.",
            "That's an interesting request. I'll make a note to learn how to do that.",
            "Let me think about that... Hmm, I'm not sure how to help with that yet."
        ]
        self.speak(responses[datetime.datetime.now().second % len(responses)])
        return True

    def run(self):
        """Main run loop"""
        self.speak("Hi! I'm Eva – your personal voice assistant. How can I help you today?")
        
        running = True
        while running:
            try:
                print("\nOptions:")
                print("1. Speak command (say 'exit' to quit)")
                print("2. Type command")
                choice = int(input("Choose input method (1/2): ").strip())
                
                if choice == 1:
                    command = self.listen()
                elif choice == 2:
                    command = input("You: ").lower()
                else:
                    print("Invalid option, please choose 1 or 2.")
                    continue
                
                
                running = self.process_command(command)
                    
            except KeyboardInterrupt:
                running = False
            except Exception as e:
                print(f"Error: {e}")
                continue
                

if __name__ == "__main__":
    assistant = EvaTerminalAssistant()
    assistant.run()
