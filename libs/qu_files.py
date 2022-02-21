def get(fname):
    try:
        with open(fname, "r", encoding = 'utf-8') as f:
            return f.read()
    except:
        return None


def set(fname, data):
    with open(fname, "w", encoding = 'utf-8') as f:
        f.write(data)
