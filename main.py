from inits.userdata import *
from inits.scene_loader import *
from inits.scene_controller import *

current_scene = "menu"
while True:
    scene_controller.prepare(current_scene)
    result_type, result_message = scene_controller.get_result()

    # если неуспешное выполнение
    if result_type == "error":
        print(result_message)
        break

    # если меняется сцена
    elif result_type == "change_scene":
        if result_message == "exit": break
        current_scene = result_message

    else:
        if result_message: print(result_message)

input("Application is finished")
