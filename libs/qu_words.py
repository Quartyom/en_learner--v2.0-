import time

word_columns = ["translation", "transcription", "notes", "time_label", "repeated_times"]

def add_spaces(*args):
    out = []
    for x in args:
        if type(x) == str:
            out.append(x.replace("_", " "))
        else:
            out.append(x)
    return out

def extend_args(args, number = 0, value = "0"):
    args = list(args)

    if len(args) > number: args = args[:number]
    while len(args) < number: args.append(value)

    return args

def build_word_attrs(args):
    word_attrs = {}

    for index in range(len(args)):
        if args[index] != "0":
            col_name = word_columns[index]
            word_attrs[col_name] = args[index]

    return word_attrs

def copy_word_attrs(word):
    out = ["0"]*len(word_columns)

    for key in word:
        index = word_columns.index(key)
        out[index] = word[key]

    return out

def should_to_repeat(time_label, span):
    if time_label + span <= int(time.time()):
        return True
    else:
        return False

def show_word(en_word, word_data, to_ask_input = True, en_word_first = True):
    arg0 = en_word
    arg1 = word_data["translation"]

    if not en_word_first: arg0, arg1 = arg1, arg0

    outp = ""
    if "transcription" in word_data: outp += f"[{word_data['transcription']}]" + "\t"
    outp += arg1
    if "notes" in word_data: outp += "\n" + word_data["notes"]


    if to_ask_input:
        input(arg0)
        print(outp)

    else:
        print(arg0)
        print(outp)
