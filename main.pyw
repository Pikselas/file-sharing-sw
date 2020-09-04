#PIKSELAS Solutions....
#fILE SHARING SW.
#COMPLETED => ANY FILE SENDING & RECEIVING.
#             PARALLEL FILE SENDING AND RECEIVING.
#             GUI PROGRAMMING.
#             FILE SENDING AND RECEIVING AT A TIME.
#             MULTIPLE DEVICE CONNECTION AT A TIME.
#             OPTION FOR CHANGING PORTS FOR PARALLEL FILE RECEIVING.
import socket
import os
import tkinter as ui
from tkinter import messagebox
from tkinter.ttk import Progressbar
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
port = 367
ServerIP = "127.0.0.1"
SenderServerPort = 367

SendDir = "FileSend/"
ReceiveDir = "FileReceived/"

window = ui.Tk()
window.iconbitmap(default = "favicon.ico")
ActivityVar = "Started PIK-SHARE" 
activity = ui.Text(window,height = 8,width = 30,background = "lavender",foreground = "navy")
progress = Progressbar(window, orient = "horizontal", length = 350, mode = 'determinate')

theme = 0

def SendFile(client,Directory):
    global progress,ActivityVar
    try:
        FileList = os.listdir(Directory)
        if len(FileList) == 0:
            raise Exception("THE DIRECTORY "+Directory+" is Empty!")
        else:
            client.send(str(len(FileList)).encode())
            count = 0
            for file in FileList:
                client.recv(100)
                client.send(file.encode())
                file = open((os.path.join(Directory,file)),"rb")
                client.recv(100)
                data = file.read(5000)
                while (data):
                    client.send("continue".encode())
                    client.recv(100)
                    client.send(data)
                    data = file.read(5000)
                file.close()
                client.send("new".encode())
                count += 1
                progress["value"] = 100 * count / len(FileList)
                window.update_idletasks()
    except FileNotFoundError:
        messagebox.showerror("PATH-NOT-FOUND","NO DIRECTORY EXIST OF NAME "+Directory)
    except Exception as e:
        messagebox.showinfo("information",e)
def RecvFile(server,Directory):
    global progress
    try:
        FileCount = int(server.recv(1024).decode())
        ActivityVar = "\nTOTAL-FILES =>>"+str(FileCount)
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        for count in range(FileCount):
            server.send("true".encode())
            ActivityVar = "\nGetting file name...."
            activity.insert(ui.END,ActivityVar)
            activity.see(ui.END)
            file = server.recv(1024).decode()
            ActivityVar = "\nNAME =>> "+file+" \ncreating file instance"
            activity.insert(ui.END,ActivityVar)
            activity.see(ui.END)
            file = open((os.path.join(Directory,file)),"wb")
            server.send("true".encode())
            while True:
                data = server.recv(1024).decode()
                if data == "continue":
                    server.send("true".encode())
                    data = server.recv(5000)
                    file.write(data)
                else:
                    ActivityVar = "\nCompleted receiving.....\nclosing current file....."
                    activity.insert(ui.END,ActivityVar)
                    activity.see(ui.END)
                    file.close()
                    break
            progress["value"] = 100 * (count+1) / FileCount
            window.update_idletasks
    except FileNotFoundError:
        messagebox.showerror("EXIST-ERROR","NO DIRECTORY EXIST OF THIS NAME "+Directory)
    except Exception as e:
        messagebox.showinfo("Information",e)
def Client(ip,port):
    global ActivityVar,window,activity,progress
    progress["value"] = 0
    window.update_idletasks
    try:
        connector = socket.socket()
        ActivityVar = "\nCreated connector"
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        global ReceiveDir
        ActivityVar = "\nConnecting to =>"+ip
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        connector.connect((ip,port))
        ActivityVar = "Starting file sharing...."
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        RecvFile(connector,ReceiveDir)
        ActivityVar = "Closing connection....."
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        connector.close()
    except ConnectionAbortedError:
        messagebox.showerror("CONNECTION-ERROR","CONNECTION CLOSED BY SERVER "+ip+" ON PORT "+str(port))
    except ConnectionRefusedError:
        messagebox.showinfo("REJECTED",ip+" REJECTED TO SHARE FILES ON PORT "+str(port))
    except Exception as error:
        messagebox.showinfo("Info",error)
    ActivityVar = "\nconnection closed..."
    activity.insert(ui.END,ActivityVar)
