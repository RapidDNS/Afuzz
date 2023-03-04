import sys
import time
import IPy

class CaseInsensitiveDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._convert_keys()

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = key.lower()

        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.lower()

        return super().__getitem__(key.lower())

    def _convert_keys(self):
        for key in list(self.keys()):
            value = super().pop(key)
            self.__setitem__(key, value)


def calctime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("The {} function takes {} s".format(func.__name__, end_time - start_time))
        return result

    return wrapper


def is_ip(address):
    try:
        IPy.IP(address)
        return True
    except Exception as e:
        return False


def compatible_path(path):
    """
    converts filepaths to be compatible with the host OS
    returns str
    """
    if sys.platform.lower().startswith('win'):
        return path.replace('/', '\\')
    return path
