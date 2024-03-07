import Listeners


class socket_base:
    def __init__(self,port=""):
        self.port = port
        self.host = "*"

class socket_pool:
    def __init__(self):
        self.pool = []

    def get_env_listener(self):
        for _ in range(len(self.pool)):
            if isinstance(self.pool[_],Listeners.env_listener):
                return self.pool[_]
        return None


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


    def get_all_active_port_numbers(self):
        ports = []
        for _ in range(len(self.pool)):
            ports.append(self.pool[_].port)
        return ports