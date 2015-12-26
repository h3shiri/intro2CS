
# Print thr numbers from 1 to n in ascending order
def print_to_n(n):
    if n <= 0:
        pass
    elif n == 1:
        print(1)
    else:
        pre = n-1
        print_to_n(pre)
        print(n)

# Print the numbers from 1 to n in descending order
def print_reversed_n(n):
    if n <= 0 :
        pass
    elif n == 1:
        print(1)
    else:
        print(n)
        pre = n-1
        print_reversed_n(pre)

# Assisting function for the primality check.
# check whether a number is divisible within a given range, assuming positive.
def has_divisor_smaller_than_equal(n,i):
    few_first_primes = {2,3,5,7}
    if n in few_first_primes:
        return False
    elif i == 1:
        return False
    elif (n % i) == 0:
        return True
    else:
        pre = i-1
        return has_divisor_smaller_than_equal(n,pre)

# Check whether a number is prime or not return value accordingly
def is_prime(n):
    if n <= 1:
        return False
    else :
        # Assign a smaller number to check divisibility
        k = n-1
        # Check divisibility with the assisting function
        res = has_divisor_smaller_than_equal(n,k)
        # No divisors means we found a prime
        if res == False:
            return True
        else:
            return False

# Assisting function to divisors parsing the dividers one by one.
def divi(n,i):
    if i == 1:
        return [1]
    elif i == n:
        return [n]
    else:
        if n%i == 0:
            return [i]
        else:
            return []
# additional assisting function to divisors using 2 parameters
def parser(a,b):
    if a == 1:
        return [b]
    else:
        res = divi((a+b-1), b)
        a -= 1
        b += 1
        res.extend(parser(a,b))
        return res

# Calculate divisors with recursion
def divisors(n):
    # Base cases
    if n == 0:
        return []
    elif n == 1:
        return [1]
    elif n < 0:
        k = n*(-1)
        return divisors(k)
    else:
        a = n
        b = 1
        return parser(a,b)

# Assisting function for exponent calculate factorial
def factorial(n):
    # Assume we deal with an integer
    if n == 0:
        return 1
    elif n < 0:
        pass

    else:
        res = n
        res *= factorial(n-1)
    return res

# Calculate an exponent using recursion.
def exp_n_x(n,x):
    if (x == 0 or n == 0):
        return 1
    elif x < 0:
        x *= -1
        return (1/exp_n_x(n,x))
    # we established x is positive and assumed n is positive
    else:
        current_sum = 0
        current_sum += ((x**n)/(factorial(n)))
        pre = n-1
        res = (current_sum + exp_n_x(pre,x))
    return res

# The function solves the hanoi game
def play_hanoi(hanoi, n, src, dest, temp):
    """
    The solution is recursive me move if n=1 we are done.
    then if n>1 we move n-1 discs from src to temp, next lowest one from source to destination.
    finally we move all the discs from the temp to destination.
    """
    if n <= 0 :
        pass
    elif n == 1:
        hanoi.move(src,dest)
    else:
        play_hanoi(hanoi, n-1, src, temp, dest)
        hanoi.move(src,dest)
        play_hanoi(hanoi, n-1, temp, dest, src)

# Assisting function to binary print using prefixes
def print_binary_sequences_with_prefix(prefix,n):
    zero = '0'
    one = '1'
    if len(prefix) > n:
        print("")
    elif len(prefix) == n:
        print(prefix)
    elif len(prefix) == n-1:
        print(prefix + zero)
        print(prefix + one)
    else:
        new_prefix1 = "".join([prefix,zero])
        new_prefix2 = "".join([prefix,one])
        print_binary_sequences_with_prefix(new_prefix1,n)
        print_binary_sequences_with_prefix(new_prefix2,n)

def print_binary_sequences(n):
    if n <= 0:
        print("")
    else:
        prefix = ""
        print_binary_sequences_with_prefix(prefix, n)

#Assisting function to printing sequences given a determined prefix.
def print_sequences_with_prefix(prefix, char_list, n):
    if n <= 0 or len(prefix) > n:
        print("")
    elif len(prefix) == n:
        print(prefix)
    elif len(prefix) == n-1:
        new_prefixes = ["".join([prefix, char]) for char in char_list]
        for n_prefix in new_prefixes:
            print(n_prefix)
    else:
        new_prefixes = ["".join([prefix, char]) for char in char_list]
        for n_prefix in new_prefixes:
            print_sequences_with_prefix(n_prefix, char_list, n)

# Printing sequences from char list with length n recursively
def print_sequneces(char_list, n):
    if n <= 0:
        print("")
    elif len(char_list) > n:
        print("")
    else:
        prefix = ""
        print_sequences_with_prefix(prefix, char_list, n)

# Assisting function to finding to non-repeating sequences
def prefix_no_repetition_sequences(prefixes, char_list, n):
    """
    calculating non-repeating strings in length n from char list.
    Provided a given prefixes (list of strings), in a recursive manner.
    return value is a list of non-repeating sequences.
    """
    if ((len(prefixes[0]) > n) or (n <= 0)):
        return []
    elif len(prefixes[0]) == n:
        return prefixes
    #TODO fix the function so it works with [""] as well if u feel like it.
    else:
        new_prefixes = []
        for prefix in prefixes:
            for char in char_list:
                if char not in set(prefix):
                    new_prefixes.append("".join([prefix,char]))
                    # recursive call
        return(prefix_no_repetition_sequences(new_prefixes,char_list,n))

# Prints all the strings with nu repetition in length n from the character list.
def print_no_repetition(char_list, n):
    # We assume 'n' is a non negative integer and len(char_list) >= n.
    if n <= 0:
        print("")
    elif n == 1:
        for char in char_list:
            print(char)
    else:
        #choose one from the list and repeat recursively.
        prefixes = [char for char in char_list]
        outcomes = prefix_no_repetition_sequences(prefixes,char_list,n)
        for possibility in outcomes:
            print(possibility)

#TODO: it works fine but the complexity isn't great

# create a list of all the non repeating sequences length n, from the char_list.
def no_repetition_sequences(char_list, n):
    if n == 0:
        return []
    prefixes = [char for char in char_list]
    outcomes = prefix_no_repetition_sequences(prefixes,char_list,n)
    return outcomes

#TODO: some basic testing for the the functions 8-10








