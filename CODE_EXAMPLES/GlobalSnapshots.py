from Engine import engine, Agent
import random

"""
An example to illustrate the Global Snapshot algorithm.

Create a network of token passing agents.
There is an edge (u, v) in the network exactly when
v is in u.successors.

Each agent holds self.num_tokens number of tokens.

Each agent responds to at most self.n messages.

An agent has a wakeup message in its input channel 
exactly when:
    self.timeout = True
which is when the agent holds at least one token, ie
    self.num_tokens > 0

Explanation of receive.
If the sender is self, then the message is a wakeup.
     In this case the agent sends a token to any of 
     its successors selected randomly.
else
     the message is a token.
     In this case the token is added to the tokens
     held by the agent.

If there is no wakeup message for this agent and the
agent has tokens then the agent sends itself a
wakeup message.

"""

class TokenPassingAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.successors = list()
        self.num_tokens = 0
        self.n = 0
        self.timeout = False

    def receive(self, message, sender):
        self.n = self.n - 1
        print('--------------------------------')
        print(self.name, ' received ', message)

        if self.n > 0:
            if sender is self:
                self.num_tokens = self.num_tokens - 1
                self.send(message="token",
                          receiver=random.choice(self.successors))
            else:
                self.num_tokens = self.num_tokens + 1
                
            if self.num_tokens > 0 and not self.timeout:
                self.send('wakeup', self)
                self.timeout = True
            print_state()


def print_state():
    
    """
    For explanation purposes.
    Print the system state.

    """
     
    print()
    for ag, mq in engine.ag_to_mq.items():
        print("state of agent ", ag.name, " is ", ag.num_tokens)
        print("states of channels to ", ag.name)
        if mq.empty():
            print("     empty")
        for q in mq.queue:
            print("    message ", q.message,
                  " from ", q.sender.name)
    print()

#-------------------------------------------
def test():
    # Create a network of 3 agents u, v, w.
    u = TokenPassingAgent()
    v = TokenPassingAgent()
    w = TokenPassingAgent()

    u.name, v.name, w.name = "u", "v", "w"
    
    u.successors = [v, w]
    v.successors = [u, w]
    w.successors = [u, v]
    u.num_tokens, v.num_tokens, w.num_tokens = 3, 3, 6

    # Specify number of receives to which the
    # agent responds
    u.n, v.n, w.n = 3, 3, 2

    u.send("wakeup", u)
    v.send("wakeup", v)
    w.send("wakeup", w)

    u.timeout, v.timeout, w.timeout = True, True, True

    print(" THE INITIAL STATE")
    print_state()

    engine.start()
    

if __name__ == '__main__':
    test()
