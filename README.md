🧠 AI Powered Gaze Tracking Using Facial Recognition Techniques 
📦 Project File Structure 
📁 Project Root 
├── GazeTracking.py # Main file for gaze-based cursor control 
├── utils.py # Eye/mouth aspect ratio and direction utils 
├── test.py # Speech command handler 
└── model/ 
    └── shape_predictor_68_face_landmarks.dat # Dlib facial landmark model 
    
    
⚙️ Requirements 
Python 3.6 or above
Hardware: Webcam and Microphone
OS: Windows recommended (for app execution like Notepad, Word, etc.)

Install Dependencies 
pip install opencv-python dlib imutils numpy pyautogui SpeechRecognition pyaudio

▶️ Step-by-Step Project Execution
🔧 1. Initial Setup Download or clone the project files.

Place shape_predictor_68_face_landmarks.dat inside the model/ folder.

Install required dependencies using the pip command above.

🏃 2. Run the Main Program  python GazeTracking.py This will:

Launch the webcam.

Activate gaze detection and tracking.

Start a background thread for voice command recognition.

👁️ 3. Gaze Tracking Instructions 
Gesture/Detection   Action 
👁️ Eye Wink (Left)  Left Click 
👁️ Eye Wink (Right) Right Click 
👄 Open Mouth (Hold) Toggle Input Mode 
👃 Nose Direction Move Cursor (Input Mode)

Move your nose in a direction after opening your mouth to control the cursor. A rectangle appears to mark the active input region.

🗣️ 4. Speech Command Features 
✨ App & Web Actions open youtube, open netflix, open prime video, open linkedin, open whatsapp

open vscode / open vs code

open notepad, open ms word, open excel, open powerpoint

open file explorer, open start menu, open task manager

💬 Text Typing type – Activates typing mode from speech Say stop typing to exit.

🖱️ Mouse Actions left click, right click, double click

refresh – Presses F5 and exits context menu

new folder / create new folder

🗔 Window Controls minimize window, maximize window, close window

📋 Editing Commands select all, cut, copy, paste

🔐 System Controls lock screen

🔁 Browser Tab Commands new tab, previous tab

❌ If a command isn't recognized, it prints: Command not recognized.

❌ 5. Exit the Program You can exit in either of these ways:

✅ Say: close window – Closes the active window via speech.

✅ Press: Esc key – Terminates the application manually.
