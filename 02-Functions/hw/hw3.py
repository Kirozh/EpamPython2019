counter_name = 0


def make_it_count(func, counter_name):
    def new_func():
        exec(func.__code__)
        globals()[counter_name] += 1  # increasing global variable
    return new_func


def foo():
    print('hello world')


def main():
    mik = make_it_count(foo, 'counter_name')  # calling function
    mik()
    mik = make_it_count(foo, 'counter_name')
    mik()


main()
