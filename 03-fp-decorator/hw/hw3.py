def collatz_steps(number):
    if number <= 1:
        return 0
    else:
        if number % 2 == 0:
            return 1+collatz_steps(number//2)
        else:
            return 1+collatz_steps(3*number+1)


assert(collatz_steps(1000000)) == 152
