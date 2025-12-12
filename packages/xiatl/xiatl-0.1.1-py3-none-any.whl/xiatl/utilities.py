class Internal_Error(Exception):
    def __init__(self, message=""):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return self.message + " (this is a bug in XIATL, please report to maintainers)"

def ensure(condition, message=""):
    if not condition:
        raise Internal_Error(message)
