def func(*args, **kwards):
    pass


def modified_func(func,  *args, **kwards):
    def new_func(*new_args, **new_kwards):
        if new_args == () and new_kwards == {}:
            sig = signature(func)
            func(*args, **kwards)
        else:

        pass
    return new_func

modified_func(func )