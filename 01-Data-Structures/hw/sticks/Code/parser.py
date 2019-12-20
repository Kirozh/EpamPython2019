
first_input_file = 'winedata_1.json'
second_input_file = 'winedata_2.json'


def parsing(file_name):
    """ The function parses input data file and makes list of dictionaries each of whom is wine

    :param file_name: input data file
    :return: list of wine dictionaries
    """

    data_file = open(file_name, 'r', encoding='UTF-8')

    wine_record_list = []  # array of wine records
    stack_of_parentheses = []  # stack contains symbols '{', '[' , '}', ", and ']'
    c = data_file.read(1)
    stack_of_parentheses.append(c)
    wine_dict = {}  # exemplar of wine-info dictionary
    inside = False  # true if current symbol is in word, else false
    key = value = ''  # key and value arrays
    key_or_value = -1  # -1 if current symbol in key , 1 if current symbol in value
    stack_size = len(stack_of_parentheses)

    while stack_size != 0:
        c = data_file.read(1)

        if c == '[':  # startring parsing and adding [ to stack
            if not inside:
                if stack_of_parentheses[-1] != '[':
                    stack_of_parentheses.append(c)
            else:
                value += c

        if c == '{':  # starting of new dictionary
            stack_of_parentheses.append(c)
            inside = False

        if c == '"' and stack_of_parentheses[-1] != '"':  # this " is opening
            stack_of_parentheses.append(c)
            inside = True

            if key_or_value == -1:  # this " in key
                key = ''

            value = ''

        elif c == '"' and stack_of_parentheses[-1] == '"':  # this " is closing
            inside = False
            stack_of_parentheses.pop(-1)

            if key_or_value < 0:  # ending of key
                key_or_value = 1

            else:  # ending value
                key_or_value = -1

        if key_or_value < 0 and inside and c != '"':  # collecting symbols to key
            if key_or_value < 0:
                key += c

        if c == ':' and not inside:  # this : shares key and value
            key_or_value = 1

        if c == ',' and not inside and stack_of_parentheses[-1] == '{':  # this ',' is after pair key-value
            key_or_value = -1
            if value.strip() == "null" or (value.strip().isdigit() and key != 'points'):
                wine_dict.update({'"' + key + '"': value.lstrip()})
            else:
                wine_dict.update({'"'+key+'"': '"'+value.lstrip()+'"'})

        if key_or_value > 0 and c != '"' and c != ':':  # collecting symbols to value
            value += c

        if c == '}':  # ending wine-information
            stack_of_parentheses.pop(-1)
            inside = False
            wine_dict.update({'"'+key+'"': '"'+value.lstrip()+'"'})
            wine_record_list.append(wine_dict.copy())

            wine_dict.clear()

        if c == ']':  # ending list of wines
            if not inside:
                stack_of_parentheses.pop(-1)
            else:
                value += c

        stack_size = len(stack_of_parentheses)

    data_file.close()
    return wine_record_list


# def merging(d_list_1, d_list_2):
#     """ the function merges two lists
#     :param d_list_1: input list of dictionaries
#     :param d_list_2: input list of dictionaries
#     :return: merged list
#
#     """
#
#     temp_list = d_list_1.copy()
#     temp_list.extend(d_list_2)
#     return temp_list


def find_duplicate(d_list_1, d_list_2):
    """ The function gets two lists of dictionaries. It runs along first list
        and tries to find identical dictionary in another list
    finally, it merges two lists in merged_list

    :param d_list_1: input list of dictionaries
    :param d_list_2: input list of dictionaries
    :return: merged list

    """

    for x in d_list_1:
        length_file_2 = len(d_list_2)
        i = 0
        while i < length_file_2 and x.values() != d_list_2[i].values():  # while two simular dictionaries won`t be found
            i += 1
        if i != length_file_2:
            print(d_list_2.pop(i))

    merged_list = d_list_1.copy()
    merged_list.extend(d_list_2)
    return merged_list


def count_null_(merged_list):
    """ The function finds number of null-prices-wines in merged list
    :param merged_list:
    :return: number of null-prices-wines

    """
    count_null = 0

    for x in merged_list:
            if x.get('"price"') == 'null':
                count_null += 1

    return count_null


