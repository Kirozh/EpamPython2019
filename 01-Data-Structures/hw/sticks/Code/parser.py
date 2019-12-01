import random
import sys

f = open('winedata_2.json', 'r', encoding='utf-8')
g = open('winedata_1.json', 'r', encoding='utf-8')


def parsing(f):
    """ Function parsing makes parsing input file
    f - input file
    parsing(f) -> list(dict)
    it returns list of dictionaries
    """

    print('starting parsing file')
    dict_list = []

    stack = []  # stack contains symbols '{', '[' , '}', ", and ']'
    c = f.read(1)
    stack.append(c)

    sigths_dict = {}  # exemplar of dictionary
    i = 0

    inside = False  # true if current symbol is in word, else false
    key = value = []  # key and value massivs
    key_or_value = -1  # -1 if current symbol in key , 1 if current symbol in value
    stack_size = len(stack)

    while stack_size != 0 :
        c = f.read(1)

        if c == '[':  # statring parsing and adding [ to stack
            if stack[-1] != '[':
                stack.append(c)

        if c == '{':  # new dictionary
            stack.append(c)
            inside = False

        if c == '"' and stack[-1] != '"':  # currently in word: key or value
            stack.append(c)
            inside = True

            if key_or_value == -1:
                key = []

            value = []

        elif c == '"' and stack[-1] == '"':
            inside = False
            stack.pop(-1)

            if key_or_value < 0:
                key_or_value = 1
            else:
                key_or_value = -1

        if key_or_value < 0 and inside and c != '"':
            if key_or_value < 0:
                key.append(c)

        if c == ':' and not inside:
            key_or_value = 1

        if c == ',' and not inside and stack[-1] == '{':
            key_or_value = -1
            sigths_dict.update({''.join(key): ''.join(value).lstrip()})

        if key_or_value > 0 and c != '"' and c != ':':

            value.append(c)

        if c == '}':
            stack.pop(-1)
            inside = False
            sigths_dict.update({''.join(key): ''.join(value).lstrip()})
            dict_list.append(sigths_dict.copy())
            sigths_dict.clear()

        if c == ']':
            stack.pop(-1)

        stack_size = len(stack)

    return dict_list


def merging(dictionary_list_1, dictionary_list_2):
    """
    merging two lists
    :param dictionary_list_1:
    :param dictionary_list_2:
    :return: list
    """
    temp_list = dictionary_list_1.copy()
    temp_list.extend(dictionary_list_2)
    return temp_list


def sort_wine_by_price(dList):
    """
    def sort_wine_by_price(dList) -> dList
    function get list of dictionaries, throwes null-prices in the end and sorts remainings
    dList - list of dictionaries
    """
    print('starting sort_wine_by_price')
    print(type(dList))
    length = len(dList)

    tempList = dList.copy()

    # counting null-prices

    count_null = 0
    for x in dList:
        if x['price'] == 'null':
            count_null += 1

    i = 0

    # pushing null-price-dictionaries to the end

    while i < length-count_null:

        j = i
        x = dList[j].copy()
        if x['price'] == 'null':

            x = dList[j+1].copy()

            if x.get('price') != 'null':

                i += 1

            temp_dict = dList.pop(j).copy()

            dList.append(temp_dict.copy())

        else:
            i += 1

    # sorting prices

    i = 1
    while i < length-count_null:
        temp_dict = {}
        temp_dict.update(dList[i].items())

        j = i

        while (j > 0 and int(dList[j-1].get('price')) < int(temp_dict.get('price'))):
            dList[j].clear()
            dList[j].update(dList[j-1].items())

            j -= 1
        dList[j].clear()
        dList[j].update(temp_dict)
        i += 1
    return dList


def find_duplicate(dictionary_list_1, dictionary_list_2):
    """
    def find_duplicate(dict_list_1, dict_list_2) -> merged_list
    function gets two lists of dictionaries. It runs along first list
        and tries to find identical dictionary in another dict_list
    finally, it merges two lists in merged_list
    """
    print('starting find_duplicate')
    merged_list = []
    for x in dictionary_list_1:
        length_file_2 = len(dictionary_list_2)
        i = 0

        while i < length_file_2 and x.values() != dictionary_list_2[i]:
            i += 1

        if i != length_file_2:
            print(dictionary_list_2.pop(i))

    merged_list = dictionary_list_1.copy()
    merged_list.extend(dictionary_list_2)
    print(len(merged_list))
    return merged_list


