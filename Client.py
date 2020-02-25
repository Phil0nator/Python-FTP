from network import Network
import base64
n = Network()
print(n.connect())
class File():
    def __init__(self, name, datatype, dataList = [], dataSTR =""):
        self.name = name
        self.datatype = datatype
        self.dataList = dataList
        self.dataSTR = dataSTR
    def write(self):
        if len(self.dataList) > 0:
            with open("%s%s"%(self.name,self.datatype), "w+") as file:
                for line in self.dataList:
                    file.write(line)
        if len(self.dataSTR) > 0:
            print(self.dataSTR)
            fh = open("%s%s"%(self.name,self.datatype), "wb")
            fh.write(base64.b64decode(self.dataSTR))
            fh.close()
print("# NOTE: because of limited resources we recommend not sending files exeeding 10mb, however nothing will stop you from doing so.")
while True:
    mode = str(input("(s,r, DIR)Send, recieve, or check what's available:"))
    if mode == "DIR":
        DIR = n.DIR()
        for file in DIR:
            print(file)
    if mode == "s":
        #name,datatype,data
        name = str(input("NAME:"))
        datatype = str(input("(.py,.txt,.png, etc...)Type of data:"))
        filePath = str(input("PATH:"))
        if datatype == ".py" or datatype == ".txt" or datatype == "py" or datatype == "txt":
            with open(filePath) as file:
                lines = []
                for line in file:
                    lines.append(line)
            #n.send("~~~create|%s|%s|%s"%(name,datatype,lines))
            textObj = File(name, datatype, dataList = lines)
            n.sendDump("~~~create", textObj)

        if datatype == ".PNG" or datatype == ".png" or datatype == ".jpg" or datatype == ".JPG":
            with open(filePath, "rb") as imageFile:
                str = base64.encodestring(imageFile.read())
                imgobj = File(name,datatype,dataSTR=str)
                print(imgobj)
                n.sendDump("~~~create", imgobj)
        else:
            print("WARNING: This is a file type unusual to this program. If it is a bytes file it should work, but this is still experimental.")
            with open(filePath, "rb") as unkownFile:
                str = base64.encodestring(unkownFile.read())
                unkownFile = File(name,datatype,dataSTR=str)
                print(unkownFile)
                n.sendDump("~~~create", unkownFile)
    elif mode == "r":
        requested = str(input("NAME OF FILE: "))
        folder = str(input("Desired Folder To In: "))
        recieved = n.get("~~~get,%s"%requested)
        recieved.write()
        print("SUCCESSFUL creation")
    else:
        print("ERROR: mode type invalid")
