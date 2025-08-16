import speech_recognition as sr
import pyttsx3
import subprocess
import time
import threading

class VoiceAssistant:
    def __init__(self, command_callback=None, response_callback=None):
        # Initialize TTS engine in a separate thread
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.command_callback = command_callback
        self.response_callback = response_callback
        self._running = True
        self.speech_queue = []
        self.speech_thread = threading.Thread(target=self._speak_thread)
        self.speech_thread.daemon = True
        self.speech_thread.start()

    def _speak_thread(self):
        """Background thread for non-blocking speech"""
        while self._running:
            if self.speech_queue:
                text = self.speech_queue.pop(0)
                print(f"🤖 MAINEC: {text}")
                if self.response_callback:
                    self.response_callback(text)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            time.sleep(0.05)

    def speak(self, text):
        """Queue text for speech without blocking"""
        self.speech_queue.append(text)

    def listen(self):
        """Optimized listening with reduced latency"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Reduced adjustment time and dynamic energy threshold
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.5
            print("\n🎤 Listening...", end='', flush=True)
            
            try:
                audio = r.listen(source, timeout=0.8, phrase_time_limit=3)
                text = r.recognize_google(audio).lower()
                print(f"\r👤 User said: {text}")
                if self.command_callback:
                    self.command_callback(text)
                return text
            except sr.WaitTimeoutError:
                print("\r", end='')  # Clear the listening line
                return ""
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that")
                return ""
            except sr.RequestError as e:
                self.speak("Speech service unavailable")
                print(f"❌ Speech service error: {e}")
                return "error"

    def execute_command(self, command):
        """Execute command with minimal delay"""
        if not command:
            return None
            
        # Speak confirmation while executing command
        self.speak(f"You said: {command}")
        
        try:
            if "open chrome" in command:
                self.speak("Opening Google Chrome")
                subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                
            elif "minimize" in command or "minimise" in command:
                self.speak("Minimizing the window")
                import screen_ops
                screen_ops.minimize_window()
                
            elif "open notepad" in command:
                self.speak("Opening Notepad")
                subprocess.Popen(["notepad.exe"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            elif "open edge" in command:
                self.speak("Opening Microsoft Edge")
                subprocess.Popen(["msedge.exe"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                
            elif "open file explorer" in command:
                self.speak("Opening File Explorer")
                subprocess.Popen(["explorer.exe"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                
            elif "stop" in command or "exit" in command:
                self.speak("Shutting down voice control")
                self._running = False
                return "exit"
                
            else:
                self.speak("Command not recognized")
            return None
            
        except Exception as e:
            self.speak("Sorry, I couldn't complete that request")
            print(f"Command execution error: {e}")
            return None

    def run(self):
        """Main voice control loop with optimized timing"""
        self.speak("MAINEC voice assistant activated!")
        
        while self._running:
            command = self.listen()
            if command == "error":
                time.sleep(1)  # Reduced error delay
                continue
                
            result = self.execute_command(command)
            if result == "exit":
                break
            time.sleep(0.1)  # Reduced sleep time between commands

    def stop(self):
        """Clean shutdown"""
        self._running = False
        self.speech_thread.join()

def initialize_voice_assistant(command_callback=None, response_callback=None):
    """Initialize the voice assistant"""
    assistant = VoiceAssistant(command_callback, response_callback)
    try:
        assistant.run()
    finally:
        assistant.stop()