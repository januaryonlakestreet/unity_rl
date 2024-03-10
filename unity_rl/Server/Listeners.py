import time
import zmq
import multiprocessing
import queue
from object_pool import socket_base




class asker(socket_base):
    #listens for messages from unity and responds
    def __init__(self, callback, port="12345",messg = "tmp"):
        super().__init__(port)
        self.port = port

        if not callable(callback):
            print("call back is not callable")
            return

        self.callback = callback
        self.message = messg

        self.message_queue = multiprocessing.Queue()
        self.listen_process = multiprocessing.Process(target=self.listen, args=(self.callback,self.message))
        self.listen_process.start()

    def process_message(self, message):
        # start stop pause.
        control_words = ["start", "stop", "pause"]
        if str(message) in control_words:
            if "start" in str(message):
                with open("simulation_details.txt", 'r') as file:
                    # Read the entire contents of the file
                    file_contents = file.read()
                    return file_contents
        else:
            self.message_queue.put_nowait(message)

    def is_utf8(self,encoded_string):
        try:
            decoded_string = encoded_string.decode('utf-8')
            return True
        except UnicodeDecodeError:
            return False
    def listen(self, callback,mess):

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.bind(f"tcp://{self.host}:{self.port}")
        while True:

            socket.send_string(str(mess))
            print("sent message")
            reply_message = socket.recv_string()
            response = callback(self=self, message=reply_message)
            print(reply_message)






class listener(socket_base):
    #listens for messages from unity and responds
    def __init__(self, callback, port="12345"):
        super().__init__(port)
        self.port = port

        if not callable(callback):
            print("call back is not callable")
            return

        self.callback = callback

        self.ask_process = None
        self.message_queue = multiprocessing.Queue()
        self.listen_process = multiprocessing.Process(target=self.listen, args=(self.callback,))
        self.listen_process.start()

    def process_message(self, message):
        # start stop pause.
        control_words = ["start", "stop", "pause"]
        if str(message) in control_words:
            if "start" in str(message):
                with open("simulation_details.txt", 'r') as file:
                    # Read the entire contents of the file
                    file_contents = file.read()
                    return file_contents
        else:
            self.message_queue.put_nowait(message)


    def listen(self, callback):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://{self.host}:{self.port}")
        while True:
            #  wait request from client
            message_rx = socket.recv()
            response = callback(self=self, message=message_rx)
            #  do something

            socket.send_string(response)


class env_listener(listener):
    def __init__(self, callback, port):
        super().__init__(callback, port)

        self.port = port
        self.callback = callback

    def process_message(self, message):
        super().process_message(message)
        return "return"


class agent_listener(listener):
    def __init__(self, callback,  port):
        super().__init__(callback, port)

        self.port = port
        self.callback = callback

    def process_message(self, message):
        super().process_message(message)
        return "return"
