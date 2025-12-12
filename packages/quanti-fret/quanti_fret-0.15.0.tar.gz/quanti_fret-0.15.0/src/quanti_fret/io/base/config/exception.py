from quanti_fret.core import QtfException


class QtfConfigException(QtfException):
    """Custom exception for configuration errors in QTFret."""
    def __init__(self, message):
        message = f'Config error: {message}'
        super().__init__(message)
