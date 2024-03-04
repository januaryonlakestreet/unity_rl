import time
import zmq
import multiprocessing
import queue


class socket_base:
    def __init__(self,host="*",port=""):
        pass

class socket_pool:
    def __init__(self,size=0):
        self.pool = []
        self.pool_start_port = 0
        for _ in range(size):
            self.pool.append(socket_base())

    def acquire(self):
        if self.pool:
            return self.pool.pop()
        else:
            return socket_base()

    def release(self,socket):
        self.pool.append(socket)



class socket_manager:
    #manages all sockets
    #makes sure all ports makes sure no overlap
    _instance = None

    def __init__(self):
        self.start_port = 0

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(socket_manager, cls).__new__(cls)
            cls.start_port = 0
        return cls._instance

    def get_new_port_number(self):
        port = self.start_port
        port = port + 1
        self.start_port = port
        return port











class listener:
    #listens for messages from unity and responds
    def __init__(self, callback, host="*", port="12345"):
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

    def ask(self,message):
        self.ask_process = multiprocessing.Process(target=self._ask, args=(self.ask_response,message))
        self.ask_process.start()


    def _ask(self, callback,message):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://{self.host}:{self.port+1}")

        while True:
            socket.send_string(message)
            #  wait request from client
            message_rx = socket.recv()
            response = callback(self=self, message=message_rx)
            print(response)


    def ask_response(self,message):
        print("t")
        self.ask_process.stop()


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
