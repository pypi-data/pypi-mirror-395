#!/usr/bin/env python3
from imutils.video import VideoStream
import cv2
import time
import datetime as dt
import socket
from random import randint

import numpy as np

import imutils
import datetime as dt


from flashcam.version import __version__
import os


# run this program on each RPi to send a labelled image stream
import time
from imutils.video import VideoStream
import imagezmq
import zmq # for timeouts??
import threading


import notifator.telegram as telegram

from console import fg

# i want also here for LAP
from PIL import ImageFont, ImageDraw, Image

from console import fg,bg
from flashcam.text_write import iprint, fonts_available, get_f_height, get_f_width, get_def_font, set_def_font

import flashcam.config as config # finally I need netport

import skvideo.io


# host name for once
SOCKET_GETHOSTNAME =socket.gethostname()

# =========================== DEFAULT FONT =====================
# get_f_height("vt4")
# #get_f_height("ty")
# #get_f_height("fj6")
# #get_f_height("re")
# #get_f_height("v14")
# #get_f_height("co")
# #get_f_height("pr4")
# get_f_height("nib")
# #get_f_height("li")
# #get_f_height("cu")
# get_f_height("di")
# #get_f_height("s8")

set_def_font("di")

class Stream_Enhancer:
    """
    definitions of positions on the frame
    ROW COLUMN  - colors defined elsewhere
   4 columns MAX
    """

    # COORDINATES used with setbox( "text", senh.TIME  ) _________
    # --------------- TOP  0,x
    TIME  = (0,0) #  basic bar
    DISP  = (0,4) # gree   -  detect delta histo
    MODE  = (0,3) # red    - DM z T
    SUBBG = (0,5) # substract background  or melt FG?

    # ------------- LOW LINE
    expo  = (2,0)
    gain  = (2,1)
    gamma = (2,2)
    speedx= (2,3)
    speedy= (2,4)
    #--------------- NEVER when speedxy
    dm=  (2,4) #  it is veeery long, overlaps

    #--------------------- 2 is bottom
    lap = (1,0) # side
    # avoid 2,0
    avg = (3,0) # accum    2,0 is for LOWLINE
    blr = (4,0) # LOW DEEP
    trh = (5,0) # side
    hist= (6,0) # side
    rot = (7,0) # side  /otate in bin...
    # ------ more (with/for uni)
    avi = (8,0) #
    jpg = (9,0) #

    scale = (10,0) #? see
    xzoom = (11,0) #? see

    delta_frame = None
    detect_frame = None
    frame_area = 1

    frame_number = 0

    motion_detected = False
    motion_detected_start = dt.datetime.now()
    expire = 10 # expire motiondetected (earlier 2 sec)
    aviopened = False

    avi_last = dt.datetime.now() - dt.timedelta(seconds=90000)
    aviopened_laps = False
    avi_started = dt.datetime.now()  # I like to have one file per day.....

    # -- age of frame for speed
    camera_age = 0
    camera_start = dt.datetime.now()

    # -- subtraction of mask
    frame_bg = None
    sub_bg = False
    frame_fg = None
    mix_fg = False

    # background path
    BGFILE = os.path.expanduser('~/.config/flashcam/background.jpg')
    FGFILE = os.path.expanduser('~/.config/flashcam/foreground.jpg')

    zmqrpi_name = socket.gethostname()
    zmqtarget = None #IP is operated from real_camera
    zmqsender = None # object
    zmqlast = dt.datetime.now()

    jtelegram = False # connector from real_camera
    telegram_tripwire = 2 # send 2 sec later after the triger...
    telegramlast = dt.datetime.now()
    telegramtrigger = False ## either BOOL or DATETIME

    aviout = None # I have a problem to seee saving the images to DaTA
    # THESE ARE 2 NEW WRITERS.....
    skwriter_laps = None
    skwriter_detm = None

    # this is used with setbox( "text", senh.TIME  ) _________
    def RC_COLOR(self,row,col):
        if not self.frame_ok: return  # B  G R
        if (row,col) == self.TIME: return (200,0,0)
        if (row,col) == self.MODE: return (0,0,255)
        if (row,col) == self.DISP: return (0,205,0)
        if (row,col) == self.SUBBG: return (90,50,200)

        if (row,col) == self.lap: return (200,100,200) #
        if row==1 and col==1: return (150,150,150) #
        if row==1 and col==2: return (50,50,50) #
        if row==1 and col==3: return (120,120,120) # brown
        if row==1 and col==4: return (180,180,180) # orange

        if (row,col) == self.avg:  return (250,0,0) #
        if (row,col) == self.blr:  return (150,150,0) #
        if (row,col) == self.trh:  return (150,0,150) #
        if (row,col) == self.hist: return (0,120,150) # brown
        if (row,col) == self.dm:   return (50,100,250) # orange
        if (row,col) == self.rot:  return (150,120,150) #


        # left side
        if (row,col) == self.expo:  return (0,0,0) #
        if (row,col) == self.gain:  return (50,50,50) #
        if (row,col) == self.gamma: return (80,80,80) #

        if (row,col) == self.speedx: return (180,80,80) #
        if (row,col) == self.speedy: return (80,180,80) #
        if (row,col) == self.avi:    return (30,30,210) # FOR UNI only
        if (row,col) == self.jpg:    return (0,0,250)   # FOR UNI only
        if (row,col) == self.scale:  return (250,0,250)   # zoom scale
        if (row,col) == self.xzoom:  return (0,100,250)   # xperimental zoom

        t=[255,255,255]
        while (t[0]+t[1]+t[2]>400) or  (t[0]+t[1]+t[2]<200) :
            t =  (randint(5,255),randint(5,255),randint(5,255) )
        #print(t[0]+t[1]+t[2])
        return t


#---------------------------------- INIT ----------

    def __init__(self, resolution=(640,480) ):
#    def __init__(self, resolution=(320,240) ):
        if  type(resolution)==str:
            w,h = resolution.split("x")
            w=int(w)
            h=int(h)
            print(f"i... {fg.yellow} STR StreamEnhancere init; resol== {w}x{h} {fg.default}")
        else:
            w,h=resolution[1],resolution[0]
            w,h=resolution[0],resolution[1]
            print(f"i... {fg.yellow} TUP StreamEnhancere init; resol== {w}x{h} {fg.default}")
        print(f"i... {fg.yellow} StreamEnhancere init; resol== {resolution} {fg.default}")
        print(f"i... {fg.yellow} StreamEnhancere init; resol== {w} x {h}  {fg.default}")
        self.resolution = (h,w)
        self.posx_offs=5
        self.posy_offs=5
        self.frame_ok = False

        self.first_frame = True
        self.accubuffer = [] # accumulation for motion
        self.accumulate_number = 1 # just informative for laps


