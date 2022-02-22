from libs.qu_json import *

class Qu_locale:
    def __init__(self, userdata):
        self._userdata = userdata
        self._tag_file = Qu_json(f"rsc/{self._userdata.data['locale']}/tags.json")

    def get(self, string):
        if string in self._tag_file.data:
            return self._tag_file.data[string]
        elif self._userdata.data["locale"] == "en":
            return string
        else:
            self._tag_file.data[string] = "[RAW]: " + string
            self._tag_file.save()
            return self._tag_file.data[string]

    def load(self):
        self._tag_file = Qu_json(f"rsc/{self._userdata.data['locale']}/tags.json")
