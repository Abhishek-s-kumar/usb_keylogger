USB Automation Script
This project automates the logging of keyboard and mouse inputs, takes periodic screenshots, and records audio from the microphone. While the idea is to work with USB drives, this script does not automatically run upon USB insertion. The script must be manually executed, or you can configure your system (e.g., using Task Scheduler on Windows) to run it when the USB drive is connected.

Features
Keyboard Logging: Captures keypresses and saves them to a key_log.txt file.
Mouse Logging: Logs mouse clicks and saves them to a mouse_log.txt file.
Screenshot Capture: Takes periodic screenshots (every minute) and saves them as .png files.
Microphone Recording: Continuously records audio from the system’s default microphone and saves it in .wav format.
Manual USB Drive Detection: The script will check if a USB drive is connected and start logging. It stops when the USB is removed, but this needs to be handled within the script execution context.
Important Note
This script does not automatically run when a USB drive is inserted. It requires manual execution. To automate this process, you can configure a system-level trigger, like Windows Task Scheduler or Linux udev rules.

How It Works
When you manually run the script, it checks for the presence of a USB drive.
The script will log activities (keyboard, mouse, screenshots, and microphone).
Logging will continue until the USB is removed or the script is stopped manually via Ctrl+C.
Setup
Prerequisites
You need to have Python installed on the system where the script will run. The following dependencies are required for this project:

pynput (for keyboard and mouse logging)
pyautogui (for screenshots)
pyaudio (for audio recording