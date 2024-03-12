import threading
import queue
import random

class MessageAndSender(object):

    """
    Parameters
    ----------
       message: object
                message sent by agent
       sender: agent
    """

    def __init__(self, message, sender):
        self.message = message
        self.sender = sender

        
#-----------------------------------------------------
class Engine(object):
    """
    Manages channels and agents of a simple simulation 
    of distributed systems used solely for teaching
    algorithms.

    Each agent, ag, has a single input queue of
    message_and_sender elements.

    This single input queue of ag has all the 
    messages in input channels of ag.

    A message_and_sender in a queue for ag is
    the message for ag and the agent that sent the
    message.

    An agent ag calls send(message, receiver) where
    message is an any object and receiver is an agent.

    When send(message, receiver) is called by ag
    MessageAndSender(message, ag)
    is placed in the queue for the receiver agent.

    When start() is called:
    any agent x with a nonempty input queue is
    selected randomly, and 
          x.receive(message, sender)
    is called where message is the message at the
    head of ag's queue.

    Parameters
    ----------
       None

    Attributes
    ----------
    ag_to_mq: dict
       key:   object, agent
       value: queue.Queue
              queue of message_and_sender pairs in the input
              message queue of the agent.

              A message_and_sender pair is a named tuple
              ('message', 'sender') where message is the
              content of a message and sender is the agent
              thqt sent the message.

    ag_list: list
             list of agents with nonempty input queues
             of messages.

    Notes
    -----

   
    """
    def __init__(self):
        self.ag_to_mq = dict()
        self.ag_list = []
        self.name = None
        
    def register_agent(self, agent):
        """
        Creates queue of MessageSender object
        for agent in the dict self.ag_to_mq.
        
        Parameters
        ----------
        agent : object, agent

        """
        self.ag_to_mq[agent] = queue.Queue()
            

    def start(self):
        """
        While there is an agent 
        with a nonempty input channel:
           1. Pick a random agent, ag, with a nonempty input.
           2. mq is the message queue to agent ag.
           3. message_and_sender is at the head of mq
           4. Call ag.receive(..)
           5. self.ag_list is a list of agents with nonempty
                queue of input messages.

        """
        self.ag_list = [ag for ag in self.ag_to_mq.keys()
                            if not self.ag_to_mq[ag].empty()]
        
        while self.ag_list:
            ag = random.choice(self.ag_list)
            mq = self.ag_to_mq[ag]

            message_and_sender = mq.get()
            ag.receive(message_and_sender.message,
                       message_and_sender.sender)

            self.ag_list = [ag for ag in self.ag_to_mq.keys()
                           if not self.ag_to_mq[ag].empty()]

            
#------------------------------------------------------ 
# engine is a shared variable for all classes
engine = Engine()

#------------------------------------------------------
class Agent(object):
    """
    The Base Class for all agents.

    """
    def __init__(self):
        engine.register_agent(self)

    def send(self, message, receiver):
        message_and_sender = MessageAndSender(
            message=message, sender=self)
        engine.ag_to_mq[receiver].put(message_and_sender)

    def receive(self, message, sender):
        pass

import random
class PositiveNumbersSource(Agent):
    def __init__(self, n, receiver):
        Agent.__init__(self)
        self.n = n
        self.receiver = receiver
        self.name = "PositiveNumbersSource"

    def receive(self, message, sender):
        if self.n > 0:
            self.n = self.n - 1
            message = random.randint(1, 10)
            self.send(message, self.receiver)
            self.send("wakeup", self)
        
class PrintMessages(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.name = "PrintMessages"
    
    def receive(self, message, sender):
        print('message = ', message)
        print('sender = ', sender.name)
        print()


#-------------------------------------------
def test():
    print_messages = PrintMessages()
    positive_number_source = PositiveNumbersSource(
        n=3, receiver=print_messages)
    positive_number_source.send("wakeup", positive_number_source)
    
    engine.start()
    

if __name__ == '__main__':
    test()
