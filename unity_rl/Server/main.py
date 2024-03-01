
import multiprocessing
import queue
import numpy as np
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

    def on_start(self):
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

if __name__ == '__main__':

    obs_space = space("discrete",(3,2,1),-100,100)

    #env_threaded = multiprocessing.Process(target=env_base())


    #env_ = env_base()


    print("listening!")
