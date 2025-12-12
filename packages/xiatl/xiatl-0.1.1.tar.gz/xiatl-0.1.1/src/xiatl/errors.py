from xiatl.constants import RED_PREFIX, RESET_POSTFIX, BOLD_PREFIX
class Loading_Error(Exception):

    def __init__(self, message):

        super().__init__(message)

class Processing_Error(Exception):

    def __init__(self, message, report=None):

        super().__init__(message)
        self.message = message
        self.report = report

    def __str__(self):

        if self.report is not None:
            return self.message + "\n" + self.report
        else:
            return self.message

class Resolution_Error(Exception):

    def __init__(self, message, report=None):

        super().__init__(message)
        self.message = message
        self.report = report

    def __str__(self):

        if self.report is not None:
            return self.message + "\n" + self.report
        else:
            return self.message

class Expansion_Error(Exception):

    def __init__(self, message, report):

        super().__init__(message)
        self.message = message
        self.report = report

    def __str__(self):

        return self.message + "\n" + self.report

class Execution_Error(Exception):

    def __init__(self, message, report, code, code_message):

        super().__init__(message)
        self.message = message
        self.report = report
        self.code = code
        self.code_message = code_message

    def __str__(self):

        s = self.message + "\n" + self.report.strip()
        s += f"{RED_PREFIX}{self.code}"
        s += f"\n{BOLD_PREFIX}Inline Error: {RESET_POSTFIX}"
        s += f"{RED_PREFIX}{self.code_message}{RESET_POSTFIX}"
        return s
