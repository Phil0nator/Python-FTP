import socket
import pickle
from time import sleep
import sys
from pathlib import Path
def clearWork():
    with ("work.txt", "wb") as work:
        work.write(0)
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server = "172.16.1.57"
        self.server = "107.208.10.118"
        #self.server = "localhost"
        self.port = 5554
        self.addr = (self.server, self.port)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(4096).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            #return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
    def DIR(self):
        self.client.send("~~~DIR".encode())
        data = self.client.recv(4096*10).decode()
        DIR = data.split("|")
        return DIR
    def get(self, data):
        self.client.sendall(str.encode(data))
        sleep(.1)
        data = self.client.recv(40960).decode()
        print(data)
        params = data.split("|")
        print(params[1],"expected size")
        time = int(params[1])
        if time > 100000:
            print("The file you have selected is very large, and sending could take some time. Please do not close this window if you wish the process to continue.")

        ab = b''
        too_many = 0
        while True:
            too_many += 1
            if too_many>9999999999:
                break
            if "|EOF|" not in "%s"%ab:
                recieved = self.client.recv(1500)
                ab = ab + recieved
                print("Got Packet %s/%s"%(too_many,time/1500))
            else:
                print("ENDING:::" + recieved.decode() + "AFTER:" + "%s"%(too_many))
                break
        obj = ab
        print(sys.getsizeof(ab), "size of object returned")
        print("DIFF:", time-sys.getsizeof(ab))
        obj = pickle.loads(ab)
        print(obj)
        return obj
    def sendDump(self, prefix, obj):
        obj = pickle.dumps(obj)
        #obj = "%s|EOF|"%str(obj)
        #obj = obj.encode()
        #print(obj)
        lengthDump = sys.getsizeof(obj)
        self.client.send(str.encode("%s|%s"%(prefix, lengthDump)))
        print("Create Request sent, with Bytes size of %s Bytes"%lengthDump)
        if lengthDump > 100000:
            print("The file you have selected is very large, and sending could take some time. Please do not close this window if you wish the process to continue.")
            print("Approx time: %s minutes"%((lengthDump/1500)/120))
        sleep(.1)
        a = self.client.sendall(obj)
        self.client.sendall("|EOF|".encode())
        print(a)
        print(obj)
        print("OBJ SENT")
