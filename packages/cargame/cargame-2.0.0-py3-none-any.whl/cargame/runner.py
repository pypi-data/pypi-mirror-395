import os
import subprocess
import platform

def main():
    base = os.path.join(os.path.dirname(__file__), "bin")

    if platform.system() == "Windows":
        exe = os.path.join(base, "car_game_windows.exe")
    else:
        exe = os.path.join(base, "car_game_linux")

    os.chmod(exe, 0o755)
    subprocess.run([exe])
