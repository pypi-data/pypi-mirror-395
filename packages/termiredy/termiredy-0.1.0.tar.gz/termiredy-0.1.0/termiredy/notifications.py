import platform
import subprocess
import sys

def send_notification(title: str, message: str):
    system = platform.system()

    if system == "Darwin":  # macOS
        safe_title = title.replace('"', '\\"')
        safe_message = message.replace('"', '\\"')
        script = f'display notification "{safe_message}" with title "{safe_title}"'
        # script = f'display alert "{safe_message}" message "{safe_title}"' 
        # TODO: Add a mode switch parameter to choose between notification and alert.
        subprocess.run(["osascript", "-e", script])

    elif system == "Linux":
        # linux need to have notify-send（libnotify-bin）
        # sudo apt install libnotify-bin
        subprocess.run(["notify-send", title, message])
    else:
        # Unknown system, fallback to print
        print(f"[{title}] {message}")
