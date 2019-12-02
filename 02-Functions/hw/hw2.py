def atom(data) -> ():

    def get_value():
        nonlocal data
        return data
    def set_value(update = data):
        nonlocal data
        data = update
        return data

    def process(*f):
        nonlocal data
        temp = data
        for c in f:
            temp = (c(data))
            data += 1
        data = temp
        return data

    def delete_value():
        nonlocal data
        del data

    return get_value(), set_value(11), process(square, one_strange_func), delete_value()
    # return process(square, square, one_strange_func)

def square(data):
    return data*data

def one_strange_func(data, proc=100):
    return data//proc


global data
data = 10

vget, vset, veval, vdel = atom(data)
print(vget, vset, veval, vdel)
