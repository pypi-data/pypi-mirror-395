import sys

sys.path.insert(0, "/usr/lib/python3/dist-packages")
import dbus
import notify2


def notification(summary, text, icon="notification-message-im"):
    notify2.init("Coauthor")
    notification_instance = notify2.Notification(summary, text, icon)  # Icon name
    notification_instance.show()
