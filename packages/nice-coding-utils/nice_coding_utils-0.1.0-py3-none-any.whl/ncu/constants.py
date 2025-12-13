ES = '\033['
class FG:
    """
    Contains all 16 Foreground Colors + Reset
    """
    GREY = ES + '30m'
    RED = ES + '31m'
    GREEN = ES + '32m'
    YELLOW = ES + '33m'
    BLUE = ES + '34m'
    MAGENTA = ES + '35m'
    CYAN = ES + '36m'
    WHITE = ES + '37m'
    
    BRIGHT_GREY = ES + '90m'
    BRIGHT_RED = ES + '91m'
    BRIGHT_GREEN = ES + '92m'
    BRIGHT_YELLOW = ES + '93m'
    BRIGHT_BLUE = ES + '94m'
    BRIGHT_MAGENTA = ES + '95m'
    BRIGHT_CYAN = ES + '96m'
    BRIGHT_WHITE = ES + '97m'
    
    RESET = ES + '39m'
    
class BG:
    """
    Contains all 16 Background Colors + Reset
    """
    GREY = ES + '40m'
    RED = ES + '41m'
    GREEN = ES + '42m'
    YELLOW = ES + '43m'
    BLUE = ES + '44m'
    MAGENTA = ES + '45m'
    CYAN = ES + '46m'
    WHITE = ES + '47m'
    
    BRIGHT_GREY = ES + '100m'
    BRIGHT_RED = ES + '101m'
    BRIGHT_GREEN = ES + '102m'
    BRIGHT_YELLOW = ES + '103m'
    BRIGHT_BLUE = ES + '104m'
    BRIGHT_MAGENTA = ES + '105m'
    BRIGHT_CYAN = ES + '106m'
    BRIGHT_WHITE = ES + '107m'
    
    RESET = ES + '49m'