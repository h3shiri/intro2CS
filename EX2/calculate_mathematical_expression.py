#Calculating basic mathematical operations
def calculate_mathematical_expression(first_number, second_number, operation):
    if operation == '+':
        result = (first_number + second_number)
        return result
    elif operation == '-':
        result = (first_number - second_number)
        return result
    elif operation == '/':
        if second_number == 0:
            return None
        else:
            result = (first_number/second_number)
            return result
    elif operation == '*':
        result = (first_number * second_number)
        return result
    else:
        return None
#Calculating basic math questions from text message
def calculate_from_string(text):
    #setting globals for calculations
    number1 = 0.0
    number2 = 0.0
    operation = 'none'

    string = list(text.partition(' '))
    #Checking input format
    if string[0] == text:
        return None
    else:
        number1 = float(string[0])
        string2 = ((string[2]).partition(' '))
        #Checking input format
        if string2[0] == string:
            return None
        else:
            number2 = float(string2[2])
            operation = string2[0]
            #checking operand is valid
            if operation not in {'+','-','/','*'}:
                return None
    result = calculate_mathematical_expression(number1,number2,operation)
    return result

#Sorting 3 elements and returning 2 values first is the largest second is the smallest
def largest_and_smallest(a,b,c):
    max_value = 0
    min_value = 0
    #finding maximum
    if (a >= b and a >= c):
        max_value = a
    elif (b >= c and b >= a):
        max_value = b
    else:
        max_value = c

    #finding minimum
    if (a <= b and a <= c):
        min_value = a
    elif (b <= a and b <= c):
        min_value = b
    else:
        min_value = c
    return (max_value,min_value)
