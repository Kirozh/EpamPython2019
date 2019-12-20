characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
              'h', 'i', 'j', 'k', 'l', 'm', 'n',
              'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']

numeral = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


def letters_range(*args, **gloss) -> None:
    """ The function executes range function for letters

    :param args: input *args
    :param gloss: input **kwards
    :return:
    """
    start = 0
    finish = 0
    step = 1

    def return_list(start, finish, step=1, **gloss):
        temp_list = []

        if gloss == {}:
            for i in range(start, finish, step):
                temp_list.append(characters[i])
        else:

            for i in range(start, finish, step):
                if gloss.get(characters[i]) is None:
                    temp_list.append(characters[i])
                else:
                    temp_list.append(gloss[characters[i]])
        return temp_list

    if len(args) == 1:

        if args[0] not in numeral:  # if only-arguement is finish
            start = 0
            finish = characters.index(args[0])
            print(return_list(start, finish))
        elif args[0] in numeral:
            print('Error: The only argument must be letter, not numeral')
        else:
            print('Error: The only argument must be letter')
    elif len(args) == 2:

        if gloss == {}:  # if 2 args are start and finish
            if args[0] in characters and args[1] in characters and \
                    characters.index(args[0]) <= characters.index(args[1]):
                # if both args are letters and ord(first) < ord(second)
                start = characters.index(args[0])
                finish = characters.index(args[1])
                print(return_list(start, finish))
            elif args[0] in characters and type(args[1]) is int:
                start = 0
                finish = characters.index(args[0])
                step = args[1]
                print(return_list(start, finish, step))
            elif type(args[0]) is int:
                print('Error: Arguments must be letter, not numeral')
            elif characters.index(args[0]) > characters.index(args[1]):
                print('Error: Wrong letter order')
        else:

            if args[0] in characters and args[1] in characters:
                # for i in range(characters.index(args[0]), characters.index(args[1]), 1):
                #     if gloss.get(characters[i]) is None:
                #         temp.append(characters[i])
                #     else:
                #         temp.append(gloss[characters[i]])
                # print(temp)

                start = characters.index(args[0])
                finish = characters.index(args[1])
                step = 1
                print(return_list(start, finish, **gloss))
    elif len(args) == 3:

        if args[0] in characters and args[1] in characters:
            if type(args[2]) is int:
                start = characters.index(args[0])
                finish = characters.index(args[1])
                step = args[2]
                print(return_list(start, finish, step))
            else:
                print('Error: Third arguement must be numeral!')
        else:
            print('Error: Arguements must be letters!')
    elif len(args) > 3:
        print('Error: Extra args!')
    elif len(args) == 0:
        print('Error: No input args')


print('range(b, w, 2)')
letters_range('bb', 'w', 2)
print('range(g)')
letters_range('g')
print('range(g, p')
letters_range('g', 'p')
print('range(p, g, -2)')
letters_range('p', 'g', -2)
print('range(a)')
letters_range('a')
glossary = {'l': 7, 'o': '00'}
print('range(g, p, {"l": 7, "o": 00 }')
letters_range('g', 'p', **glossary)