#----------------------------------------- RETURN THE FRAME ----BACK
    def get_frame(self,  typ=""):
        if typ=="delta":
            if not(self.delta_frame is None):
                return self.delta_frame

        if typ=="detect":
            if not(self.detect_frame is None):
                return self.detect_frame

        if typ=="histo":
            #if "histo_frame" in locals():
            if not(self.histo_frame is None):
                return self.histo_frame

        return self.frame


#---------------------------  INSERT FRAME TO THIS OBJECT ----
    def add_frame(self, image):
        # print("D... adding fframe")
        h,w = 480,640
        self.frame_ok = True
        try:
           h,w = image.shape[0],image.shape[1]
        except Exception as ex:
            print(f"X... add_frame exc: ",ex)
            pass

        # EARLIER I DID CONVERT THE SIZE.... NOW I DO NOT WANT
        # BUT it is initialized already with 1280x720 e.g.
        # I CHANGE BRUTALY THE RESOLUTION NOW
        if image is not None and  image.shape[1]!=self.resolution[0] or image.shape[0]!=self.resolution[1]:
            #print("X... res0 == ",image.shape[0], self.resolution[0])
            #print("X... res1 == ",image.shape[1], self.resolution[1])
            #self.frame = cv2.resize(image, (self.resolution[1], self.resolution[0]), interpolation=cv2.INTER_NEAREST)
            #print(f" SH>>{fg.red}{self.frame.shape}{fg.default} ", end = "" )
            self.frame = image
            self.resolution = (image.shape[1], image.shape[0] )
            # print(f" {fg.red}SH!size{fg.default} ", end = "" )
        else:
            self.frame = image
        self.frame_ok = True
        #except Exception as e:
        #    print("D... in add frame bad frame")
        #    self.frame_ok = False
        if not self.frame_ok:
            return False

        self.maxcol=5 # NORMALLY 4
        # self.maxcol=7 # with x y
        self.maxrow=14
        # #if fontScale == 0.5
        #if w==320:
        #    self.maxcol=2
        #    self.maxrow=5
        # #if fontScale is W/640 *0.5
        if w==320:
        #    self.maxcol=2
            self.maxrow=13

        if self.first_frame:
            print( "D... 1st frame len=",len(self.frame) )
            self.averageValue1 = np.float32(self.frame)
            self.first_frame = False


        return True


#---------------------------  INSERT FRAME from CAMERA TO THIS OBJECT ----
    def add_frame_from_cam(self):
        """

        """
        self.imstream = VideoStream(0).start()
        self.imstream.stream.set(3, self.resolution[0])
        self.imstream.stream.set(4, self.resolution[1])
        image = self.imstream.read()
        self.imstream.stop()
        return self.add_frame(image)

#--------------------------- imshow ---------------------
    def show_frame(self):
        if not self.frame_ok: return
        cv2.imshow("A", self.frame)
        wkey="a"
        while wkey!=ord("q"):
            wkey = cv2.waitKey(10)
        cv2.destroyAllWindows()

#--------------------------- imshow ---------------------
    def blimp_frame(self):
        if not self.frame_ok: return
        cv2.imshow("A", self.frame)
        cv2.waitKey(100)

    def get_font_params(self, txt, fname=None):
        """
        I think this is obsolete
        """
        if not self.frame_ok: return
        self.font       = cv2.FONT_HERSHEY_SIMPLEX
        self.font       = cv2.FONT_HERSHEY_SIMPLEX
        self.font       = cv2.FONT_HERSHEY_DUPLEX

        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.font = cv2.FONT_HERSHEY_PLAIN  # needs offset

        self.fontScale  = 0.85 * (self.frame.shape[1]/640) # 0.5 * (self.frame.shape[1]/640)
        self.lineType   = 1
        self.text_width, self.text_height = cv2.getTextSize(txt,self.font,self.fontScale,self.lineType)[0]

        if fname is None:
            self.text_width, self.text_height = len(txt)*get_f_width(), get_f_height()
        #self.text_width, self.text_height = 15, 15



#------------------------------------------------------PUT TEXT --------------
    def textbox(self,txt, pos=[5,5], bgcolor=(0,0,0), fgcolor=(255,255,255) , target = None):
        #if txt.find("DM") >= 0:      print(" -->", end="")
        if not self.frame_ok: return
        #if txt.find("DM") >= 0:      print("ok")
        self.get_font_params(txt )
        # top left 0 0
        beginCorner=( pos[0]-2                , pos[1]- self.text_height-1 )
        endCorner  =( pos[0]+self.text_width+1, pos[1]+1   )

        if target is None or target == "direct":
            cv2.rectangle(self.frame, beginCorner, endCorner, bgcolor, cv2.FILLED)
            # if txt.find("DM") >= 0:              print(  beginCorner, endCorner )

            self.frame = iprint( self.frame,
                             txt,
                             get_def_font() ,
                             tuple(pos),
                             color_rgb= fgcolor#(255,255,255,0)
                            )
        elif target=="detect" and self.detect_frame is not None:
            cv2.rectangle(self.detect_frame, beginCorner, endCorner, bgcolor, cv2.FILLED)
            self.detect_frame = iprint( self.detect_frame,
                             txt,
                             get_def_font() ,
                             tuple(pos),
                             color_rgb= fgcolor#(255,255,255,0)
                            )
        elif target=="delta" and self.delta_frame is not None:
            cv2.rectangle(self.delta_frame, beginCorner, endCorner, bgcolor, cv2.FILLED)
            self.delta_frame = iprint( self.delta_frame,
                             txt,
                             get_def_font() ,
                             tuple(pos),
                             color_rgb= fgcolor#(255,255,255,0)
                            )
        elif target=="histo" and self.histo_frame is not None:
            cv2.rectangle(self.histo_frame, beginCorner, endCorner, bgcolor, cv2.FILLED)
            self.histo_frame = iprint( self.histo_frame,
                             txt,
                             get_def_font() ,
                             tuple(pos),
                             color_rgb= fgcolor#(255,255,255,0)
                            )


