
import multiprocessing
import queue
import numpy as np
from torchrl.modules import MLP
import torch

from Listeners import env_listener,Listener



class space:
    def __init__(self,shape,low,high):
        self.shape = shape
        self.low = low
        self.high = high

    def sample(self):
        return np.random.uniform(self.low, self.high, size=self.shape)


class env_base:
    def __init__(self):
        self.listener = env_listener(env_listener.process_message,"*","12344")
        self.obs_space = None
        self.action_space = None
        self.on_start()
        self.episodes = 1000000000000

        self.agents = []
        self.agents.append(agent("tmp1"))
        self.agents.append(agent("tmp2"))


    def on_start(self):
        # for each agent
        # ask unity do you have a game object with this name?
        # can the game object send and recv messages?
        # if yes add to list
        # send gm listen details
        # if not error
        # each agent should have own listener
        # port should be env port + agent id


        self.on_step()

    def poll_listener(self):
        try:
            received_message = self.listener.message_queue.get(False)
            return received_message
        except queue.Empty:
            pass

    def on_step(self):
        while True:
            mess = self.poll_listener()
            if mess != None:
                print(mess)

            self.episodes -= 1
            if self.episodes < 0:
                return

class agent:
    def __init__(self,game_object_name):
        self.brain = MLP(92,92)





if __name__ == '__main__':
    a_= agent()



    env_threaded = multiprocessing.Process(target=env_base())


    #env_ = env_base()


    print("listening!")
