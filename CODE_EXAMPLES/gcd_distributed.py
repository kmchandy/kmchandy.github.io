from Engine import engine, Agent


def gcd(X, Y):
    x, y = X, Y
    while x != y:
        # gcd(x, y) = gcd(X, Y)
        if x > y: x = x - y
        else: y = y - x
    return x

class gcd_distributed(Agent):
    def __init__(self, n, successors, name):
        Agent.__init__(self)
        self.n = n
        self.successors = successors
        self.name = name

    def broadcast(self):
        for successor in self.successors:
            self.send(self.n, successor)

    def receive(self, message, sender):
        if self.n != message:
            self.n = gcd(self.n, message)
            self.broadcast()
        else: print (self.n, self.name)


class gcd_pair(Agent):
    def __init__(self, n, other, name):
        Agent.__init__(self)
        self.n = n
        self.other = other
        self.name = name

    def receive(self, message, sender):
        print (self.name, self.n, message)
        if self.n != message:
            self.n = (self.n - message if self.n > message
                      else message - self.n)
            self.send(self.n, self.other)
        else:
            print (self.n, self.name)
        




#-------------------------------------------
def test():
    x = gcd_distributed(n=36, successors=[], name='x')
    y = gcd_distributed(n=30, successors=[], name='y')
    z = gcd_distributed(n=27, successors=[], name='z')
    x.successors = [y, z]
    y.successors = [x, z]
    z.successors = [x, y]

    x.broadcast()
    y.broadcast()
    z.broadcast()

    """
    a = gcd_pair(n=30, other=None, name='a')
    b = gcd_pair(n=12, other=None, name='b')
    a.other = b
    b.other = a
    a.send(a.n, a.other)
    b.send(b.n, b.other)
    """
    
    engine.start()
    

if __name__ == '__main__':
    test()
