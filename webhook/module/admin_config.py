import os

OV_APP_HOST_URL = os.getenv('OV_APP_HOST', '127.0.0.1:8000')

DELAY_FOR_BAD_REQUEST = 0.5  # second

DEFAULT_MAX_ACTIVE_BRIDGES = 1
DEFAULT_RATE_LIMIT_PER_URL = 14
DEFAULT_ALLOWED_FREQUENCY = {
    'af1': True,
    'af2': True,
    'af3': True,
    'af4': True
}
DEFAULT_ALLOWED_FILE_FLUSH = {
    'aff1': True,
    'aff2': True,
    'aff3': True,
    'aff4': True,
}
DEFAULT_AVAILABLE_BRIDGE = {
    'ab1': True,
    'ab2': True,
    'ab3': True,
    'ab4': True,
    'ab5': True,
    'ab6': True,
    'ab7': True,
    'ab8': True,
    'ab9': True,
    'ab10': True,
}