from receiver_server import Server
from gevent import socket

udp_port = 4444
def start_server(port=None):

    if port == None:
        port = udp_port
    server = Server(':' + str(port))
    server.start()
    return server


def send_message(message, address, port=None):

    if port == None:
        port = udp_port

    address = (address, port)

    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.connect(address)
    sock.send(message)
    sock.close()