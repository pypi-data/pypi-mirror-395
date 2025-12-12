#!/usr/bin/env python3

#
# import pyautogui
from flashcam.version import __version__
from console import fg,bg
# from imutils.video import VideoStream
import socket
import time
import signal
from contextlib import contextmanager
# import argparse

import cv2
import datetime

import os

from fire import Fire

#import urllib.request
import numpy as np

# user pass
#import base64
#import getpass

import sys

from flashcam.stream_enhancer import Stream_Enhancer
import webbrowser

import math

import requests  # crosson=CROSSON
from PIL import ImageFont, ImageDraw, Image

from flashcam.uniwrec_keys import remap_keys
from flashcam.uniwrec_manip import disp_mutext, rotate_image, adjust_gamma, make_measurements, matrix_undistort
from flashcam.uniwrec_io import setupsave, get_stream, get_FILE_REDCROSS

# ------------------problem with SHIFT
# from pynput.keyboard import Key, Listener


global SHIFT, CTRL
SHIFT = CTRL = False

global centerX1, centerY1
# global FILE_USERPASS
#global FILE_REDCROSS
# ---------- files:
#FILE_USERPASS = "~/.config/flashcam/.flashcam_upw"  # will extend
#FILE_REDCROSS0 = "~/.config/flashcam/crossred"  # will extend
#FILE_REDCROSS = "~/.config/flashcam/crossred"  # will extend


global local_gamma, integrate
local_gamma = 1  # adjust_gamma
integrate = 1  # call accum

# automatic tuning histogram
global countdownpause, optimgain, optimexpo, optim_histo, countdown_gain
countdownpause = 5
optimgain = -1
optimexpo = -1
optim_histo = 49  # we try middle of the range in %
countdown_gain = False  # Sonix USB 0c45:62c0 has broken expo, but gain ok

jpgkompr2 = [100, 95, 90, 80, 70, 60, 50, 40, 30,20,10, 5]
jpgkompr1 = [x for x in jpgkompr2]


# i needed a warning before 't'
global allow_tracker, allow_tracker_demand
allow_tracker = False
allow_tracker_demand = False

global show_help
show_help = False

# break everything in realcam/config
global timelaps
timelaps = 0

expande = 1 # i weant to keep it global

# qwertyuiop
# quit/web/rot/track+komp/gamma/unrtrak+??/integr/oautotune??
#  asdfghjkl
#avi/save/gamm/fg+measure/gain/ hjkl
#   zxcvbnm
#zoom/xzoo/cross/crs/bg/ n-measuremode/ m measuremode.

"""
u  freeslot
o to change
p free
"""

# x ... expand 2x ... buggy
HELPTEXT = """ a/A ... AVI/stop (~/DATA/) (ctl-a PNG stream)
 s/S C-p ... save 1 JPG (PNG) (to ~/DATA/) (C-p remote PNG)

 z ... cycle zoom 2x (mouse click fixes the center)
 Z,x ... zoom 1x ... expandviewer
 r/R ... rotate by +-1; Ctl-r= 180 degrees

 c/C ... red cross on/off (save when off)
 hjkl ... move the red/green* cross (HJKL)
 t/u ... tracker 1 (cross sync, speed)
 T/u ... tracker 2 (more steady, but fragile)

 m/M ... measure/not distance,  (-v 110,1.2)
 n/N ... inc/decrease distance
 f/F ... inc/dec Field Of View (-v FOV,dist)

 v/V* ... green cross ON/OFF
 b/f* ... substract BG, mix FG
 B/F* ... SAVE BG/ SAVE FG

 egy* ...  expo/gain/gm (+ shift or ctl)
 d   ...  gamma (local) (+shift or ctl)
 o/O ... autotune expo / break tuning
 i/I* ... accumulate images

 w ... open web browser
 q ... quit           ? ... HELP
ctl: t=kompr  h=histo  j=direct  k=detect l=lapAstro
       * on remote flashcam """

####  rotate_image was here
####  disp_mutex was here ==================================

@contextmanager
def timeout(atime):
    # register a function to raise a TimeoutError on the signal
    signal.signal(signal.SIGALRM, raise_timeout)
    # schedule the signal to be sent after 'time'
    signal.alarm(atime)
    # print("D... timeout registerred")

    try:
        # tok = False
        # print("D... yielding timeout")
        yield
    finally:
        # tok = True
        # unregister the signal so it wont be triggered
        # if the timtout is not reached
        # print("D... timeout NOT!  unregisterred")
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


# adjust_gamma was here ===============================
# img_estim was here

# ------------------------------------------------------------------------ 3
# ================================================================================================

# ================================================================================================


