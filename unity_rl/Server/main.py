import time
import random
import zmq
import numpy as np
import multiprocessing
import queue

from Listeners import Env_listener,Listener


class env_base:
    def __init__(self):
        self.listen = Env_listener(Env_listener.process_message,"*","12344")
        self.on_start()

    def on_start(self):
        self.on_step()

    def poll_listener(self):
        try:
            received_message = self.listen.message_queue.get(False)
            return received_message
        except queue.Empty:
            pass

    def on_step(self):
        while True:
            mess = self.poll_listener()
            if mess != None:
                print(mess)




if __name__ == '__main__':

    env_ = env_base()


    print("listening!")
