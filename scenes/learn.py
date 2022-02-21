import random
import libs.qu_files
import libs.qu_words
import libs.qu_datetime as qu_datetime
from inits.scene_controller import *
from inits.scene_parsers_init import *
from inits.qu_json_init import *
from inits.userdata import *

@learn_parser.method("help", 0, 1)
def help_com(*args):
    if not args:
        print("Commands avialable")

        for k in learn_parser._methods:
            print(k)

        print("You may also use help help")

    else:
        descr = libs.qu_files.get(f"rsc/commands_descriptions/{args[0]}_learn.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/commands_descriptions/{args[0]}.txt")
        if not descr: descr = libs.qu_files.get(f"rsc/commands_descriptions/no_description.txt")
        print(descr[:-1])

    learn_parser.set_result("ask_input_again", "from help")

@learn_parser.method("skip", 0)
def skip_com(*args):
    word, foo = learn_parser._get_method_to_method_data()
    Words.data[word]["time_label"] = qu_datetime.now()
    Words.save()

@learn_parser.method("reset", 0)
def reset_com(*args):
    word, foo = learn_parser._get_method_to_method_data()
    menu_parser.prepare(f"reset {word}")
    learn_parser._result = menu_parser.get_result()  # learn parser should know about execution result

@learn_parser.method("edit", 0, 4)
def edit_com(*args):
    word, foo = learn_parser._get_method_to_method_data()
    menu_parser.prepare(f"edit {word} {' '.join(args)}")
    learn_parser._result = menu_parser.get_result()

@learn_parser.method("del", 0)
def del_com(*args):
    word, foo = learn_parser._get_method_to_method_data()
    menu_parser.prepare(f"del {word}")
    learn_parser._result = menu_parser.get_result()

@learn_parser.method("menu", 0)
def menu_com(*args):
    learn_parser.set_result("change_scene", "menu")

@learn_parser.method("viewdict", 0)
def viewdict_com(*args):
    learn_parser.set_result("change_scene", "viewdict")

@learn_parser.method("exit")
def exit_com(*args):
    learn_parser.set_result("change_scene", "exit")

@learn_parser.method("ok")  # attention: userdata save is in the end
def ok_com(*args):
    en_word, is_this_sudden_repeat = learn_parser._get_method_to_method_data()

    if is_this_sudden_repeat:
        learn_parser.set_result("error", "unavilable")
        return

    if not args:
        Words.data[en_word]["repeated_times"] += 1
        Words.data[en_word]["time_label"] = qu_datetime.now()
        # word is learnt
        if Words.data[en_word]["repeated_times"] >= len(Repetition_intervals.data):
            print("congrats, you\'ve learned this word")
            print("it will be deleted, if you wont reset it")
            inp = input("input reset if you wish: ").strip()

            if inp == "reset":
                menu_parser.prepare(f"reset {en_word}")
                learn_parser._result = menu_parser.get_result()
            else:
                Userdata.data["words_learned"] += 1
                menu_parser.prepare(f"del {en_word}")
                learn_parser._result = menu_parser.get_result()

    elif args == ("ok", "ok"):
        key = str(random.randint(1000,9999))
        print("do you wish to mark this word as learned and to delete it?")
        if input(f'input "{key}": ') == key:
            Userdata.data["words_learned"] += 1
            menu_parser.prepare(f"del {en_word}")
            learn_parser._result = menu_parser.get_result()
        else:
            learn_parser.set_result("success", "cancelled")

    else:
        learn_parser.set_result("error", "invalid arguments")

    Userdata.save()

@learn_parser.method("now", 0)
def now_com():
    print(qu_datetime.now())
    learn_parser.set_result("ask_input_again", "from now")

def should_to_repeat_this_word(word_data):
    time_label = word_data["time_label"]
    rep_times = word_data["repeated_times"]
    span = Repetition_intervals.data[rep_times]
    return libs.qu_words.should_to_repeat(time_label, span)

def how_much_to_learn():
    words_list = list(Words.data.keys())
    result = 0
    for en_word in words_list:
        word_data = Words.data[en_word]
        if should_to_repeat_this_word(word_data):
            result += 1
    return result

@scene_controller.method("learn")
def run():
    cn_word_to_ln = how_much_to_learn()

    if cn_word_to_ln > 0:
        print("words to learn:", cn_word_to_ln)
    else:
        print("its nothing to repeat so far")
        scene_controller.set_result("change_scene", "menu")
        return

    is_this_sudden_repeat = False
    is_sudden_repeat_available = True

    while cn_word_to_ln > 0:
        words_list = list(Words.data.keys()) # to get & shuffle words list
        random.shuffle(words_list)

        for en_word in words_list:

            word_data = Words.data[en_word]

            if should_to_repeat_this_word(word_data):
                is_this_sudden_repeat = False
                is_sudden_repeat_available = True
                libs.qu_words.show_word(en_word, word_data, en_word_first = random.randint(0, 1))

            elif is_sudden_repeat_available and random.randint(1,8) == 8:
                is_this_sudden_repeat = True
                is_sudden_repeat_available = False
                print("this is sudden repeatition")
                libs.qu_words.show_word(en_word, word_data, to_ask_input = False)

            else:
                continue

            while True: # there is break in the end, new iteration is on continue only
                learn_parser._method_to_method_data = en_word, is_this_sudden_repeat
                learn_parser.prepare()
                result_type, result_message = learn_parser.get_result()

                if result_type == "error":
                    if result_message == "empty input":
                        pass
                    else:
                        print(result_message)
                        continue

                elif result_type == "change_scene":
                    scene_controller.set_result(result_type, result_message)
                    return

                elif result_type == "ask_input_again":
                    continue

                else:
                    if result_message: print(result_message)

                break

        cn_word_to_ln = how_much_to_learn()

    print("words are over")
    scene_controller.set_result("change_scene", "menu")
