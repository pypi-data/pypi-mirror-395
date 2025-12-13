import os
import subprocess
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QLibraryInfo

# Define the base directory for resources
# This assumes the resources folder is next to this file in the installed package
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

def load_vazirmatn_font(point_size: int = 10) -> QFont:
    """
    Loads the Vazirmatn font from the resources directory and returns a QFont object.
    """
    font_path = os.path.join(RESOURCE_DIR, "Vazirmatn-Regular.ttf")
    
    if not os.path.exists(font_path):
        # print(f"Could not find Vazirmatn font at {font_path}. Using system default as fallback.")
        font = QFont("Arial", point_size)
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
    font = QFont("Arial", point_size) # Fallback font
    font.setBold(True)
    return font

def play_notification_sound(sound_file: str = "msr.mp3"):
    """
    Plays a sound file using the mpg123 command-line player asynchronously.
    This is a fallback for environments where PyQt's QtMultimedia or
    other Python sound libraries are difficult to install.
    """
    sound_path = os.path.join(RESOURCE_DIR, sound_file)
    
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
        print("Error: mpg123 command not found. Please install it (e.g., sudo apt-get install mpg123).")
    except Exception as e:
        print(f"An error occurred while trying to play sound: {e}")
