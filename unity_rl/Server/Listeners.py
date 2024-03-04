import time
import zmq
import multiprocessing
import queue


class socket_base:
    def __init__(self,host="*",port=""):
        self.port = port
        self.host = host

class socket_pool:
    def __init__(self,size=0):
        self.pool = []
        for _ in range(size):
            self.pool.append(socket_base(port=self.get_port_number(len(self.pool))))

    def acquire(self):
        if self.pool:
            return self.pool.pop()
        else:
            return socket_base()

    def release(self,socket):
        self.pool.append(socket)




    def add_to_pool(self,socket):
        self.pool.append(socket)

    def get_port_number(self,number=0):
        #ether returns the port number or the first valid port
        for _ in range(len(self.pool)):
            if self.pool[_].port == number:
                self.get_port_number(number+1)
        return number



class listener(socket_base):
    #listens for messages from unity and responds
    def __init__(self, callback, host="*", port="12345"):
        super().__init__(host, port)
        self.host = host
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
    def __init__(self, callback, host, port):
        super().__init__(callback, host, port)

        self.host = host
        self.port = port
        self.callback = callback

    def process_message(self, message):
        super().process_message(message)
        return "return"


class agent_listener(listener):
    def __init__(self, callback, host, port):
        super().__init__(callback, host, port)

        self.host = host
        self.port = port
        self.callback = callback

    def process_message(self, message):
        super().process_message(message)
        return "return"
