#!/usr/bin/env python3
"""
Simple Pomodoro timer (cross-platform).
- Default: 25 min work, 5 min short break, 15 min long break every 2 pomodoros.
- Customize durations via CLI flags.
- Sends desktop notifications (plyer library required).
- Plays a beep sound when a phase ends.
Stop any time with Ctrl+C.
"""

import argparse
import platform
import subprocess
import time
from contextlib import redirect_stderr
from datetime import datetime
from io import StringIO

try:
    from plyer import notification  # type: ignore

    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


def notify(title: str, message: str) -> None:
    """Fire a desktop notification (cross-platform)."""
    notification_sent = False

    if HAS_PLYER:
        # Use plyer for cross-platform notifications
        # Suppress stderr to hide internal plyer import errors
        stderr_buffer = StringIO()
        try:
            with redirect_stderr(stderr_buffer):
                notification.notify(title=title, message=message, app_name="Pomodoro", timeout=5)
            notification_sent = True
        except Exception:
            # Plyer failed, try fallback
            pass

    # Fallback if plyer not available or failed
    if not notification_sent:
        if platform.system() == "Darwin":
            # macOS fallback using osascript
            script = f'''
                display notification "{message}" with title "{title}"
                tell application "System Events"
                    activate
                end tell
            '''
            try:
                subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
            except Exception:
                pass
        else:
            # Fallback: print to console
            print(f"\n[{title}] {message}")

    # Play sound
    try:
        if platform.system() == "Darwin":
            subprocess.run(
                ["afplay", "/System/Library/Sounds/Ping.aiff"],
                check=False,
                capture_output=True,
            )
        elif platform.system() == "Windows":
            import winsound  # type: ignore

            winsound.Beep(1000, 500)  # type: ignore # 1000Hz for 500ms
        else:
            # Linux - try to use beep command or print bell
            try:
                subprocess.run(["beep"], check=False, capture_output=True)
            except FileNotFoundError:
                print("\a", end="", flush=True)  # Terminal bell
    except Exception:
        print("\a", end="", flush=True)  # Fallback to terminal bell


def wait_for_user_confirmation(message: str) -> bool:
    """Show dialog and wait for user to click 'Start Next' or 'Quit'."""
    if platform.system() == "Darwin":
        # macOS: use osascript
        script = f'''
            display dialog "{message}" buttons {{"Quit", "Start Next"}} default button 2
        '''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return "Start Next" in result.stdout
    else:
        # Windows/Linux: use console input
        print(f"\n{message}")
        while True:
            response = input("Continue? (y/n): ").lower().strip()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            print("Please enter 'y' or 'n'")


def format_minutes(seconds: int) -> str:
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"


def countdown(label: str, seconds: int) -> None:
    notify("Pomodoro", f"{label} start ({seconds // 60} min)")
    end_at = time.time() + seconds
    try:
        while True:
            remaining = int(end_at - time.time())
            if remaining <= 0:
                break
            print(f"{label}: {format_minutes(remaining)} remaining", end="\r", flush=True)
            time.sleep(1)
    finally:
        print()
    notify("Pomodoro", f"{label} done")


def run_pomodoro(work: int, short_break: int, long_break: int, long_every: int) -> None:
    session = 0
    while True:
        session += 1
        countdown("Focus", work)
        if session % long_every == 0:
            countdown("Long break", long_break)
            # Wait for user confirmation after long break
            if not wait_for_user_confirmation("Long break finished! Ready for next session?"):
                notify("Pomodoro", "Session ended")
                print("Session ended. Good work!")
                return
        else:
            countdown("Break", short_break)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Lightweight Pomodoro timer for macOS notifications."
    )
    parser.add_argument(
        "--work", type=int, default=25, help="Focus duration in minutes (default: 25)"
    )
    parser.add_argument(
        "--short",
        type=int,
        default=5,
        help="Short break duration in minutes (default: 5)",
    )
    parser.add_argument(
        "--long",
        type=int,
        default=15,
        help="Long break duration in minutes (default: 15)",
    )
    parser.add_argument(
        "--every", type=int, default=2, help="Long break every N sessions (default: 2)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        run_pomodoro(args.work * 60, args.short * 60, args.long * 60, args.every)
    except KeyboardInterrupt:
        notify("Pomodoro", "Stopped")
        print("Stopped. Good work!")


if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    main()
