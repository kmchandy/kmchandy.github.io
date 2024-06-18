from Engine import engine, Agent


def gcd(X, Y):
    x, y = X, Y
    while x != y:
        # gcd(x, y) = gcd(X, Y)
        if x > y: x = x - y
        else: y = y - x
    return x

#-------------------------------------------
def test():
    X = 40
    Y = 18
    
    print ('result ', gcd(X, Y))
    

if __name__ == '__main__':
    test()
