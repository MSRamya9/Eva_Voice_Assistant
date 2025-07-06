import sys

def run_voice_assistant():
    from assistant import EvaTerminalAssistant
    eva = EvaTerminalAssistant()
    print("🎙️ Eva is listening... Say something!")

    while True:
        try:
            command = input("You: ")
            eva.process_command(command)
        except KeyboardInterrupt:
            print("\n👋 Exiting Eva. Goodbye!")
            break


def run_web_interface():
    from server import app
    import os, webbrowser

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://localhost:5000")

    app.run(debug=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        run_web_interface()
    else:
        run_voice_assistant()
