import argparse
import subprocess
import sys
import os
import simpleaudio as sa

# Global player object (so we can stop sound)
play_obj = None

def play_sound(sound_name):
    """Play a WAV sound file."""
    global play_obj
    base = os.path.dirname(__file__)
    sound_path = os.path.join(base, sound_name)

    print("Trying to load:", sound_path)

    if os.path.exists(sound_path):
        wave = sa.WaveObject.from_wave_file(sound_path)
        play_obj = wave.play()
        print("▶️ Playing sound:", sound_name)
    else:
        print(f"❌ Sound file not found: {sound_path}")

def stop_sound():
    global play_obj
    if play_obj:
        play_obj.stop()
        print("⏹ Sound stopped.")
    else:
        print("⚠ No sound playing.")

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    subprocess.run([sys.executable, script_path])

def main():
    parser = argparse.ArgumentParser(description="Turtle CLI Tool + Sound")

    parser.add_argument(
        "-d", "--draw",
        choices=["cake", "heart", "virus", "disco"],
        help="Choose a graphic to draw."
    )

    parser.add_argument(
        "-s", "--song",
        choices=["dooron"],
        help="Play standalone song."
    )

    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop currently playing sound."
    )

    args = parser.parse_args()

    # -----------------------
    # STOP SOUND MODE
    # -----------------------
    if args.stop:
        stop_sound()
        return

    # -----------------------
    # SONG MODE
    # -----------------------
    if args.song == "dooron":
        play_sound("dooron.wav")
        return

    # -----------------------
    # DRAWING MODE
    # -----------------------
    if args.draw == "cake":
        # ❌ No sound for cake anymore
        run_script("cake.py")

    elif args.draw == "heart":
        play_sound("rabba.wav")
        run_script("heart.py")

    elif args.draw == "virus":
        # No sound unless you add one later
        run_script("virus.py")

    elif args.draw == "disco":
        play_sound("dooron.wav")     # ✔ disco has dooron song
        run_script("disco.py")

if __name__ == "__main__":
    main()
