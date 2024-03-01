import time
import random
import zmq
import numpy as np
import multiprocessing
import queue
class Listener:
    def __init__(self,callback,host="*",port="12345"):
        self.host = host
        self.port = port

        if not callable(callback):
            print("call back is not callable")
            return
        self.callback = callback
        self.message_queue = multiprocessing.Queue()
        self.listen_process = multiprocessing.Process(target=self.listen,args=(self.callback,))
        self.listen_process.start()


    def process_message(self,message):
        #start stop pause.
        control_words = ["start","stop","pause"]
        if str(message) in control_words:
            if "start simulation" in str(message):
                with open("simulation_details.txt", 'r') as file:
                    # Read the entire contents of the file
                    file_contents = file.read()
                    return file_contents
        else:
            self.message_queue.put_nowait(message)


    def listen(self,callback):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://{self.host}:{self.port}")
        while True:
            #  wait request from client
            message_rx = socket.recv()
            response = callback(self=self,message=message_rx)
            #  do something
            time.sleep(0.1)
            socket.send_string(response)


class Env_listener(Listener):
    def __init__(self, callback, host, port):
        super().__init__(callback, host, port)

        self.host = host
        self.port = port
        self.callback = callback



    def process_message(self,message):
        super().process_message(message)
        return "return"


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
    #listener_ = Listener(Listener.process_message)
    env_ = env_base()


    print("listening!")
