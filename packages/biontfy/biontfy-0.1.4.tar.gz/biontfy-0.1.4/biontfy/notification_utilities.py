import os
import subprocess
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QLibraryInfo

# Define the base directory for resources
# This assumes the resources folder is next to this file in the installed package
RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")

def load_vazirmatn_font(size: int) -> QFont:
    """
    Loads the Vazirmatn font from the embedded resources directory and returns a QFont object.
    """
    # Path relative to this file: biontfy/notification_utilities.py -> biontfy/resources/fonts/Vazirmatn-Regular.ttf
    font_path = os.path.join(os.path.dirname(__file__), "resources", "fonts", "Vazirmatn-Regular.ttf")
    
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        # print("Error: Cannot load Vazirmatn font. Using Segoe UI as fallback.")
        return QFont("Segoe UI", size)  # fallback
    
    family = QFontDatabase.applicationFontFamilies(font_id)
    if not family:
        # print("Error: Cannot get font family. Using Segoe UI as fallback.")
        return QFont("Segoe UI", size)  # fallback
        
    return QFont(family[0], size)

def play_notification_sound(sound_file: str = "msr.mp3"):
    """
    Plays a sound file using the mpg123 command-line player asynchronously.
    This is a fallback for environments where PyQt's QtMultimedia or
    other Python sound libraries are difficult to install.
    """
    sound_path = os.path.join(os.path.dirname(__file__), "resources", sound_file)

    if not os.path.exists(sound_path):
        # print(f"Sound file not found: {sound_path}")
        return

    # Use subprocess to run mpg123 in the background
    # -q: quiet (suppress output)
    # -f 1000: set volume to 1000 (out of 32768) for a "reasonable" volume
    try:
        # The user requested the msr sound to play with a reasonable volume.
        # I'm using -f 1000 which is about 3% of max volume, which should be reasonable.
        subprocess.Popen(["mpg123", "-q", "-f", "1000", sound_path],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Warning: mpg123 command not found. Sound playback is disabled. To enable, please install mpg123 (e.g., 'sudo apt-get install mpg123' on Linux, or add the Windows executable to PATH).")
    except Exception as e:
        print(f"An error occurred while trying to play sound: {e}")