def push_null_in_the_end(merged_list):
    """ The function pushes dictionaries with null-price-wines to the end of list
    
    :param merged_list: input merged list
    :return: modified merged list

    """

    count_null = count_null_(merged_list)
    i = 0
    length = len(merged_list)

    # push null-price-dictionaries to the end
    while i < length - count_null:
        j = i
        x = merged_list[j].copy()
        if x['"price"'] == 'null':
            x = merged_list[j + 1].copy()

            if x.get('"price"') != 'null':
                i += 1

            temp_dict = merged_list.pop(j).copy()
            merged_list.append(temp_dict.copy())

        else:
            i += 1

    return merged_list


"""
quick_sort(merged_list, fst, lst)
sorting merged list by Quick sort algorithm
"""


def quick_sort(merged_list, fst, lst):

    if fst >= lst:
        return

    i, j = fst, lst
    pivot = merged_list[random.randint(fst, lst)]

    while i <= j:
        while int(merged_list[i].get('"price"')) < int(pivot.get('"price"')):
            i += 1
        while int(merged_list[j].get('"price"')) > int(pivot.get('"price"')):
            j -= 1
        if i <= j:

            merged_list[i], merged_list[j] = merged_list[j], merged_list[i]
            i, j = i + 1, j - 1

    quick_sort(merged_list, fst, j)
    quick_sort(merged_list, i, lst)


def wine_sort_information(sort, merged_lists):
    """ The function get sort of wine and returns sort`s information:
    - max price
    - min price
    - most common country
    - most common region
    - average price
    - score

    :param sort: name of wine sort
    :param merged_lists: input list of wine`s records
    :return:

    """

    average_price = 0
    price = 0
    min_price = sys.float_info.max
    max_price = -1
    average_score = 0
    score = 0
    sort_count = 0
    countries = {}  # dictionary of counties where the sort was produced and matched to them numbers
    regions = {}  # dictionary of regions where the sort was produced and matched to them numbers

    for x in merged_lists:
        # if x['variety'] == sort:
        if x['"variety"'].find(sort) != -1 or (x.get('"title"') is not None and x['"title"'].find(sort) != -1):
            # if sort was mentioned in title or in variety

            sort_count += 1
            if x['"price"'] != 'null':  # if price isn`t null, checking if it is max or min
                price += int(x['"price"'])
                if sort_count == 1:  # Because merged list has already been sorted
                    min_price = int(x['"price"'])
                if int(x['"price"']) > max_price:
                    max_price = int(x['"price"'])

            cur_country = x['"country"']  # searching for most coomon countries
            if cur_country != 'null':
                if countries.get(cur_country) is None:  # if the country haven`t been in country dictionary
                    countries.update({x['"country"']: 1})
                else:  # if already have this country in dictionary
                    countries.update({x['"country"']: int(countries[cur_country]) + 1})

            cur_region = x['"region_1"']  # searching for most common region
            if cur_region != 'null':
                if regions.get(cur_region) is None:  # if the region haven`t been in region dictionary
                    regions.update({x['"region_1"']: 1})
                else:
                    regions.update({x['"region_1"']: int(regions[cur_region]) + 1})

            cur_region = x['"region_2"']
            if cur_region != 'null':
                if regions.get(cur_region) is None:
                    regions.update({x['"region_2"']: 1})
                else:
                    regions.update({x['"region_2"']: int(regions[cur_region]) + 1})

            score += int(x['"points"'][1:-1])

    if sort_count != 0:
        average_price = float(price) / sort_count
        average_score = float(score) / sort_count
    else:
        max_price = 0
        min_price = 0

    max_count_country_name = ''
    max_count_countries = 0
    # searching for most common country
    for key in countries:
        if countries[key] > max_count_countries:
            max_count_countries = countries[key]
            max_count_country_name = key

    max_count_region_name = ''
    max_count_regions = 0
    # searching for most common region
    for key in regions:
        if regions[key] > max_count_regions:
            max_count_regions = regions[key]
            max_count_region_name = key
    # if the wine is not in dictionary, then no country and no region produce it
    if max_count_countries == 0:
        max_count_country_name = '"null"'
    if max_count_regions == 0:
        max_count_region_name = '"null"'

    return {'"average price"': average_price,
            '"max price"': max_price,
            '"min price"': min_price,
            '"most common country"': max_count_country_name,
            '"most common region"': max_count_region_name,
            '"average score"': average_score
            }


