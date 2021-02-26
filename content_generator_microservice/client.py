"""
    micro_server.py

    This module contains the definition of the micro_client class. This class
    can be instantiated with a keyword in order to specify which microservice it will
    be requesting from. A new micro_client should be instantiated for each unique request.
    connections will be automatically closed once data is recieved back from the server.

    Sources Cited:
    Title: Python Socket Programming Tutorial
    Author: Tech With Tim
    URL: https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2593s
    Description: We followed this tutorial and used/refactored the code into our
    own implementation to build the server as a portable class.

    Sources Cited:
    Title: Sockets Tutorial with Python 3 part 3 - sending and receiving Python Objects w/ Pickle
    Author: HSKinsley (Sentdex)
    URL: https://www.youtube.com/c/sentdex/about
    Description: We followed this tutorial and used it as a reference for using
    pickling with python sockets
    """
import socket


class micro_client:
    def __init__(self, REQ_DEST):
        self.__STDPORTS = {'LIFE_GEN': 5467, 'CONT_GEN': 5468, 'POP_GEN': 5479,
                           'PERS_GEN': 5480}

        # address data members
        self.__PORT = self.__STDPORTS[REQ_DEST]
        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__ADDR = (self.__IP, self.__PORT)

        # functional data members
        self.__HEAD = 64  # header of 64 bytes for message protocol
        self.__DCON = "&END"
        self.__socket = self.define_micro_socket_client()

    def define_micro_socket_client(self):
        """Create and bind socket to port 5467"""
        micro_socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        micro_socket_client.connect(self.__ADDR)
        return micro_socket_client

    def wait_for_response(self):
        """waits for response data and closes socket connection"""
        # recieve header and data from server
        response_length = self.get_response_length()
        server_response = self.get_response_data(response_length)

        # close connection
        self.__socket.close()
        return server_response

    def send_message(self, msg):
        """Sends the message to the server"""
        message = msg.encode('utf-8')
        message_length = len(message)

        send_length = str(message_length).encode('utf-8')
        send_length += b' ' * (self.__HEAD - len(send_length))

        self.__socket.send(send_length)  # send header with message length
        self.__socket.send(message)  # send request message content

        return self.wait_for_response()

    def get_response_length(self):
        """intercepts header containing response length"""
        # blocks until request header recieved
        server_resp_header = self.__socket.recv(self.__HEAD).decode('utf-8')

        # cast decoded header as integer length of incoming data
        data_length_int = int(server_resp_header)
        return data_length_int

    def get_response_data(self, response_length):
        """recieves response data content"""
        # blocks until request data recieved
        response = self.__socket.recv(response_length).decode('utf-8')
        return response


# main function for test
if __name__ == "__main__":
    client = micro_client('LIFE_GEN')  # create a life generator request client

    response_data = client.send_message("Generate some life!!")

    print(f'Response from server was: {response_data}')
