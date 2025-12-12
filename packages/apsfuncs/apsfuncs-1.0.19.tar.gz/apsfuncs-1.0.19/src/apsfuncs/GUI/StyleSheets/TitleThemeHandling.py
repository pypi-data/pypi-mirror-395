import ctypes, winreg
from PyQt6.QtCore import QObject, pyqtSignal, QAbstractNativeEventFilter, QCoreApplication

# DWM constants
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36
DWMWA_BORDER_COLOR = 34

# Manager class to handle detection of theme chaneges and matches the window title bar to the active theme
class TitleThemeManager(QObject):
    # Conneciton to all hooking to a theme change if needed
    theme_changed = pyqtSignal(str, tuple)  # emits (theme, accent_color)

    # Declare the instance so only one title theme manager is used
    _instance = None

    def __init__(self):
        super().__init__()
        self.registered_windows = []
        self.current_theme = get_windows_theme()
        self.accent_color = get_accent_color()

        # Install Windows message listener
        self.filter = WindowsThemeEventFilter(self.on_system_theme_change)
        QCoreApplication.instance().installNativeEventFilter(self.filter)

        # Set the default colour values
        self.light_text_colour = (0, 0, 0)
        self.dark_text_colour = (255, 255, 255)

        self.light_back_colour  = (85, 107, 194) #Set as None to use the windows option
        self.dark_back_colour = (35, 35, 35)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = TitleThemeManager()
        return cls._instance

    # Add new widget to the set to update the title bars off
    def register_window(self, widget):
        if widget not in self.registered_windows:
            self.registered_windows.append(widget)
            self.apply_theme(widget)

    # Remove widget to the set to update the title bars off
    def unregister_window(self, widget):
        if widget in self.registered_windows:
            self.registered_windows.remove(widget)

    # Apply the set theme colours to the given widget
    def apply_theme(self, widget):
        if self.current_theme == "light":
            # Set the text colour
            text_color = self.light_text_colour
            # If there is a constant over-write colour to use, then use it, otherwise use the Windows set colour
            if self.light_back_colour is not None:
                set_win_titlebar_color(widget, self.light_back_colour, text_color)
            else:
                set_win_titlebar_color(widget, self.accent_color, text_color)
        else:
            # Set the text colour
            text_color = self.dark_text_colour
            # If there is a constant over-write colour to use, then use it, otherwise use the Windows set colour
            if self.dark_back_colour is not None:
                set_win_titlebar_color(widget, self.dark_back_colour, text_color)
            else:
                set_win_titlebar_color(widget, self.accent_color, text_color)

        

    # Method to ctach a theme change and updated all registered widgets as well as triggering the signal so the rest of the program knows
    def on_system_theme_change(self):
        # Get the current theme and accent
        new_theme = get_windows_theme()
        new_accent = get_accent_color()

        # Check that at least one has been changed
        if new_theme != self.current_theme or new_accent != self.accent_color:
            self.current_theme = new_theme
            self.accent_color = new_accent
            self.theme_changed.emit(new_theme, new_accent)

            # Update all registered windows
            for w in list(self.registered_windows):
                if w.isVisible():
                    self.apply_theme(w)

# Class to handle listening for a settigns chaneg in windows so the theme and colour can be checked
class WindowsThemeEventFilter(QAbstractNativeEventFilter):

    # Key for settings changes
    WM_SETTINGCHANGE = 0x001A

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def nativeEventFilter(self, eventType, message):
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        if msg.message == self.WM_SETTINGCHANGE:
            self.callback()
        return False, 0

# Fucntion to return the windows theme "light" or "dark"
def get_windows_theme():
    key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
            value, _ = winreg.QueryValueEx(k, "AppsUseLightTheme")
            return "light" if value == 1 else "dark"
    except FileNotFoundError:
        return "light"


# Fucntion to return the rgb for the window accent colour
def get_accent_color():
    key = r"Software\Microsoft\Windows\DWM"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
            color, _ = winreg.QueryValueEx(k, "ColorizationColor")
            b = color & 0xFF
            g = (color >> 8) & 0xFF
            r = (color >> 16) & 0xFF
            return (r, g, b)
    except FileNotFoundError:
        return (0, 120, 215)

# Convertion funciton to take an rgb list and convert it to a ctypes colour
def _to_colorref(rgb):
    return ctypes.c_int((rgb[2] << 16) | (rgb[1] << 8) | rgb[0])

# Method to set the colour of the windows title bar
def set_win_titlebar_color(widget, color_rgb, text_rgb=(255, 255, 255), border_rgb=None):

    # Get the window settings
    hwnd = int(widget.winId())
    dwmapi = ctypes.windll.dwmapi

    # Set the caption, text and border colours if they are given
    caption = _to_colorref(color_rgb)
    dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_CAPTION_COLOR,
                                 ctypes.byref(caption), ctypes.sizeof(caption))

    text = _to_colorref(text_rgb)
    dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_TEXT_COLOR,
                                 ctypes.byref(text), ctypes.sizeof(text))

    if border_rgb:
        border = _to_colorref(border_rgb)
        dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_BORDER_COLOR,
                                     ctypes.byref(border), ctypes.sizeof(border))