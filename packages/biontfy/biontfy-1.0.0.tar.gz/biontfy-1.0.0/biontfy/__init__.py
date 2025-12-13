from .notification_manager import NotificationManager
from .notification_item import NotificationItem
from .notification_utilities import play_notification_sound

# Expose the main entry point for the library
def get_manager() -> NotificationManager:
    """
    Returns the singleton instance of the NotificationManager.
    """
    return NotificationManager.instance()

# Optionally, expose the NotificationItem for advanced customization
__all__ = [
    "get_manager",
    "NotificationManager",
    "NotificationItem",
    "play_notification_sound"
]