def display2(
    videodev,
    save=False,
    passfile="~/.pycamfw_userpass",
    rotate=0,
    vof="99,2",
    savepngcont=False,
    XY=None,
):
    """ """
    # sname,sfilenamea,sme,sfilenamea,sfilenamea,sfourcc,saviout
    print("D... in display2 ")
    sme = socket.gethostname()
    # frame = None  #  gigavg a vaio have strange behaviour

    global jpgkompr1, jpgkompr2
    global CTRL, SHIFT
    global centerX1, centerY1, clicked
    #global FILE_USERPASS, FILE_REDCROSS, FILE_REDCROSS0
    global show_help
    global timelaps
    global allow_tracker, allow_tracker_demand
    global local_gamma, integrate
    global countdown_gain
    global expande # i want to remember x after reconnect
    centerX1, centerY1, clicked = 0, 0, True  # center zoom ion start

    filesource = False

    # ==========================  I fire here the listener from pynput !!!
    # NOT ON UBUNTU22 ############################################################
    #listener = Listener(on_press=kb_on_press, on_release=kb_on_release)
    #listener.start()
    # ------------------------------------------------------ let;s see

    def MOUSE(event, x, y, flags, param):
        global centerX1, centerY1, clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked = not clicked
        if event == cv2.EVENT_MOUSEMOVE:
            if not (clicked):
                centerX1, centerY1 = x, y
            # print('({}, {})'.format(x, y))
            # imgCopy = frame.copy()
            # cv2.circle(imgCopy, (x, y), 5, (255, 0, 0), -1)
            # cv2.imshow('image', imgCopy)

    """


{
“avi” : [ “avc1”, “DIVX”, “H264”, “X264”, “V264”, “IYUV”, “MJPG”, “MPEG”, “MP42”, “mp4v”, “XVID” ],
“mov” : [ “avc1”, “DIVX”, “mp4v”, “XVID” ],
“mp4” : [ “avc1”, “mp4v” ],
“mkv” : [ “avc1”, “DIVX”, “H264”, “X264”, “V264”, “IYUV”, “MJPG”, “MPEG”, “MP42”, “mp4v”, “XVID” ],
“mkv” : [ “avc1”, “DIVX”, “H264”, “X264”, “V264”, “IYUV”, “MJPG”, “MPEG”, “MP42”, “mp4v” ],
“3gp” : [ “avc1”, “mp4v” ]
}


Notes:
– avc1 is equivalent/identical to H264, X264, V264
– mp4v is the same as DIVX, XVID

File size & compression
– most compact format: avc1
– least compact format is IYUV (by a long shot), followed by MPJPG/MPEG
– middle/similar: MP42, mp4v

Recommendation:
– use avi or mkv for best compatibility across all codecs for the maximum flexibility
– use mp4 (avc1, mp4v) for compatibility across players with most/reasonable compression

"""
    # =============setupsave was here ================

    # ==================getstream was here ==============

    # ********************************************************** main loop
    io_none = 0  # to reset stream
    sfilename = ""  # move up to limi # of AVI files.... tst?
    sfilenamea = ""

    stream_length = 1024 * 50  # i had 50k all the time from 1st working versn
    stream_length = 1024 * 15  #

    if save:
        sfilenamea, saviout = setupsave( resolution=(640,480) , videodev=videodev )
    while True:  # ==================== MAIN LOOP =================
        mjpg = False

        # #===================== OPENCV START CAPTURE==========================

        bytex = b""  # stream
        rpi_name = videodev
        frame_num = 0

        if (str(videodev).find("http://") == 0) or (
            str(videodev).find("https://") == 0
        ):
            # infinite loop for stream authentication
            stream = None
            while stream is None:
                print("D... waiting for stream")
                # ## HERE PUT BWIMAGE
                # cv2.imshow(rpi_name, frame) # 1 window for each RPi
                if "frame" in locals():
                    print("D... frame in locals() ")
                    if frame is not None:
                        print("D.... graying")
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                        (w, h, c) = frame.shape

                        for i in range(0, w, 10):
                            x1, y1 = 0, i
                            x2, y2 = h, i
                            line_thickness = 1
                            cv2.line(
                                gray,
                                (x1, y1),
                                (x2, y2),
                                (111, 111, 111),
                                thickness=line_thickness,
                            )
                        cv2.imshow(rpi_name, gray)  # 1 window for each RPi
                        key = cv2.waitKey(1)

                time.sleep(1)
                stream, u, p = get_stream( videodev=videodev)
        else:
            print("X... use http:// address")
            print("i... or this may be a file?...")
            # sys.exit(0)

        if (str(videodev).find("http://") == 0) or (
            str(videodev).find("https://") == 0
        ):
            ret_val = 0
            oi = 0
            while ret_val == 0:
                oi += 1

                # with timeout(2):
                print("D... IN 1st TIO..", end="")
                try:
                    # THIS CAN TIMEOUT #######################################
                    print("D... try ...", end="")
                    bytex += stream.read(stream_length)  # must be long enou?
                except:
                    print("X... exception - timout in 1.st stream.read, ")
                    # bytex+=b"\x00\x00\x00"
                    bytex = b""

                a = bytex.find(b"\xff\xd8")  # frame starting
                b = bytex.find(b"\xff\xd9")  # frame ending
                if a != -1 and b != -1:
                    io_none = 0
                    jpg = bytex[a: b + 2]
                    bytex = bytex[b + 2:]
                    # frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                    # cv2.CV_LOAD_IMAGE_COLOR)
                    if len(jpg) > 1000:  # was crash here
                        frame = cv2.imdecode(
                            np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR
                        )
                        ret_val = 1
                        io_none = 0
                        stream_length = int((b + 2 - a) / 2)  # expected length
                    else:
                        ret_val = 0
                        # print("D...              ok frame http",oi,len(bytex) )
                else:
                    ret_val = 0
                    print(
                        "D...                        frame set None http",
                        oi,
                        len(bytex),
                        end="\r",
                    )
                    # it can count to milions here.... why? need to check
                    #          stream ## OTHER CRASHES
                    #  i try two things now:
                    # bytex+=b""
                    time.sleep(0.2)
                    io_none += 1
                    if io_none > 50:
                        stream = None
                        print(
                            "X... ---------------  too many unseen frames",
                            io_none,
                            "breaking",
                        )
                        io_none = 0
                        break

                    # frame = None
        if "stream" in locals():
            if stream is None:
                continue
        else:  # from file ---- 1st moment open
            # replay video from file
            ret_val = 0
            stream = cv2.VideoCapture(videodev)
            filesource = True
            print("i... FILE open  = ", stream.isOpened())
            ok, frame = stream.read()
            frame_num += 1
            if frame is not None:
                print( frame.shape() )
            # pause = True too early.... defined later
            print(f"X... {ok}, frame from {videodev}")
            # print("i... stream in locals() == ", 'stream' in locals() )
            # print("i... stream is None     == ", stream is None, stream )
            print("i...   PAUSED: press SPACE to play")

        # ----------------------------------------------------------------

        first = True

        timestamp_of_last_socket_refresh = time.time()

        i = 0
        fps = 0
        resetfps = True
        lastminu = 88
        motion_last = "999999"

        i7 = 0
        artdelay = 0.05

        connection_ok = True

        # ---- bytes per second.  strange looks like 7MB/s
        BPS = 0
        BPSlast = 0
        BPStag = datetime.datetime.now()
        FPS = 0
        FPSlast = 0
        frames_total = 0
        frame_num = 0

        if frame is not None:
            print(f"i... {fg.red} SENH: {frame.shape} ########### {fg.default}")
            #print(f"i... initiating stream enhancer {f}x{height} ###########")
            senh = Stream_Enhancer(  (frame.shape[1],frame.shape[0] ) )  # resolution  )
        saved_jpg = 0  # 0, 1jpg, 2png

        zoomme = 1
        centerX1, centerY1 = 320, 240
        ###expande = 1 # i want to have keep global value
        rorate180 = False

        # measurements (distance)
        measure = 0  # 1.7

        #print(vof, type(vof))
        #print(vof)
        #print(vof)
        if type(vof) is list: # never happened
             measure_fov, measure  = vof[0], vo[1]
        elif str(vof).find(",") > 0: # this happens
            vof = str(vof).strip("(")
            vof = str(vof).strip(")")
            vof = str(vof).strip("[") # when cfg from memory does this
            vof = str(vof).strip("]")
            measure_fov, measure  = (float(vof.split(",")[0]), float(vof.split(",")[1]) ) # ??? BUG?
            print("D... measure == ", measure )
            float(vof.split(",")[1])
        else:
            measure_fov = float(vof)  # config.CONFIG['vof'] #

        cross = None
        greencross = False  # just tell if on/off

        print(" ... ... reset of all trackers/zoom/measure etc..")

        tracker1 = None
        tracker2 = None
        tracker1_fname = None  # change filename for tracking
        tracker2_fname = None  # change filename for tracking
        tracker_list = []
        cropped = None  # created during tracking1
        orb = None  # i dont use

        # file - pause
        pause = True  # FOR FILE but not for CAM
        if filesource is False:
            pause = False
        frame_from_file = None  # backup the frame: for effects + for CAMER

        # -see the values sent from the webpy - i can use in track,
        #   but not in savejpg,saveavi!
        webframen = ""  # frame number from web.py()
        webframetime = ""

        save_decor = False # save with decor or original... save is def in call...

