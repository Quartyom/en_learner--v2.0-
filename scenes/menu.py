import os, time, random                 # now()
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

@menu_parser.method("help", 0, 1)
def help_com(*args):
    if not args:
        print(Locale.get("commands avialable"))

        commands_available_list = []
        for k in menu_parser._methods:
            if k[0] == "_": continue # hidden
            commands_available_list.append(k)
        print(", ".join(commands_available_list))

        print(Locale.get("you may also use help help"))

    elif args[0] not in menu_parser._methods or args[0][0] == "_":
        print(Locale.get("not found"))
        print(Locale.get("you may use this: help"))
    else:
        locale_path = Userdata.data["locale"]
        descr = libs.qu_files.get(f"rsc/{locale_path}/commands_descriptions/{args[0]}_menu.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/{locale_path}/commands_descriptions/{args[0]}.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/{locale_path}/commands_descriptions/no_description.txt")
        print(descr[:-1])

@menu_parser.method("new")
def new_word_com(*args):
    if len(args) == 0:
        menu_parser.execute("_new_0")
    elif 2 <= len(args) <= 4:
        menu_parser.execute("_new_2_4", *args)
    else:
        menu_parser.set_result("error", "invalid argument(s)")

@menu_parser.method("_new_2_4", 2, 4)
def _new_word_com_2_4(en_word, *args):
    en_word, *args = libs.qu_words.add_spaces(en_word, *args)

    if en_word != "0" and args[0] != "0":
        args = libs.qu_words.extend_args(args,3)
        args.append(qu_datetime.now()) # for time_label
        args.append(0) # for repeated_times

        menu_parser.execute("_new_6", en_word, *args)

    else:
        menu_parser.set_result("error", "dodger :D")

@menu_parser.method("_new_0", 0)
def _new_word_com_0():
    print(Locale.get("unavilable"))

@menu_parser.method("_new_6", 6)
def _new_word_com_6(en_word, *args):
    if en_word not in Words.data:
        word_attrs = libs.qu_words.build_word_attrs(args)
        Words.add(en_word, word_attrs)

        menu_parser.set_result("success", "added")
    else:
        menu_parser.set_result("error", "already exists")


@menu_parser.method("del", 1)
def delete_word_com(en_word):
    if en_word in Words.data:
        Words.delete(en_word)
        menu_parser.set_result("success", "deleted")

    else:
        menu_parser.set_result("error", "not found")

@menu_parser.method("_check", 1, 2)
def _check_word(en_word_dict, to_show_when_to_repeat = True):
    print(en_word_dict)

    if to_show_when_to_repeat:
        time_label = en_word_dict["time_label"]
        repeated_times = en_word_dict["repeated_times"]
        when = time_label + Repetition_intervals.data[repeated_times] - qu_datetime.now()
        if when > 0:
            when_formatted = qu_datetime.seconds_to_form(when)
            print(Locale.get("the next repetition is in"), when_formatted)
        else:
            print(Locale.get("its time to repeat it"))

@menu_parser.method("check", 1)
def check_word_com(en_word):
    if menu_parser._get_method_to_method_data() == "dont show repeat":
        to_show_when_to_repeat = False
    else:
        to_show_when_to_repeat = True

    if en_word in Words.data:
        menu_parser.execute("_check", Words.data[en_word])
    else:
        menu_parser.set_result("error", "not found")

@menu_parser.method("find", 1)
def find_word_com(en_word):
    recommended_to_find = Settings.get("find_words_purpose_count")
    words_by_sequence = []

    for key in Words.data:
        if en_word in key:
            words_by_sequence.append(key.replace(en_word, en_word.upper()))

    if words_by_sequence: print(*words_by_sequence, sep = "\n")

    if len(words_by_sequence) < recommended_to_find:
        how_much_else = recommended_to_find - len(words_by_sequence)

        word_by_dist = find_similar(en_word, Words.data.keys(), how_much_else)

        if how_much_else - len(word_by_dist) == recommended_to_find:
             menu_parser.set_result("error", "not found")
             return

        print(*word_by_dist, sep = "\n")

@menu_parser.method("reset", 1)
def reset_word_com(en_word):
    if en_word in Words.data:
        Words.data[en_word]["time_label"] = int(time.time())
        Words.data[en_word]["repeated_times"] = 0
        menu_parser.set_result("success", "reseted")

    else:
        menu_parser.set_result("error", "not found")

