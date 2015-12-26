
import xml.etree.ElementTree as ET

#Entering a store data base, item code and tag to find attribute
def get_attribute(store_db, ItemCode, tag):

    item = store_db[ItemCode]
    result = item[tag]
    return result

def string_item(item):
    '''
    Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'
    '''
    result = "".join("["+item["ItemCode"]+"]\t"+"{"+item["ItemName"]+"}")
    return result

#Textual representation of a store representing each string in a new line
def string_store_items(store_db):
    result = str("")
    line_breaker = "\n"
    if store_db == {}:
        return ""
    else:
        #entering the keys and going throught the store item by item
        list_of_items =[string_item(store_db[i]) for i in store_db]
        new_list = ["".join(i + line_breaker) for i in list_of_items]
        result = "".join(new_list)
        return result

#Reading a file of item prices into a dictionary in the required format
#input is file path and return value is sore_id and store_db
def read_prices_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    #Setting the store_id
    store_id = root.find("StoreId").text
    #setting a new root for the items
    items_tree = root.find("Items")
    #creating the store_db one element at a time.
    store_db = {}
    for item in items_tree.findall("Item"):
        #creating a dictionary for the spesific item
        item_dictionary = {}
        for element_property in item:
            item_dictionary[element_property.tag] = element_property.text
        store_db[item.find("ItemCode").text] = item_dictionary
    return (store_id,store_db)

#assisting function to check if one string is contained in another
def sub_string(target,key):
    step = 1
    result = False
    #checking one letter at a time
    for i in range(len(target)):
        counter = 0
        for j in range(len(key)):
            #checking whether we are in range
            if (i+j) >= len(target):
                break
            elif key[j] != target[i+j]:
                break
            else:
                counter += step
        if counter == len(key):
             result = True
    return result

#filtering items out of a store using a string, returns a new dictionary of dictionaries
#filer_text determines which items we take out of the store_db, maintaining the same structure
def filter_store(store_db, filter_txt):
    name_field = "ItemName"
    new_dictionary = {}
    for item in store_db:
        #checking whether to include the specific item
        if sub_string(store_db[item][name_field],filter_txt):
            new_dictionary[item] = store_db[item]
    return new_dictionary

#creating a basket of codes from text, return list of complete ItemCodes
def create_basket_from_txt(basket_txt):
    list_of_codes =[]
    empty_string = "empty"
    left_char = "["
    right_char = "]"
    #creating a set of numbers to check code validity
    valid_numbers = {str(i) for i in range(0,10)}
    for open_char in range(len(basket_txt)):
        if basket_txt[open_char] == left_char:
            potential_ItemCode = empty_string
            for closing_char in range(open_char,len(basket_txt)):
                if basket_txt[closing_char] == right_char:
                    potential_ItemCode = basket_txt[open_char+1:closing_char]
                    break
            #checking it is a valid code
            for letter in range(len(potential_ItemCode)):
                if potential_ItemCode[letter] not in valid_numbers:
                    potential_ItemCode = empty_string
                    break
            #we append the code in case it is valid
            if potential_ItemCode != empty_string:
                list_of_codes.append(potential_ItemCode)

    return list_of_codes


#returning a list of prices from a given store and a basket of items
#In case we miss an item from the store we shall return None
def get_basket_prices(store_db, basket):
    price_field = "ItemPrice"
    #creating an empty list of prices
    price_list = [None]*(len(basket))
    valid_Item_Codes = set(store_db.keys())
    #going one item at a time
    for item in range(len(basket)):
        #checking we have the item in the store and updating its price
        if basket[item] in valid_Item_Codes:
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

    # might be just filename
    new_basket = ["".join("["+i+"]") for i in basket]
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
    # might be just filename with no .txt
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
    #initial price counters for each list
    prices = [0]*len(list_of_price_list)
    #initial maximum price for each item
    Number_of_items = len(list_of_price_list[0])
    list_of_maximum_prices = [0]*Number_of_items
    #punishment is set to be 25%
    punish = 1.25
    for i in range(Number_of_items):
        temp_list = [0]
        for store in list_of_price_list:
            if store[i] != None:
                temp_list.append(store[i])
        list_of_maximum_prices[i] = max(temp_list)
    #We established the maximum prices list

    #calculating the store prices..etc
    for i in range(len(list_of_price_list)):
        for j in range(Number_of_items):
            if list_of_price_list[i][j] is None:
                prices[i] += ((list_of_maximum_prices[j])*punish)
            else:
                prices[i] += list_of_price_list[i][j]

    #cheapest shop
    result = prices.index((min(prices)))
    return result

