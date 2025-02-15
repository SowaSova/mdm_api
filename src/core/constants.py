from .enums import DeviceStatus, Command

COMMAND_STATUS_MAPPING = {
    Command.REBOOT: DeviceStatus.OFFLINE,
    Command.SHUTDOWN: DeviceStatus.OFFLINE,
    Command.WIPE: DeviceStatus.INACTIVE,
}
