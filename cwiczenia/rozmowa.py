class new_dic:
    def __init__(self):
        self._list = []
    def set(self, key, value = 0):
        obj = self.get(key)
        if obj:
            obj[1] = value
        else:
            self._list.append([key, value])
    def get(self, key):
        for it in self._list:
            if key == it[0]:
                return it
        return None
    def remove(self, key):
        obj = self.get(key)
        if obj:
            self._list.remove(obj)
        else:
            print("brak elementu" + str(key))
