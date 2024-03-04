
import multiprocessing
import queue
import numpy as np
from torchrl.modules import MLP
import torch

from Listeners import env_listener



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
        self.episodes = 10000
        self.episode_length = 100

        self.agents = []
        self.agents.append(agent("tmp1"))
        self.agents.append(agent("tmp2"))



    def on_start(self):
        print("*********************************************************")
        print("loading enviroment from file")
        print("expecting X gameobjects")
        print("found X gameobjects")
        print("*********************************************************")
        print("GO!")
        print("")

        #for agent_idx in range(len(self.agents)):
         #   agent_name = self.agents[agent_idx].game_object_name

        # for each agent
        # ask unity do you have a game object with this name?
        # can the game object send and recv messages?
        # if yes add to list
        # send gm listen details
        # if not error
        # each agent should have own listener
        # port should be env port + agent id

        self.listener.ask("hi!")
        self.on_step()


    def register_agents(self):
        # verifys the unity scene has the agent based on supplied gameobject name
        #if no removes from list
        pass

    def get_transform(self,game_object_name):
        # returns the transfrom of the game object by searching list for agent with right name
        pass

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





class basic_env(env_base):
    def __init__(self):
        super().__init__()

        self.episodes = 1000
        self.agents.append(agent("tmp1"))
        self.agents.append(agent("tmp2"))




class game_object:
    def __init__(self,game_object_name):
        self.game_object_name = game_object_name

    def get_transform(self):
        # turns tuple of gameobject transform [location,scale,rotation(euler)]
        pass
class agent(game_object):
    def __init__(self,game_object_name):
        super().__init__(game_object_name)

        self.game_object_name = game_object_name
        self.brain = MLP(92,92)







if __name__ == '__main__':
    env_threaded = multiprocessing.Process(target=env_base())


    #env_ = env_base()


    print("listening!")
