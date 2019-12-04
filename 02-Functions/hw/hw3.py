import inspect

counter_name = -10
def make_it_count(func, counter):
    temp = namevar(counter)[0]
    print(temp)
    exec('global temp')
    temp1 = globals().get(counter)
    # print(temp1)
    inspect.getsource(func)
    exec('print(temp)')
    # exec('namevar(counter_name)[0] += 1')
    # exec('return namevar(counter_name)[0]')
    # exec('return temp')
    return
    print(counter_name)
    counter_name=0
    print(counter)
    counter_name += 1


def func():
    print('Hello worlds!')

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def namevar(var):
    return [name for name, value in inspect.currentframe().f_back.f_locals.items() if value is var]


# print(make_it_count(func, 'counter_name'))
make_it_count(func, 'counter_name')
# print(inspect.getsource(func))
# print(inspect.Parameter(counter_name))