#----------------------------------------------- DEFINE GRID HERE-------
    def setbox(self, txt, rowcol, side="" , target = None, grayed = False, kompr=None):
        """
        uses textbox, pots on positions....
        """
        frametgt = "direct"
        if target is None or target=="direct":
            frametgt = "direct" #self.frame
        elif target == "detect":
            frametgt = "detect"
        elif target == "delta":
            frametgt = "delta"
        elif target == "histo":
            frametgt = "histo"

        row,col=list(rowcol)
        if not self.frame_ok: return
        stretchy = 2.2
        stretchx = 1.3 # this also compensates center-left align?
        pos=[ self.posx_offs, self.posy_offs ]
        self.get_font_params(" WEB 2.3, ")
        WIDTH = self.text_width
        self.get_font_params(txt )

        if side=="left":  col=0
        if side=="right":  col=-1
        pos[0] = self.posx_offs + int(col*WIDTH*stretchx)
        pos[1] = self.posy_offs + self.text_height + int(row*stretchy*self.text_height)
        pos[1] = 2+ self.text_height + int(row*stretchy*self.text_height)


        # Just columns
        if col>self.maxcol:
            print("X... only {} columns allowed".format(self.maxcol) )
            return

        # manually I set leftside
        # if (row==1)and(col==0):  side="left"
        # if (row==2)and(col==0):  side="left" # low deck
        if (row==3)and(col==0):  side="left"
        if (row==4)and(col==0):  side="left"
        if (row==5)and(col==0):  side="left"

        if (row==6)and(col==0):  side="left"
        if (row==7)and(col==0):  side="left"
        if (row==8)and(col==0):  side="left"
        if (row==9)and(col==0):  side="left"

        if (row==10)and(col==0):  side="left"
        if (row==11)and(col==0):  side="left" # xzoom

        if side=="" and row>2:
            print("X... SENH: Too many rows or undef.row ")
            return

        #------sides
        if side=="left" or side=="right":
            #print("D.. SIDES", self.maxrow, self.maxcol)
            if row>self.maxrow:
                print("X... {} rows {} cols allowed".format(self.maxrow,self.maxcol) )
                return
            #-----OK i go for it---
            #txt=txt[0:3] # i dont restrict...
            #print(txt)
            self.get_font_params("txt")
            WIDTH = self.text_width
            # ----- i dont remember why this ADDITION...
            #pos[1]+= int(2*stretchy*self.text_height)
            #---- right side
            if side=="right":
                pos[0] = self.frame.shape[1] - self.posx_offs - int(stretchx*WIDTH)


        else: # --------------------------- TimeStamp and G/R circle automatic HERE
            if row==0:
                if (col==0):
                    NOW = dt.datetime.now()
                    date = NOW.strftime("__%H:%M:%S %Y/%m/%d")
                    me = SOCKET_GETHOSTNAME #socket.gethostname()
                    txt = f"{date} {me} {__version__}"
                    # print("X... timemark requested")
                    self.textbox(txt, pos )

                    if kompr is not None:
                        # jpgkompr
                        self.get_font_params("99")
                        WIDTH = self.text_width
                        xmax = int(self.frame.shape[1] - 0.*self.posx_offs - int(stretchx*WIDTH) )
                        self.textbox( str(kompr), ( xmax,pos[1]) )

                    # RED GREEN CIRCLE:
                    #cirdiam = int(self.fontScale*10) # int(self.fontScale*16)
                    # not really # cirdiam = self.text_height + int(row*stretchy*self.text_height)
                    cirdiam = 1.2*get_f_height()/2
                    cirdiam = round(cirdiam)
                    if NOW.second % 2 == 0:
                        #  fontsize 0.5=> 10   or 0.3 for RPI 320x240
                        cv2.circle( self.frame, (cirdiam,cirdiam), cirdiam, (0,0,255), -1 )
                        # pass
                    else:
                        cv2.circle( self.frame, (cirdiam,cirdiam), cirdiam, (0,255,0), -1 )

                    return
                if col<3:
                    return


            #if row==2:
                #pos[1] = self.posy_offs + int(stretchy*self.text_height)
            if row==2:
                pos[1] = self.frame.shape[0] - int(1.5*self.posy_offs)

        #print(pos)
        bgcolor =  self.RC_COLOR(row,col)
        if grayed: bgcolor = (120,120,120)
        #print( "D... # bgcolor", bgcolor )
        self.textbox(txt, pos , bgcolor= bgcolor , target = frametgt)
        # if txt.find("DM") >= 0:            print(f" .. {txt}  {pos} {bgcolor}  {frametgt}")

    #-------------------------------------------- ENDOF LABELS----------


    def rotate180(self, angle):
        #print(f" rotate {angle}")
        if angle == 0:
            return
        elif angle == 180:
            self.frame = cv2.rotate(self.frame, cv2.ROTATE_180)
        else:
            self.frame = imutils.rotate(self.frame, angle)

    def save_background(self):
        cv2.imwrite( self.BGFILE , self.frame ) # nicely saved
        self.frame_bg = self.frame.copy() # else artifacts remain
        # frame_bg = self.frame.copy()
        # frame_bg2 = cv2.imencode('.jpg', frame_bg)[1].tobytes()
        # save_bg = False

    def save_foreground(self):
        cv2.imwrite( self.FGFILE , self.frame ) # nicely saved
        self.frame_fg = self.frame.copy() # else artifacts remain
        # frame_bg = self.frame.copy()
        # frame_bg2 = cv2.imencode('.jpg', frame_bg)[1].tobytes()
        # save_bg = False

    def subtract(self):
        if self.frame_bg is None:
            if os.path.exists( self.BGFILE ):
                self.frame_bg = cv2.imread( self.BGFILE )
                print("OLD BACKGROUND IMAGE FOUND", self.frame_bg.shape)
            else:
                return
        if self.frame.shape !=  self.frame_bg.shape:
            print("X... cannot substract bg, different shapes...")
            return
        frame1 = cv2.subtract(self.frame , self.frame_bg ) #, mask = frame_mask
        # frame 1 is difference...
        # frame1[:22,:]  = self.frame [:22,:]
        # frame1[-22:,:] = self.frame [-22:,:]
        self.frame = frame1



    def mix(self):
        if self.frame_fg is None:
            if os.path.exists( self.FGFILE ):
                self.frame_fg = cv2.imread( self.FGFILE )
                print("OLD FOREGROUND IMAGE FOUND", self.frame_fg.shape)
            else:
                return
        if self.frame.shape != self.frame_fg.shape:
            print("X... different sizes of the frames")
            return
        frame1 = 0.5*self.frame + 0.5*self.frame_fg
        #*imgs[ random.randint(0,len(imgs)-1) ]

        #frame1 = cv2.subtract(self.frame , self.frame_fg ) #, mask = frame_mask
        # frame 1 is difference...
        # frame1[:22,:]  = self.frame [:22,:]
        # frame1[-22:,:] = self.frame [-22:,:]
        self.frame = frame1



    def reset_camera_start(self):
        self.camera_start = dt.datetime.now()

    def translate(self, speedx = -0.35,  speedy = -0.015 ):
        #print(f"translate {speedx} {speedy}")
        if ( abs(speedx)>1 ) or ( abs(speedy)>1 ):
            self.camera_age = 1
        else:
            self.camera_age = (dt.datetime.now() - self.camera_start ).total_seconds()

        # --- for larger speeds
        dwidth = speedx * self.camera_age  #negative up
        dheight = speedy * self.camera_age  # positive down
        T = np.float32([[1, 0, dwidth], [0, 1, dheight]])
        shifted = cv2.warpAffine(self.frame, T, (self.frame.shape[1], self.frame.shape[0]))
        # print( T )
        self.frame = shifted



    def crosson(self,  dix, diy, color = "g", box_small = True, box_large = False):
        """
        two types  g (just cross, r boxed cross)
        """
        #if color == 'r': crotype = 'line'
        #
        RADIUS=63
        y = int(self.frame.shape[0]/2)
        x = int(self.frame.shape[1]/2)

        ix = x+dix
        iy = y+diy

        if color=="g":
            lcolor=(0,255,55)
        elif (color=="r"):
            lcolor=(55,0,255) #BGR
        else:
            lcolor=(0,255,55)

        crscal = 4
        crnx,crny = int(64/crscal),int(48/crscal)
        #if crotype == "box":
        midskip = crnx
        midskipy = crny
        #else:
        #    midskip = 7
        #    midskipy = 7


        i2=cv2.circle( self.frame, (ix,iy), RADIUS, lcolor, 1)
        i2=cv2.line(i2, (ix-RADIUS+midskip,iy), (ix-midskip,iy), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix+RADIUS-midskip,iy), (ix+midskip,iy), lcolor, thickness=1, lineType=8)

        i2=cv2.line(i2, (ix,iy-RADIUS+midskipy), (ix,iy-midskipy), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix,iy+RADIUS-midskipy), (ix,iy+midskipy), lcolor, thickness=1, lineType=8)

        # mid
        i2=cv2.line(i2, (ix,iy), (ix,iy), lcolor, thickness=1, lineType=8)

        #if crotype == "box":
        if box_small:
            #corners  #  position 0.5deg from 11 deg. OK
            crscal = 4 # normal original box
            crscal = 3.2 # normal original box
            crnx,crny = int(64/crscal),int(48/crscal)

            i2=cv2.line(i2, (ix-crnx,iy-crny), (ix+crnx,iy-crny), lcolor, thickness=1, lineType=8)
            i2=cv2.line(i2, (ix+crnx,iy-crny), (ix+crnx,iy+crny), lcolor, thickness=1, lineType=8)
            i2=cv2.line(i2, (ix+crnx,iy+crny), (ix-crnx,iy+crny), lcolor, thickness=1, lineType=8)
            i2=cv2.line(i2, (ix-crnx,iy+crny), (ix-crnx,iy-crny), lcolor, thickness=1, lineType=8)

        if box_large:
            #corners  #  position 0.5deg from 11 deg. OK
            crscal = 1.4 # normal original box
            crnx,crny = int(64/crscal),int(48/crscal)

            i2=cv2.line(i2, (ix-crnx,iy-crny), (ix+crnx,iy-crny), lcolor, thickness=1 )
            i2=cv2.line(i2, (ix+crnx,iy-crny), (ix+crnx,iy+crny), lcolor, thickness=1 )
            i2=cv2.line(i2, (ix+crnx,iy+crny), (ix-crnx,iy+crny), lcolor, thickness=1 )
            i2=cv2.line(i2, (ix-crnx,iy+crny), (ix-crnx,iy-crny), lcolor, thickness=1 )

        #return self.frame


    #---------- for motion detect i need a second processing line frame2
    # to keep the camera on

    def setblur(self, blur=0, dmblur = 0):
        if (blur>0) and (blur % 2 ==0):
            print("D... wrong gaussian value, incrementing by 1")
            blur+=1
        if blur>0:
            self.frame = cv2.GaussianBlur(self.frame, (blur, blur), 0)
        if (dmblur>0) and (dmblur % 2 ==0):
            dmblur+=1
        # if dmblur>0:
        #     grayB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        #     grayB = cv2.GaussianBlur(grayB, (dmblur, dmblur), 0)


    def setaccum(self, accumulate=0):
        self.accumulate_number = accumulate # info for laps
        if accumulate>1:
            if self.frame.shape == self.averageValue1.shape:
                cv2.accumulateWeighted(self.frame, self.averageValue1, 1/accumulate )
                #self.frame = self.averageValue1 all is white
                self.frame = cv2.convertScaleAbs(self.averageValue1)
        else: # reset
            self.averageValue1 = np.float32(self.frame)



    def chk_threshold(self, threshold=100,  framekind = None):
        """
        preceeded by call to DETMO()
        .
        compare threshold and eventually set DETECTED True
        due to iprint xxx i need to fill a proper frameframekind
        """
        self.motion_detected = False # I reset every test
        motion = False
        self.detect_frame = self.frame.copy() # FOR   -f detect,delta,direct
        self.frame_number+= 1

        #print( self.delta_frame)
        if self.delta_frame is not None:
            # ------------- THIS IS TUNABLE FROM COMMANDLINE/CONFIG
            # it cuts the scene in B-W and determines the MOTION AMOUNT
            #
            thresh = cv2.threshold(self.delta_frame, threshold, 255,
                                cv2.THRESH_BINARY)[1]
            # print(thresh)
            ok = False
            noz = 0 # non zero?
            try:
                noz = cv2.countNonZero(thresh)
                #  I dont use nonzeroes anymore.....
                ok = True
            except:
                ok = False
            if not(ok):
                return

            # ----------------------------------- dilate TRESH
            thresh = cv2.dilate(thresh, None, iterations=3)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            totarea = 0
            largest = cnts # ?? trick later
            largesta = 0
            largest = []
            frame_area = self.delta_frame.shape[0]*self.delta_frame.shape[1]
            for c in cnts:
                dearea = cv2.contourArea(c)
                # print("    search {}".format( dearea ) )
                totarea+=dearea # total over threshold = totarea; X frame_area
                (x, y, w, h) = cv2.boundingRect(c)
                if (y+h<self.text_height*3) or (y>self.delta_frame.shape[0]-self.text_height*3):
                    continue

                # NO YES  DISPLAY green rectangles....
                cv2.rectangle(self.detect_frame, (x,y),(x+w,y+h),(0,255,0),1)  #BGR = greens

                if largesta<dearea:
                    largesta = dearea
                    largest = [c] # cheap trick, one instead of all

            # for c in cnts:
            largesta = int(largesta/frame_area*1000)/10 # recode for late


            # ------------------------------  MOTION FALSE --- AND CALCULATE
            motion = False
            # -----one in the list  for now.... if larger than 0.7 ==> i dont care...
            for c in largest: # THE LIST OF ONE ELEMENT - TRICK!!
                area = cv2.contourArea(c)
                # print("Largest: {}/{}  ... {:.2f}%".format(area, frame_area, area/frame_area*100) )
                # rectangl 1% IS FINE. I pUSH to 0.1%
                AREA_THR_MIN = 0.001
                AREA_THR_MAX = 0.7
                if (area/frame_area < AREA_THR_MIN) or (area/frame_area > AREA_THR_MAX): #minarea 0.5%
                    # go away for any smaller
                    continue
                # what is here means detection
                motion = True
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(self.detect_frame, (x,y),(x+w,y+h),(0,0,255),1)  # BGR
                area=w*h # of the largest box

                #  DM conditions in orange :  area/frame % / noz/frame % / cnts
                #dtext = "{:4.1f}%/{:4.1f}%/{}".format(
                #    area/frame_area*100, noz*100/frame_area, len(cnts) )
                #
                # area of he largest RECT
                #
                # BUT I DONT USE NO-ZEROES
                #dtext = f"{area/frame_area*100:4.1f}%/{noz*100/frame_area:4.1f}%/{len(cnts):2d}"
                dtext = f"{area/frame_area*100:4.1f}%/{len(cnts):2d}"

                # --- all with detection is done here.... detect and delta frames must exist then
                #if framekind is None or framekind == "direct":

                # always print on main
                self.setbox( f"{dtext}", rowcol=self.dm    )
                if framekind == "detect":
                    dtext = f"LARGEST={area/frame_area*100:4.1f}%/ NONZERO={noz*100/frame_area:4.1f}%/CONTOURS={len(cnts):2d}"
                    self.setbox( f"* {dtext}", self.dm , target = "detect" )
                elif framekind == "delta":
                    ## it is BW - it may create a problem in iprint:
                    self.setbox( f"{dtext}", self.dm ,  target = "delta" )
                elif framekind == "histo":
                    if "self.histo_frame" in locals():
                        self.setbox( f"{dtext}", self.dm ,  target = "histo" )


            # all calculation done:
            # NEW MOTION:
            #if (motion) and (not self.motion_detected):
            # AnY Motion
            if motion:
                self.motion_detected_start = dt.datetime.now() # Set New Time
                #print("i... NEW motion detected", self.motion_detected_start, self.frame_number)
            if motion:
                self.motion_detected = True
                #print("i... Motion ON")  # comming here mns already TRUE


            # this IS now the forced recording .....
            if ((dt.datetime.now() - self.motion_detected_start).total_seconds() < self.expire) :
                if self.motion_detected == False:
                    #print(f"i...   {(dt.datetime.now()-self.motion_detected_start).total_seconds():.1f} s/{self.expire}" )
                    proc = (dt.datetime.now() - self.motion_detected_start).total_seconds() / self.expire
                    bar = 13 - int(proc*13)
                    #if not motion:
                    self.setbox( " "*bar, self.dm    )
                self.motion_detected = True
            else:
                # it expired
                pass
                #if motion:
                #    # and no motion is here
                #    self.motion_detected = False

                    #print("i... Motion OFF", self.frame_number)
            #if len(largest)==0: # ----------- if no contour - set OFF
            #    self.motion_detected = False # this kills
                # print("i... Motion OFF", self.frame_number)




    def detmo(self,  dmaccumulate=0, dmblur = 0):
        """
        if there is an accumulation - process it
        if there is NO detection, rewrite the buffer
        """
        if dmaccumulate>1:
            if (dmblur>0) and (dmblur % 2 ==0):
                dmblur+=1


            frame2 = None
            if dmblur==0:
                dmblur=1



            self.accubuffer.append(self.frame)
            while len(self.accubuffer)>dmaccumulate: # i compare against X frames back
                frame2=self.accubuffer.pop(0) # get more time distance

            if not (frame2 is None):
                # create version A
                if dmaccumulate!=0:
                    cv2.accumulateWeighted(frame2, self.averageValue1, 1/dmaccumulate, None)
                else:
                    cv2.accumulateWeighted(frame2, self.averageValue1, 1, None)

                grayA = cv2.cvtColor(cv2.convertScaleAbs(self.averageValue1), cv2.COLOR_BGR2GRAY)
                grayA = cv2.GaussianBlur(grayA, (dmblur, dmblur), 0)

                # create version B
                grayB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                grayB = cv2.GaussianBlur(grayB, (dmblur, dmblur), 0)
                # grayA = cv2.cvtColor(averageValue1, cv2.COLOR_BGR2GRAY)
                #----see the difference
                #frame = cv2.absdiff(grayA, grayB)
                self.delta_frame = cv2.absdiff(grayB, cv2.convertScaleAbs(grayA))
            else:
                print("i... No delta in detection, using frame")
                self.delta_frame = self.frame



