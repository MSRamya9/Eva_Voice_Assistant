document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ Fixed script.js loaded");

  const chatBox   = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn   = document.getElementById("send-btn");
  const micBtn    = document.getElementById("mic-btn");
  speak("Hello! I'm Eva, your voice assistant. Ready to chat?")

  let lastMessageCount = 0;

  // 🛠️ Load chat history cleanly at startup
  fetch("/api/history")
    .then(res => res.json())
    .then(history => {
      lastMessageCount = history.length;
      history.forEach(entry => {
        if (entry.user) appendMessage("You", entry.user);
        if (entry.eva)  appendMessage("Eva", entry.eva);
      });
    });

  // 🔄 Poll only for new messages every 2 seconds
  setInterval(async () => {
    const res = await fetch("/api/history");
    const history = await res.json();

    if (history.length > lastMessageCount) {
      const newMessages = history.slice(lastMessageCount);
      newMessages.forEach(entry => {
        if (entry.eva)  appendMessage("Eva", entry.eva);
      });
      lastMessageCount = history.length;
    }
  }, 2000);

  // 💬 Add message bubble to chat
  function appendMessage(sender, text) {
  const msgWrapper = document.createElement("div");
  msgWrapper.classList.add("message-wrapper");

  const avatar = document.createElement("img");
  avatar.classList.add("avatar");

  // Assign appropriate avatar and class
  if (sender === "Eva") {
    avatar.classList.add("eva-avatar");
    avatar.src = "/static/assets/eva-avatar.png";
  } else {
    avatar.src = "/static/assets/user-avatar.png";
  }

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message");
  msgDiv.classList.add(sender === "Eva" ? "eva-bubble" : "user-bubble");
  msgDiv.textContent = text;

  const timestamp = document.createElement("div");
  timestamp.classList.add("timestamp");
  timestamp.textContent = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });

  // Message layout: avatar + bubble + timestamp
  if (sender === "Eva") {
    msgWrapper.style.justifyContent = "flex-start";
    msgWrapper.appendChild(avatar);
    msgWrapper.appendChild(msgDiv);
    msgWrapper.appendChild(timestamp);

    // Nod animation on reply
    avatar.classList.add("nod");
    setTimeout(() => avatar.classList.remove("nod"), 700);
  } else {
    msgWrapper.style.justifyContent = "flex-end";
    msgWrapper.appendChild(timestamp);
    msgWrapper.appendChild(msgDiv);
    msgWrapper.appendChild(avatar);
  }

  chatBox.appendChild(msgWrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}



  // 🗣️ Text-to-speech for Eva
  function speak(text) {
    if (!("speechSynthesis" in window)) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 1;

    const synth = window.speechSynthesis;
    const setVoiceAndSpeak = () => {
      const voices = synth.getVoices();
      const preferred = voices.find(v =>
        ["female", "samantha", "zira", "linda", "karen"].some(name =>
          v.name.toLowerCase().includes(name)
        )
      );
      if (preferred) utterance.voice = preferred;
      synth.speak(utterance);
    };

    if (synth.getVoices().length === 0) {
      synth.addEventListener("voiceschanged", setVoiceAndSpeak);
    } else {
      setVoiceAndSpeak();
    }
  }

  // 🚀 Send message to backend
  async function submitInput() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage("You", text);
    userInput.value = "";

    // Show Eva typing indicator
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("typing-indicator");
    typingDiv.innerHTML = "<span></span><span></span><span></span>";
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const replies = await res.json();

      chatBox.removeChild(typingDiv);  // 💨 Remove animation

      replies.forEach(reply => {
        appendMessage("Eva", reply);
        speak(reply);
      });
    } catch (err) {
      console.error("❌ Chat error:", err);
      chatBox.removeChild(typingDiv);

      const fallback = "Sorry, I can't reach the server right now.";
      appendMessage("Eva", fallback);
      speak(fallback);
    }
  }


  // 🎙️ Voice recognition
  function startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      appendMessage("Eva", "Speech recognition not supported.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.start();
    micBtn.classList.add("glowing");

    recognition.onresult = event => {
      micBtn.classList.remove("glowing");
      const transcript = event.results[0][0].transcript;
      userInput.value = transcript;
      submitInput();
    };

    recognition.onerror = () => {
      micBtn.classList.remove("glowing");
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
