import json

class Qu_json:

    def __init__(self, file_path):
        self.data = dict()
        self.file_path = file_path

        try: self.load()
        except: self.save()

    def save(self):
        with open(self.file_path, "w", encoding = "utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
            return self.data

    def load(self):
        with open(self.file_path, "r", encoding = "utf-8") as file:
            self.data = json.load(file)
            return self.data

    def add(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        return self.data[key]

    def delete(self, key):
        del self.data[key]
        self.save()

    def set_default(self):
        self.data = dict()
        self.save()

    def set_default_func(self):
        def wrap(func):
            self.set_default = func
            return func
        return wrap
