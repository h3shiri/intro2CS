import math

#Printing a list of inputs in a list using a while loop.
def create_list():
    result = []
    while True:
        #no meassage for input request.
        user_input = input()
        if user_input == "":
            break
        else:
            #adding the input
            result.append(user_input)
    return result

#Returning a concatenation of a list using a for loop.
def concat_list(lst_str):
    result = ""
    for i in range(len(lst_str)):
        #adding the elements one at a time
        result += lst_str[i]
    return result

#Calculating the avarage of floats
def avr(num_list):
    #checking empty list case
    if len(num_list) == 0:
        return None
    else:
        total_sum = 0
        #finding sum
        for i in range(len(num_list)):
            total_sum += num_list[i]
    #avarage
    result = (total_sum/(len(num_list)))
    return result

#checking if one list is a cyclic permutation of the other one.
def cyclic(lst1,lst2):
    #making sure they have the same number of elements
    if len(lst1) != len(lst2):
        return False
    else:
        #running on all the given permutations and each time checking element by element
        lists_length = len(lst2)
        list_of_permutations = range(len(lst1))
        for i in list_of_permutations:
            #we are going to check if one of the permutations on list1 equal to list2
            success_counter = 0
            step = 1
            for j in range(len(lst1)):
                #checking each element
                new_index = (j+i)%lists_length
                if (lst1[new_index] != lst2[j]):
                     break
                else:
                    success_counter += step
            #checking if we found a valid solution
            if (success_counter == lists_length):
                return True
    #We haven't found a successful permutation
    return False

#Creating a histogram of in integers from 1 to n-1 in a list
def hist(n,list_num):
    result = [0]*n
    step = 1
    for i in list_num:
        #Updating the relevant index
        result[i] += step
    return result

#Assisting function - checks primality
def is_prime(p):
    first_prime = 2
    if p == first_prime:
        return True
    else:
        for i in range(2,(int((math.sqrt(p))+1))):
            #checking divisability by all the numbers until sqrt of p.
            if (p % i == 0):
                return False
        return True

#Diving into prime factors
def fact(n):
    result = []
    if (is_prime(n)):
        result.append(n)
        return result
    else:
        #diving until hitting the bottom rock of primes.
        temp = n
        while not(is_prime(temp)):
            for i in range(2,(int((math.sqrt(temp))+1))):
                if (temp % i == 0):
                    result.append(i)
                    temp = int(temp/i)
                    break
        #we escaped the loop and the last factor is also prime so we append it
        result.append(temp)
    return result

#creating the cartesian product of 2 lists
def cart(lst1,lst2):
    result = []
    #Checking whether the lists are empty
    if (len(lst1) == 0 or len(lst2) == 0):
        return result
    else:
        #moving on the first list then crossing them with the second list
        for i in range(len(lst1)):
            #matching pairs according to i and j.
            for j in range(len(lst2)):
                result.append([lst1[i],lst2[j]])
        return result

#Calculating all the valid pairs in a list of integers such that they add up to parameter n.
def pair(n, num_list):
    result = []
    #Checking all hte possible selections of 2 elements
    cut = 1
    for i in num_list:
        for j in num_list:
            if (i + j == n):
                result.append([i,j])
        #Cutting out all the used combinations
        num_list = num_list[cut:]

    #Checking whether any successful pairs were found
    if (len(result) == 0):
        return None
    else:
        return result

