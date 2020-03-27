# Algorithm to compute mean incrementally
#
# Given the following logic:
# Avg_n = sum_i_n(x_i)/n; -> (x_1+x_2+...+x_n)/n
#
# adding new values :
# Avg_n+1 = (sum_i_n(x_i) + x_n+1)/(n+1)
# ----->  = (n*Avg_n + x_n+1)/(n+1)
# ----->  = (n*Avg_n + x_n+1 + Avg_n - Avg_n)/(n+1)
# ----->  = Avg_n + (x_n+1 - Avg_n)/(n+1)

def inc_calc(list_in,average):
    for i,elem in enumerate(list_in):
        average += (elem - average)/(i+1)
    return average

def incremental_avg(x, y = None, N_x = 0):
    # provided a list of values we can calculate the 
    # average incrementally.
    # x can be list or previous average value
    # N_x is the length of numbers in the previous average x if provided 
    # if x is previous average, must include N_x
    # y can be either single value or list
    # returns the mean of the list
    
    # checking if x is list or not.
    # if single value, then must provide N_x, and calculate average of two numbers
    if not isinstance(x, (list, tuple)):
        if N_x==0:
            print('x is a single value (previous average), Must provide a value for N_x')
        else:
            n=N_x
            avg = 0
            if y==None:
                print('y is missing, must provide a value for y')
            elif not isinstance(y, (list, tuple)):
                avg = (x*n + y)/(n+1)
            else:
                x=[x]
                list_x = x + y
                avg = inc_calc(list_x,avg)
                
    else:
        n=len(x)
        avg = 0
        if n==0:
            print("List is empty, please enter list of numbers")
            exit(1)
        else:
            if y==None:
                list_x = x
            elif not isinstance(y, (list, tuple)):
                y = [y]
                list_x = x + y
            else:
                list_x = x + y
            avg = inc_calc(list_x,avg) 
            

    return avg
        
        
