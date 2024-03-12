from Engine import engine, Agent

import random

class PositiveNumbersSource(Agent):
    def __init__(self, n, receiver):
        Agent.__init__(self)
        self.n = n
        self.receiver = receiver

    def receive(self, message, sender):
        if self.n > 0:
            self.n = self.n - 1
            message = random.randint(1, 10)
            self.send(message, self.receiver)
            self.send("wakeup", self)


class SumPosNeg(Agent):
    def __init__(self, pos, neg, results):
        Agent.__init__(self)
        self.pos = pos
        self.neg = neg
        self.results = results
        self.sum = 0

    def receive(self, message, sender):
        if sender is self.pos:
            self.sum += message
        else:
            self.sum -= message
        print ("Agent =", self.name, " sender =", sender.name, 
            "  message =", message, "  sum =", self.sum)
        self.send(self.sum, self.results)

        
class PrintMessages(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.name = "PrintMessages"
    
    def receive(self, message, sender):
        print()
        print('PrintMessages: ', ' sender = ', sender.name,
                  '  message = ', message)
        print()


#-------------------------------------------
def test():
    print_messages = PrintMessages()
    pos = PositiveNumbersSource(n=3, receiver=None)
    neg = PositiveNumbersSource(n=3, receiver=None)
    sum_pos_neg = \
      SumPosNeg(pos=pos, neg=neg, results=print_messages)
    pos.name = "pos"
    neg.name = "neg"
    sum_pos_neg.name = "sum_pos_neg"
    pos.receiver = sum_pos_neg
    neg.receiver = sum_pos_neg
    
    pos.send("wakeup", pos)
    neg.send("wakeup", neg)
    
    engine.start()
    

if __name__ == '__main__':
    test()