def Server(ip,port):
    global ActivityVar,window,activity,progress
    progress['value'] = 0
    window.update_idletasks
    connector = socket.socket()
    try:
        connector.bind((ip,port))
        ActivityVar = "\nCreated SERVER"
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        connector.listen(1)
        receiver , addr = connector.accept()
        ActivityVar = "\nGot Connection from => "+str(addr)+";\nSending Files"  
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)             
        SendFile(receiver,SendDir)
        ActivityVar = "\nCompleted Sending to "+str(addr)
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        receiver.close()
        #connector.shutdown(socket.SHUT_RDWR)
        ActivityVar = "\nClosed server"
        activity.insert(ui.END,ActivityVar)
        activity.see(ui.END)
        connector.close()
    except ConnectionAbortedError:
        messagebox.showinfo("Information","Connection aborted by remote host")
    except Exception as err:
        messagebox.showinfo("Information",err)
    ActivityVar = "\nconnection closed..."
    activity.insert(ui.END,ActivityVar)
def GUIwindow():
    def Configure():
        def Stop():
            messagebox.showwarning("Warning","All process will be closed and data maybe lost.")
            exit(0)
        def SetAll():
            try:
                global SendDir,ReceiveDir,port,ServerIP,SenderServerPort
                ServerIP = SenderIPEntry.get()
                SenderServerPort = int(SenderPortEntry.get())
                port = int(ThisDevicePortEntry.get())
                SendDir = SendFileDir.get()
                ReceiveDir = ReceiveFileDir.get()
                ThisPortLabel.config(text = "ACQUIRED-PORT => "+str(port))
                window.update_idletasks()
                messagebox.showwarning("ATTENTIION","ALL THE CHANGES WILL BE SAVED ONLY FOR THIS SESSION.WRONG ENTRY MAY CAUSE THIS SOFTWARE FOR NOT WOKING PROPERLY")
                cnfWindow.destroy()
            except Exception:
                messagebox.showerror("ERROR","SOME ERROR HAS OCCURED CHANGES CAN'T APPLIED")
        def ChangeTheme():
            try:
                global theme
                if theme == 0:
                    window.configure(bg = "gainsboro")
                    activity.configure(bg = "lavender",fg = "navy")
                    SB.config(bg = "gray15",fg = "white")
                    RB.config(bg = "darkorchid3",fg = "black")
                    CB.config(bg = "green2",fg = "black")
                    window.update_idletasks()
                    theme = 1
                    ThemeLabel.configure(text = "(**CURRENT THEME OHIYO LIGHT**)")
                    cnfWindow.update_idletasks()
                else:
                    window.configure(bg = "gray15")
                    activity.configure(bg = "snow",fg = "black")
                    SB.config(bg = "royal blue")
                    RB.config(bg = "seagreen1")
                    CB.config(bg = "orangered2")
                    window.update_idletasks()
                    theme = 0
                    ThemeLabel.configure(text = "(**CURRENT THEME COMBAUWA DARK**)")
                    cnfWindow.update_idletasks()
            except Exception:
                messagebox.showerror("ERROR","SOME ERROR HAS OCCURED CHANGES CAN'T APPLIED")
        global ServerIP,SenderServerPort,port,SendDir,ReceiveDir
        cnfWindow = ui.Tk()
        cnfWindow.title("CONFIGURE")
        cnfWindow.geometry("400x220")
        ui.Label(cnfWindow,text = "SET SENDER IP/addrs:").place(x = 10,y = 10,anchor = "nw")
        SenderIPEntry = ui.Entry(cnfWindow)
        SenderIPEntry.place(x = 150,y= 10,anchor = "nw")
        ui.Label(cnfWindow,text = "SET SENDER PORT:").place(x = 10,y = 30,anchor = "nw")
        SenderPortEntry = ui.Entry(cnfWindow)
        SenderPortEntry.place(x = 150,y = 30,anchor = "nw")
        ui.Label(cnfWindow,text = "SET THIS DEVICE'S PORT:").place(x = 10,y = 50,anchor = "nw")
        ThisDevicePortEntry = ui.Entry(cnfWindow)
        ThisDevicePortEntry.place(x = 150,y = 50,anchor = "nw")
        ui.Label(cnfWindow,text = "SEND (FILE's) FOLDER:").place(x = 10,y = 70,anchor = "nw")
        SendFileDir = ui.Entry(cnfWindow)
        SendFileDir.place(x = 150,y = 70,anchor = "nw")
        ui.Label(cnfWindow,text = "RECEIVE (FILE's) FOLDER:").place(x = 10,y = 90,anchor = "nw")
        ReceiveFileDir = ui.Entry(cnfWindow)
        ReceiveFileDir.place(x = 150,y = 90,anchor = "nw")
        ui.Button(cnfWindow,text = "Apply",command = SetAll).place(x = 300,y = 180,anchor = "nw")
        ui.Button(cnfWindow,text = "Change Theme",command = ChangeTheme).place(x = 150,y = 120,anchor = "nw")
        ThemeLabel = ui.Label(cnfWindow,text = "(**CURRENT THEME COMBAUWA DARK**)")
        ThemeLabel.place(x = 90,y = 150,anchor = "nw")
        ui.Button(cnfWindow,text = "Stop all",command = Stop).place(x = 100,y = 180,anchor = "nw")
        SenderIPEntry.insert(ui.END,ServerIP)
        SenderPortEntry.insert(ui.END,SenderServerPort)
        ThisDevicePortEntry.insert(ui.END,port)
        SendFileDir.insert(ui.END,SendDir)
        ReceiveFileDir.insert(ui.END,ReceiveDir)
        cnfWindow.mainloop()
    def Send():
        ThreadSend = threading.Thread(target=Server,args=(IP,port))
        ThreadSend.start()
    def Receive():
        ThreadReceive = threading.Thread(target=Client,args=(ServerIP,SenderServerPort))
        ThreadReceive.start()
    global window,ActivityVar,ServerIP,port,IP
    window.title("piksShare-Share files")
    window.resizable(0,0)
    window.geometry("450x250")
    window.configure(bg= "gray15")
    ui.Label(window,text = "DEVICE-ID => "+IP).place(x = 10,y = 10,anchor = "nw" )
    ThisPortLabel = ui.Label(window,text = "ACQUIRED-PORT => "+str(port))
    ThisPortLabel.place(x = 250 ,y= 20, anchor = "center")
    progress.place(x = 50,y = 200,anchor = "nw")
    SB = ui.Button(window,text = "Send",command = Send,background = "royal blue",foreground = "white",height = 2,width =10)
    SB.place(x = 50,y = 50,anchor = "nw")
    RB = ui.Button(window,text = "Receive",command = Receive,background = "sea green1",foreground = "black",height = 2,width = 10)
    RB.place(x = 50,y = 100,anchor = "nw")
    CB = ui.Button(window,text = "Configure",command = Configure,background = "orange red",foreground = "white",height = 2,width = 10)
    CB.place(x = 50,y = 150,anchor = "nw")
    activity.place(x = 150,y = 55,anchor="nw")
    activity.insert(ui.END,ActivityVar)
    window.mainloop()
if __name__ == "__main__":
   try:
       GUIwindow()
   except Exception:
       messagebox.showerror("Error","AN ERROR HAS OCCURED")
       exit()