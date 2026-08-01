from utils.theme_manager import ThemeManager

def __getattr__(name):
    return ThemeManager.get(name)