# =================================================================================
# =================================================================================
# =================================================================================
#                CONNECTION HERE =========================
# =================================================================================
# =================================================================================
# =================================================================================

        while connection_ok:  # ===============================================
            # read the frame from the camera and send it to the server
            # time.sleep(0.05)

            # while True:
            if (str(videodev).find("http://") == 0) or (
                str(videodev).find("https://") == 0
            ):
                print("-", end="")
                artdelay = 0
                ret_val = 0
                try:
                    with timeout(4):
                        while ret_val == 0:
                            for i8 in range(1):  # I decimate and remove delay
                                # print("1-", flush=True,end="")
                                bytex += stream.read(stream_length)
                                a = bytex.find(b"\xff\xd8")  # frame starting
                                b = bytex.find(b"\xff\xd9")  # frame ending
                                ttag = bytex.find(
                                    "#FRAME_ACQUISITION_TIME".encode("utf8")
                                )  # frame ending
                                webframen = " " * 7
                                webframetime = " " * 23
                                if ttag != -1:
                                    # print(f"i... FRACQT: /{ttag}/ \
                                    # /{bytex[ttag:ttag+32]}/----------------")
                                    webframen = bytex[ttag: ttag + 32 + 23].decode(
                                        "utf8"
                                    )
                                    webframen = webframen.split("#")
                                    # print(len(webframen), webframen)
                                    webframen, webframetime = webframen[2], webframen[3]

                                    # print( webframen )
                                    # print( webframetime)

                                if a != -1 and b != -1:
                                    jpg = bytex[a: b + 2]
                                    BPS += len(jpg) / 1024
                                    if len(jpg) > 0:
                                        FPS += 1
                                    bytex = bytex[b + 2:]
                                    # just a test.... if I can append
                                    # jpg = jpg+b'#FRAME_ACQUISITION_TIME#'+
                                    # f"a".encode("utf8")
                                    frame = cv2.imdecode(
                                        np.frombuffer(jpg, dtype=np.uint8),
                                        cv2.IMREAD_COLOR,
                                    )

                                    # ----taken for pause
                                    if (not pause) or (frame_from_file is None):
                                        frame_from_file = frame
                                        frame_num += 1
                                    else:
                                        frame = frame_from_file
                                        # ret_val = 1
                                        # frame_num+=1 # ??? I keep this stopped or better not?

                                    # stream_length = b+2-a
                                    stream_length = int(
                                        (b + 2 - a) * 0.9
                                    )  # expected length

                                    ret_val = 1
                                    #print( f"{stream_length/1024:.1f}k #{frame_num:06d}/{webframen} {BPSlast*8/1024:4.1f}Mb/s {FPSlast:2d}fps" , end = "\r" )
                                    print( f"{stream_length/1024:.1f}k #{frame_num:06d}/{webframen} {BPSlast*8/1024:4.1f}Mb/s {FPSlast:2d}fps cap={webframetime} now={str(datetime.datetime.now())[11:-4]}  {sfilenamea.replace('/home/', '')}", end = "\r" )
                                        # "{:.1f}k #{:06d}/{} {:4.1f}Mb/s {:2d}fps {} w{} {} ".format(
                                        #     # len(bytex)/1024,
                                        #     stream_length / 1024,
                                        #     frame_num,
                                        #     webframen,
                                        #     BPSlast * 8 / 1024,
                                        #     FPSlast,
                                        #     str(datetime.datetime.now())[11:-4],
                                        #     webframetime[11:],
                                        #     sfilenamea.replace("/home/", ""),

                                        # ),
                                        # end="\r",               )

                                else:
                                    ret_val = 0
                                    # frame = None
                                    # print("Non  sizE={:6.0f}kB ".format(len(bytex)/1024), end = "\r" )
                                    # print("Non", end = "\r" )
                except:
                    print("X... exception - connection lost, ")
                    ret_val = 0
                    # frame = None
                    print("RDE  siZe={:6.0f}kB ".format(len(bytex) / 1024), end="\n")
                    connection_ok = False

                # print("-2", flush=True,end="")
                if (datetime.datetime.now() - BPStag).total_seconds() > 1:
                    BPStag = datetime.datetime.now()
                    BPSlast = BPS
                    BPS = 0
                    FPSlast = FPS
                    FPS = 0

                # while

            else:  # from file 2nd point
                if (not pause) or (frame_from_file is None):
                    ret_val, frame = stream.read()
                    frame_from_file = frame
                    frame_num += 1
                else:
                    frame = frame_from_file
                    ret_val = 1
                if ret_val == 0:
                    sys.exit(0)
            if connection_ok:
                if (ret_val == 0) or (type(frame) == "NoneType"):
                    print("Not a good frame", type(frame), end="\r")
                    continue
                frame = frame
                (w, h, c) = frame.shape
                frame_area = w * h
                motion_det = False

                # print(".", end="")
                # print("RPINAME=",rpi_name)
                # print(frame)

                wname = videodev

                frames_total += 1

                # ======================================== GAMES WITH FRAMES
                #   hack-expand;  tracker; zoom; rotate; save; measure

                # cv2.namedWindow( wname, cv2.WINDOW_KEEPRATIO ,cv2.WINDOW_GUI_EXPANDED)
                #
                # cv2.WINDOW_KEEPRATIO 2 may allow resize on gigavg
                # but troja...
                #
                # https://stackoverflow.com/a/43497012
                #

                # cv2.namedWindow( wname , cv2.WINDOW_KEEPRATIO ) #
                # QT cv2.namedWindow( wname , cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_OPENGL  ) #
                # try this
                # cv2.namedWindow( wname , cv2.WINDOW_KEEPRATIO ) # 2 may allow resize on gigavg
                # NEW IN 1.1.8
                cv2.namedWindow(wname, cv2.WINDOW_GUI_NORMAL)  #
                #cv2.namedWindow( wname , 2 ) # 2 may allow resize on gigavg
                if frames_total < 2:
                    # cv2.namedWindow(wname,cv2.WND_PROP_FULLSCREEN)
                    # ?https://stackoverflow.com/questions/62870031/pixel-coordinates-and-colours-not-showing
                    # TRICK !!!!!!!!!!!!
                    # https://stackoverflow.com/a/52776376
                    #  remove bars....  BUT IN UBUNTU 22 - I remove this and all is fine
                    #cv2.setWindowProperty( wname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN  )

                    #cv2.setWindowProperty( wname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN  )
                    bit_fs = 0
                    if sme in [
                        "gigavg",
                        "vaio",
                    ]:  # strange behavior on some PC concerning resize...(checked in MS with vadim)
                        bit_fs = 1
                    cv2.setWindowProperty(wname, cv2.WND_PROP_FULLSCREEN, bit_fs)
                    cv2.resizeWindow(wname, frame.shape[1], frame.shape[0])
                    if XY is not None:
                        xy1, xy2 = XY.split("x")
                        print("D.. MOOOOOOOVING WINDOWWWWWWW ", xy1,xy2, wname)
                        #####cv2.imshow(wname, frame)
                        #time.sleep(3)
                        #cv2.imshow(wname, np.zeros([10,10], dtype=np.uint8))
                        cv2.moveWindow(wname, int(xy1), int(xy2))

                # -------- i tried all---no help for csrt tracking-------
                # -------- i tried all---no help for csrt tracking-------
                # -------- i tried all---no help for csrt tracking-------
                # frame = cv2.bilateralFilter(frame,5,100,20) # preserve edges
                # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                # (T,frame) = cv2.threshold(frame,  100, 255,
                #                          cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                # frame = cv2.blur( frame, (6,6) ) # doesnt help


