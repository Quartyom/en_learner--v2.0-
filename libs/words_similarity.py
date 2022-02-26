import importlib
try:
    importlib.import_module("Levenshtein")
except ImportError:
    import pip
    pip.main(['install', "Levenshtein"])
finally:
    globals()["Levenshtein"] = importlib.import_module("Levenshtein")


def find_similar(word, words_list, how_many):
    out = []

    for item in words_list:
        dist = Levenshtein.distance(word, item)
        abs_dist = dist/len(word)

        out.append([abs_dist, item])

    out.sort()
    out = [x[1] for x in out]

    if len(out) < how_many:
        return out
    else:
        return out[:how_many]
