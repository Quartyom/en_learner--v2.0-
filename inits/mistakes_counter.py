value = 0

def get(and_add = True):
    global value

    if and_add: value += 1
    return value
