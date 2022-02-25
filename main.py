# pip install python-Levenshtein
import libs.qu_datetime
from inits.userdata import *
from inits.settings import *
from inits.scene_loader import *
from inits.scene_controller import *
from inits.qu_locale_init import *

if delta_from_the_last_launch > libs.qu_datetime.form_to_seconds(days = Settings.get("inactivity_notification_days")):
    print(Locale.get("you havent been there for "),
        libs.qu_datetime.seconds_to_form(delta_from_the_last_launch),
        Locale.get(", come back more often"), sep = "")

current_scene = "menu"
scene_controller._set_method_to_method_data("dont show greetings")  # dont print "you are in menu"

while True:
    scene_controller.prepare(current_scene)
    result_type, result_message = scene_controller.get_result()

    if result_type == "error":
        print(Locale.get(result_message))
        break

    elif result_type == "change_scene":
        current_scene = result_message
        if result_message == "exit": break

    # are not supposed to be executed
    else:
        print(result_type)
        if result_message: print(Locale.get(result_message))

input(Locale.get("application is finished"))
