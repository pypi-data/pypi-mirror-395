#!/usr/bin/env python3

from fire import Fire
# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq

import datetime as dt
import os
import sys

import notifator.telegram as telegram

import threading
import time
import numpy as np

import datetime as dt
import socket

allimages={}


results = [None]*2

MYSTART = dt.datetime.now()
OPENEDWR = {}

def receive_image(image_hub, results):
    rpi_name, image = image_hub.recv_image( )
    #return rpi_name, image
    results[0] = rpi_name
    results[1] = image



def setupsave( rpi_name,  resolution = (640,480) ):
    global MYSTART, OPENEDWR
    sme = socket.gethostname()

    # identifiable name
    sfilenamea = f'~/DATA/ZMQ_{sme}_{rpi_name}_{MYSTART.strftime("%Y%m%d_%H%M%S")}.mkv'
    sfilenamea = f'~/DATA/ZMQ_{sme}_{rpi_name}_{MYSTART.strftime("%Y%m%d_%H%M%S")}.avi'


    dir2create = os.path.expanduser("~/DATA/")
    if not os.path.isdir( os.path.expanduser(dir2create )):
        print(f"D... trying to create directory {dir2create} for saving")
        #result = False
        os.mkdir( os.path.expanduser(dir2create ))

    sfilenamea = os.path.expanduser(sfilenamea)
    if os.path.exists( sfilenamea ):
        return sfilenamea,OPENEDWR[sfilenamea]

    # codec
    #sfourcc = cv2.VideoWriter_fourcc(*'XVID')
    ### sfourcc = cv2.VideoWriter_fourcc(*'LAGS') # lossless NOT mkv,avi..,
    #sfourcc = cv2.VideoWriter_fourcc(*'X264') # +avi small
    #sfourcc = cv2.VideoWriter_fourcc(*'MP4V')

    sfourcc = cv2.VideoWriter_fourcc(*'IYUV') # huge + avi
    #  25 FPS
    saviout = cv2.VideoWriter( sfilenamea,sfourcc,1.0, resolution )
    OPENEDWR[sfilenamea] = saviout
    return sfilenamea,saviout





def main( display=False,  test= False):
    global MYSTART, OPENEDWR
    if test:
        print("test")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imshow('WebCam', frame)
        print( type(frame) )

        if type(frame) == np.ndarray:
            print("i... NUMPY ARRAY ####################################")
        time.sleep(1)

        telegram.bot_send("ALERT",f"test izmq {dt.datetime.now().strftime('%a %H:%M:%S')}", frame)

        time.sleep(2)
        cap.release()
        cv2.destroyAllWindows()

        sys.exit(0)
        # print("test")
        # telegram.bot_send("Login",f"test izmq {dt.datetime.now().strftime('%a %H%M%S')}")
        # sys.exit(0)





    image_hub = imagezmq.ImageHub()
    while True:  # show streamed images until Ctrl-C
        print("i... waiting receive..." )

        # i cannot use threading, it is returning parameters

        #x = threading.Thread( target=image_hub.recv_image , args=() )
        x = threading.Thread( target = receive_image , args=(image_hub, results) )
        x.start()
        while x.is_alive():
            #print("x", flush=True, end="")
            print(f"i... {dt.datetime.now().strftime('%a %H:%M:%S')} display={display}        ",  end="\r")
            time.sleep(0.05)


            #--------------------------------display section --
            if display:
                #print( allimages )
                for k,i in allimages.items():
                    #print(f"   key = {k}")
                    cv2.imshow( k, i) # 1 window for each RPi
                cv2.waitKey(1)


        x.join()
        #print(results)
        rpi_name = results[0]
        image = results[1]

        #rpi_name, image = image_hub.recv_image( )


        print(f"\ni... received {rpi_name}")
        rpi_name = f"ZMQ_Camera_{rpi_name}"
        # it appeared  ZMQ_gigajm_ZMQ_Camera_rpi4b456_20
        rpi_name = f"{rpi_name}"

        allimages[rpi_name] = image # if I have several incomming images...


        #fname =  f'~/DATA/{rpi_name}_{dt.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        #fname = os.path.expanduser( fname )
        #print(fname)
        #cv2.imwrite( fname ,  image )

        sfilenamea,saviout = setupsave(rpi_name)
        print(f"i... writing image to  {sfilenamea} ")
        #saviout.write( image ) # I USED 2 images at once......
        saviout.write( image )

        if (dt.datetime.now()-MYSTART).total_seconds()>24*3600:
            MYSTART = dt.datetime.now() # .strftime("%Y%m%d_%H%M%S")
            for (i,v) in OPENEDWR.items():
                ## NO : 'NoneType' object has no attribute 'release'
                if not v is None:
                    v.release()
                OPENEDWR[i]=None




        #cv2.waitKey(1)
        image_hub.send_reply(b'OK')

if __name__=="__main__":
    Fire(main)