def find_duplicate_temp(dictionary_list_1, dictionary_list_2):
    """
        temp function finds duplicates
    """
    temp_merged_list = dictionary_list_1.copy()
    temp_merged_list.extend(dictionary_list_2)
    merged_set = set(temp_merged_list)
    merged_list = list(merged_set)
    print(len(merged_list))
    return merged_list


def count_null_(merged_list):
    """
        def count_null(merged_list) -> int
        finds num of null-prices in merged list
    """
    count_null = 0

    for x in merged_list:
        if x['price'] == 'null':
            count_null += 1

    return count_null


def push_null_in_the_end(merged_list):
    """
    def push null in the end(merged_list) -> merged list
    pushes dictionaries with null - price to the end
    """
    count_null = count_null_(merged_list)
    i = 0
    length = len(merged_list)

    # push null-price-dictionaries to the end
    while i < length - count_null:

        j = i
        x = merged_list[j].copy()
        if x['price'] == 'null':
            x = merged_list[j + 1].copy()

            if x.get('price') != 'null':
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

    if fst >= lst: return

    i, j = fst, lst
    pivot = merged_list[random.randint(fst, lst)]

    while i <= j:
        while int(merged_list[i].get('price')) < int(pivot.get('price')):
            i += 1
        while int(merged_list[j].get('price')) > int(pivot.get('price')):
            j -= 1
        if i <= j:

            merged_list[i], merged_list[j] = merged_list[j], merged_list[i]
            i, j = i + 1, j - 1

    quick_sort(merged_list, fst, j)
    quick_sort(merged_list, i, lst)


def merge_sorted_by_price_JSON(dictionary_list_1, dictionary_list_2):
    """
    :param dictionary_list_1:
    :param dictionary_list_2:
    :return:
    """
    print('starting merge_sorted_by_price')

    return sort_wine_by_price(find_duplicate(dictionary_list_1.copy(), dictionary_list_2.copy()))


def wine_sort_information(sort, merged_lists):
    """
    wine sort information(sort, merged list) -> dict()
    function get sort of wine and returns sort`s information:
    - max price
    - min price
    - most common country / region
    - average price
    - score
    """

    print('starting wine sort information')
    average_price = 0
    price = 0
    min_price = 10000
    max_price = -1

    average_score = 0
    score = 0
    sort_count = 0

    countries = {}

    regions = {}

    for x in merged_lists:
        if x['variety'] == sort:
            sort_count += 1
            if x['price'] != 'null':
                price += int(x['price'])
                if int(x['price']) < min_price:
                    min_price = int(x['price'])
                if int(x['price']) > max_price:
                    max_price = int(x['price'])
            cur_country = x['country']
            if cur_country != 'null':
                if countries.get(cur_country) is None:
                    countries.update({x['country']: 1})
                else:
                    countries.update({x['country']: int(countries[cur_country]) + 1})

            cur_region = x['region_1']
            if cur_region != 'null':
                if regions.get(cur_region) is None:
                    regions.update({x['region_1']: 1})
                else:
                    regions.update({x['region_1']: int(regions[cur_region]) + 1})

            cur_region = x['region_2']
            if cur_region != 'null':
                if regions.get(cur_region) is None:
                    regions.update({x['region_2']: 1})
                else:
                    regions.update({x['region_2']: int(regions[cur_region]) + 1})

            score += int(x['points'])
    if sort_count != 0:
        average_price = float(price) / sort_count
        average_score = float(score) / sort_count
    else:
        max_price = 0
        min_price = 0

    countries_count = ''
    max_count_countries = 0
    for key in countries:
        if countries[key] > max_count_countries:
            max_count_countries = countries[key]
            countries_count = key

    region_count = ''
    max_count_regions = 0
    for key in regions:
        if regions[key] > max_count_regions:
            max_count_regions = regions[key]
            region_count = key
    print('count', sort_count)
    print('average price: ', average_price)
    print('min price: ', min_price)
    print('max price: ', max_price)

    print('most common country: ', countries_count, ' - ', max_count_countries)
    print('most common region: ', region_count,' - ' ,max_count_regions)
    print('average score: ', average_score)

    return {'average price': average_price,
            'max price': max_price,
            'min price': min_price,
            'most common country': countries_count,
            'region_count': region_count,
            'average score': average_score
            }


