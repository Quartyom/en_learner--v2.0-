import libs.qu_files
import libs.qu_words
import libs.qu_datetime as qu_datetime
from inits.scene_controller import *
from inits.scene_parsers_init import *
from inits.qu_json_init import *
from inits.userdata import *
from inits.settings import *
from inits.qu_locale_init import *
import inits.mistakes_counter

@viewdict_parser.method("help", 0, 1)
def help_com(*args):
    if not args:
        print(Locale.get("commands avialable"))

        commands_available_list = []
        for k in viewdict_parser._methods:
            if k[0] == "_": continue # hidden
            commands_available_list.append(k)
        print(", ".join(commands_available_list))

        print(Locale.get("you may also use help help"))

    elif args[0] not in menu_parser._methods or args[0][0] == "_":
        print(Locale.get("not found"))
        print(Locale.get("you may use this: help"))
    else:
        locale_path = Userdata.data["locale"]
        descr = libs.qu_files.get(f"rsc/{locale_path}/commands_descriptions/{args[0]}_viewdict.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/{locale_path}/commands_descriptions/{args[0]}.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/{locale_path}/commands_descriptions/no_description.txt")
        print(descr[:-1])

    viewdict_parser.set_result("ask_input_again", "from help")

@viewdict_parser.method("edit", 0, 4)
def edit_com(*args):
    word = viewdict_parser._get_method_to_method_data()
    menu_parser.execute("edit", word, *args)
    viewdict_parser._result = menu_parser.get_result() # viewdict parser should know about execution result

@viewdict_parser.method("del", 0)
def del_com():
    word = viewdict_parser._get_method_to_method_data()
    menu_parser.execute("del", word)
    viewdict_parser._result = menu_parser.get_result()

@viewdict_parser.method("menu", 0)
def menu_com(*args):
    viewdict_parser.set_result("change_scene", "menu")

@viewdict_parser.method("learn", 0)
def learn_com(*args):
    viewdict_parser.set_result("change_scene", "learn")

@viewdict_parser.method("exit")
def exit_com(*args):
    viewdict_parser.set_result("change_scene", "exit")

@viewdict_parser.method("now", 0)
def now_com():
    print(qu_datetime.now())
    viewdict_parser.set_result("ask_input_again", "from now")

@viewdict_parser.method("reload", 0)
def reload_com():
    menu_parser.execute("reload")
    print(Locale.get("resources are reloaded"))
    viewdict_parser.set_result("ask_input_again", "from reload")

@scene_controller.method("viewdict")
def run():
    print(Locale.get("words in dictionary:"), len(Words.data))

    current_words_list = list(Words.data.keys())
    random.shuffle(current_words_list)

    for en_word in current_words_list:

        libs.qu_words.show_word(en_word, Words.data[en_word], to_ask_input = False)

        while True: # there is break in the end, new iteration is on continue only
            viewdict_parser._set_method_to_method_data(en_word)
            viewdict_parser.prepare()
            result_type, result_message = viewdict_parser.get_result()

            if result_type == "error":
                if result_message == "empty input":
                    pass
                else:
                    print(Locale.get(result_message))
                    if inits.mistakes_counter.get() % 3 == 0:
                        print(Locale.get("you may use this: help"))
                    continue

            elif result_type == "change_scene":
                scene_controller.set_result(result_type, result_message)
                return

            elif result_type == "ask_input_again":
                continue

            else:
                if result_message: print(Locale.get(result_message))

            break

    print(Locale.get("words are over"))
    scene_controller.set_result("change_scene", "menu")
