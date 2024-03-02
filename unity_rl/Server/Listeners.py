import time
import zmq
import multiprocessing
import queue


class listener:
    def __init__(self, callback, host="*", port="12345"):
        self.host = host
        self.port = port

        if not callable(callback):
            print("call back is not callable")
            return

        self.callback = callback
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
            time.sleep(0.1)
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
