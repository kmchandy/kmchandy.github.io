from Engine import engine, Agent

class PassingTokens(Agent):
    def __init__(self, other):
        Agent.__init__(self)
        self.other = other
        

    def receive(self, message, sender):
        self.n = self.n - 1
        print(self.name, ' received ', message)

        if self.n > 0:
            if sender is self.other:
                self.list_of_tokens_I_hold.append(message)
            else:
                token_I_hold = self.list_of_tokens_I_hold.pop()
                print(self.name, ' sent ', token_I_hold)
                self.send(message=token_I_hold, receiver=self.other)

            if len(self.list_of_tokens_I_hold):
                self.send('wakeup', self)

#-------------------------------------------
def test():
    u = PassingTokens(other=None)
    v = PassingTokens(other=None)
    u.n, v.n = 3, 3
    u.other, v.other = v, u
    u.name, v.name = 'u', 'v'
    u.list_of_tokens_I_hold = ['blue']
    v.list_of_tokens_I_hold = ['red']
    u.send("wakeup", u)
    v.send("wakeup", v)
    
    engine.start()
    

if __name__ == '__main__':
    test()
