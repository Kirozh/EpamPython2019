def atom(data=None):
    """ The function encapsulates variable data

    :param data: input variable
    :return vget, vset, veval, vdel: output functions that set, get, deletes and produces values
    """

    def get_value():
        global data
        return data

    def set_value(update=data):
        global data
        data = update
        return data

    def process(*f):
        global data
        for c in f:
            data = c()
        return data

    def delete_value():
        global data
        del data

    return get_value, set_value, process, delete_value


def square():  # one of functions to apply
    return data * data


def one_strange_func(proc=5):  # one of functions to apply
    return data % proc


''' Main part

'''
data = 10

vget, vset, veval, vdel = atom()
print(vset(12))
print(vget())
print(vset(14))
print(data)
print(veval(one_strange_func, square, one_strange_func))
vdel()

