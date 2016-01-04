#TODO: check whether to insert assertion on the input of all these functions
import math
EPSILON = 1e-5
DELTA = 1e-3
SEGMENTS = 100

def plot_func(graph, f, x0, x1, num_of_segments=SEGMENTS, c='black'):
    """
    plot f between x0 and x1 using num_of_segments straight lines.
    use the plot_line function in the graph object. 
    f will be plotted to the screen with color c.
    """
    delta = ((x1 - x0)/num_of_segments)
    for i in range(num_of_segments):
        xLeft = (x0 + (i*delta))
        xRight =  (xLeft + delta)
        leftPoint = (xLeft, f(xLeft))
        rightPoint = (xRight, f(xRight))
        graph.plot_line(leftPoint, rightPoint, c)


def const_function(c):
    """return the mathematical function f such that f(x) = c
    >>> const_function(2)(2)
    2
    >>> const_function(4)(2)
    4
    """
    return lambda x: c


def identity():
    """return the mathematical function f such that f(x) = x
    >>> identity()(3)
    3
    """
    return lambda x: x


def sin_function():
    """return the mathematical function f such that f(x) = sin(x)
    >>> sin_function()(math.pi/2)
    1.0
    """
    return lambda x: math.sin(x)


def sum_functions(g, h):
    """return f s.t. f(x) = g(x)+h(x)"""
    return lambda x: (g(x) + h(x))


def sub_functions(g, h):
    """return f s.t. f(x) = g(x)-h(x)"""
    return lambda x: (g(x) - h(x))



def mul_functions(g, h):
    """return f s.t. f(x) = g(x)*h(x)"""
    return lambda x: (g(x) * h(x))


def div_functions(g, h):
    """return f s.t. f(x) = g(x)/h(x)"""
    return lambda x: (g(x)/h(x))

    # The function solve assumes that f is continuous.
    # solve return None in case of no solution
def solve(f, x0=-10000, x1=10000, epsilon=EPSILON):
    """return the solution to f in the range between x0 and x1"""
    if (((f(x0) * f(x1))>0) or (epsilon == 0)):
        return None
    # Due to the symetry of the problem we shall adopt 'f' to be negative in f(x0) and positive in f(x1)
    if (f(x0) > 0):
        new_f = lambda x: (-1 * f(x))
    else:
        new_f = lambda x: f(x)
    # Our algorithm looks at a new midpoint each time and check whether its positive or negative to move accordingly.
    x_trail = ((x0 + x1)/2)
    condition = (abs(new_f(x_trail)) >= epsilon)
    while (condition):
        # Move to the new mid-point on the left
        if new_f(x_trail) < 0:
            x0 = x_trail
            x_trail = ((x0 + x1)/2)
            condition = (abs(new_f(x_trail)) >= epsilon)
        # Move to the new mid-point on the right
        elif new_f(x_trail) > 0:
            x1 = x_trail
            x_trail = ((x0 + x1)/2)
            condition = (abs(new_f(x_trail)) >= epsilon)
        # In case we got lovely zero we solve the problem
        else:
            break
    # We know the while-loop is going to exit due to the continius assumption on f.
    return x_trail

    # inverse assumes that g is continuous and monotonic. 
def inverse(g, epsilon=EPSILON):
    """return f s.t. f(g(x)) = x"""
    def result(x):
        # Search magic numbers
        SEARCH_FACTOR = 5
        L_BOUND = -1
        R_BOUND = 1
        # looking for the appropriate value to return in the inverse function using solve.
        const_x = const_function(x)
        h = sub_functions(g, const_x)
        answer_not_valid = True
        while (answer_not_valid):
            answer = solve(h, L_BOUND, R_BOUND, epsilon)
            if answer != None:
                answer_not_valid = False
            else:
                # Increse seraching bounds
                L_BOUND *= SEARCH_FACTOR
                R_BOUND *= SEARCH_FACTOR
        return answer
    # we now return the required inverse function as result
    return result


def compose(g, h):
    """return the f which is the compose of g and h """
    return lambda x: g(h(x))


