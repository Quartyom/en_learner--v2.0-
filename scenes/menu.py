import os, time                         # now()
from libs.qu_parse import *             # menu_parser
import libs.qu_words                    # new()
import libs.qu_files                    # help()
import libs.qu_datetime as qu_datetime  # new()
from inits.qu_json_init import *        # new()
from inits.scene_controller  import *   # run()
from inits.scene_parsers_init import *
from inits.userdata import *

@menu_parser.method("help", 0, 1)
def help_com(*args):
    if not args:
        print("Commands avialable")
        for k in menu_parser._methods:
            print(k)
        input("You may also use help help")

    else:
        descr = libs.qu_files.get(f"rsc/commands_descriptions/{args[0]}_menu.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/commands_descriptions/{args[0]}.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/commands_descriptions/no_description.txt")
        print(descr[:-1])

@menu_parser.method("new", 2, 4)
def new_word_com(en_word, *args, to_show_result = True):
    en_word, *args = libs.qu_words.add_spaces(en_word, *args)

    if en_word != "0" and args[0] != "0":
        if en_word not in Words.data:
            if len(args) == 6: # системный вызов (из edit())
                pass
            else:
                args = libs.qu_words.extend_args(args,3)
                args.append(qu_datetime.now()) # for time_label
                args.append(0) # for repeated_times

            word_attrs = libs.qu_words.build_word_attrs(args)
            Words.add(en_word, word_attrs)

            if to_show_result: print("added")
        else:
            if to_show_result: print("Already exists")
            menu_parser.set_result("error", "Already exists")
    else:
        if to_show_result: print("Dodger")

@menu_parser.method("del", 1)
def delete_word_com(en_word, to_show_result = True):

    if en_word in Words.data:
        Words.delete(en_word)
        if to_show_result: print("deleted")
    else:
        if to_show_result: print("Not found")

@menu_parser.method("check", 1)
def check_word_com(en_word, to_show_when_to_repeat = True):
    if en_word in Words.data:
        print(Words.data[en_word])

        if to_show_when_to_repeat:
            time_label = Words.data[en_word]["time_label"]
            repeated_times = Words.data[en_word]["repeated_times"]
            when = time_label + Repetition_intervals.data[repeated_times] - qu_datetime.now()
            if when > 0:
                when_formatted = qu_datetime.seconds_to_form(when)
                print("Следующее повторение через", when_formatted)
            else:
                print("Слово пора повторять")
    else:
        print("WordNot found")

@menu_parser.method("find", 1)
def find_word_com(en_word):
    is_any_found = False

    for key in Words.data:
        if en_word in key:
            print(key.replace(en_word, en_word.upper()))
            is_any_found = True

    if not is_any_found:
        print("Not found")

@menu_parser.method("reset", 1)
def reset_word_com(en_word):
    if en_word in Words.data:
        Words.data[en_word]["time_label"] = int(time.time())
        Words.data[en_word]["repeated_times"] = 0
        print("Reseted")
    else:
        print("Not found")

@menu_parser.method("edit", 2, 5)
def edit_word_com(prev_en_word, new_en_word = "1", *args):
    if prev_en_word in Words.data:
        prev_word = Words.data[prev_en_word]
        prev_word_attrs = libs.qu_words.copy_word_attrs(prev_word)
        new_word_attrs = libs.qu_words.extend_args(args, len(prev_word_attrs), value = "1")

        if new_en_word == "1": new_en_word = prev_en_word
        if new_en_word == "0" or new_word_attrs[0] == "0":
            print("Так делать запрещено")
            return

        for index in range(len(prev_word_attrs)):
            if new_word_attrs[index] == "1":
                new_word_attrs[index] = prev_word_attrs[index]

        if new_word_attrs == prev_word_attrs and new_en_word == prev_en_word:
            print("edited?")
            return

        new_word_com(new_en_word, *new_word_attrs, to_show_result = False)

        check_word_com(new_en_word, to_show_when_to_repeat = False)
        inp = input('Input "ok" to accept: ').strip()
        if inp == "ok":
            delete_word_com(prev_en_word, to_show_result = False)
            print("edited")
        else:
            delete_word_com(new_en_word, to_show_result = False)
            print("cancelled")
    else:
        print("Not found")

@menu_parser.method("now", 0)
@viewdict_parser.method("now", 0)
@learn_parser.method("now", 0)
def now_com():
    print(qu_datetime.now())

@menu_parser.method("locale", 1)
def locale_com(*args):
    print("No implementation provided")

@menu_parser.method("donate", 0)
def locale_com(*args):
    print("Maybe in the next version")

@menu_parser.method("about", 0)
def locale_com(*args):
    print("No implementation provided")

@menu_parser.method("license", 0)
def locale_com(*args):
    print("No implementation provided")

@menu_parser.method("stats", 0)
def locale_com(*args):
    _data = Userdata.data
    usage_time = qu_datetime.now() - _data["the_first_launch"]
    usage_time_formatted = qu_datetime.seconds_to_form(usage_time)
    print("You\'re using app for", usage_time_formatted)
    print("Words learned:", _data["words_learned"])
    print("Words are being learned:", len(Words.data))

@menu_parser.method("clear", 0)
@learn_parser.method("clear", 0)
@viewdict_parser.method("clear", 0)
def clear_com():
    os.system("cls")

@menu_parser.method("learn", 0)
def learn_com():
    menu_parser.set_result("change_scene", "learn")

@menu_parser.method("viewdict", 0)
def viewdict_com():
    menu_parser.set_result("change_scene", "viewdict")

@menu_parser.method("exit")
def exit_com(*args):
    menu_parser.set_result("change_scene", "exit")

@scene_controller.method("menu")
def run():
    print("Вы в меню")
    while True:
        menu_parser.prepare()
        result_type, result_message = menu_parser.get_result()

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

        elif result_type == "success":
            pass

        else:
            if result_message: print(result_message)
