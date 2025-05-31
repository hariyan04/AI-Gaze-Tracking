import speech_recognition as sr
import pyautogui
import os
import time

def open_app(app_name):
    """Opens an application by searching in the Start menu."""
    print(f"🟢 Opening {app_name}...")
    pyautogui.hotkey("win")
    time.sleep(1)
    pyautogui.write(app_name)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    print(f"✅ Performed: open {app_name.lower()}")

def open_youtube():
    """Opens YouTube in Google Chrome."""
    print("🌍 Opening YouTube in Chrome...")
    os.system("start chrome https://www.youtube.com")
    print("✅ Performed: open YouTube")

def create_new_folder():
    """Creates a new folder using the right-click menu."""
    print("🟢 Creating a new folder...")
    pyautogui.hotkey("shift", "f10")  # Right-click context menu
    time.sleep(0.5)
    pyautogui.press("w")  
    pyautogui.press("f")  
    time.sleep(1)
    print("✅ New folder created.")

def refresh_screen():
    """Performs refresh and closes the right-click menu automatically."""
    print("🔄 Refreshing screen...")
    pyautogui.press("f5")
    time.sleep(0.5)
    pyautogui.click()  # Click anywhere to close the right-click menu
    print("✅ Performed: refresh")

def lock_screen():
    """Locks the Windows screen."""
    print("🔒 Locking screen now...")
    os.system("rundll32.exe user32.dll,LockWorkStation")
    print("✅ Performed: lock screen")

def type_text():
    """Types text using speech-to-text until the user says 'stop typing'."""
    print("⌨️ Typing mode activated. Say 'stop typing' to exit.")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                print("🎤 Listening for text to type...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                
                if "stop typing" in command:
                    print("🛑 Typing mode deactivated.")
                    break
                
                # Type the recognized speech
                print(f"⌨️ Typing: {command}")
                pyautogui.write(command)
                
            except sr.UnknownValueError:
                print("⚠️ Could not understand the command.")
            except sr.RequestError:
                print("⚠️ Speech recognition service is unavailable.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

def perform_action(command):
    """Executes actions based on recognized speech command."""
    command = command.lower()

    if "type" in command:
        type_text()
    elif "open youtube" in command:
        open_youtube()
    elif "open prime video" in command:
        open_app("Prime Video")
    elif "open netflix" in command:
        open_app("Netflix")
    elif "open linkedin" in command:
        open_app("LinkedIn")
    elif "open vscode" in command or "open vs code" in command:
        open_app("Visual Studio Code")
    elif "open whatsapp" in command:
        open_app("WhatsApp")
    elif "open notepad" in command:
        os.system("notepad")
    elif "open ms word" in command or "open word" in command:
        open_app("Word")
    elif "open excel" in command:
        open_app("Excel")
    elif "open powerpoint" in command:
        open_app("PowerPoint")
    elif "open start menu" in command:
        pyautogui.hotkey("win")
    elif "lock screen" in command:
        lock_screen()
    elif "open file explorer" in command:
        os.system("explorer")
    elif "open task manager" in command:
        pyautogui.hotkey("ctrl", "shift", "esc")
    elif "previous tab" in command:
        pyautogui.hotkey("ctrl", "shift", "tab")
    elif "new tab" in command:
        pyautogui.hotkey("ctrl", "t")
    elif "right click" in command:
        pyautogui.rightClick()
    elif "double click" in command:
        pyautogui.doubleClick()
    elif "left click" in command:
        pyautogui.click()
    elif "refresh" in command:
        refresh_screen()
    elif "new folder" in command or "create new folder" in command:
        create_new_folder()
    elif "minimize window" in command or "minimise window" in command:
        pyautogui.hotkey("win", "d")  # Minimizes all windows
    elif "maximize window" in command:
        pyautogui.hotkey("win", "up")
    elif "close window" in command:
        pyautogui.hotkey("alt", "f4")
    elif "select all" in command:
        pyautogui.hotkey("ctrl", "a")
    elif "cut" in command or "cut this" in command or "cut text" in command:
        pyautogui.hotkey("ctrl", "x")
    elif "copy" in command or "copy this" in command:
        pyautogui.hotkey("ctrl", "c")
    elif "paste" in command or "paste here" in command:
        pyautogui.hotkey("ctrl", "v")
    else:
        print("❌ Command not recognized.")

def listen_and_execute():
    """Continuously listens for speech commands and executes them."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {command}")
            perform_action(command)
        except sr.UnknownValueError:
            print("⚠️ Could not understand the command.")
        except sr.RequestError:
            print("⚠️ Speech recognition service is unavailable.")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    while True:
        listen_and_execute()
