from core.exceptions import BackToMenu

def ask(p=""):
    value = input(p).strip()     
    if value.lower() == "back":
        raise BackToMenu()
    return value