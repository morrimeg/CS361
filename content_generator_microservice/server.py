"""
micro_server.py

This module contains the definition of the micro_server class that
will listen for requests from other microservices on the port specified
and initialization. These ports are defined in the STDPORTS dictionary.
each different microservice will listen on its own individual port.

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


class micro_server:

    def __init__(self, call_back, MSERVICE):
        self.__STDPORTS = {'LIFE_GEN': 5467, 'CONT_GEN': 5468, 'POP_GEN': 5479, 'PERS_GEN': 5480}

        # address data members
        self.__PORT = self.__STDPORTS[MSERVICE]
        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__ADDR = (self.__IP, self.__PORT)

        # functional data members
        self.__HEAD = 64  # header of 64 bytes for message protocol
        self.__DCON = "&END"
        self.__call_back = call_back
        self.__socket = self.define_micro_socket()

    def define_micro_socket(self):
        """Create and bind socket to port 5467"""
        micro_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        micro_socket.bind(self.__ADDR)
        return micro_socket

    def start_listening(self):
        """continuously listen for connections"""
        self.__socket.listen(100)
        while True:
            # blocks until connection to socket is detected
            client, address = self.__socket.accept()
            request = self.handle_client_requests(client, address)

            # process client request
            response = self.process_client_request(request, client)

            if response is not None:

                # send response to client
                self.send_response(client, response)

    def handle_client_requests(self, client, address):
        # print successful connection message
        print(f"New Connection from {address}")

        connected = True
        while connected:
            # fetch length of incoming message from header
            data_length = self.get_data_length(client)

            # fetch incoming request
            request = self.get_actual_data(client, data_length)
            return request

    def get_data_length(self, client):
        """helper to handle_client_requests()"""
        # blocks until request header recieved
        data_length = client.recv(self.__HEAD).decode('utf-8')

        # cast decoded header as integer length
        data_length_int = int(data_length)

        return data_length_int

    def get_actual_data(self, client, data_length):
        """helper to handle_client_requests()"""
        # blocks until request data recieved
        request = client.recv(data_length).decode('utf-8')
        return request

    def process_client_request(self, request, client):
        """processes a client request with the desired callback function"""

        # check for close request
        if request == self.__DCON:
            client.close()
            return None
        else:
            # return data from responding microservice
            return self.__call_back(request)

    def send_response(self, client, response):
        """Sends the requested data back to the client"""
        response_msg = response.encode('utf-8')
        response_length = len(response_msg)

        send_length = str(response_length).encode('utf-8')
        send_length += b' ' * (self.__HEAD - len(send_length))

        client.send(send_length)  # send header with response message length
        client.send(response_msg)  # send response message content

# main function for test
if __name__ == "__main__":

    # test callback function
    def call_back(request):
        print(f'I am the Callback Function!! The request is {request}')
        return 'Success!!'

    server = micro_server(call_back, 'LIFE_GEN') # create a life generator server
    server.start_listening()