def sorts_information(wine_sorts, merged_lists):
    """ The function applies wine_sort_information function for each sort in wine_sorts
    :param wine_sorts: list of wines
    :param merged_lists: merged list

    """
    sorts_info = []  # array of information of each wine sort from 'Gewurztraminer', 'Gewürztraminer', ext...
    for wine in wine_sorts:
        sorts_info.append({wine: wine_sort_information(wine, merged_lists)})

    return sorts_info


def search_extremum_in_dictionary(dikt, mode):
    """ The function search for max/min value in dictionary depending on mode

    :param dikt: input dictionary
    :param mode:
    :return:
    """

    extremal_keys = []
    extremal = 0
    if mode == 'min':
        extremal = sys.float_info.max
        for x in dikt:
            if int(dikt[x]) < extremal:
                extremal = (dikt[x])
                extremal_keys.clear()
                extremal_keys.append(x)
            elif int(dikt[x]) == extremal:
                extremal_keys.append(x)
    elif mode == 'max':
        extremal = sys.float_info.min
        for x in dikt:
            if int(dikt[x]) > extremal:
                extremal = (dikt[x])
                extremal_keys.clear()
                extremal_keys.append(x)
            elif int(dikt[x]) == extremal:
                extremal_keys.append(x)

    return extremal_keys, extremal


def array_to_str(array_):
    """ The function translates input list in str if the list contains only 1 element, unless returns input list

    :param array_:
    :return:
    """
    if len(array_) == 1:
        return str(array_[0])
    else:
        return array_


