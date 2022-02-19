def get(fname):
    try:
        with open(fname, "r") as f:
            return f.read()
    except:
        return None


def set(fname, data):
    with open(fname, "w") as f:
        f.write(data)
