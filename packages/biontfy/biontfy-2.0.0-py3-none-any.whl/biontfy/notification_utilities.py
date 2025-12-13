import os
import subprocess
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QLibraryInfo, QUrl
try:
    from PyQt6.QtMultimedia import QSoundEffect
    HAS_SOUND_EFFECT = True
except ImportError:
    HAS_SOUND_EFFECT = False

# Define the base directory for resources
# This assumes the resources folder is next to this file in the installed package
# Define the base directory for resources
# This assumes the resources folder is next to this file in the installed package
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

def load_vazirmatn_font(point_size: int = 10) -> QFont:
    """
    Loads the Vazirmatn font from the resources directory and returns a QFont object.
    """
    font_path = os.path.join(RESOURCE_DIR, "fonts", "Vazirmatn-Regular.ttf")

    if not os.path.exists(font_path):
        # print(f"Could not find Vazirmatn font at {font_path}. Using system default as fallback.")
        font = QFont("Segoe UI", point_size)
        font.setBold(True)
        return font

    font_id = QFontDatabase.addApplicationFont(font_path)

    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            font = QFont(families[0], point_size)
            # print(f"Successfully loaded font: {families[0]}")
            return font

    # print(f"Could not load Vazirmatn font from {font_path}. Using system default as fallback.")
    font = QFont("Segoe UI", point_size) # Fallback font
    font.setBold(True)
    return font

# Global variable to hold a reference to QSoundEffect to prevent garbage collection
sound_effect_ref = None

def play_notification_sound(sound_file: str = "msr.mp3"):
    global sound_effect_ref
    """
    Plays a sound file using the mpg123 command-line player asynchronously.
    Plays a sound file using QSoundEffect for cross-platform compatibility,
    falling back to mpg123 if QSoundEffect is unavailable.
    """
    sound_path = os.path.join(RESOURCE_DIR, sound_file)

    if not os.path.exists(sound_path):
        # print(f"Sound file not found: {sound_path}")
        return

    if HAS_SOUND_EFFECT:
        try:
            # QSoundEffect needs a QUrl
            url = QUrl.fromLocalFile(sound_path)
            # Use a global reference to keep the sound effect alive for the duration of playback
            # The global declaration is at the function start, so we can assign directly.
            sound_effect_ref = QSoundEffect()
            sound_effect_ref.setSource(url)
            sound_effect_ref.setVolume(0.5) # Set volume to 50%
            sound_effect_ref.play()
            return
        except Exception as e:
            print(f"QSoundEffect failed to play sound: {e}. Falling back to mpg123.")

    # Fallback to mpg123
    try:
        # The user requested the msr sound to play with a reasonable volume.
        # I'm using -f 1000 which is about 3% of max volume, which should be reasonable.
        subprocess.Popen(["mpg123", "-q", "-f", "1000", sound_path],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Error: mpg123 command not found. Please install it (e.g., sudo apt-get install mpg123).")
    except Exception as e:
        print(f"An error occurred while trying to play sound with mpg123: {e}")