def sorts_information(wine_sorts, merged_lists):
    """
    def sorts_information(wine_sorts, merged_lists) -> None
    function applies wine_sort_information function for each sort in wine_sorts
    """
    print('sorts information')
    for wine in wine_sorts:
        print(wine + ':')
        wine_sort_information(wine, merged_lists)


def wine_info(merged_list):
    """
    def wine_info(merged_lists) -> dict()
    function finds information:
    - max / min price
    - average price
    - most rated / underrated countries
    """

    print('starting wine information')
    most_expensive_wine = []
    most_expensive = 0
    cheapest_wine = []
    cheapest = 100000
    highest_score = 0
    highest_score_list = []
    lowest_score = 1000
    lowest_score_list = []
    country_price = {}
    country_rating = {}
    tasters = {}
    for x in merged_lists:
        if x['taster_name'] != 'null':
            if tasters.get(x['taster_name']) is None:
                tasters.update({x['taster_name']: 1})
            else:
                tasters.update({x['taster_name']: int(tasters[x['taster_name']]) + 1})

        if x['country'] != 'null':
            if country_price.get(x['country']) is None:
                if x['price'] != 'null':
                    country_price.update({x['country']: [int(x['price']), 1]})
            else:
                temp_list = country_price[x['country']]
                if x['price'] != 'null':
                    temp_list[0] += int(x['price'])
                    temp_list[1] += 1
                country_price.update({x['country']: temp_list})

        if x['country'] != 'null':

            if country_rating.get(x['country']) == None:
                if x['points'] != 'null':
                    country_rating.update({x['country']: [int(x['points']), 1]})
            else:
                temp_list = country_price[x['country']]
                if x['points'] != 'null':
                    temp_list[0] += int(x['points'])
                    temp_list[1] += 1
                country_rating.update({x['country']: temp_list})

        if x['price'] != 'null':
            if int(x['price']) > most_expensive:
                most_expensive = int(x['price'])
                most_expensive_wine.clear()
                most_expensive_wine.append(x['title'])

            if int(x['price']) < cheapest:
                cheapest = int(x['price'])
                cheapest_wine.clear()
                cheapest_wine.append(x['title'])
            elif int(x['price']) == cheapest:
                cheapest_wine.append(x['title'])

        if int(x['points']) > highest_score:
            highest_score = int(x['points'])

            highest_score_list.clear()
            highest_score_list.append(x['title'])
        elif int(x['points']) == highest_score:
            highest_score_list.append(x['title'])

        if int(x['points']) < lowest_score:
            lowest_score = int(x['points'])
            lowest_score_list.clear()

            lowest_score_list.append(x['title'])
        elif int(x['points']) == lowest_score:
            lowest_score_list.append(x['title'])

    country_with_most_expensive_average_price = []
    country_with_cheapest_average_price = []
    cheapest_average_price = 10000
    most_expensive_average_price = 0

    for x in country_price:
        t_list = country_price.get(x)
        if float(t_list[0]) / t_list[1] > most_expensive_average_price:
            most_expensive_average_price = float(t_list[0]) / t_list[1]
            country_with_most_expensive_average_price.clear()
            country_with_most_expensive_average_price.append(x)
        elif float(t_list[0]) / t_list[1] == most_expensive_average_price:
            country_with_most_expensive_average_price.append(x)

        if float(t_list[0]) / t_list[1] < cheapest_average_price:
            cheapest_average_price = float(t_list[0]) / t_list[1]
            country_with_cheapest_average_price.clear()
            country_with_cheapest_average_price.append(x)
        elif float(t_list[0]) / t_list[1] == cheapest_average_price:
            country_with_cheapest_average_price.append(x)

    most_rated_country = []
    most_underrated_country = []
    highest_average_rating = 0
    lowest_average_rating = 100

    for x in country_rating:
        t_list = country_rating.get(x)
        if float(t_list[0]) / t_list[1] > highest_average_rating:
            highest_average_rating = float(t_list[0]) / t_list[1]
            most_rated_country.clear()
            most_rated_country.append(x)
        elif float(t_list[0]) / t_list[1] == highest_average_rating:
            most_rated_country.append(x)

        if float(t_list[0]) / t_list[1] < lowest_average_rating:
            lowest_average_rating = float(t_list[0]) / t_list[1]
            most_underrated_country.clear()
            most_underrated_country.append(x)
        elif float(t_list[0]) / t_list[1] == lowest_average_rating:
            most_underrated_country.append(x)

    name_taster = []
    taster_count = 0

    for x in tasters:
        if int(tasters[x]) > taster_count:
            taster_count = int(tasters[x])
            name_taster.clear()
            name_taster.append(x)
        elif int(tasters[x]) == taster_count:
            name_taster.append(x)

    return {'most expensive wine': most_expensive_wine,
            'cheapest wine': cheapest,
            'highest score': highest_score_list,
            'lowest score': lowest_score_list,
            'most expensive average price': country_with_most_expensive_average_price,
            'cheapest average price': country_with_cheapest_average_price,
            'most rated country': most_rated_country,
            'most underrated country': most_underrated_country,
            'most active commentator': name_taster
            }