def derivative(g, delta=DELTA):
    """return f s.t. f(x) = g'(x)"""
    utility_func = lambda x: x + delta
    temp1 = compose(g, utility_func)
    temp2 = sub_functions(temp1, g)
    temp3 = const_function((1/delta))
    res_function = mul_functions(temp2, temp3)
    return res_function


def definite_integral(f, x0, x1, num_of_segments=SEGMENTS):
    """
    return a float - the definite_integral of f between x0 and x1
    >>> definite_integral(const_function(3),-2,3)
    15
    """
    delta = ((x1 - x0)/num_of_segments)
    # we create a list of points that jumps delta at a time and includes x0 and x1.
    tot_sum = 0
    # Preform Riemann integral on the given number of segments.
    for i in range(num_of_segments):
        xLeft = (x0 + (i*delta))
        xRight =  (xLeft + delta)
        temp = ((xLeft + xRight)/2)
        tot_sum += ((f(temp))*delta)
    return tot_sum

def integral_function(f, delta=0.01):
    """return F such that F'(x) = f(x)"""
    def res_func(x):
        num_of_segments = math.ceil(abs(x)/delta)
        if x > 0:
            return definite_integral(f, 0, x, num_of_segments)
        elif x < 0:
            g = mul_functions(f, const_function(-1))
            return definite_integral(g, x, 0, num_of_segments)
        else:
            return 0
    return res_func

def ex11_func_list():
    """return a list of functions as a solution to q.12"""
    func_list = []
    f0 = const_function(4)
    func_list.append(f0)
    #Create function1
    sin = sin_function()
    f1 = sum_functions(sin, const_function(4))
    func_list.append(f1)
    #Create function2
    temp2 = sum_functions(identity(), const_function(4))
    f2 = compose(sin, temp2)
    func_list.append(f2)
    #Create function3
    temp3 = div_functions(mul_functions(identity(), identity()), const_function(100))
    f3 = mul_functions(sin, temp3)
    func_list.append(f3)
    #Create function4
    cos = derivative(sin)
    temp4 = sum_functions(cos, const_function(2))
    f4 = div_functions(sin,temp4)
    func_list.append(f4)
    #Create function5
    x_squared = mul_functions(identity(), identity())
    linear_part = sub_functions(identity(), const_function(3))
    quadratic = sum_functions(x_squared, linear_part)
    f5 = integral_function(quadratic)
    func_list.append(f5)
    #Create function6
    sin_comp_with_cos = compose(sin, cos)
    trigu_func = sub_functions(sin_comp_with_cos, cos)
    f6 = mul_functions(trigu_func, const_function(5))
    func_list.append(f6)
    #Create function7
    x_cubed = mul_functions(x_squared, identity())
    f7 = inverse(x_cubed)
    func_list.append(f7)
    return func_list

# function that genrate the figure in the ex description
def example_func(x):
    return (x/5)**3


#TODO: remember to remove tests
'''
g = lambda x: x**3
h = integral_function(g)
m = derivative(h)
print(m(2))
'''
'''
g = lambda x: x**5
h = derivative(g, 0.001)
print(h(2))
'''
'''
f = lambda x: x**3
g = inverse(f, 0.01)
h = compose(f,g)
print(h(40))
'''
'''
f = lambda x: x**2 - 7
M = solve(f, 0, 5, epsilon = 0.0001)
print(f(M)<0.0001,M)
'''

#TODO: check whether to delete main driver...etc
#Remove comment to run graphic display
if __name__ == "__main__":
    import tkinter as tk
    from ex11helper import Graph
    master = tk.Tk()
    graph = Graph(master, -10, -10, 10, 10)

    color_arr = ['black', 'blue', 'red', 'green', 'brown', 'purple',
                 'dodger blue', 'orange']
    func_list = ex11_func_list()
    for f in func_list:
        color_index = func_list.index(f)
        color = color_arr[color_index]
        plot_func(graph, f, -10, 10, SEGMENTS, color)

    master.mainloop()