# ============================================================================================
# ============================================================================================
# ============================================================================================
#
#            Window refreshed/resized ------ something..... From now - real things
#
# ============================================================================================
# ============================================================================================
# ============================================================================================
#
#        RUNNING TRACKERS -=-----------------------------
#
                # ======================== track before zoom
                if (tracker1 is not None) and (not pause):
                    # print("tracking",tracker1)
                    ok, bbox = tracker1.update(frame)
                    if not ok:
                        continue
                    bbox = [round(i * 10) / 10 for i in bbox]
                    (x, y, w, h) = [v for v in bbox]
                    cx, cy = round(10 * (x + w / 2)) / 10, round(10 * (y + h / 2)) / 10
                    # print("tracking",ok,bbox," ->", cx,cy)
                    with open(tracker1_fname, "a") as f:
                        f.write(f"{webframetime} {webframen} {cx} {cy}\n")
                        #   f.write( f"{webframetime[11:]} {webframen} {cx} {cy}\n" )

                    # there is time sent from server... by a trick  ************ NICE TRICK **********
                    # if from file(or elsewhere) it is int or nothing...
                    #
                    #print( "WEBFRAMEN...",type(webframen), f"/{webframen}/")
                    if (type(webframen) == int) or (webframen.strip(" ") == ""):
                        # no acq timestamp info from server
                        webframen = frame_num
                        ttime = int(webframen)
                    elif type(webframen)==str and len(webframen.strip())>9 and webframen!="0000000":
                        # better this, fractions are kept...
                        ttime = datetime.datetime.strptime(
                            # THIS IS A PROBLEM _ WITH NEW WEBTAG_ NEW TTIME NEEDED
                            webframetime, "%H:%M:%S.%f"
                            #                            webframetime, "%Y-%m-%d %H:%M:%S.%f"
                        )
                    else:
                        ttime = datetime.datetime.now()


                    tracker_list.append((round(cx), round(cy), ttime))
                    colmax = 255
                    colmaxb = 0
                    for i in reversed(tracker_list):
                        x2, y2, ttime = i
                        frame[y2, x2] = (colmaxb, 255 - colmax - colmaxb, 255)
                        if colmax > 1:
                            colmax -= 1
                        elif (colmaxb < 255) and (colmaxb > 1):
                            colmaxb += 1

                    # ------------ play on cropping -- may further stabilize
                    cropped = frame[round(y) : round(y + h), round(x) : round(x + w)]

                    cv2.rectangle(
                        frame,
                        (round(x), round(y)),
                        (round(x + w), round(y + h)),
                        (0, 255, 0),
                        1,
                        1,
                    )
                    cv2.line(
                        frame,
                        (round(cx), round(cy)),
                        (round(cx), round(cy)),
                        (0, 255, 0),
                        2,
                        1,
                    )

                    # cv2.rectangle(frame, (xh,yh), (xh+wh,yh+hh), (0,0,255),1,1)
                    # cxh,cyh= round( 10*(xh+wh/2))/10, round(10*(yh+hh/2))/10
                    # cv2.line(frame,(round(cxh),round(cyh)),(round(cxh),round(cyh)),
                    #          (0,0,255),2,1)

                # ================= track2
                if tracker2 is not None:
                    # print("tracking",tracker)
                    # frame = cv2.blur( frame, (4,4) )
                    ok2, bbox2 = tracker2.update(frame)
                    bbox2 = [round(i * 10) / 10 for i in bbox2]
                    # print("\ntracking2",ok2,bbox2)
                    (x2, y2, w2, h2) = [v for v in bbox2]
                    # if not( (x<0)or(y<0)or(x+w>=frame.shape[1])or(y+h>=frame.shape[0]) ):
                    # print("rect")
                    cv2.rectangle(
                        frame,
                        (int(x2), int(y2)),
                        (int(x2 + w2), int(y2 + h2)),
                        (0, 255, 255),
                        1,
                        1,
                    )
                    cx2, cy2 = (
                        round(10 * (x2 + w2 / 2)) / 10,
                        round(10 * (y2 + h2 / 2)) / 10,
                    )
                    cv2.line(
                        frame,
                        (int(cx2), int(cy2)),
                        (int(cx2), int(cy2)),
                        (0, 255, 255),
                        2,
                        1,
                    )
                    with open(tracker2_fname, "a") as f:
                        if webframen == "":
                            webframen = frame_num
                        f.write(f"{webframetime} {webframen} {cx2} {cy2}\n")

                # framelo = np.clip(frame, 60, None )
                # framelq = np.less_equal( frame, framelo)
                # frame = np.where( framelo<=60, 0  , framelo )
                # print(frame) # 255 levels

                # ------------------------redcross here: before zoom--------------------------------------
                # print(f" ... cross == {cross}")
                if not (cross is None):
                    if senh.add_frame(frame):
                        w, h, c = frame.shape
                        # print(w-centerY1, h-centerX1)
                        # print(f" ... cross {w} {h} /2")
                        senh.crosson(cross[0], cross[1], color="r" , box_large = True)  # dx dy
                        # senh.setbox(f"CROS",  senh.jpg)
                        frame = senh.get_frame()
                    else:
                        print("X... senh did not accept frame (in redcross)")

                # =========================== ZOOM ME and OTHERS =======

                if (
                    zoomme > 1
                ):  # FUNNY - it continues to zoom where the mouse pointer is !!!!
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox(f"z {zoomme}", senh.scale)
                        w, h = frame.shape[0], frame.shape[1]
                        # print(w-centerY1, h-centerX1)
                        senh.zoom(zoomme, int(centerX1 - h / 2), int(centerY1 - w / 2))
                        frame = senh.get_frame()

                # ---------------------------------------------------- rotate ------------------
                # if rotate180:
                #     if senh.add_frame(frame):
                #         senh.setbox(f"ROT",  senh.rot)
                #         # w,h,c = frame.shape
                #         # print(w-centerY1, h-centerX1)
                #        senh.rotate180( 180 )
                #        frame = senh.get_frame(  )
                if rotate == 180:
                    frame = cv2.rotate(frame, cv2.ROTATE_180)
                    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                elif rotate != 0:
                    frame = rotate_image( frame , rotate )

                # I just need to put local gamma before avisave...
                # else astroimage shows nothing..
                if local_gamma != 1:
                    frame = adjust_gamma(frame, local_gamma)

                if savepngcont:
                    sfilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    sname = "snapshot"
                    sfilename = f"{sme}_{sfilename}_{sname}.png"
                    sfilename = os.path.expanduser("~/DATA/" + sfilename)
                    print(f"i... PNGcontinuous {sfilename}")

                    cv2.imwrite(sfilename, frame)
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox("png", senh.jpg)
                        frame = senh.get_frame()

                if save:
                    if not save_decor:
                        saviout.write(frame)
                    if senh.add_frame(frame):
                        # print("avi..")
                        if save_decor:
                            senh.setbox("AVId", senh.avi)
                        else:
                            senh.setbox("AVI", senh.avi)
                        frame = senh.get_frame()

                if saved_jpg == 1:
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox("JPG", senh.jpg)
                        frame = senh.get_frame()
                if saved_jpg == 2:
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox("PNG", senh.jpg)
                        frame = senh.get_frame()

                if show_help:
                    # show_help = True
                    frame = disp_mutext(frame, HELPTEXT)


                if (allow_tracker_demand) and not (allow_tracker):
                    TRACKERHELP = """
u ... return back

t ... use tracker1
T ... use tracker2
  ...  ENTER or SPACE to accept region
  ...  c cancel
"""
                    frame = disp_mutext(frame, TRACKERHELP)


                    #======================
                    #
                    #  first big mess
                    #
                    #=====================


                # MEASUREMENT ==================================

                if measure > 0:
                    frame = make_measurements(frame, measure_fov, zoomme, measure, tracker1, tracker_list, cross)



                # ANY chnges to imge BEFORE IMSHOW!!
                if cross is not None:
                    overtext = f"({cross[0]},{cross[1]})"
                    fontpath = os.path.expanduser("~/.config/flashcam/small_pixel.ttf")
                    #fontpath = os.path.expanduser("~/.config/flashcam/digital-7.mono.ttf")
                    position = ( 320+15+cross[0],240-40+cross[1] ) # 480 on x
                    font = ImageFont.truetype(fontpath, 8)
                    img_pil = Image.fromarray(frame).convert("RGBA")
                    draw = ImageDraw.Draw(img_pil)
                    #draw.line((0, 0) + img_pil.size, fill=128)
                    draw.fontmode = "1" # NO ANTIALIASING
                    #overtext = ' '.join(overtext[i:i+1] for i in range(0, len(overtext), 1))
                    drtext =  str(overtext) # to be sure
                    print(drtext, end=" ")
                    b,g,r,a = 0,0,255,0
                    draw.text( position,  drtext, font = font, fill = (b, g, r, a))
                    composite = img_pil #Image.alpha_composite(img_pil, img_pil)
                    frame = np.array(composite)
                    #print(frame.shape)



                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW


                apply_distortion = False
                if apply_distortion:
                    # Assuming no distortion
                    frame = matrix_undistort(frame)


                if expande > 1: # with wayland
                    from screeninfo import get_monitors
                    # Get monitor size
                    monitor = get_monitors()[0]  # Assuming the first monitor
                    screen_width, screen_height = int(monitor.width ), int(monitor.height )
                    # Get image dimensions
                    image_height, image_width = frame.shape[:2]
                    # Calculate aspect ratio
                    aspect_ratio = min(screen_width / image_width, screen_height / image_height)

                    # Resize the image while maintaining aspect ratio
                    new_width = int(image_width * aspect_ratio)
                    new_height = int(image_height * aspect_ratio)
                    frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

                    # Create a fullscreen window
                    cv2.namedWindow(rpi_name, cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty(rpi_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                else:
                    cv2.setWindowProperty(rpi_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

                # IMSHOW #############==================================================================
                # IMSHOW #############==================================================================
                # IMSHOW #############==================================================================
                # IMSHOW #############==================================================================
                cv2.imshow(rpi_name, frame)  # 1 window for each RPi
                ##########cv2.moveWindow(rpi_name, int(xy1), int(xy2))
                # ======================================================== IMSHOW
                if save_decor:
                    saviout.write(frame)
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # this may be useful?
                if False:
                    if not (cropped is None):
                        cropped = cv2.resize(cropped, (640, 480))
                        cv2.imshow("tracking1", cropped)  # ZOOM ON TRACK
                        # cv2.resizeWindow(

                # not - i do full screen
                # if expande > 0: # always tune win size ** because of wayland, we have now resize
                #     cv2.resizeWindow(
                #         rpi_name,
                #          frame.shape[1],
                #          frame.shape[0]
                #     )

                    # print(frame.shape)
                # cv2.setWindowProperty(rpi_name, cv2.WND_PROP_TOPMOST, 1)
                # cv2.namedWindow(rpi_name, cv2.WINDOW_GUI_EXPANDED)
                # time.sleep(0.2)
                cv2.setMouseCallback(rpi_name, MOUSE)
                #
                #  waitkeyex sometimes sees shift and ctrl... but not on zen...
                #########################################################################
                #########################################################################
                #########################################################################
                #key = cv2.waitKey(1)  # same problem with shift on ubu22 as ex
                #########################################################################
                #########################################################################
                #########################################################################
                #
                key = cv2.waitKeyEx(1) # this may work in ubuntu 22 - let us check....

                c = s = "     "
                # non-ubuntu22 version makes sense with Listener
                #if CTRL:  c = "ALT  "
                #if SHIFT: s = "SHIFT"
                # print(f" {c} x {s} ...      ", end = "       \n")

                #
                # UBUNTU 22 - ctrl and alt give 227 and 233 resp
                #
                if key != -1:
                    print(f" ****key== {key}   /{chr(0xFF&key)}/  .. {c} : {s}  >>>.      ")
                    key, CTRL = remap_keys(key, CTRL ) # make compatible with waitKey()
                    try:
                        print(f" ... --------------------------------------------- remapped {key} : {chr(key)}")
                    except:
                        print(f" ... ----------------------------------------------r-m-p-ed {key} : {key}")
                    # if SHIFT: key = ord(chr(key).upper())



                # print(f"{centerX1} {centerY1}")
                # --------------------------------------------------------------------3rd line allows automatic grab to pandas help table!!!
                if ( (cross is None) and not greencross):
                     if ((frame is not None) and (rpi_name != "")
                    and (key == ord("?") and not CTRL) # HELP
                    ):
                        print("h PRESSED! - ")
                        show_help = not (show_help)
                        print(HELPTEXT)

                # -----------------------------------------------------rotate zoom

                if ((frame is not None) and \
                   (rpi_name != "")
                    and (key == ord("r") and not CTRL)# rotate +1
                    ):
                    print("r PRESSED! - rotate change")
                    if rotate is None:
                        rotate = 0
                    if rotate == 180:
                        rotate = 0
                    else:
                        rotate+=1

                if ((frame is not None) and \
                   (rpi_name != "")
                    and (key == ord("R") and not CTRL) # rotate -1
                    ): # rotate
                    print("R PRESSED! - rotate change")
                    if rotate is None:
                        rotate = 0
                    if rotate == 180:
                        rotate = 0
                    else:
                        rotate-=1

                if ((frame is not None) and \
                   (rpi_name != "")
                    and (key == ord("r") and CTRL)  #   rotate 0/180
                    ):
                    print("r PRESSED! - reset rotate")
                    if rotate is None:
                        rotate = 0
                    if rotate == 180:
                        rotate = 0
                    else:
                        rotate = 180


                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("z") and not CTRL)  # zoom start
                    ):
                    print(f"z PRESSED! - ZOOM {zoomme}x")
                    zoomme *= 2
                    if zoomme > 4:
                        zoomme = 1
                    sfilenamea = ""

                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("Z") and not CTRL) # zoom end
                    ):
                    print("Z PRESSED! - ZOOM ended")
                    zoomme = 1
                    sfilenamea = ""

                # ------------------------------------------ web  pause quit expa---------------

                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("w") and not CTRL) # open browser
                    ):
                    print("w PRESSED! - openning web browser")
                    webbrowser.open(videodev.replace("/video", ""))  # BRUTAL


                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord(" ") and not CTRL)  # PAUSE
                ):
                    print("SPC PRESSED! - pause/play") # (k e y == 1048608 or
                    pause = not pause
                    print(f" ... pause = {pause}")


                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("q") and not CTRL) # quit
                    ):
                    print("q PRESSED!")
                    print("i... it was version:", __version__)
                    sys.exit(1)

                # ------------------- X just x
                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("x") and not CTRL) # expand IMAGE2x
                    ):
                    print("x PRESSED! - expand 1x or 2x from  ", expande)
                    if expande == 2:
                        print("x PRESSED! - expand 1x ")
                        expande = 1
                    else:
                        print("x PRESSED! - expand  2x")
                        expande = 2

                # switch RES c-x  - consistent to  z,s-z .... x,c-x,s-x
                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("x") and CTRL)  # switch res ON
                    ):
                    print("Ctrl-x PRESSED! - resolution to MAX ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"switch_res_on": "SWITCH_RES_ON"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # switch RES  s-x
                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("X") and not CTRL) # switch res OFF
                    ):
                    print("X PRESSED! - resolution to 640 ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"switch_res_off": "SWITCH_RES_OFF"}
                    post_response = requests.post(url=post_addr, data=post_data)


                # -----------------------------------------------------save s a

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("a") and not CTRL) # start  savedecor avi
                ):
                    if save:
                        print("a PRESSED! - STOPPING AVI ... decor==",save_decor)
                        sfilenamea = ""
                        savepngcont = False
                        save = False
                    else:
                        print("a PRESSED! - saving AVI WITHOUT DECOR (mkv)")
                        save = True
                        save_decor = False

                        height, width, channel = frame.shape

                        sfilenamea, saviout = setupsave((width, height) , videodev=videodev )
                        print(">>>", sfilenamea)



                if ( (frame is not None) and \
                   (rpi_name != "")
                    and (key == ord("A") and not CTRL) # stop AVI save (decor)
                    ):
                    if save:
                        print("A PRESSED! - STOPPING AVI (mkv)  decor ==", save_decor)
                        sfilenamea = ""
                        savepngcont = False
                        save = False
                    else:
                        print("A PRESSED! - WITH DECOR saving AVI (mkv)")
                        save = True
                        save_decor = True
                        height, width, channel = frame.shape

                        sfilenamea, saviout = setupsave((width, height), videodev=videodev)
                        print(">>>", sfilenamea)



                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("a") and CTRL) # continuous local PNG save
                    ):
                    print("Ctrl-a PRESSED! -  ")
                    if savepngcont:
                        savepngcont = False
                    else:
                        print("ctl-a PRESSED! - LOCALY saving PNG continuosly !!!")  # ctrla
                        savepngcont = True



                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("p") and CTRL) # remote save PNG full q
                ):
                    print("Ctrl-s pressed  ... calling remote save of Full Quality PNG")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"savepn": "SAVEPN"}
                    post_response = requests.post(url=post_addr, data=post_data)

                saved_jpg = 0

                # defined above # sme = socket.gethostname()
                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("s") and not CTRL) # save JPG
                     ):
                    print("s or S PRESSED!  - ")
                    print("      ... not the internal save_image...")
                    sname = "snapshot"
                    sfilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    sfilename = f"{sme}_{sfilename}_{sname}.jpg"
                    saved_jpg = 1 #JPG

                    dir2create = os.path.expanduser("~/DATA/")
                    if not os.path.isdir(os.path.expanduser(dir2create)):
                        print(f"D... trying to create directory {dir2create} for saving")
                        os.mkdir(os.path.expanduser(dir2create))
                    sfilename = os.path.expanduser("~/DATA/" + sfilename)
                    isWritten = cv2.imwrite(sfilename, frame)
                    if isWritten:
                        print("Image is successfully saved as file.", sfilename)
                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("S") and not CTRL) # save PNG
                ):
                    print("s or S PRESSED!  - ")
                    print("      ... not the internal save_image...")
                    sname = "snapshot"
                    sfilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    sfilename = f"{sme}_{sfilename}_{sname}.png"
                    saved_jpg = 2 # PNG

                    dir2create = os.path.expanduser("~/DATA/")
                    if not os.path.isdir(os.path.expanduser(dir2create)):
                        print(f"D... trying to create directory {dir2create} for saving")
                        os.mkdir(os.path.expanduser(dir2create))
                    sfilename = os.path.expanduser("~/DATA/" + sfilename)
                    isWritten = cv2.imwrite(sfilename, frame)
                    if isWritten:
                        print("Image is successfully saved as file.", sfilename)


                # ------------------------- measure and cross -------------------------------

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("C") and not CTRL) # red cross save
                    ):
                        FILE_REDCROSS = get_FILE_REDCROSS( videodev )
                        print(
                            f"c PRESSED! - cross = {cross} OFF; saving {FILE_REDCROSS}"
                        )
                        if (cross is None) or (len(cross) != 2):
                            break
                        with open(os.path.expanduser(FILE_REDCROSS), "w") as f:
                            f.write(f"{cross[0]}\n{cross[1]}\n")
                            cross = None
                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("c") and not CTRL) # red cross  load
                     ):
                        if cross is None:
                            FILE_REDCROSS = get_FILE_REDCROSS( videodev )
                            cross = [0, 0]
                            if os.path.exists(os.path.expanduser(FILE_REDCROSS)):
                                try:
                                    with open(os.path.expanduser(FILE_REDCROSS)) as f:
                                        cr = f.readlines()
                                        cross = [int(cr[0]), int(cr[1])]
                                        print(f"i... redcross loaded {FILE_REDCROSS}")
                                except:
                                    print(f"X... problem to open {FILE_REDCROSS}")
                            print(f"c PRESSED! - cross = {cross} ON")

                # --------- redcross manip
                if cross is not None:
                    if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("h") and not CTRL) #  cross left
                    ):  # <
                        cross[0] -= 4
                    if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("j") and not CTRL) # cross down
                    ):  # v
                        cross[1] += 4
                    if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("k") and not CTRL) # cross up
                    ):  # ^
                        cross[1] -= 4
                    if (  (frame is not None) and (rpi_name != "")
                    and (key == ord("l") and not CTRL) # cross right
                    ):  # >
                        cross[0] += 4

                    if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("H") and not CTRL) # cross left
                    ):  # <
                        cross[0] -= 17
                    if (  (frame is not None) and (rpi_name != "")
                    and (key == ord("J") and not CTRL) # cross down
                    ):  # v
                        cross[1] += 17
                    if (   (frame is not None) and (rpi_name != "")
                    and (key == ord("K") and not CTRL) # cross up
                    ):  # ^
                        cross[1] -= 17
                    if (   (frame is not None) and (rpi_name != "")
                    and (key == ord("L") and not CTRL) # cross righht
                    ):  # >
                        cross[0] += 17
                    #print(frame.shape)

                if (
                    (measure > 0)
                    and (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("N") and not CTRL) # @measure distance far
                ):
                    print("N PRESSED! - measure distance - far")
                    measure_prev_tmp = measure
                    measure = round(10 * measure / 1.2) / 10
                    if measure_prev_tmp == measure:
                        measure = measure/2
                    if measure < 0.1:
                        measure = 0.1

                if (
                    (measure > 0)
                    and (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("n") and not CTRL) # @measure distance close
                ):
                    print("m PRESSED! - measure distance - closer")
                    measure_prev_tmp = measure
                    if measure == 0:
                        measure = 1
                    if measure < 0:
                        measure = -measure
                    measure = round(10 * measure * 1.15) / 10
                    if measure_prev_tmp == measure:
                        measure = measure*2
                    if measure > 20000:
                        measure = 20000

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("m") and not CTRL) # measure
                     ):
                    print("m PRESSED! - measure distance - ON")
                    print("i... cheap Sonix :  44 deg")
                    print("i... Sony imx    : 101 deg")
                    print("i... zenbook     :  56 deg")
                    if measure < 0:
                        measure = -measure
                    if measure == 0:
                        measure = 1

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("M") and not CTRL) # M measure
                    ):
                    print("M PRESSED! - DEmeasure")
                    measure = -abs(measure)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure > 0)
                    and (key == ord("f") and not CTRL) # @measure FOV inc
                ):
                    print("f PRESSED! - FOV increase", measure_fov)
                    prev_fov_tmp = measure_fov
                    measure_fov = measure_fov * 1.15
                    if measure_fov > 4:
                        measure_fov = round(measure_fov)
                        if measure_fov == prev_fov_tmp:
                            measure_fov = 2* measure_fov
                    else:
                        measure_fov = round(measure_fov * 10) / 10
                        if measure_fov == prev_fov_tmp:
                            measure_fov = 2* measure_fov
                    if measure_fov > 160:
                        measure_fov = 160


                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure > 0)
                    and (key == ord("F") and not CTRL) # @measure FOV  dec
                ):
                    print("F PRESSED! - FOV decrease")
                    measure_fov = measure_fov / 1.25
                    if measure_fov > 3:
                        measure_fov = round(measure_fov)
                    else:
                        measure_fov = round(measure_fov * 10) / 10

                    if measure_fov < 0.3:
                        measure_fov = 0.3

                # ---------------- trackers--------------- t T u---------------

                # ==========================================================================
                # ==========================================================================
                # ==========================================================================
                #  TRACKER THING
                # ==========================================================================
                # ==========================================================================
                # ==========================================================================
                # ------if ALLOWED - first - to have no display help
                # elif to skip one loop
                if (
                    (allow_tracker)
                    and (frame is not None)
                    and (rpi_name != "")
                    # and allow_tracker1
                ):
                    print("i ... setting allowed tracker1 \n") # ??????????????????????????????????
                    allow_tracker = False
                    tracker1 = cv2.TrackerCSRT_create()  # KCF GOTURN MIL
                    bbox = cv2.selectROI(frame)
                    if (len(bbox) < 4) or (bbox[-1] < 10):
                        tracker1 = None
                        print("i... fail init track")
                    else:
                        # bbox = tuple([ i+0.5 for i in bbox ])
                        ok = tracker1.init(frame, bbox)
                        tracker_list = []
                        tracker1_fname = datetime.datetime.now().strftime(
                            "tracker1_%Y%m%d_%H%M%S.dat"
                        )
                        # #------------this is for histotracker
                        # x,y,w,h = bbox
                        # track_window = bbox
                        # # roi = frame[x:x+w, y:y+h]
                        # roi = frame[ y:y+h, x:x+w]
                        # hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                        # mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
                        # roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
                        # cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
                        # term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 0.1 ) #iters, eps

                        # orb = cv2.ORB_create() # I dont use now


                if (
                    (allow_tracker)
                    and (frame is not None)
                    and (rpi_name != "")
                    #                    and allow_tracker2
                ):
                    print("t PRESSED! - track", tracker2)  #??????????????????????????????????
                    print("i ... setting allowed tracker2 \n")
                    allow_tracker = False
                    tracker2 = cv2.TrackerKCF_create()  # KCF GOTURN MIL
                    bbox2 = cv2.selectROI(frame)
                    if (len(bbox2) < 4) or (bbox2[-1] < 10):
                        tracker2 = None
                        print("i... fail init track2")
                    else:
                        # bbox2 = tuple([ i+0.5 for i in bbox2 ])
                        ok2 = tracker2.init(frame, bbox2)
                        tracker2_fname = datetime.datetime.now().strftime(
                            "tracker2_%Y%m%d_%H%M%S.dat"
                        )

                # -----  allow display help, after allow tracker true
                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("t") and not CTRL) # TRACKer demand ask
                    and not (allow_tracker_demand)
                    and not (allow_tracker)
                ):
                    print("Ctrl-t/T PRESSED! -  ")
                    print("i... allow tracker demand\n")
                    allow_tracker_demand = True
                    allow_tracker2 = False
                    allow_tracker1 = False
                    # switch on the menu display

                # --- 2nd 't' press :  is before demand=True, sets allow true
                elif (  (frame is not None) and (rpi_name != "")
                    and (key == ord("T") and not CTRL) # Tracker2 ON
                    and (allow_tracker_demand) and not (allow_tracker)
                      ):
                    print("i... allowing tracker2, removing tracker_demand\n")
                    allow_tracker = True  # but I need one loop to remove menu
                    allow_tracker_demand = False
                    allow_tracker2 = False
                    allow_tracker1 = False
                    allow_tracker2 = True
                elif ( (frame is not None) and (rpi_name != "")
                    and (key == ord("t") and not CTRL) # Tracker 1 ON
                    and (allow_tracker_demand) and not (allow_tracker)
                         ):
                    print("i... allowing tracker1, removing tracker_demand\n")
                    allow_tracker = True  # but I need one loop to remove menu
                    allow_tracker_demand = False
                    allow_tracker2 = False
                    allow_tracker1 = False
                    allow_tracker1 = True

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("u") and not CTRL) # UNTRACK
                    ):
                    print("u PRESSED! - UNtrack")
                    tracker1 = None
                    tracker2 = None
                    tracker_date = None
                    allow_tracker_demand = False
                    allow_tracker = False


                    # ==================================================
                    # ==================================================
                    # ==================================================
                    # END OF TRACKERS
                    # ==================================================
                    # ==================================================
                    # ==================================================

                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("v") and not CTRL) #  green cross ON
                    ):
                    print("v PRESSED! - green crosson")
                    greencross = True
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"crosson": "CROSSON"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("V") and not CTRL) # green cross off
                    ):
                    print("V PRESSED! - green crossoff")
                    greencross = False
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"crossoff": "CROSSOFF"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("b") and not CTRL) # substract BG
                    ):
                    print("b PRESSED! - substract background")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"subbg": "SUBBG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("B") and not CTRL) # save BG
                     ):
                    print("B PRESSED! - save background")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"savebg": "SAVEBG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("f") and not CTRL) # mix foreground
                ):
                    print("f PRESSED! - mix foreground")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"mixfg": "MIXFG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("F") and not CTRL) # save foreground
                ):
                    print("F PRESSED! - save foreground")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"savefg": "SAVEFG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("o") and not CTRL) #  countdown optimization
                    ):
                    print("o PRESSED! - ")
                    # post_addr = videodev.replace("/video","/cross" )
                    # post_data = {'exposet':'EXPOSET','expovalue':0.3145}
                    # post_response = requests.post(url=post_addr, data=post_data)
                    countdown = [
                        0.0,
                        0.001,
                        0.002,
                        0.004,
                        0.008,
                        0.01,
                        0.02,
                        0.04,
                        0.08,
                        0.1,
                        0.2,
                        0.4,
                        0.8,
                        1.0,
                        -2,
                        0.0,
                        0.001,
                        0.002,
                        0.004,
                        0.008,
                        0.01,
                        0.02,
                        0.04,
                        0.08,
                        0.1,
                        0.2,
                        0.4,
                        0.8,
                        1.0,
                        -97,
                        -98,
                        -99,
                    ]
                    countdown_gain = False
                    # -2, -97 calc. , -98 -99 perform
                    now = datetime.datetime.now()
                    delta = now - datetime.datetime(1970, 1, 1)
                    countdown_s = delta + datetime.timedelta(seconds=countdownpause)
                    countdown_ana_on = False
                    countdown_ana_results = []
                    # sqitch off gain
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain": "GAIN"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if "countdown" in locals() and len(countdown) > 0:
                    now = datetime.datetime.now()
                    delta = now - datetime.datetime(1970, 1, 1)
                    if delta > countdown_s:
                        if "countdown_ana_on" in locals():
                            if countdown_ana_on:
                                # print("   ------ analysing ----------------")
                                countdown_ana_on = False
                                senh.add_frame(
                                    frame[21: frame.shape[0] - 21, 0: frame.shape[1]]
                                )
                                hmean = senh.histo_mean()
                                print(
                                    f"i... histogram mean:{hmean:3d} / pre{countdown[0]:.3f} {len(countdown)*countdownpause:3.0f} sec. remains"
                                )
                                countdown_ana_results.append(hmean)

                                # print( countdown_ana_results )

                                # ------ analyze first batch -   (-2)
                                if (countdown[0] < -1) and (
                                    countdown[0] > -3
                                ):  # without gain
                                    resx = np.array(countdown_ana_results[::2])
                                    resy = np.array(countdown_ana_results[1::2])
                                    # allx = resx
                                    # ally = resy
                                    allx = np.logspace(-4, 1, 400)
                                    ally = np.interp(allx, resx, resy, 100)

                                    # if not good
                                    # if  (np.abs(ally - optim_histo).min()>1): # works for dark
                                    # if good
                                    if (np.abs(ally - optim_histo).min() <= 1) or (
                                        ally - optim_histo
                                    ).min() > 1:  # always brighter:: #
                                        if (
                                            ally - optim_histo
                                        ).min() > 1:  # always brighter:: #
                                            print(
                                                "i... always brighter, I stop here without gain 1"
                                            )
                                        countdown = [-98, -99]
                                        allx_idx = np.abs(ally - optim_histo).argmin()
                                        optimexpo = allx[allx_idx]
                                        optimgain = -1
                                        print(resx)
                                        print(resy)
                                        print(
                                            f"i... best x  {optimexpo} at element {allx_idx}, no gain games"
                                        )
                                    else:
                                        if ally.max() - ally.min() < 3:
                                            print(
                                                "i... there is no effect of EXPO: cheap Sonix cam?"
                                            )
                                            countdown_gain = True
                                        countdown_ana_results = []

                                if countdown[0] == -97:  # final with gain 1
                                    resx = np.array(countdown_ana_results[::2])
                                    resy = np.array(countdown_ana_results[1::2])
                                    allx = resx
                                    ally = resy
                                    allx = np.logspace(-4, 1, 400)
                                    ally = np.interp(allx, resx, resy, 100)

                                    # if  (np.abs(ally - optim_histo).min()>1) and (countdown[0]>-3):
                                    #    break
                                    # elif countdown[0]>-3:
                                    #    countdown=[-98,-99]

                                    # optimexpo = resx[ np.abs(resy - optim_histo).argmin() ]
                                    allx_idx = np.abs(ally - optim_histo).argmin()
                                    optimexpo = allx[allx_idx]
                                    if optimexpo > 1:
                                        optimexpo = 1
                                    optimgain = 1
                                    if countdown_gain:  # when cheap sonix camera:
                                        optimexpo = 20
                                        optimgain = allx[allx_idx]
                                        if optimgain > 1:
                                            optimgain = 1
                                        print(f"i... OPTIMAL GAIN = {optimgain}")
                                    else:
                                        print(f"i... OPTIMAL EXPO = {optimexpo}")
                                        print("i... BUT USE GAIN 1 !")

                                    print("RESULTS:")
                                    print(resx)
                                    print(resy)
                                    print(
                                        f"i... best x  {optimexpo} at element {allx_idx} "
                                    )
                                    # with open(f"expo_calib_{now.strftime('%H%M%S')}.txt",'w') as f:
                                    #    f.write(" ".join( [str(e) for e in countdown_ana_results]))
                        #                                        f.write("\n")

                        # print("   --------- counting down ------: ", len(countdown) )
                        countdown_s = delta + datetime.timedelta(seconds=countdownpause)
                        exnow = float(
                            countdown.pop(0)
                        )  # 0 left way; -1 default  is from right
                        post_addr = videodev.replace("/video", "/cross")
                        if exnow < -98:  # -99 back to default with gain
                            post_data = {"gain": "GAIN"}
                            if optimgain > 0:  # can be only 1 or -1
                                post_data = {
                                    "gainset": "GAINSET",
                                    "gainvalue": optimgain,
                                }
                        elif exnow < -97:  # -99 back to default with expo
                            post_data = {"expo": "EXPO"}
                            if optimexpo >= 0:
                                post_data = {
                                    "exposet": "EXPOSET",
                                    "expovalue": optimexpo,
                                }
                        elif exnow < -1:
                            # exnow = float( countdown.pop(0) )
                            post_data = {"gainset": "GAINSET", "gainvalue": 1.0}
                        else:  # testing data
                            if (
                                countdown_gain
                            ):  # i will play on gain with cheap sonix camera
                                post_data = {"gainset": "GAINSET", "gainvalue": exnow}
                            else:
                                post_data = {"exposet": "EXPOSET", "expovalue": exnow}
                            countdown_ana_on = True
                            countdown_ana_results.append(exnow)
                        post_response = requests.post(url=post_addr, data=post_data)

                # if 'countdown_ana_on' in locals():
                #     if countdown_ana_on:
                #         print("   ------ analysing ----------------")
                #         countdown_ana_on = False
                #         senh.add_frame( frame )
                #         hmean = senh.histo_mean( )
                #         print(hmean)
                #         countdown_ana_results.append(hmean)
                #         print( countdown_ana_results )
                #         if len(countdown)==0:
                #             print( "RESULTS:", countdown_ana_results )

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("O") and not CTRL) # break expo optimizatioon - ??
                    ):
                    print("O PRESSED! - break expo optim")
                    # post_addr = videodev.replace("/video","/cross" )
                    # post_data = {'gainset':'GAINSET','gainvalue':1.}
                    # post_response = requests.post(url=post_addr, data=post_data)
                    if "countdown" in locals():
                        countdown = []

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("e") and not CTRL) # expo up
                ):
                    print("e PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"expo2": "EXPO2"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("E") and not CTRL) # expo down
                    ):
                    print("e PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"expo05": "EXPO05"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # ------------------default expo----------------------
                if (  (frame is not None) and (rpi_name != "")
                    and (key == ord("e") and CTRL) # expo reset
                ):
                    print("Ctrl-e PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"expo": "EXPO"}
                    post_response = requests.post(url=post_addr, data=post_data)


                # --------------------------gain ----------------------

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("g") and not CTRL) # gain up
                ):
                    print("g PRESSED! -  gain up")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain2": "GAIN2"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if  (  (frame is not None) and (rpi_name != "")
                    and (key == ord("G") and not CTRL) # gamma down
                     ):
                    print("G PRESSED! - gain down")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain05": "GAIN05"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("g") and CTRL) # gain reset
                ):
                    print("Ctrl-g PRESSED! -  gain reset")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain": "GAIN"}
                    post_response = requests.post(url=post_addr, data=post_data)


                # --------------------------gamma ----------------------

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("y") and not CTRL) # gamma up
                ):
                    print("y PRESSED! -  gamm up")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gamma2": "GAMMA2"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("Y") and not CTRL) # Gain down
                ):
                    print("Y PRESSED! - gain down")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gamma05": "GAMMA05"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("y") and CTRL) # gamma reset
                ):
                    print("Ctrl-y PRESSED! -  gamma reset")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gamma": "GAMMA"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # ------------------------------local gamma --------------------------
                if ( (frame is not None)   and (rpi_name != "")
                    and (key == ord("d") and not CTRL) #  local gamma up
                    ):
                    print("d PRESSED! - local gamma+")
                    local_gamma = local_gamma * 1.4

                if (   (frame is not None)  and (rpi_name != "")
                    and (key == ord("D") and not CTRL) #  local gamma down
                    ):
                    print("D PRESSED! - local gamma -")
                    local_gamma = local_gamma / 1.4

                if (     (frame is not None)  and (rpi_name != "")
                    and (key == ord("d") and CTRL)  #  local gamma reset
                    ):
                    print("Ctrl-d PRESSED! - reset local gamma")
                    local_gamma = 1



                # -------------------------------------------------------- p fixed live ----------pause

                if (
                        (frame is not None) and (rpi_name != "")
                    and (key == ord("p") and not CTRL)  # show fixed image
                ):
                    print("p PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"fixed": "FIXED"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if ((frame is not None) and (rpi_name != "")
                    and (key == ord("P") and not CTRL)  # show live:(opposite to fixed)
                    ):
                    print("P PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"live": "LIVE"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # --------- greencross manip
                if (cross is None) and greencross:
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {}

                    if ( (frame is not None) and (rpi_name != "")
                        and (key == ord("h") and not CTRL) #green c  left
                        )  :  # <
                        post_data = {"left": "LEFT"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("j") and not CTRL) # green c down
                        ):  # v
                        post_data = {"down": "DOWN"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("k") and not CTRL) # greenc up
                        ):  # ^
                        post_data = {"up": "UP"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("l") and not CTRL) # green c right
                        ):  # >
                        post_data = {"right": "RIGHT"}

                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("H") and not CTRL) # greenc left
                        ):  # <
                        post_data = {"left2": "LEFT2"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("J") and not CTRL) # green c down
                        ):  # v
                        post_data = {"down2": "DOWN2"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("K") and not CTRL) # greenc up
                        ):  # ^
                        post_data = {"up2": "UP2"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("L") and not CTRL) # greenc right
                        ):  # >
                        post_data = {"right2": "RIGHT2"}

                    if post_data != {}:
                        post_response = requests.post(url=post_addr, data=post_data)

                # --------- pantilthat manip
                if (cross is None) and not greencross:
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {}

                    if ( (frame is not None) and (rpi_name != "")
                        and (key == ord("h") and not CTRL) # pantilt
                        ):  # <
                        post_data = {"left": "LEFT"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("j") and not CTRL) # pantilt
                        ):  # v
                        post_data = {"down": "DOWN"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("k") and not CTRL) # pantilt
                        ):  # ^
                        post_data = {"up": "UP"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("l") and not CTRL) # pantilt
                        ):  # >
                        post_data = {"right": "RIGHT"}

                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("H") and not CTRL) # pantilt
                        ):  # <
                        post_data = {"left2": "LEFT2"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("J") and not CTRL) # pantilt
                        ):  # v
                        post_data = {"down2": "DOWN2"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("K") and not CTRL) # pantilt
                        ):  # ^
                        post_data = {"up2": "UP2"}
                    if ((frame is not None) and (rpi_name != "")
                        and (key == ord("L") and not CTRL) # pantilt
                        ):  # >
                        post_data = {"right2": "RIGHT2"}

                    if post_data != {}:
                        post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("i") and not CTRL) # accumulate (integrate)
                ):
                    integrate *= 2
                    print(f"i PRESSED! - accum  {integrate} snapshots")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"accum": "ACCUM", "accumtxt": int(integrate)}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("I") and not CTRL) #accumulate (integrate) BACK 1
                ):
                    print("i PRESSED! - accum integrate 1")
                    integrate = 1
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"accum": "ACCUM", "accumtxt": 0}
                    post_response = requests.post(url=post_addr, data=post_data)


                # ctrl -- MODES   histo / direct /  detect /lapAstro
                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("h") and CTRL) # ctrl HISTOGRAM frame
                ):
                    print("Ctrl-h PRESSED! - HISTOGRAM BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"framekind": "HISTOGRAM" }
                    post_response = requests.post(url=post_addr, data=post_data)


                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("j") and CTRL) # ctrl DIRECT frame
                ):
                    print("Ctrl-j PRESSED! - directmode BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"framekind": "DIRECT" }
                    post_response = requests.post(url=post_addr, data=post_data)


                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("k") and CTRL) # ctrl detectmode frame
                ):
                    print("Ctrl-k PRESSED! - detectmode BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"framekind": "DETECT" }
                    post_response = requests.post(url=post_addr, data=post_data)

                # --------------------------------------------------------------------3rd line allows automatic grab to pandas help table!!!
                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("l") and CTRL) # ASTRO-LAPS
                ):
                    print("Ctrl-l PRESSED! - Laps-ASTRO  BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    if timelaps == 0:
                        timelaps = -1
#                    elif timelaps == -1: # ONLY ASTRO FOR NOW   -1 OR 0
#                        timelaps = 15
                    else:
                        timelaps = 0
                    print(f"Ctrl-l PRESSED! - Laps Astro {timelaps}  ---------------------")
                    # it is already in webform....
                    # ImmutableMultiDict([('timelaps', 'TIMELAPS'), ('timelaps_input', '0'), ('inputx', ''), ('inputy', ''), ('accumtxt', '')])

                    post_data = {"timelaps": "TIMELAPS" ,"timelaps_input": str(timelaps) }
                    post_response = requests.post(url=post_addr, data=post_data)



                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("t") and CTRL) # Test- jpg compression
                ):
                    print("Ctrl-t PRESSED! - TEST BUTTON ----jpg komression------------")
                    print(" ... clears countdown .... ")
                    #print(" try to keep ctl pressed and then press t")
                    post_addr = videodev.replace("/video", "/cross")
                    if len(jpgkompr1)==0:
                        jpgkompr1 = [x for x in jpgkompr2]
                    aaa = jpgkompr1.pop(0)
                    print(" ... available comp",jpgkompr1)
                    print(" ... sets  kompression:", aaa)
                    post_data = {"kompress": "KOMPRESS", "kompressvalue": aaa}
                    post_response = requests.post(url=post_addr, data=post_data)
                    if "countdown" in locals():
                        countdown = []

                # TEST key code
                # if key!=-1:
                #    print(f"\n{key}\n")

        print("i... it was version", __version__)


if __name__ == "__main__":
    Fire(display2)
    # Fire({ "disp":display2,   "disp2":display2    })
