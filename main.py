from time import sleep
from threading import Thread

from pystray import Icon, Menu, MenuItem
from winreg import ConnectRegistry, OpenKey, EnumValue, HKEY_CURRENT_USER

import icons
from prevent_sleep_win import updatePreventionState

VERSION = '1.3'


class App:
    _enabled = False  # Sleep prevention enabled
    _timerId = -1  # Timer id used to prevent multiple timers disabling each other
    _timerActive = False  # Used for showing checked status in menu
    _requireDisplay = True  # Whether display needs to be turned on or off (system won't sleep either)

    def __init__(self):
        self._trayIcon = Icon('Sleepkiller', self.getCurrentIcon(), menu=Menu(
            MenuItem(
                'Prevent sleeping',
                lambda icon, item: self.onClick(icon, item),
                default=True,
                checked=lambda item: self._enabled,
            ),
            MenuItem(
                "Awake timer",
                Menu(
                    MenuItem(
                        '15 minutes',
                        action=lambda: self.delayWrapper(15),
                    ),
                    MenuItem(
                        '30 minutes',
                        action=lambda: self.delayWrapper(30),
                    ),
                    MenuItem(
                        '45 minutes',
                        action=lambda: self.delayWrapper(45),
                    ),
                    MenuItem(
                        '1 hour',
                        action=lambda: self.delayWrapper(60),
                    ),
                    MenuItem(
                        '1.5 hours',
                        action=lambda: self.delayWrapper(90),
                    ),
                    MenuItem(
                        '2 hours',
                        action=lambda: self.delayWrapper(120),
                    ),
                    MenuItem(
                        '3 hours',
                        action=lambda: self.delayWrapper(180),
                    ),
                    MenuItem(
                        '5 hours',
                        action=lambda: self.delayWrapper(300),
                    ),
                    MenuItem(
                        '10 hours',
                        action=lambda: self.delayWrapper(600),
                    ),
                ),
                checked=lambda item: self._timerActive,
            ),
            Menu.SEPARATOR,
            MenuItem(
                'Allow screen to turn off',
                action=lambda: self.toggleDisplayRequirement(),
                checked=lambda item: not self._requireDisplay,
            ),
            Menu.SEPARATOR,
            MenuItem(
                'Quit',
                lambda icon, item: icon.stop(),
            ),
        ))

    def run(self):
        self._trayIcon.run()

    @staticmethod
    def isDarkBackground():
        reg = ConnectRegistry(None, HKEY_CURRENT_USER)
        key = OpenKey(reg, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize')

        for i in range(128):  # 128 should be enough for the registry key used here
            name, value, valueType = EnumValue(key, i)
            if name == 'SystemUsesLightTheme':
                return value == 0
        return True  # if can't get the value

    def getCurrentIcon(self):
        if self.isDarkBackground():
            return icons.enabledDark if self._enabled else icons.disabledDark
        else:
            return icons.enabledLight if self._enabled else icons.disabledLight

    def onClick(self, icon, _):
        self._enabled = not self._enabled
        updatePreventionState(self._enabled, self._requireDisplay)

        icon.icon = self.getCurrentIcon()

        if not self._enabled and self._timerActive:
            self._timerActive = False

    def toggleDisplayRequirement(self):
        self._requireDisplay = not self._requireDisplay

    def delayFunction(self, minutes):
        self._timerId += 1
        currentTimerId = self._timerId
        self._timerActive = True

        self._enabled = True
        updatePreventionState(self._enabled, self._requireDisplay)

        self._trayIcon.update_menu()  # should be called after changing self.enabled and self.timerActive
        self._trayIcon.icon = self.getCurrentIcon()
        self._trayIcon.notify('Awake timer started', f'Not sleeping for {minutes} minutes')

        sleep(minutes * 60)  # not a great solution but ok for now

        if self._timerId == currentTimerId:
            self._enabled = False
            updatePreventionState(self._enabled)

            self._timerActive = False
            self._trayIcon.update_menu()  # should be called after changing self.enabled and self.timerActive
            self._trayIcon.icon = self.getCurrentIcon()
            self._trayIcon.notify('Awake timer stopped', f'Your system can sleep again')

    def delayWrapper(self, delay):
        return Thread(target=self.delayFunction, args=(delay,), daemon=True).start()


if __name__ == '__main__':
    app = App()
    app.run()