def collect_data_for_json(merged_lists):
    """
    collecting data for evaling
    """
    colection = []

    colection.extend(['{', 'statistics',
                         '[',
                            '{',
                            'wine',
                                '[',
                                    '{',
                                        'Gewürztraminer', wine_sort_information(u'Gewürztraminer',
                                                                                 merged_lists),
                                    '}',
                                    '{',
                                        'Gewurztraminer', wine_sort_information('Gewurztraminer', merged_lists),
                                    '}',
                                    '{',
                                        'Riesling', wine_sort_information('Riesling', merged_lists),
                                    '}',
                                    '{',
                                        'Merlot', wine_sort_information('Merlot', merged_lists),
                                    '}',
                                    '{',
                                        'Madera', wine_sort_information('Madera', merged_lists),
                                    '}',
                                    '{',
                                        'Tempranillo', wine_sort_information('Tempranillo', merged_lists),
                                    '}',
                                    '{',
                                        'Red Blend', wine_sort_information('Red Blend', merged_lists),
                                    '}',

                                ']',
                            '}',
                            '{',
                                wine_info(merged_lists),
                            '}',
                         ']',
                     '}'])

    return colection


def write_json_to_file(colection, output):
    tab = '\t'

    stack_len = 0

    for c in colection:
        if c == '[' or c == '{':
            for i in range(stack_len):
                output.write(tab)

            output.write(c)
            output.write('\n')

            stack_len += 1
        elif c == '}' or c == ']':
            for i in range(stack_len-1):
                output.write(tab)

            output.write(c)
            output.write(',')
            output.write('\n')

            stack_len = stack_len - 1

        if type(c) == dict:

            for key in c:
                for i in range(stack_len):
                    output.write(tab)
                # output.write(tab)

                output.write(key)
                output.write(' : ')
                if type(c[key]) == list:
                    for cc in c[key]:
                        for i in range(stack_len + 1):
                            output.write(tab)
                        output.write(str(cc))
                        output.write('\n')
                else:
                    output.write(str(c[key]))
                    output.write('\n')

        if type(c) == str and (c != '{' and c != '[' and c != ']' and c != '}' and c != ','):
            for i in range(stack_len):
                output.write(tab)
            # output.write(tab)

            output.write(c)
            output.write('\n')

        if type(c) == list:
            for cc in c:
                output.write(str(cc))
                output.write('\n')


"""
main part
"""
output = open('stats.json', 'w')

dictionary_list_1 = parsing(f)
dictionary_list_2 = parsing(g)

limit = sys.getrecursionlimit()
sys.setrecursionlimit(20*limit)

merged_lists = merging(dictionary_list_1, dictionary_list_2)  # merging 2 dictionaries

count_nul = count_null_(merged_lists)  # counting null-prices
temp_merged_lists = merged_lists.copy()
merged_lists = push_null_in_the_end(temp_merged_lists)

quick_sort(merged_lists, 0, 131470 - count_nul)  # sorting file by quick sort

write_json_to_file(collect_data_for_json(merged_lists), output)  # writing statistics to json file

f.close()
g.close()

