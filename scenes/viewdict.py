import libs.qu_files
import libs.qu_words
from inits.scene_controller import *
from inits.scene_parsers_init import *
from inits.qu_json_init import *

@viewdict_parser.method("help", 0, 1)
def help_com(*args):
    if not args:
        print("Commands avialable")

        for k in viewdict_parser._methods:
            print(k)

        input("You may also use help help")

    else:
        descr = libs.qu_files.get(f"rsc/commands_descriptions/{args[0]}_viewdict.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/commands_descriptions/{args[0]}.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/commands_descriptions/no_description.txt")
        print(descr[:-1])

@viewdict_parser.method("edit", 0, 4)
def edit_com(*args):
    word = viewdict_parser._get_method_to_method_data()
    print("raw:", f"edit {word} {' '.join(args)}")
    menu_parser.prepare(f"edit {word} {' '.join(args)}")

@viewdict_parser.method("del", 0)
def del_com(*args):
    word = viewdict_parser._get_method_to_method_data()
    menu_parser.prepare(f"del {word}")

@viewdict_parser.method("test_viewdict")
def test_com(*args):
    print("Something uniq from viewdict")

@viewdict_parser.method("menu", 0)
def menu_com(*args):
    viewdict_parser.set_result("change_scene", "menu")

@viewdict_parser.method("learn", 0)
def learn_com(*args):
    viewdict_parser.set_message("change_scene", "learn")

@viewdict_parser.method("exit")
def exit_com(*args):
    viewdict_parser.set_message("change_scene", "exit")

@scene_controller.method("viewdict")
def run():
    print("Words in dictionary:", len(Words.data))

    current_words_list = list(Words.data.keys())
    for en_word in current_words_list:

        libs.qu_words.show_word(en_word, Words.data[en_word], to_ask_input = False)

        viewdict_parser._set_method_to_method_data(en_word)
        viewdict_parser.prepare()
        result_type, result_message = viewdict_parser.get_result()

        # если неуспешное выполнение
        if result_type == "error":
            if result_message == "empty_input":
                pass
            else:
                print(result_message)
            continue

        # если меняется сцена
        elif result_type == "change_scene":
            scene_controller.set_result(result_type, result_message)
            return

        else:
            if result_message: print(result_message)

    print("Слова закончились")
    scene_controller.set_result("change_scene", "menu")
