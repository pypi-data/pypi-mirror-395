class CancelException(Exception):
    def __init__(self, message="Unrecoverable error"):
        super().__init__(message)