@menu_parser.method("edit", 2, 5)
def edit_word_com(prev_en_word, new_en_word = "1", *args):
    if prev_en_word in Words.data:
        prev_word_dict = Words.data[prev_en_word]
        prev_word_attrs = libs.qu_words.copy_word_attrs(prev_word_dict) # listed attributes
        new_word_attrs = libs.qu_words.extend_args(args, len(prev_word_attrs), value = "1")

        if new_en_word == "1": new_en_word = prev_en_word
        if new_en_word == "0" or new_word_attrs[0] == "0": # if en_word or translation fields are empty
            menu_parser.set_result("error", "you cant do it")
            return

        for index in range(len(prev_word_attrs)): # copies prev_word_attrs attrs to new_word_attrs
            if new_word_attrs[index] == "1":
                new_word_attrs[index] = prev_word_attrs[index]

        if new_word_attrs == prev_word_attrs and new_en_word == prev_en_word: # if the word hasnt changed
            menu_parser.set_result("error", "edited?")
            return

        new_word_attrs = libs.qu_words.add_spaces(*new_word_attrs)
        word_dict = libs.qu_words.build_word_attrs(new_word_attrs)
        menu_parser.execute("_check", word_dict, False)

        inp = input(Locale.get('input "ok" to accept: ')).strip()
        if inp == "ok":
            menu_parser.execute("del", prev_en_word)
            menu_parser.execute("_new_6", new_en_word, *new_word_attrs)
            menu_parser.set_result("success", "edited")
        else:
            menu_parser.set_result("success", "cancelled")
    else:
        menu_parser.set_result("error", "not found")

@menu_parser.method("now", 0)
def now_com():
    print(qu_datetime.now())

@menu_parser.method("reload", 0)
def reload_com():
    Words.load()
    Userdata.load()
    Locale.load()
    Settings.load()
    menu_parser.set_result("success", "resources are reloaded")

@menu_parser.method("default", 0)
def reload_com():
    key = str(random.randint(1000,9999))
    print(Locale.get("This action is irreversable. All application data will be set to default values"))
    if input(f'input "{key}": ') == key:
        Words.set_default()
        Userdata.set_default()
        Settings.set_default()
        menu_parser.set_result("success", "resources are default")
    else:
        menu_parser.set_result("success", "cancelled")

@menu_parser.method("locale", 1)
def locale_com(arg):
    if not os.path.exists(f"rsc/{arg}"):
        menu_parser.set_result("error", "no such locale")
    elif not os.path.exists(f"rsc/{arg}/tags.json"):
        menu_parser.set_result("error", "no tags found")
    elif not os.path.exists(f"rsc/{arg}/commands_descriptions"):
        menu_parser.set_result("error", "commands descriptions are not found")
    elif not os.path.exists(f"rsc/{arg}/commands_descriptions/no_description.txt"):
        menu_parser.set_result("error", "file no_description.txt is not found")
    else:
        Userdata.data["locale"] = arg
        Userdata.save()
        Locale.load()
        menu_parser.set_result("success", "locale changed")

#@menu_parser.method("multy", 1)
#def multy_com(com_name):
#    menu_parser.set_result("change_scene", "multy")

@menu_parser.method("settings", 0, 2)
def settings_com(*args):
    if len(args) == 0:
        print(Locale.get("settings available"))
        keys = Settings.data.keys()
        for key in keys:
            print(f"{key} : {Settings.data[key]}")

    elif len(args) == 1:
        key = args[0]
        if key in Settings.data:
            print(Settings.data[key])
        else:
            menu_parser.set_result("error", "not found")
    else:
        key, new_value = args
        if key in Settings.data:
            old_value = Settings.get(key)

            try:
                new_value = type(old_value)(new_value)

                if new_value == old_value:
                    menu_parser.set_result("error", "edited?")
                    return

                print(Locale.get("the new value will be:"), new_value)

                inp = input(Locale.get('input "ok" to accept: ')).strip()
                if inp == "ok":
                    Settings.add(key, new_value)
                    menu_parser.set_result("success", "edited")
                else:
                    menu_parser.set_result("success", "cancelled")
            except:
                menu_parser.set_result("error", "invalid argument(s)")
        else:
            menu_parser.set_result("error", "not found")

@menu_parser.method("donate", 0)
def donate_com(*args):
    menu_parser.set_result("success", "maybe in the next version")

@menu_parser.method("about", 0)
def about_com(*args):
    info = libs.qu_files.get("rsc/about.txt")
    print(info, end = str())

@menu_parser.method("license", 0)
def license_com(*args):
    info = libs.qu_files.get("rsc/license.txt")
    print(info, end = str())

@menu_parser.method("stats", 0)
def stats_com(*args):
    _data = Userdata.data
    usage_time = qu_datetime.now() - _data["the_first_launch"]
    usage_time_formatted = qu_datetime.seconds_to_form(usage_time)
    print(Locale.get("you\'re using app for"), usage_time_formatted)
    print(Locale.get("words learned:"), _data["words_learned"])
    print(Locale.get("words are being learned:"), len(Words.data))

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
    if scene_controller._get_method_to_method_data() != "dont show greetings":
        print(Locale.get("you are in menu"))
    while True:
        menu_parser.prepare()
        result_type, result_message = menu_parser.get_result()

        if result_type == "error":
            if result_message == "empty input":
                pass
            else:
                print(Locale.get(result_message))
                if inits.mistakes_counter.get() % 3 == 0:
                    print(Locale.get("you may use this: help"))
            continue

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
