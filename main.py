from inits.userdata import *
from inits.scene_loader import *
from inits.scene_controller import *

current_scene = "menu"
scene_controller._set_method_to_method_data("dont show greetings")  # dont print "you are in menu"

while True:
    scene_controller.prepare(current_scene)
    result_type, result_message = scene_controller.get_result()

    if result_type == "error":
        print(result_message)
        break

    elif result_type == "change_scene":
        current_scene = result_message
        if result_message == "exit": break

    # are not supposed to be executed
    else:
        print(result_type)
        if result_message: print(result_message)

input("Application is finished")
