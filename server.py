import socket
from _thread import *
import pickle
import base64
import math
import sys
from time import sleep
from pathlib import Path
import os
import time
image_types = [".PNG",".png",".JPG",".jpg",".jpeg"]
assets = "/media/pi/Lexar/RASPI/PFTP Assets"
####MODULE CLASSES
class File():
    def __init__(self, name, datatype, dataSTR =""):
        self.name = name
        self.datatype = datatype
        self.dataSTR = dataSTR
    def write(self):
        #print(self.dataSTR)
        fh = open("%s/%s%s"%(assets, self.name,self.datatype), "wb")
        fh.write(base64.b64decode(self.dataSTR))
        fh.close()
        updateLog("New File creation called: %s.%s"%(self.name,self.datatype))


###END



#"172.16.1.57"
#server = "172.16.1.57"
#server = "107.208.10.118"
server = "172.16.1.44"
port = 5554

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:

    print("binded")
    print("binded")
    print("binded")
except socket.error as e:
    str(e)
s.bind((server, port))
s.listen(4)
print("Waiting for a connection, Server Started")
def sendDump(prefix, obj,conn):
    obj = pickle.dumps(obj)
    #obj = "%s|EOF|"%str(obj)
    #obj = obj.encode()
    #print(obj)
    lengthDump = sys.getsizeof(obj)
    print("Create Request sent, with Bytes size of %s Bytes"%lengthDump)
    if lengthDump > 100000:
        print("The file you have selected is very large, and sending could take some time. Please do not close this window if you wish the process to continue.")
        print("Approx time: %s minutes"%((lengthDump/1500)/120))
    conn.sendall(("%s|%s"%(prefix, lengthDump)).encode())
    print(obj)
    #print(a)
    #print(obj)

    sleep(.05)

    a = conn.sendall(obj)
    print(a)
    conn.sendall("|EOF|".encode())
    print(a)
    print(obj)
    print("OBJ SENT")

DIR = []
def updateDir():
    global DIR
    #Update DIr list with items from ASSETS
    DIR = []
    for root, dirs, files in os.walk(assets):
        for filename in files:
            DIR.append(filename)

updateDir()
print(DIR)
def threaded_client(conn):
    global chats
    reply = ""
    while True:
        try:
            data = conn.recv(40960).decode()
        except:
            break
        if not data:
            break
        else:
            print("Some data got" + data)
            updateLog("Some data got" + data)
            if "~~~DIR" in data:
                updateDir()
                msg = ""
                for item in DIR:
                    msg = "%s|%s"%(msg,item)
                conn.sendall(msg.encode())
            if "~~~get" in data:
                #get,name
                params = data.split(",")
                name = params[1]
                path = "%s/%s"%(assets, name)
                with open(path, "r") as file:
                    fileType = file.name.split(".")[1]
                    print(fileType)
                with open(path, "rb") as imageFile:
                    str = base64.encodestring(imageFile.read())
                    imgobj = File(name,fileType,dataSTR=str)
                    print(imgobj)
                    #conn.sendall(pickle.dumps(imgobj))
                    sendDump("~~~create",imgobj,conn)
                '''
                
                datatype = ".%s"%fileType
                if datatype == ".py" or datatype == ".txt" or datatype == "py" or datatype == "txt":
                    with open(name) as file:
                        lines = [line for line in file]
                    #n.send("~~~create|%s|%s|%s"%(name,datatype,lines))
                    textObj = File(name, datatype, dataList = lines)
                    #conn.sendall(pickle.dumps(textObj))
                    sendDump("~~~create",textObj,conn)

                if datatype in image_types:
                    with open(path, "rb") as imageFile:
                        str = base64.encodestring(imageFile.read())
                        imgobj = File(name,datatype,dataSTR=str)
                        print(imgobj)
                        #conn.sendall(pickle.dumps(imgobj))
                        sendDump("~~~create",imgobj,conn)
                else:
                    with open(path, "rb") as imageFile:
                        str = base64.encodestring(imageFile.read())
                        imgobj = File(name,datatype,dataSTR=str)
                        print(imgobj)
                        #conn.sendall(pickle.dumps(imgobj))
                        sendDump("~~~create",imgobj,conn)
                '''
            if "~~~create" in data:
                params = data.split("|")
                #obj = pickle.loads(params[1])
                print(params[1],"expected size")
                time = int(params[1])


                ab = b''

                too_many = 0
                while True:
                    too_many += 1
                    if too_many>9999999999:
                        break
                    if "|EOF|" not in "%s"%ab:
                        recieved = conn.recv(1500)
                        print("Got Packet %s/%s"%(too_many,time/1500))
                        #ab = r"%s%s"%(ab,recieved.decode())
                        #ab = "%s%s"%(ab,recieved)
                        ab = ab + recieved
                    else:
                        print("Recieved all Packets")
                        break
                #a = recvfrom(conn,params[1])

                #ab=ab.decode()[0:len(ab)-5]
                #ab = ab.decode().replace(r"%s"%(" \ ".strip(" ")) , "//")
                #ab = ab.encode()
                #print(ab)
                print("\n\n\n\n\n\n\n\n")
                #print(ab[0:40])
                with open("recievedpickle.txt", "w+") as doc:
                    doc.write("%s"%ab)
                    content = doc.readline()
                obj = ab
                print(sys.getsizeof(ab), "size of object returned")
                print("DIFF:", time-sys.getsizeof(ab))
                #print(ab.decode())
                #obj = pickle.loads(b'\\x80\\x03c__main__\\nFile\\nq\\x00)\\x81q\\x01}q\\x02(X\\x04\\x00\\x00\\x00nameq\\x03X\\x07\\x00\\x00\\x00testdocq\\x04X\\x08\\x00\\x00\\x00datatypeq\\x05X\\x04\\x00\\x00\\x00.txtq\\x06X\\x08\\x00\\x00\\x00dataListq\\x07]q\\x08(X\\x08\\x00\\x00\\x00TESTDOC\\nq\\tX\\x14\\x00\\x00\\x00Hi my name is steve\\nq\\nX\\x14\\x00\\x00\\x00this is a test file\\nq\\x0beX\\x07\\x00\\x00\\x00dataSTRq\\x0cX\\x00\\x00\\x00\\x00q\\rub.')
                obj = pickle.loads(ab)
                #print(obj)
                print("WRITING")
                obj.write()
                print("SUCCESSFUL TRANSFER")
                '''
                if obj.datatype == ".py" or obj.datatype == ".txt" or obj.datatype == "py" or obj.datatype == "txt":

                    obj.write()


                elif obj.datatype in image_types:
                    print("writing")
                    #fh = open("%s%s"%(name,datatype), "wb")
                    #fh.write(str.decode(data))
                    #fh.close()
                    obj.write()

                else:
                    print("Writing")
                    obj.write()
                print("SUCCESSFUL creation")
                updateDir()
                '''

def updateLog(info):
    with open("LOG.txt", "a") as log:
        localtime = time.asctime( time.localtime(time.time()) )
        log.write("%s at %s\n"%(info,localtime))
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    updateLog("Connected to: %s"%str(addr))
    conn.send(str.encode("SUCCESSFUL CONNECTION"))
    start_new_thread(threaded_client, (conn,))
