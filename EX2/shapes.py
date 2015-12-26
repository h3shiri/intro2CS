#Calculating the area of various shapes
import math
#calculating area of a circle
def circle_area(r):
    result = (math.pi)*(r**2)
    return result
#calculating area of a rectangle
def rectangle_area(a,b):
    result = a*b
    return result
#calculating area of trapezoid
def trapezoid_area(a,b,h):
    result = (a + b)*(h/2)
    return result
#Calculating the area of a selected shape
def shapes_area():
    user_input = int(input("Choose shape (1=circle, 2=rectangle, 3=trapezoid): "))
    if user_input not in {1,2,3}:
        return None
    elif (user_input == 1):
        radius = float(input(""))
        return circle_area(radius)
    elif (user_input == 2):
        side1 = float(input(""))
        side2 = float(input(""))
        return rectangle_area(side1,side2)
    else:
        base1 = float(input(""))
        base2 = float(input(""))
        height = float(input(""))
        return trapezoid_area(base1,base2,height)
print(shapes_area())