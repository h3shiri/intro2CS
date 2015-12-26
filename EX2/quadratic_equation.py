#Solving a quadratic equation a is quadratic, b linear, c const.
def quadratic_equation(a,b,c):
    #finding delta and then classifying solution according to delta
    delta = b**2 + (-4*a*c)
    if delta < 0:
        return (None,None)
    elif delta == 0:
        x1 = (-b + (delta**(0.5)))/(2*a)
        return (x1,None)
    else:
        x1 = (-b + (delta**(0.5)))/(2*a)
        x2 = (-b - (delta**(0.5)))/(2*a)
        return (x1,x2)

#solving quadratic with a user given input
def quadratic_equation_user_input():
    user_input = input("Insert coefficients a, b, and c: ")
    coefficients = user_input.split()
    #setting quadratic coefficients
    a = float(coefficients[0])
    b = float(coefficients[1])
    c = float(coefficients[2])
    #Calculating solution
    (X,Y) = quadratic_equation(a,b,c)
    #Printing appropriate output
    if (X,Y) == (None,None):
        print("The equation has no solutions")
    elif (Y == None):
        print("The equation has 1 solution:",X)
    else:
        print("The equation has 2 solutions:",X,"and",Y)

quadratic_equation_user_input()