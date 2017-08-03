# my server 
import socket,sys,urllib
from threading import Thread
import datetime
import os,urlparse
import argparse
import requests,time,json
from time import sleep
from firebase import firebase

PORT = int(sys.argv[1])
firebase = firebase.FirebaseApplication(os.environ['furl'], None)

class Client(Thread):
    def __init__(self,cs,ca):
        Thread.__init__(self)
        self.cs = cs
        self.ca = ca
    def run(self):
        handle(self,self.cs,self.ca)
def handle(self,client,client_address):
    req = client.recv(65535)
    res = 'HTTP/1.1 200 OK\r\n'
    try:
        path = req.split(" ",3)[1][1:]
        data = datetime.datetime.now().strftime("%I:%M:%S:%f%p on %B %d, %Y")
        xt = path[2:].split('&')
        dt = dict()
        for xtz in xt:
            dtz = xtz.split('=')
            if len(dtz) == 2:
                dt[dtz[0]] = dtz[1]
        if dt['date']:
            data = [data,dt['date']];
        dt['date'] = data
        firebase.post('/',dt)
        res = res+'Content-Type: text/plain\r\n'
        res = res+'\r\n'+data
    except Exception as e:
        res = res+repr(e)#.replace('\n','<br>')
    client.sendall(res)
    client.close()
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client, client_address = listen_socket.accept()
    c = Client(client,client_address)
    c.start()