def wine_records(merged_lists):
    """ The functions searches for wine records
    function finds information:
    - max / min price
    - average price
    - most rated / underrated countries
    - most_expensive_coutry
    - cheapest_coutry
    - most_active_commentator
    :param merged_lists: input data list
    :return: dictionary with records

    """

    most_expensive_wine_title = [] # most expensive countries
    most_expensive_wine_cost = 0 # most expensive cost is matched to most expensive wine title
    cheapest_wine_title = []
    cheapest_wine_cost = sys.float_info.max
    highest_score = 0
    highest_score_title = []  # list of wines with highest score
    lowest_score = 1000
    lowest_score_title = []  # list of wines with lowest score
    country_price = {}  # dictionary where countries are keys and sum of prices for each country are values
    country_price_entrances = {}  # dictionary matched to country_price where countries are keys and number of
    # founding them in input list of dictionaries are values
    country_rating = {}  # dictionary where countries are keys and sum of points are values
    country_rating_entrances = {}  # dictionary matched to previous where keys are countries and values are
    # number of entrance for eac country in input file
    most_expensive_country_title = []
    cheapest_country_title = []
    tasters = {}

    for x in merged_lists:
        '''
            Searching for most active commentator
        '''
        if x['"taster_name"'] != 'null':  # forming tasters` dictionary
            if tasters.get(x['"taster_name"']) is None:
                tasters.update({x['"taster_name"']: 1})
            else:
                tasters.update({x['"taster_name"']: int(tasters[x['"taster_name"']]) + 1})

        if x['"country"'] != 'null':
            ''' 
            Searching for most expensive/cheapest countries
            '''
            cur_country = x['"country"']
            if country_price.get(cur_country) is None:
                # if current country hasn`t already been added to country_price dict
                if x['"price"'] != 'null':
                    country_price.update({cur_country: int(x['"price"'])})
                    country_price_entrances.update({cur_country: 1})
            else:
                # if current country has already been added to country_price dict
                if x['"price"'] != 'null':
                    # summarizing wine`s cost for the country
                    country_price.update({cur_country: int(x['"price"']) + country_price[cur_country]})
                    # summarizing wine`s entrancenses for the country
                    country_price_entrances.update({cur_country: country_price_entrances[cur_country] + 1})

            ''' 
            Searching for most rated/underrated countries
            '''
            if country_rating.get(cur_country) is None:
                # if current country hasn`t already been added to country_rating dict
                if x['"points"'] != 'null':
                    country_rating.update({cur_country: int(x['"points"'][1:-1])})
                    country_rating_entrances.update({cur_country: 1})
            else:
                # if current country has already been added to country_rating dict
                if x['"points"'] != 'null':
                    # summarizing wine`s cost for the country
                    country_rating.update({cur_country: int(x['"points"'][1:-1]) + country_rating[cur_country]})
                    # summarizing wine`s entrancens for the country
                    country_rating_entrances.update({cur_country: country_rating_entrances[cur_country] + 1})

        ''' 
        Searching for most expensive/cheapest wine 
        '''
        if x['"price"'] != 'null':  # if price is not null
            if int(x['"price"']) > most_expensive_wine_cost:  # if current price is higher than most_expensive_wine_cost
                most_expensive_wine_cost = int(x['"price"'])
                most_expensive_wine_title.clear()
                most_expensive_wine_title.append(x['"title"'])

            elif int(x['"price"']) == most_expensive_wine_cost:  # if current price is equal to expensive cost
                if x.get('"title"') is not None:
                    most_expensive_wine_title.append(x['"title"'])

            if int(x['"price"']) < cheapest_wine_cost:  # if current price is lower than cheapest_wine_cost
                cheapest_wine_cost = int(x['"price"'])
                cheapest_wine_title.clear()
                cheapest_wine_title.append(x['"title"'])

            elif int(x['"price"']) == cheapest_wine_cost:  # if current price is equal to cheapest cost
                if x.get('"title"') is not None:
                    cheapest_wine_title.append(x['"title"'])

        '''
        Searching for wines with highest/lowest score
        '''
        if int(x['"points"'][1:-1]) > int(highest_score):  # if current points is higher than highest_score
            highest_score = int(x['"points"'][1:-1])

            highest_score_title.clear()
            highest_score_title.append(x['"title"'])

        elif int(x['"points"'][1:-1]) == int(highest_score):  # if current points are equal to highest
            highest_score_title.append(x['"title"'])

        if int(x['"points"'][1:-1]) < int(lowest_score):  # if current points are lower than lowest_score
            lowest_score = int(x['"points"'][1:-1])

            lowest_score_title.clear()
            lowest_score_title.append(x['"title"'])

        elif int(x['"points"'][1:-1]) == int(lowest_score):  # if current points are equal to lowest
            lowest_score_title.append(x['"title"'])

    # searching for most active tasters
    most_active_taster_name, taster_count = search_extremum_in_dictionary(tasters, 'max')

    # search for country with most expensive/cheapest average price
    country_average_price = {}
    for country in country_price:
        country_average_price.update(
            {country: (country_price[country]) / country_price_entrances[country]})
        most_expensive_country_title, \
        most_expensive_country_average_price = search_extremum_in_dictionary(country_average_price, 'max')
        cheapest_country_title, \
        cheapest_country_average_price = search_extremum_in_dictionary(country_average_price, 'min')

    # search for country with most rated/underrated score
    country_average_rating = {}
    for country in country_rating:
        country_average_rating.update({country: (country_rating[country]) / country_rating_entrances[country]})

    most_rated_country_title, \
    most_rated_country_average_score = search_extremum_in_dictionary(country_average_rating, 'max')

    most_underrated_country_title, \
    most_underrated_country_average_score = search_extremum_in_dictionary(country_average_rating, 'min')

    return (
            array_to_str(most_expensive_wine_title),  # if the list contain only 1 item it must be transformed to str
            array_to_str(cheapest_wine_title),
            array_to_str(highest_score_title),
            array_to_str(lowest_score_title),
            array_to_str(most_expensive_country_title),
            array_to_str(cheapest_country_title),
            array_to_str(most_rated_country_title),
            array_to_str(most_underrated_country_title),
            array_to_str(most_active_taster_name)
    )


