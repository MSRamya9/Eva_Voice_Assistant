// static/script.js
document.addEventListener("DOMContentLoaded", () => {
  console.log("🐛 script.js has loaded");

  const chatBox   = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn   = document.getElementById("send-btn");
  const micBtn    = document.getElementById("mic-btn");

// 🧠 Send message to Eva
sendBtn.addEventListener('click', async () => {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage('You', message);
  userInput.value = '';

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  const replies = await res.json();
  replies.forEach(reply => appendMessage('Eva', reply));
});

// 🔁 Poll for reminders and updates every 5 seconds
let lastMessageCount = 0;

setInterval(async () => {
  const res = await fetch('/api/history');
  const history = await res.json();

  if (history.length > lastMessageCount) {
    const newMessages = history.slice(lastMessageCount);
    newMessages.forEach(entry => {
      if (entry.user) {
        appendMessage('You', entry.user);
      } else if (entry.eva) {
        appendMessage('Eva', entry.eva);

        // ✅ Speak reminders immediately when they arrive
        if (entry.eva.includes("⏰ Reminder")) {
          speak(entry.eva);
        }
      }
    });
    lastMessageCount = history.length;
  }
}, 2000); // Poll every 2 seconds


// 🧱 Helper to append messages
function appendMessage(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = sender.toLowerCase();
  msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  if (sender === 'Eva' && text.includes("⏰ Reminder")) {
    speak(text); // 🗣️ Speak all Eva responses
  }
}

  // ✅ Load chat history from the server
  fetch("/api/history")
    .then(res => res.json())
    .then(history => {
      history.forEach(([sender, message]) => {
        appendMessage(sender, message);
      });
    })
    .catch(err => {
      console.error("🐛 Failed to load chat history:", err);
    });

  // 🧠 Append message to chat
  function appendMessage(sender, message) {
    const msg = document.createElement("div");
    msg.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

 function speak(text) {
  if (!("speechSynthesis" in window)) return;

  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 1;

  const setVoiceAndSpeak = () => {
    const voices = synth.getVoices();
    const preferredVoice = voices.find(v =>
      v.name.toLowerCase().includes("female") ||
      v.name.toLowerCase().includes("zira") ||
      v.name.toLowerCase().includes("samantha") ||
      v.name.toLowerCase().includes("linda") ||
      v.name.toLowerCase().includes("karen")
    );
    if (preferredVoice) utterance.voice = preferredVoice;
    synth.speak(utterance);
  };

  if (synth.getVoices().length === 0) {
    synth.addEventListener("voiceschanged", setVoiceAndSpeak);
  } else {
    setVoiceAndSpeak();
  }
}



  // 🚀 Send message to Flask backend
  async function submitInput() {
    console.log("🐛 submitInput fired");
    const text = userInput.value.trim();
    if (!text) {
      console.log("🐛 no text to send");
      return;
    }

    appendMessage("You", text);
    userInput.value = "";

    try {
      console.log("🐛 Sending POST to /api/chat");
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      console.log("🐛 Got HTTP status", res.status);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const replies = await res.json();
      console.log("🐛 JSON response:", replies);

      replies.forEach(reply => {
        appendMessage("Eva", reply);
        speak(reply); // 🗣️ Speak each reply
      });
    } catch (err) {
      console.error("🐛 Fetch error:", err);
      appendMessage("Eva", "Sorry, I can't reach the server right now.");
      speak("Sorry, I can't reach the server right now.");
    }
  }

  // 🎙️ Start voice recognition
  function startListening() {
    console.log("🐛 startListening fired");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      appendMessage("Eva", "Sorry, your browser doesn't support speech recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = event => {
      const transcript = event.results[0][0].transcript;
      console.log("🐛 transcript:", transcript);
      userInput.value = transcript;
      submitInput();
    };

    recognition.onerror = event => {
      console.error("🐛 Speech recognition error:", event.error);
      appendMessage("Eva", "Sorry, I couldn't hear you.");
      speak("Sorry, I couldn't hear you.");
    };
  }

  // 🎯 Event listeners
  sendBtn.addEventListener("click", submitInput);

  userInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      submitInput();
    }
  });

  micBtn.addEventListener("click", startListening);
});
