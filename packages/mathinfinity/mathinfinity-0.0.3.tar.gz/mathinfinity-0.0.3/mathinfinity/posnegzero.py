from converttonumber import *
def posnegzero (input):
    ip = converttonumber(input)

    if ip > 0:
        print(f"{ip} Is Positive Number.")
    elif ip < 0:
        print(f"{ip} Is Negative Number.")
    else:
        print(f"{ip} Is Zero value.")