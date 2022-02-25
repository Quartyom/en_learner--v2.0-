from libs.qu_json import *

Settings = Qu_json("rsc/settings.json")

@Settings.set_default_func()
def settings_set_default_func():
    Settings.data = dict()
    Settings.add("inactivity_notification_days", 1.5)
    Settings.add("sudden_repeat_chance_1_in", 8)
    Settings.add("find_words_purpose_count", 3)
    Settings.save()


if "inactivity_notification_days" not in Settings.data:
    Settings.set_default()
