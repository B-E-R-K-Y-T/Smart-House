# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Кастомные исключения для проекта

# ----------------------------------------------------------------------------------------------------------------------

class ExceptionErrorProtocol(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ExceptionErrorProtocol: {0}.'.format(self.message)
        else:
            return 'ExceptionErrorProtocol: Unknown protocol!'


class ExceptionErrorCommand(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ExceptionErrorCommand: {0}.'.format(self.message)
        else:
            return 'ExceptionErrorCommand: Unknown command!'


class ExceptionDockerFileNotFound(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ExceptionErrorCommand: {0}.'.format(self.message)
        else:
            return 'ExceptionDockerFileNotFound: Docker file does not exist!'
