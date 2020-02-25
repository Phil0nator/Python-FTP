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
        #self.server = "~~~.~~~.~~.~~~"
        self.server = "107.208.10.118"
        #self.server = "localhost"
        self.port = 5554
        self.addr = (self.server, self.port)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(4096).decode()

    def send(self, data):
        try:
            self.client.send(data.encode())
            #return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
    def DIR(self):
        self.client.send("~~~DIR".encode())
        data = self.client.recv(4096*10).decode()
        DIR = data.split("|")
        return DIR
    def get(self, data):
        self.client.sendall(data.encode())
        data = self.client.recv(1024).decode()
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
                print("  --$ Got Packet %s/%s"%(too_many,time/1500))
            else:
                print("ENDING:::" + recieved.decode() + "AFTER:" + "%s"%(too_many))
                break
        obj = ab
        print(sys.getsizeof(ab), "size of object returned")
        print("DIFF:", time-sys.getsizeof(ab))
        obj = pickle.loads(ab)
        #print(obj)
        return obj
    def sendDump(self, prefix, obj):
        obj = pickle.dumps(obj)
        lengthDump = sys.getsizeof(obj)
        self.client.send(("%s|%s"%(prefix, lengthDump)).encode())
        print("Create Request sent, with Bytes size of %s Bytes"%lengthDump)
        if lengthDump > 100000:
            print("The file you have selected is very large, and sending could take some time. Please do not close this window if you wish the process to continue.")
            print("Approx time: %s minutes"%((lengthDump/1500)/120))
        sleep(.1)
        a = self.client.sendall(obj)
        self.client.sendall("|EOF|".encode())
        #print(a)
        #print(obj)
        #print("OBJ SENT")
import base64
n = Network()
print(n.connect())
class File():
    def __init__(self, name, datatype,dataSTR =""):
        self.name = name
        self.datatype = datatype
        self.dataSTR = dataSTR
    def write(self):
        print(self.dataSTR)
        #fh = open("%s%s"%(self.name,self.datatype), "wb")
        fh = open("%s"%self.name, "wb")
        fh.write(base64.b64decode(self.dataSTR))
        fh.close()
print("# NOTE: because of limited resources we recommend not sending files exeeding 10mb, however nothing will stop you from doing so.")
while True:
    print('''
            s    --Send a file
            r    --Recieve a file
            DIR  --View all files available
            u    --update software
    ''')
    mode = input("--$")
    if mode == "DIR" or mode == "dir":
        DIR = n.DIR()
        for file in DIR:
            print(file)
    elif mode == "u":
        recieved = n.get("~~~get,PFTP.py")
        recieved.write()
        print("sucessful update, restart the program to take effect.")
        break
    elif mode == "sudo":
        pw = input("Password --$")
        command = input("###SUDO###--$")
        n.send("sudo|%s|%s"%(pw,command))
    elif mode == "s":
        #name,datatype,data
        name = input("NAME:")
        datatype = input("(.py,.txt,.png, etc...)Type of data:")
        filePath = input("PATH:")
        with open(filePath, "rb") as imageFile:
            str = base64.encodestring(imageFile.read())
            imgobj = File(name,datatype,dataSTR=str)
            print(imgobj)
            n.sendDump("~~~create", imgobj)
    elif mode == "r":
        requested = input("NAME OF FILE: ")
        folder = input("Desired Folder To In: ")
        recieved = n.get("~~~get,%s"%requested)
        recieved.write()
        print("SUCCESSFUL creation")
    else:
        print("ERROR: mode type invalid")
