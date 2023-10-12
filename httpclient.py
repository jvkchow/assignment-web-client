#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        # break down the header until just the response code number is left
        header = self.get_headers(data)
        header_components = header.split("\r\n")
        code = header_components[0].split()
        return int(code[1])

    def get_headers(self,data):
        whole = data.split("\r\n\r\n") # split between the header and the body
        return whole[0] # return the first part (the header)

    def get_body(self, data):
        whole = data.split("\r\n\r\n") # split between the header and the body
        return whole[1] # return the second part (the body)
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):

        code = 500
        body = ""

        # get the necessary components from the url
        components = urllib.parse.urlparse(url)
        host = components.hostname
        port = components.port
        scheme = components.scheme
        path = components.path

        # get the proper port number if none was found
        if scheme == "http" and port == None:
            port = 80
        elif scheme == "https" and port == None:
            port = 443
        
        # create the string for sending the GET request (and change the path to / if a path was not given)
        if path == "":
            request = "GET / HTTP/1.1\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"
        else:
            request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"

        # send the request and retrieve the response
        self.connect(host, port)
        self.socket.sendall(bytearray(request, 'utf-8'))
        response = self.recvall(self.socket)
        
        # get the code and body to return back to the caller
        code = self.get_code(response)
        body = self.get_body(response)

        self.socket.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        # get the necessary components from the url
        components = urllib.parse.urlparse(url)
        host = components.hostname
        port = components.port
        scheme = components.scheme
        path = components.path

        # get the proper port number if none was found
        if scheme == "http" and port == None:
            port = 80
        elif scheme == "https" and port == None:
            port = 443

        # get the content of the argument if there is any
        content = ""
        if args != None:
            for key, value in args.items():
                content += f'{key}={value}&'
            content_length = len(content)
        else:
            content_length = 0

        # create the string for sending the POST request (and change the path to / if a path was not given)
        if path == "":
            request = "POST / HTTP/1.1\r\nHost: " + host + "\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(content_length) + "\r\nConnection: Closed\r\n\r\n" + content
        else:
            request = "POST " + path + " HTTP/1.1\r\nHost: " + host + "\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(content_length) + "\r\nConnection: Closed\r\n\r\n" + content

        # send the request and retrieve the response
        self.connect(host, port)
        self.socket.sendall(bytearray(request, 'utf-8'))
        response = self.recvall(self.socket)
        
        # get the code and body to return back to the caller
        code = self.get_code(response)
        body = self.get_body(response)

        self.socket.close()

        return HTTPResponse(code, body)
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
