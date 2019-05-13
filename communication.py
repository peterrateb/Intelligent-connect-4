from networking import send_message
import numpy as np
class networkAgent():

    def __init__(self,ip_address,port):
        self.ip_address=ip_address
        self.port=port
        self.received_data=None

    def send(self,board,move):
        message=[{'type': 'MV', 'content': move}, {'type': 'BR', 'content': np.int64(board).tolist()}]
        send_message(str(message).encode('ascii'), self.ip_address, self.port)

if __name__ == "__main__":
    y = networkAgent('127.0.0.1', 9998)
    from connect4 import Connect4
    x=Connect4()
    y.send(x.board, 5)