import socket

def get_hostname():
    return socket.gethostname()

def get_ip():
    return socket.gethostbyname(get_hostname())