def dumping(data_list)->str:
    """ The function dumps input structure to .json format
    :param data_list: input structure
    :return:.json string

    """

    string = ''

    if type(data_list) is dict:  # type of input structure is dict
        string += '{\n'
        keys_ = data_list.keys()
        len_of_key_array = len(keys_)
        i = 0
        for key in data_list:
            if type(data_list[key]) in (str, int, float, complex, bool):  # if type of value is str

                string += str(key)
                string += ': '
                string += str(data_list[key])

            elif type(data_list[key]) is dict:  # if type(value) is dict again

                string += key
                string += ': \n'
                string += dumping(data_list[key])

            elif type(data_list[key]) is list:  # if type(value) is list

                string += key + ':' + '\n'
                string += '[\n'
                for id_, d in enumerate(data_list[key]):  # for each in list

                    if id_ != len(data_list[key]) - 1:  # if current item not last, use comma after dumping it
                        string += dumping(d)
                        string += ',\n'
                    else:
                        string += dumping(d) + '\n'
                string += ']'

                if i != len_of_key_array - 1:
                    string += '\n'

            if i != len_of_key_array - 1:  # if the key is not last, use comma to share
                string += ',\n'
            else:
                string += '\n'
            i += 1

        string += '}'
        return string

    elif type(data_list) in (str, float, int, complex, ):  # if type of input structure is immutable

        string += str(data_list)
        return string

    elif type(data_list) is list:  # if type of input structure is list
        if len(data_list) == 1:  # if list contains only 1 item
            string += dumping((data_list[0]))
        else:
            string += '[\n'
            for i, d in enumerate(data_list):
                if i != len(data_list) - 1:  # using comma to share
                    string += dumping(d) + ',\n'
                else:
                    string += dumping(d)
            string += '\n]'
        return string


def print_json(data_string, file_name)->None:
    """ The function gets data string, that was translated to json, and writes it

    :param data_string: input da string in .json
    :param file_name: name of file to write
    :return: None

    """

    with open(file_name, 'w') as f:
        tab = ''  # string of tabs at the beginnings of lines
        key_and_value = ''  # string that contains pair: key and value
        inside = False  # if inside word true, else false

        for i, char in enumerate(data_string):
            if char == '"' and not inside:  # if the " is opening
                inside = True
            elif char == '"' and inside:  # if the " is closing
                inside = False

            if char in ('[', '{'):
                if inside:  # if symbols are inside the word, then just add it to key_and_value
                    key_and_value += char

                    f.write(tab + char)

                else:  # if symbol is closing or opening
                    f.write(tab + char)
                    tab += '\t'
                    inside = False
            elif char in (']', '}'):
                if inside:
                    key_and_value += char

                else:
                    tab = tab[:-1]
                    f.write(tab + char)
                    key_and_value = ''
                    inside = False
            elif char == '\n':
                    f.write(tab + key_and_value)
                    f.write('\n')
                    key_and_value = ''
            else:
                key_and_value += char


"""
main part
"""

dictionary_list_1 = parsing(first_input_file)
dictionary_list_2 = parsing(second_input_file)

merged = find_duplicate(dictionary_list_1, dictionary_list_2)  # looking for duplicates

count_nul = count_null_(merged)  # counting null-prices

temp_merged_lists = merged.copy()
merged = push_null_in_the_end(temp_merged_lists)  # pushing null- prices to the end for comfortable sorting
merged_length = len(merged)

quick_sort(merged, 0, merged_length-count_nul-1)
data = dumping(merged)

print_json(data, 'winedata_full.json')  # dumping

wine_sorts = \
    ['"Gewurztraminer"',
     '"Gewürztraminer"',
     '"Riesling"',
     '"Merlot"',
     '"Madera"',
     '"Tempranillo"',
     '"Red Blend"'
     ]

wine_sorts_info = sorts_information(wine_sorts, merged)  # searching for information for each sort from wine_sorts

(most_expensive_wine_title,
 cheapest_wine_title,
 highest_score_title,
 lowest_score_title,
 most_expensive_country_title,
 cheapest_country_title,
 most_rated_country_title,
 most_underrated_country_title,
 most_active_taster_name) = wine_records(merged)

list_to_json = {'"statistics"':
                {'"wine:"': wine_sorts_info,
                 '"most_expensive_wine"': most_expensive_wine_title,
                 '"cheapest wine"': cheapest_wine_title,
                 '"highest score"': highest_score_title,
                 '"lowest score"': lowest_score_title,
                 '"most expensive country"': most_expensive_country_title,
                 '"cheapest country"': cheapest_country_title,
                 '"most rated country"': most_rated_country_title,
                 '"most underrated country"': most_underrated_country_title,
                 '"most active commentator"': most_active_taster_name}}

print_json(dumping(list_to_json), 'stats.json')    # writing statistics to .json file
