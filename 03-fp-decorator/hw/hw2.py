def num_length(number):
    if number == 0:
        return 0
    else:
        return 1 + num_length(number//10)


def is_armsrong(number):
    length = num_length(number)

    def armstrong(number_):
        nonlocal length
        if number_ == 0:
            return 0
        else:
            return pow(number_ % 10, length) + armstrong(number_//10)

    return armstrong(number) == number


assert is_armsrong(153) == True
