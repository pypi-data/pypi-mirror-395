def set_log_level(level):
    with open('LOGGING_LEVEL', 'w') as f:
        f.write(level)

def get_log_level():
    try:
        with open('LOGGING_LEVEL', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return 'INFO'
