import os
import sys
import subprocess


def main() -> int:
    base_dir = os.path.dirname(__file__)

    if sys.platform.startswith("linux"):
        exe_name = "car_game_linux"
    elif sys.platform == "win32":
        exe_name = "car_game_windows.exe"
    else:
        print(f"Unsupported platform: {sys.platform}")
        return 1

    exe = os.path.join(base_dir, "bin", exe_name)

    if not os.path.exists(exe):
        print("Error: game binary not found:")
        print(" ", exe)
        return 1

    if sys.platform != "win32":
        try:
            os.chmod(exe, 0o755)
        except PermissionError:
            pass

    try:
        return subprocess.call([exe])
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