# ------------------------------------------------------- HISTO ---------------------------
    def histo_medi(self):
        def find_med( arr ):
            # not transposed!
            bina = 0
            suma = 0
            for i in arr:
                #print(i)
                bina+=1
                suma+=i
                #print(suma)
                if suma>0.5:
                    return bina
            return len(arr)

        BINS = 256 # 128
        #bins = np.arange(BINS)
        bins = np.arange(BINS).reshape(1,BINS)
        framegray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # images; channels; mask none; histSize [BINS]
        hist_gray = cv2.calcHist([framegray], [0], None, [BINS], [0, 256])

        #hist_gray = np.transpose( hist_gray) # array
        sumhist = hist_gray.sum()
        hist_gray = hist_gray/sumhist
        sumhist = hist_gray.sum()

        #print(hist_gray)
        #print(sumhist)
        med = np.median( hist_gray )
        med2= find_med( hist_gray)
        #print( f" sum = {sumhist:6.1f}    med={med:.5f}  bin={med2}" )
        return med2

        # cv2.normalize(hist_gray,hist_gray,0,255,cv2.NORM_MINMAX)
        #med =
        black = (hist_gray[0] + hist_gray[1] )/2 #1st two bins
        white = (hist_gray[-1]+hist_gray[-2] )/2 #last 2 bins

        mean = np.dot( bins, hist_gray )
        #print("MEAN",mean)
        mean = round(100*mean[0][0]/sumhist/BINS) # min is bin 1, max is bin BINS.

        # print(f"   {len(hist_gray)}  {hist_gray[0]}..{hist_gray[-1]}  sum={sumhist}  med={med},  mean={mean}  ")

        #print("MEAN",mean)
        #print( "LEN TYPE", len(mean),type(mean) )
        BW = ""
        if white>100: BW=BW+"W"
        elif white>0: BW=BW+"w"

        if black>100: BW=BW+"B"
        elif black>0: BW=BW+"b"

        #return mean
        return f"*{mean:.0f}{BW}"  #/255*100


    def histo_mean(self):

        BINS = 128
        #bins = np.arange(BINS)
        bins = np.arange(BINS).reshape(1,BINS)

        framegray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # images; channels; mask none; histSize [BINS]
        hist_gray = cv2.calcHist([framegray], [0], None, [BINS], [0, 256])
        # cv2.normalize(hist_gray,hist_gray,0,255,cv2.NORM_MINMAX)

        #hist_gray = hist_gray/hist_gray.max() # norm 1
        #mean = 1

        #print(f"i... mimax mean  {hist_gray.min():4.1f},  {hist_gray.max():4.1f}, {hist_gray.mean():4.1f} ... {mean}" )
        #print( hist_gray[:9],  bins[:9]  , len(hist_gray), len(bins) , type(hist_gray), type(bins) )

        # strange problem WITH 046d:080f  Webcam C120
        #print(f"hg                     binslen={len(bins)}=1; BINS={BINS}  lenHG={len(hist_gray)}")
        sumhist = hist_gray.sum()
        #print(f"hg                     sumhist = {sumhist} all the same!")


        black = (hist_gray[0] + hist_gray[1] )/2
        white = (hist_gray[-1]+hist_gray[-2] )/2

        #print(f"hg              {max(hist_gray)} - {min(hist_gray)} wh{white} blk2{black}")
        #if sumhist<1:
        #    return 100 # I DONT KNOW WHAT IS THIS
        mean = np.dot( bins, hist_gray )
        #print("MEAN",mean)
        mean = round(100*mean[0][0]/sumhist/BINS) # min is bin 1, max is bin BINS.
        #print("MEAN",mean)
        #print( "LEN TYPE", len(mean),type(mean) )

        #cv2.normalize(hist_gray,hist_gray)
        #mean = hist_gray.mean()/BINS #/len(hist_gray)
        ###mean = mean.mean()/BINS
        # mean = hist_gray.mean() #/len(hist_gray)
        # min1 = hist_gray.min()
        # max1 = hist_gray.max() #/len(hist_gray)
        #print(f"i... .flattened gray    {mean}")
        #  {min1:.1f} {max1:.1f}

        BW = ""
        if white>100: BW=BW+"W"
        elif white>0: BW=BW+"w"

        if black>100: BW=BW+"B"
        elif black>0: BW=BW+"b"

        return mean
        return f"{mean:.0f}{BW}"  #/255*100




    def zoom(self, scale, x=None,y=None):
        #scale = zoom
        #get the webcam size

        if len(self.frame.shape)==3:
            height, width, channels = self.frame.shape
        else:
            height, width = self.frame.shape
        #prepare the crop
        centerX = int(height/2)
        centerY = int(width/2)

        #if not x is None:
        #    centerX+= x
        #if not y is None:
        #    centerY+= y
        if (x!=None) or (y!=None):
            dwidth = -x    #negative up
            dheight = -y   # positive down
            T = np.float32([[1, 0, dwidth], [0, 1, dheight]])
            self.frame = cv2.warpAffine(self.frame, T, (self.frame.shape[1], self.frame.shape[0]))

        # return
        radiusX,radiusY= int(height/2/scale),int(width/2/scale)

        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY
        #minX=max(minX,0)
        #minY=max(minY,0)
        #maxX=min(maxX,height)
        #maxY=min(maxY,width)

        #print(" cut x=",minX,maxX, "  and y=",minY,maxY )
        cropped = self.frame[minX:maxX, minY:maxY]
        #print("CENTER:",centerX, centerY,"#",  cropped.shape, scale,"x")
        self.frame = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_NEAREST)


    def histo(self):

        h = self.frame.copy()
        BINS = 128
        bins = np.arange(BINS).reshape(BINS,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]

        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([self.frame],[ch],None,[BINS],[0,255])
            #cv2.normalize(hist_item,hist_item, 0, 255, cv2.NORM_MINMAX)
            hist_item = hist_item/hist_item.max()*255
            hist=np.int32(np.around(hist_item))
            pts = np.column_stack((bins*int(640/BINS),475-(hist*440/255).astype(int)))
            cv2.polylines(h,[pts],False,col)

        framegray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([framegray], [0], None, [BINS], [0, 255])
        #cv2.normalize(hist_gray,hist_gray,0,255,cv2.NORM_MINMAX)
        hist_gray = hist_gray/hist_gray.max()*255

        hist=np.int32(np.around(hist_gray))
        pts = np.column_stack((bins*int(640/BINS),475-(hist*440/255).astype(int)))
        cv2.polylines(h,[pts], False,  [255,255,255], thickness= 2 )

        self.histo_frame = h


    def zmqsender_send_image(self):
        """
        just send, but catch exception....
        """
        try:
            self.zmqsender.send_image( self.zmqrpi_name, self.frame )
            print(f"i... zmq was sent to {self.zmqtarget}")
        except:
            print(f"i... zmq NOT sent to {self.zmqtarget}")
            self.zmqsender = None
        return


    def telegram_send_image(self, blocking = True):
        """
        send telegram from here... be sure:no flooding
        """
        # telegram
        TELEGRAMBLOCK = 300 # seconds
        if self.jtelegram and (os.path.exists(os.path.expanduser("~/.telegram.token"))):
            telegramnow = dt.datetime.now()
            # 5 minutes
            # protection against flooding
            if blocking==False or  (telegramnow-self.telegramlast).total_seconds()>TELEGRAMBLOCK:
                print(f"fCAMERA {self.zmqrpi_name} ")
                print(f"fCAMERA {self.zmqrpi_name} {telegramnow.strftime('%a %H:%M:%S')}")
                y = threading.Thread(target=telegram.bot_send, args=("ALERT", f"CAMERA {self.zmqrpi_name} {telegramnow.strftime('%a %H:%M:%S')}", self.frame))
                y.start()
                print("i.. telegram SENT============")
                self.telegramlast=telegramnow
            else:
                print(f"i.. telegram not allowed due to block-time ({TELEGRAMBLOCK} s); now=", (telegramnow-self.telegramlast).total_seconds())
        #else:
        #    print(f"X...  jtele=={self.jtelegram}, token")
        return




    #--- what happens if not 640x480 and xvid?  XVID....too lossy compression
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # https://learn.microsoft.com/en-us/windows/win32/medfound/video-fourccs
    #
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')  # NOT a QUALITY
    # fourcc = cv2.VideoWriter_fourcc(*'IYUV')  # SHOULD BE HUGE....
    #
    # --------------------------------------------------------save avi ------------
    # ------------------------------------------------- also ZMQ and TELEGRAM
    def save_avi_close_laps(self):
        # was aviout - CALLED FROM real_cam
        self.skwriter_laps.close()
        self.skwriter_laps = None
        print(f"i... {bg.red}LAPS skwriter  Closed{bg.default}")

    def save_avi_close_dm(self):
        # itis new but shouldwas aviout - CALLED HERE
        if self.skwriter_detm is not None:
            self.skwriter_detm.close()
        self.skwriter_detm = None
        print(f"i... {bg.red}DetMo skwriter  Closed{bg.default}")

    def assure_DATA(self):
        """
        just do the same as in uniwrec, check+create data dir
        """
        dir2create = os.path.expanduser("~/DATA/")
        if not os.path.isdir(os.path.expanduser(dir2create)):
            print(
                f"D... trying to create directory {dir2create} for saving"
            )
            # result = False
            os.mkdir(os.path.expanduser(dir2create))

    def save_avi(self, seconds =  1, name = "" ,  basecamera_string= None ,
                 mycodec = "DIVX", frnum= -1,
                 container = "avi",
                 TIMEOUT_NEWFILE = 3600,
                 fps = 10.1):
        """
        seconds>0 for TIMELAPS  ;   0.001 intentional for every frame
         0 just return
        -1 with name="dm" for detectmotion
        frnum .. if >0 and seconds <0.1 => omit may omit accumulated
         ...
        https://gist.github.com/docPhil99/a612c355cd31e69a0d3a6d2f87bfde8b
        https://trac.ffmpeg.org/wiki/Encode/H.264
        """
        #print("i... save_avi", seconds, name)
        # -------------- one shot



        if seconds == 0:
            #
            # NO SAVING
            #
            return
        elif seconds == -1: # <0 [ -1 now] means saving avi - motion detect or in uni...*******
            #
            #
            #  NEGATIVE :  means saving all ......
            #     -  USED  FOR DETECTION  ...
            #

            WH = (self.frame.shape[1],self.frame.shape[0])

            avi_age = (dt.datetime.now()-self.avi_started).total_seconds()
            if not self.aviopened or avi_age>TIMEOUT_NEWFILE:
                me = SOCKET_GETHOSTNAME # socket.gethostname()
                filename = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                self.assure_DATA()
                filename = os.path.expanduser("~/DATA/"+f"{me}{name}_{filename}_{str(config.CONFIG['netport'])}_{mycodec}.{container}")
                for i in range(3):
                    print(f"i... {bg.green}LAPS<0:{filename}{bg.default}")
                if (dt.datetime.now()-self.avi_started).total_seconds()>TIMEOUT_NEWFILE:
                    print("i... RELEASING VIDEOFILE ..... EVERY sec.==", TIMEOUT_NEWFILE)
                    self.save_avi_close_dm()
                    #if self.aviout is not None:
                        #self.aviout.release()
                    time.sleep(0.5)
                    print("i... RELEASING VIDEOFILE ..... EVERY sec.==", TIMEOUT_NEWFILE)
                    self.avi_started = dt.datetime.now()
                #
                #
                fourcc = cv2.VideoWriter_fourcc(*mycodec)  #
                # I_BLOCK_NOW# self.aviout = cv2.VideoWriter( filename , fourcc , fps, WH )


                if not self.skwriter_detm:#
                    fnama = filename #f"{filename}.mp4"
                    print(f"i... SAVING with ffmpeg TO: {fnama}")
                    self.skwriter_detm = skvideo.io.FFmpegWriter( fnama,  outputdict={
                        '-vcodec': 'libx264',  #use the h.264 codec
                        '-crf': '12',           # quality: 0 lossless,+6 halfqual; 51 worse
                        '-tune':'zerolatency', # lowers deblocking hq movie
    #                    '-movflags': '',
    #                    '+faststart':'',
                        '-preset':'slow'   #the slower the better compression,
                        #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
                    })
                    #
                #self.skwriter_detm.writeFrame(self.frame)#[:,:,::-1])  #write the frame as RGB not BGR


                # #
                # self.skwriter = skvideo.io.FFmpegWriter( f"{filename}.mp4",  outputdict={
                #     '-vcodec': 'libx264',  #use the h.264 codec
                #     '-crf': '0',           #set the constant rate factor to 0, which is lossless
                #     '-preset':'veryslow'   #the slower the better compression, in princple, try
                #     #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
                # })
                # #
                self.save_avi_counter = 0 # count saved frames
                self.aviopened = True
                for i in range(3): # doesnt help much to create a file
                    #print(".", flush=True, end="")
                    #if self.aviout is not None:
                    if self.skwriter_detm is not None:
                        #self.aviout.write(self.frame)
                        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                        self.skwriter_detm.writeFrame(rgb_frame)#self.frame)
                    #self.skwriter.writeFrame(self.frame[:,:,::-1])  #write the frame as RGB not BGR


            # ---- repeat the (later) printout
            if basecamera_string is not None:
                overtext=basecamera_string
            else:
                overtext = ";"
            overtext = f"D {self.save_avi_counter:07d} / {overtext}"
            #overtext = ' '.join(overtext[i:i+1] for i in range(0, len(overtext), 1))
            position = ( 460, self.frame.shape[0]-1 ) # 480 on x-axis
            self.frame = iprint(self.frame, str(overtext), font="di",
                            position=position,color_rgb=(0,255,0) )

            #if self.aviout is not None:
            if self.skwriter_detm is not None:
                #self.aviout.write(self.frame)
                rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.skwriter_detm.writeFrame(rgb_frame)#self.frame)
            #self.skwriter.writeFrame(self.frame[:,:,::-1])  #write the frame as RGB not BGR
            self.save_avi_counter+=1 # count saved frames

            #
            # If telegram => check the tripwire (time block)
            #
            if self.jtelegram and type(self.telegramtrigger)==bool:
                self.telegramtrigger = dt.datetime.now()+dt.timedelta(seconds=self.telegram_tripwire) # TRIPWIRE 2 seconds
                print("i... telegramtrigger preset to +2 sec.",self.telegramtrigger.strftime("%H:%M:%S"))
            # MOMENT WHEN AVI IS SAVED===========> imagezmq, telegram...

            #
            # If ZMQ is initialized
            #
            if  (self.zmqsender is None) and not (self.zmqtarget is None):
                print(self.zmqsender,self.zmqtarget," INITIALIZING",f'tcp://{self.zmqtarget}:5555')

                self.zmqsender = imagezmq.ImageSender(connect_to=f'tcp://{self.zmqtarget}:5555')
                self.zmqsender.zmq_socket.setsockopt(zmq.LINGER, 0)  # prevents ZMQ hang on exit
                # NOTE: because of the way PyZMQ and imageZMQ are implemented, the
                #       timeout values specified must be integer constants, not variables.
                #       The timeout value is in milliseconds, e.g., 2000 = 2 seconds.
                self.zmqsender.zmq_socket.setsockopt(zmq.RCVTIMEO, 2000)  # set a receive timeout
                self.zmqsender.zmq_socket.setsockopt(zmq.SNDTIMEO, 2000)  # set a send timeout




            # if zmqtarget IP address is given:
            if not(self.zmqtarget is None) and not(self.zmqsender is None):
                #print(self.zmqsender,self.zmqtarget," action")
                zmqnow = dt.datetime.now()


                # imagezmq
                if (zmqnow-self.zmqlast).total_seconds()>1.5:
                    #x = threading.Thread(target=self.zmqsender.send_image, args=(self.zmqrpi_name, self.frame))
                    x = threading.Thread(target=self.zmqsender_send_image ) # i will try to catch exceptions...
                    x.start()
                    #self.zmqsender.send_image(self.zmqrpi_name, self.frame)
                    self.zmqlast=zmqnow



        elif seconds>0:
            #
            # POSITIVE ....  used for LAPS and  ASTRO too
            # -------------- timelapse if seconds>0: ******************************* MKV FOR LOOP
            #
            # ..0.01 means EVERY FRAME .. seconds is in principle different from 'timelapse' value
            #
            WH = (self.frame.shape[1],self.frame.shape[0])

            me = SOCKET_GETHOSTNAME # socket.gethostname()
            filename = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            fseconds = int(seconds)
            self.assure_DATA()
            filename = os.path.expanduser("~/DATA/"+ f"{me}_laps{fseconds:04d}_{filename}_{str(config.CONFIG['netport'])}_{mycodec}.{container}" )

            if not self.aviopened_laps:
                #
                # AVI OPENED made True now
                #
                for i in range(1):
                    print(f"i...{bg.green}LAPS>0:{filename}{bg.default}")
                self.save_avi_counter = 0 # count saved frames

                fourcc = cv2.VideoWriter_fourcc(*mycodec)  #
                # I_BLOCK_NOW# self.aviout_laps = cv2.VideoWriter( filename , fourcc , fps, WH  )
                #  10x larger size of ffmpeg mp4

                self.aviopened_laps = True
                # self.avi_last = dt.datetime.now()


            if (dt.datetime.now()-self.avi_last).total_seconds() > seconds:
                # ... second can be 0.001 too ... we pay attention to averaging then
                #      self.accumulate_number = accumulate # info for laps
                #
                # I would like to encode time
                #   DETAILED FONT NO ATIALIAS
                #  ls  -trh | tail -1 | xargs mpv --screenshot-format=png
                #   https://www.dafont.com/small-pixel.font?text=digital
                #
                if seconds<0.1 and  self.accumulate_number>1 and frnum>0:
                    if frnum % self.accumulate_number  != 0:
                        # print(f" NOSAVE    {self.accumulate_number} {frnum}        ")
                        # do not record when accumu
                        return

                self.save_avi_counter+=1

                # # pixel typing
                # for i in range(300,300+ self.save_avi_counter):
                #     self.frame[100,i]=[255,255,255]
                if basecamera_string is not None:
                    overtext=basecamera_string
                    overtext = f"L {self.save_avi_counter:07d} / {overtext}"
                    #overtext = ' '.join(overtext[i:i+1] for i in range(0, len(overtext), 1))
                    #drtext =  str(overtext) # to be sure
                    position = ( 460, self.frame.shape[0]-9 ) # 480 on x-axis
                    self.frame = iprint(self.frame, str(overtext), font="di",
                                   position=position,color_rgb=(0,255,0) )

                # I_BLOCK_NOW# self.aviout_laps.write(self.frame)
                #  10x larger size of ffmpeg mp4

                if not self.skwriter_laps:#
                    fnama = filename #f"{filename}.mp4"
                    print(f"i... SAVING with ffmpeg TO: {fnama}")
                    self.skwriter_laps = skvideo.io.FFmpegWriter( fnama,  outputdict={
                        '-vcodec': 'libx264',  #use the h.264 codec
                        '-crf': '0',           #set the constant rate factor to 0, which is lossless
                        '-tune':'stillimage', #
    #                    '-movflags': '',
    #                    '+faststart':'',
                        '-preset':'veryslow'   #the slower the better compression, in princple, try
                        #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
                    })
                    #
                rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.skwriter_laps.writeFrame(rgb_frame)#self.frame)#[:,:,::-1])  #write the frame as RGB not BGR

                self.avi_last = dt.datetime.now()
                #@{dt.datetime.now().strftime('%H:%M:%S.%f')[:-4]}
                print(f"i... saving timelaps  #{self.save_avi_counter:07d}   [ {basecamera_string} ]" )





#===============================================================
if __name__=="__main__":
    es1 = Stream_Enhancer()
    #if not(es1.add_frame_from_cam()):
    es1.add_frame_from_cam()
    # es1.show_frame()

    print("DD..... RUNALl")
    for i in range(1000):
        for row in range(4): # max 3 rows
            for col in range(6): # 5 columns @ 480 max
                es1.setbox("_Row{}COL{}_".format(row,col), (row,col) )
        for row in range(16): # 5 columns @ 480 max
            es1.setbox("{}COL{}_".format(row,col), (row,col), "left")
        for row in range(16): # 5 columns @ 480 max
            es1.setbox("{}COL{}_".format(row,col), (row,col), "right")

        es1.setbox("MODE avg ",es1.MODE)
        es1.setbox("DISP laps ",es1.DISP)

        es1.setbox("avg = 1 ",es1.avg)
        es1.setbox("blr = 0 ",es1.blr)

        es1.blimp_frame()
