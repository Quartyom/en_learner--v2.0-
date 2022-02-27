import os, time                         # now()
from libs.qu_parse import *             # menu_parser
import libs.qu_words                    # new()
import libs.qu_files                    # help()
import libs.qu_datetime as qu_datetime  # new()
from libs.words_similarity import *
from inits.qu_json_init import *        # new()
from inits.scene_controller  import *   # run()
from inits.scene_parsers_init import *
from inits.userdata import *
from inits.settings import *
from inits.qu_locale_init import *
import inits.mistakes_counter

@scene_controller.method("multy")
def run():
    print(Locale.get("leave input empty to quit"))
    com_name = multy_parser._get_method_to_method_data()
    while True:
        inp = input(">>> ").strip().split()

        # executions
        if inp == ["0"]:
            menu_parser.execute(com_name)
            result_type, result_message = menu_parser.get_result()
            if not result_type: result_type = "success"
        elif inp:
            menu_parser.execute(com_name, *inp)
            result_type, result_message = menu_parser.get_result()
            if not result_type: result_type = "success"
        else:
            scene_controller.set_result("change_scene", "menu") # if input is empty - quit
            return

        # outputs
        if result_type == "error":
            print(Locale.get(result_message))

        # transfer data to scene controller to switch scene
        elif result_type == "change_scene":
            scene_controller.set_result(result_type, result_message)
            return

        elif result_type == "success":
            if result_message: print(Locale.get(result_message))

        # are not supposed to be executed
        else:
            print(result_type)
            if result_message: print(Locale.get(result_message))
