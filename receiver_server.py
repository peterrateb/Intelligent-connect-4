from gevent.server import DatagramServer
import gevent
import json


received_data=""
class Server(DatagramServer):
    def handle(self, data, address):
        #global received_data
        received_data =json.loads(data.decode("utf-8").replace("'", '"'))
        print(received_data)



if __name__ == "__main__":
    server = Server(':9998') # creates a new server
    server.start()
    while 1:
        gevent.sleep(0)
        if received_data=="":
            continue
        print(received_data)
        received_data=""