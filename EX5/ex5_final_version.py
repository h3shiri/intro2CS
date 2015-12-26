

import xml.etree.ElementTree as ET


FINE = 1.25


def get_attribute(store_db, ItemCode, tag):
    """ Returns the attribute (tag) of an Item with code: ItemCode in the
    given store.
    """
    item = store_db[ItemCode]
    result = item[tag]
    return result


def string_item(item):
    """ Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'
    """

    result = "".join("["+item["ItemCode"]+"]\t"+"{"+item["ItemName"]+"}")
    return result


def string_store_items(store_db):
    """ Textual representation of a store.
    Returns a string in the format of:
    string representation of item1
    string representation of item2
    """
    result = str("")
    line_breaker = "\n"
    if store_db == {}:
        return ""
    else:
        # enters keys, goes through the store item by item
        list_of_items = [string_item(store_db[i]) for i in store_db]
        new_list = ["".join(i + line_breaker for i in list_of_items)]
        result = "".join(new_list)
        return result


def read_prices_file(filename):
    """ Read a file of item prices into a dictionary.  The file is assumed to
    be in the standard XML format of "misrad haclcala".
    Returns a tuple: store_id and a store_db, where the first variable is the
    store name and the second is a dictionary describing the store.
    The keys in this db will be ItemCodes of the different items and the
    values smaller  dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    # Sets store_id
    store_id = root.find("StoreId").text
    # sets a new root for the items
    items_tree = root.find("Items")
    # creates the store_db one element at a time.
    store_db = {}

    for item in items_tree.findall("Item"):
        # creates a dictionary for the specific item
        item_dictionary = {}
        for element_property in item:
            item_dictionary[element_property.tag] = element_property.text
        store_db[item.find("ItemCode").text] = item_dictionary

    return (store_id, store_db)


def sub_string(target, key):
    """ Finds if one string is contained in another completely.
    """
    step = 1
    result = False
    # check one letter at a time
    for i in range(len(target)):
        counter = 0
        for j in range(len(key)):
            # check whether we are in range
            if (i+j) >= len(target):
                break
            elif key[j] != target[i+j]:
                break
            else:
                counter += step
        if counter == len(key):
            result = True
    return result


def filter_store(store_db, filter_txt):
    """ Create a new dictionary that includes only the items
    that were filtered by user.
    I.e. items that text given by the user is part of their ItemName.
    Args:
    store_db: a dictionary of dictionaries as created in read_prices_file.
    filter_txt: the filter text as given by the user.
    """
    name_field = "ItemName"
    new_dictionary = {}

    for item in store_db:
        # checks whether to include the specific item
        if sub_string(store_db[item][name_field],filter_txt):
            new_dictionary[item] = store_db[item]

    return new_dictionary


def create_basket_from_txt(basket_txt):
    """ Receives text representation of few items (and maybe some garbage
    at the edges). Returns a basket- list of ItemCodes that were included in
    basket_txt
    """
    list_of_codes = []
    empty_string = "empty"
    left_char = "["
    right_char = "]"
    # creates a set of numbers to check code validity
    valid_numbers = {str(i) for i in range(0, 10)}

    for open_char in range(len(basket_txt)):
        if basket_txt[open_char] == left_char:
            potential_itemcode = empty_string
            for closing_char in range(open_char, len(basket_txt)):
                if basket_txt[closing_char] == right_char:
                    potential_itemcode = basket_txt[open_char+1:closing_char]
                    break
            # checks validity of code
            for letter in range(len(potential_itemcode)):
                if potential_itemcode[letter] not in valid_numbers:
                    potential_itemcode = empty_string
                    break
            # append code if valid
            if potential_itemcode != empty_string:
                list_of_codes.append(potential_itemcode)

    return list_of_codes


def get_basket_prices(store_db, basket):
    """ Arguments: a store - dictionary of dictionaries and a basket - a list
    of ItemCodes. Go over all the items in the basket and create a new list
    that describes the prices of store items. In case one of the items is not
    part of the store, its price will be None
    """
    price_field = "ItemPrice"
    # create an empty list of prices
    price_list = [None]*(len(basket))
    valid_item_codes = set(store_db.keys())
    # check that item is in store and update price
    for item in range(len(basket)):
        if basket[item] in valid_item_codes:
            ItemCode = basket[item]
            price_list[item] = float(store_db[ItemCode][price_field])

    return price_list


def sum_basket(price_list):
    """ Receives a list of prices
    Returns a tuple - the sum of the list (when ignoring Nones)
    and the number of missing items (Number of Nones)
    """

    sum_price_list = 0
    missing_items = 0

    for price in price_list:
        if price is None:
            missing_items += 1
        else:
            sum_price_list += price

    price_tuple = (sum_price_list, missing_items)
    return price_tuple


def basket_item_name(stores_db_list, ItemCode):
    """ stores_db_list is a list of stores (list of dictionaries of
    dictionaries). Find the first store in the list that contains the item
    and return its string representation (as in string_item()).
    If the item is not available in any of the stores return only [ItemCode]
    """

    for store in stores_db_list:
        if ItemCode in store:
            result = string_item(store[ItemCode])

        else:
            result = '['+ItemCode+']'

    return result


def save_basket(basket, filename):
    """ Save the basket into a file.
    The basket representation in the file will be in the following format:
    [ItemCode1]
    [ItemCode2]
    ...
    [ItemCodeN]
    """

    new_basket = ["".join("["+i+"]") for i in basket]
    #add another line
    new_basket.append("")
    with open(filename, "a") as file:
        file.write("\n".join(new_basket))
    file.close()


def load_basket(filename):
    """ Create basket (list of ItemCodes) from the given file.
    The file is assumed to be in the format of:
    [ItemCode1]
    [ItemCode2]
    ...
    [ItemCodeN]
    """
    basket = []
    file = open(filename, "r")

    for line in file.readlines():
        line = "".join(ch for ch in line if ch not in ("[","]","\n"))

        basket.append(line)
    file.close()

    return basket


def best_basket(list_of_price_list):
    """ Arg: list of lists, where each inner list is list of prices as created
    by get_basket_prices.
    Returns the cheapest store (index of the cheapest list) given that a
    missing item has a price of its maximal price in the other stores *1.25
    """
    # initial price counters for each list
    prices = [0]*len(list_of_price_list)
    # initial maximum price for each item
    number_of_items = len(list_of_price_list[0])
    list_of_maximum_prices = [0]*number_of_items

    for i in range(number_of_items):
        temp_list = [0]
        for store in list_of_price_list:
            if store[i] is not None:
                temp_list.append(store[i])
        list_of_maximum_prices[i] = max(temp_list)
    # We establish the maximum prices list
    # calculate the store prices..etc

    for i in range(len(list_of_price_list)):
        for j in range(number_of_items):
            if list_of_price_list[i][j] is None:
                prices[i] += ((list_of_maximum_prices[j])*FINE)
            else:
                prices[i] += list_of_price_list[i][j]

    # cheapest supermarket is:
    result = prices.index((min(prices)))

    return result
