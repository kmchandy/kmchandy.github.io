from Engine import engine, Agent

class DataSource(Agent):
    def __init__(self, my_data, receiver):
        Agent.__init__(self)
        self.my_data = my_data
        self.receiver = receiver
        self.n = 0

    def receive(self, message, sender):
        self.send(message=self.my_data[self.n],
                  receiver=self.receiver)
        self.n += 1
        if self.n < len(self.my_data):
            self.send(message="wakeup", receiver=self)


            
class Total(Agent):
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
            if self.sum < 0: self.sum = 0
                
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
    # Create agents
    print_messages = PrintMessages()
    pos = DataSource(my_data=[3, 5], receiver=None)
    neg = DataSource(my_data=[2, 4], receiver=None)
    total = \
      Total(pos=pos, neg=neg, results=print_messages)
    pos.receiver = total
    neg.receiver = total
    pos.name = "pos"
    neg.name = "neg"
    total.name = "total"
    
    pos.send("wakeup", pos)
    neg.send("wakeup", neg)
    
    engine.start()
    

if __name__ == '__main__':
    test()
