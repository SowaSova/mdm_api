import enum


class Command(enum.Enum):
    REBOOT = "reboot"
    SHUTDOWN = "shutdown"
    WIPE = "wipe"


class DeviceStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OFFLINE = "offline"


class DeviceType(enum.Enum):
    ANDROID = "android"
    WEB = "windows"
    # IOS = "ios"
