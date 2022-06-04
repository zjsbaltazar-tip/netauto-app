class Options(object):

    def __init__(self):
        self._dict = {}
    
    def __iadd__(self, obj: tuple):
        if isinstance(obj, tuple):
            self._dict[obj[0]] = [obj[1], lambda: None]
        return self

    def getall(self) -> dict:
        return self._dict

    def get(self, key):
        if key in self._dict:
            return self._dict[key]

    def connect(self, key, func):
        if key in self._dict:
            self._dict[key][1] = func
            return True
        return False

    def trigger(self, key) -> bool :
        if key in self._dict:
            self._dict[key][1]()
            return True
        return False
            