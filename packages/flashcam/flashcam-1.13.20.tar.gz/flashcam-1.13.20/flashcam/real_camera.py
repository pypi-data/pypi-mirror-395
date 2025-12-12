# FOR CONNECTION TO FLASHCAM AND NOTIFATOR - SEE FLASHCAM README.org
#   astro 1st;  dm+laps very last...
from console import fg,bg
import importlib
ROOTimported = False
s9009 = None
histogram_v = None
histogram_h = None
try:
    importlib.import_module( "ROOT" )
    ROOTimported = True
    globals()["ROOT"] = importlib.import_module( "ROOT" )
    print(f"i... {fg.green} ROOT     IMPORTED {fg.default}")
except ImportError:
    print(f"i... {fg.red} ROOT NOT IMPORTED {fg.default}")
# finally:
#     print("I... importing",i) # check if fire is imported
#     globals()[i] = importlib.import_module( importnames[i] )
#     print("I... imported:",i)

#import ROOT

import random
import cv2
from flashcam.base_camera2 import BaseCamera

from flashcam.usbcheck import recommend_video
from flashcam.v4lc import  get_resolutions
# import base_camera  #  Switches: slowrate....

import datetime as dt
import time
import socket

import glob

import subprocess as sp
import numpy as np

import flashcam.config as config

from  flashcam.stream_enhancer import Stream_Enhancer

from flashcam import v4lc
from flashcam.v4lc import set_gem, get_gem, tune_histo

from flashcam.mmapwr import mmread_n_clear, mmread

import os
import sys

from notifator import telegram
import threading

from PIL import ImageFont, ImageDraw, Image

from console import fg,bg
import socket

from flashcam.text_write import iprint,fonts_available,\
    get_f_height, get_f_width, get_def_font,\
    dial, signal_strength, text_box, tacho, \
    get_color_based_on_brightness, \
    MSG_FONT

# also in stream_enhancer??!!
SOCKET_GETHOSTNAME =socket.gethostname()

#try:
#    import pyautogui # take screenshot
#except:
#    print("X... no DISPLAY, pyautogui cannot be used")
# -----------------------------------------------------------------


from flashcam import mmapwr

# -------------------- mqtt IMPORT set
import struct
import paho.mqtt.client as mqtt
import numpy as np
import datetime as dt
import time
# -------------------- mqtt IMPORT set


current_ip = None



gaint, expot, gammat = None, None, None # One shot, almost always None
gaintv, expotv, gammatv = None, None, None # remember some values...



def create_mqtt_payload(image, framenumber, timestamp, recording_started, exposition, gain, gamma):
    height, width = image.shape[:2]
    header = struct.pack(
        '!HHQddIfff',
        width,
        height,
        int(framenumber),
        timestamp.timestamp(),
        recording_started.timestamp(),
        0,  # padding for alignment if needed
        float(exposition),
        float(gain),
        float(gamma)
    )
    #print( float(exposition) )
    payload = header + image.tobytes()
    return payload







def shot():
    """
    screenshot works on wayland
    """
    # Use gnome-screenshot to take a screenshot and save it to a file
    sp.run(['gnome-screenshot', '-f', '/tmp/screenshot.png'])
    image = Image.open('/tmp/screenshot.png')
    return image




def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n) # 0.0
        int_n = int(float_n) #0.0
    except ValueError:
        return False
    else:
        return float_n == int_n

def is_float(n):
    if n is None:return False
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True

def is_bool(n):
    if type(n) is str and n=="False": return True
    if type(n) is str and n=="True": return True
    return False



# -----------------------------------------------------------------

def get_ip( myip ):
    global current_ip
    if current_ip is None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            current_ip = s.getsockname()[0]
            ### current_ip = SOCKET_GETHOSTNAME
            s.close()
        except:
            current_ip = "no network"
            print("X... Network is unreachable ...  no network?")
    return current_ip

def leftmost_txt_wid( txt ):
    minx = int(640/2)
    lines = str(txt)
    if lines.find("\n")<0:
        lines = [txt]
    else:
        lines = lines.split("\n")
    for i in lines:
        posx = int(640/2 - len( str(i) )*32/2)
        if posx<minx:
            minx = posx
    return minx


def force_center_text( frame, overtext , posy = 400, fg_bgr = (0,255,0) , fosize = 2*32):
    """
    7segment LCD text in the middle is a good example
    siglost, nocamera, overtext, baduser....
    """
    FONT = "utfh"
    midl = 320
    midl = midl - len(str(overtext))*get_f_width(FONT)//2 # center
    frame = iprint( frame, drtext=str(overtext), font=FONT, position=(midl,posy), color_rgb=fg_bgr)
    return frame

# -----------------------------------------------------------------


class widget:
    """
    Every start, for 1 second the widgets will light up
    ^ connectors is corresponding UNO shield with 6 plugs
    Also see creation of widgets.....
    """
    def __init__(self,connector=1, typ = "signal", pos = (580,60), timeout=1, adaptive_position=True, radius=None):
        self.connector = int(connector)

        if self.connector == 1: self.inputi = config.CONFIG['mminput1']
        elif self.connector == 2: self.inputi = config.CONFIG['mminput2']
        elif self.connector == 3: self.inputi = config.CONFIG['mminput3']
        elif self.connector == 4: self.inputi = config.CONFIG['mminput4']
        elif self.connector == 5: self.inputi = config.CONFIG['mminput5']
        elif self.connector == 6: self.inputi = config.CONFIG['mminput6']
        # or a seconds batch of connectors for a different port like 5000
        elif self.connector == 11: self.inputi = config.CONFIG['mminput11']
        elif self.connector == 12: self.inputi = config.CONFIG['mminput12']
        elif self.connector == 13: self.inputi = config.CONFIG['mminput13']
        elif self.connector == 14: self.inputi = config.CONFIG['mminput14']
        elif self.connector == 15: self.inputi = config.CONFIG['mminput15']
        elif self.connector == 16: self.inputi = config.CONFIG['mminput16']
        else:
            print("X... nonexisting widget connector", connector)
            sys.exit(1)

        self.title = "ooo"
        self.inputi = os.path.expanduser( self.inputi )
        self.typ = typ
        self.position = pos
        self.timeout = timeout # default timeout==1 sec
        self.last = dt.datetime.now()
        self.value0100 = 50
        self.value = 12.3
        self.raw = "test1 mA,test2 uSv"
        #if typ != "sub":
        self.adaptive_position = adaptive_position
        if radius is None:
            self.default_radius = 30
        else:
            self.default_radius = radius
        #else:
        #    self.adaptive_position = False
        #
        # I try to put extra DATA mmap file here
        #
        PORT = mmapwr.mmcreate( self.inputi, add_port=True) # Create Really what you are asked



    def refresh(self):
        """
        read adn interpret values
        value;min;max;
        """
        input1,input1ext = mmread_n_clear( self.inputi ) # this will be a string fron cfg, but :no reference here
        input1 = input1.strip()

        if (input1 is not None) and (type(input1) == str) and (input1 in ['signal', 'dial', 'box', 'sub', 'tacho']):
            self.last = dt.datetime.now() # refresh
            print(">",input1, "Exteded==", input1ext)

            self.typ = input1

            res = input1ext.split(";")
            self.raw = res[0].strip()  # table text box split ,comma,

            print(res)
            if is_int(res[0]):
                self.value = float(res[0]) # BUG HERE???? 0.0 is int!?
            elif is_float(res[0]):
                self.value = float(res[0]) #
            else:
                self.value = res[0]
            print("D... self.value == ", self.value, "  raw=", self.raw )

            self.value0100 = 50
            if (len(res)>2) and (type(self.value) == int ) or (type(self.value) == float):
                mini,maxi=0,100
                if is_float(res[1]): mini = float(res[1]) #
                if is_float(res[2]): maxi = float(res[2]) #
                if mini<maxi:
                    self.value0100 = (self.value-mini)/(maxi-mini)*100
                if self.value0100<0: self.value0100=0
                if self.value0100>100: self.value0100=100

            if len(res)>3: # timeout
                timo = self.timeout
                if is_float(res[3]): timo = float(res[3])
                if (timo>0.8) and (timo <= 99999): # between 1 sec and 1 hour
                    self.timeout = timo
                    #print("X... changing  timeout (1-3600sec)", timo)
                else:
                    print(f"X... {fg.red}uneligible timeout (1-3600sec):  {timo} {type(timo)} {fg.default} ")

            if len(res)>4: # title
                self.title = str(res[4])


           #print(self.value)

    def is_active(self):
        delta = (dt.datetime.now()-self.last).total_seconds()
        #print(self.connector, delta )
        if delta<self.timeout:
            return True
        else:
            return False


    def display(self, frame ):
        cposition = list(self.position)
        radius = 30 # Guess - not systematic
        #
        # all but sub are mofed to right side
        #
        if self.adaptive_position and self.typ != "sub":
            cposition[0] = frame.shape[1] - radius * 2
        if self.adaptive_position and self.typ == "sub":
            cposition[1] = frame.shape[0] - radius

        left_up_point = (cposition[0] - radius, cposition[1] - radius)
        right_down_point = (cposition[0] + radius, cposition[1] + radius)
        dcolor = get_color_based_on_brightness( frame, left_up_point , right_down_point)
        #if self.is_active():
        if self.typ == "signal":  # size ==50xxx NEWLY radius = 30
            frame = signal_strength( frame, position=cposition , percentage= self.value0100 , value=self.value, color=dcolor, title=self.title, radius=self.default_radius)
        if self.typ == "dial": # radius = 30
            frame = dial( frame, position=cposition , percentage= self.value0100 , value=self.value , color=dcolor, title=self.title, radius=self.default_radius)
        if self.typ == "tacho": #radius = 30
            frame = tacho( frame, position=cposition , percentage= self.value0100 , value=self.value , color=dcolor, title=self.title, radius=self.default_radius)
        if self.typ == "box": # nothing like size
            frame = text_box( frame, position=cposition , title = self.title  , values = str(self.value).replace(",","\n") , color=dcolor)
        if self.typ == "sub": # just Brutal Iprint
            #print("D... STARTING SUB PRINT")
            frame = iprint( frame, f"{self.title}: {self.value}" , MSG_FONT,
                            position=cposition,color_rgb=dcolor)
        return frame



# -----------------------------------------------------------------

my_speed_last = dt.datetime.now()
my_speed_now = dt.datetime.now()

# -------------------------  this is refered as global
mqtt_broker = "127.0.0.1"
##### print(f"XYZ.... {config.CONFIG['netport']}")
mqtt_topic = "image/raw8000" # I will change later
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, 1883, 10)
mqtt_started = dt.datetime.now()

class Camera(BaseCamera):

    # video_source = 0
    histomean = 50
    #nfrm = 0 # number frame.... nonono
    # capdevice = None # global

    # CAINI 0
    @staticmethod
    def init_cam(  ):
        """
        should return videocapture device
        but also sould set Camerare.video_source
        """
        global s9009, histogram_v, histogram_h
        #  - all is taken from BaseCam
        # res = "640x480"
        res = config.CONFIG["resolution"]


        print("i... init _ cam caleld with prod:",  config.CONFIG["product"] )

        # here, I need to  wait until the correct video is reported.... ????
        #
        #### HACK ===
        vids = recommend_video( config.CONFIG["product"] , slow_track = False ) # if jpg => give -1
        # with  jpg or clock  IMMEDIATELY returns [-1]
        #
        # if error is lsusb=>>> return [-1] ??????? or [] ???? test it NONONOO
        #

        if len(vids)>0:
            if vids[0]==-1:
                print(f"D... returns jpg:   {config.CONFIG['product']}")  # end immediatelly back
                config.generic_bg_image = None # TRIP WIRE!!!!
                #
                # # NOT DEF camera_or_image( cap, vidnum) # I tried to add this to enable again beam swirtch
                # config.fullpath_bg_fixed_image = f"{os.path.dirname(config.CONFIG['filename'])}/{config.CONFIG['product']}"
                # config.fullpath_bg_fixed_image = os.path.expanduser( config.fullpath_bg_fixed_image)
                # # debug print( cap, vidnum)
                # if not os.path.exists(config.fullpath_bg_fixed_image):
                #     print("X...  config.fullpath_bg_fixed_image  doesnt exist")
                #     config.fullpath_bg_fixed_image = None
                # print(config.fullpath_bg_fixed_image)
                return config.CONFIG["product"] , -1, None

            vidnum = vids[0]
            print("D... asking VideoCapture", vidnum, dt.datetime.now() )
            #
            #  00.0-usb-0:1.3:1.0   00.0-usb-0:1.1:1.0
            #  00.0-usb-0:1.4:1.0   00.0-usb-0:1.2:1.0
            #
            #
            cap = cv2.VideoCapture(vidnum,  cv2.CAP_V4L2)
            #cap = cv2.VideoCapture(vidnum )
            ### cap = cv2.VideoCapture(vidnum,  cv2.CAP_DSHOW) ## ??? ## https://stackoverflow.com/questions/59371075/opencv-error-cant-open-camera-through-video-capture#61817613
            print("D... got    VideoCapture", vidnum , dt.datetime.now())

            # config.CONFIG["camera_on"] = True

            # - with C270 - it showed corrupt jpeg
            # - it allowed to use try: except: and not stuck@!!!
            #cap = cv2.VideoCapture(vidnum)
            #   70% stucks even with timeout


            #pixelformat = "MJPG"

            pixelformat = "YUYV" # I use lossless format for camera readout
            pixelformat = config.CONFIG['PIXELFORMAT']

            time.sleep(0.6)
            fourcc = cv2.VideoWriter_fourcc(*pixelformat) # for capture device
            print("i... fourcc ", fourcc)
            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            time.sleep(0.6)
            print("i... buffersize 1")
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            time.sleep(0.6)

            w,h =  int(res.split("x")[0]), int(res.split("x")[1])
            print(f"i... {fg.green}   RESOLUTIONwh= {w} x {h}, PIXELFORMAT {pixelformat}  {fg.default}")
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,   w )
            time.sleep(0.5)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  h )
            print(f"i... {fg.green}   RESOLUTIONwh= {w} x {h}, PIXELFORMAT {pixelformat}  {fg.default}")

            if ROOTimported and s9009 is None:
                print(f"i... {fg.yellow} ------------------------------ server register {fg.default}")
                histogram_h = ROOT.TH1F("hhtest","hhtest",640,0,640)
                histogram_v = ROOT.TH1F("hvtest","hvtest",480,0,480)
                # serv = ROOT.THttpServer("http:9009?loopback")
                serv = ROOT.THttpServer("http:9009")
                serv.Register("/",histogram_h)
                serv.Register("/",histogram_v)
                serv.SetItemField("/", "_monitoring", "1000")
                serv.SetItemField("/", "_layout", "vert2")
                serv.SetItemField("/", "_drawitem", "[hvtest,hhtest]")


                s9009 = serv
            else:
                serv = None
            return cap,vidnum, serv
        else:
            # returned [] : product not found or a crash in usbls...rpi4b 2 cams
            time.sleep(1)
        return None, None, None

    # ================================================================================
    #  ----------- ACQUIRE ONE FRAME ----------
    # --------------------------------------------------------------------------------

    @staticmethod
    def acquire_one_frame(cap):
        global             my_speed_last, my_speed_now, mqtt_client, mqtt_topic, mqtt_started # CLIENT
        global expotv, gaintv, gammatv
        # put propoer port
        mqtt_topic = mqtt_topic.replace("8000", str(config.CONFIG['netport']))
        frame = None
        ret = True #  I change it later
        # capture_time=""
        #print("i...acq_onef: cap==", cap)
        if type(cap) == tuple:
            print("i... TUPLE    cap==", cap, "  --->[0]")
            cap = cap[0] # THIS IS STRANGE FOR newcam20211117
            print(f"i... TUPLE[0] cap== {cap}  type==  {type(cap)}   --- redefined cap" )
        if (cap is None):
            print("X... cap is None")
            ret = False
        else:
            if  (type(cap) != str) and (not cap.isOpened()):
                print("X... 1st attempt camera  not Opened(@real_cam aof)")
                time.sleep(0.7)
            if  (type(cap) != str) and (not cap.isOpened()):
                print("X... 2nd attempt camera  not Opened(@real_cam aof)")
            #
            # ################# I DONT KNOW BUT REMOVING THIS HELPED ON SLOW RPI3B.. RECONSIDER
            #
            #ret = False
        if type(cap) == str:
            print("X...  type cap == str == {type(cap)}   - : False")
            ret = False
        if ret:
            my_speed_last = my_speed_now
            my_speed_now = dt.datetime.now()
            totsecpf= (my_speed_now - my_speed_last).total_seconds()
            print(f"i... frame {BaseCamera.nframes:8d}  {BaseCamera.capture_time}   {1/totsecpf:4.0f} fps  ", end="\r" )

            try:
                ret, frame = cap.read()
            except  e :
                print("X... ", type(e))
                print("X... ", e )
            try: #----this catches errors of libjpeg with cv2.CAP_V4L2
                # ret is frequently false on RPI3.... I give 2 more chances
                #
                #ret, frame = cap.read() #.......................... this may be THE READ
                #
                #
                #
                if ret:
                    if frame is not None:
                        now = dt.datetime.now()
                        mq_exposition, mq_gain, mq_gamma = 0.5, 0.5, 0.5
                        #mqtt_payload = create_mqtt_payload(frame, framenumber, timestamp, recording_started, exposition, gain, gamma))# "Frame-1"

                        #print(" direct egg   ", expotv,gaintv,gammatv)
                        if not expotv is None: mq_exposition = expotv
                        if not gaintv is None:  mq_gain = gaintv
                        if not gammatv is None: mq_gamma = gammatv
                        mqtt_payload = create_mqtt_payload(frame, BaseCamera.nframes+1,
                                                           now, mqtt_started,
                                                           mq_exposition, mq_gain, mq_gamma)
                        mqtt_result=mqtt_client.publish(mqtt_topic, mqtt_payload )
                #
                #
                if histogram_v is not None and histogram_h is not None:
                    # print(type(frame), len(frame))

                    framered = np.amax(frame, axis=2)

                    suma480 = np.max( framered, axis = 1)
                    suma640 = np.max( framered, axis = 0)

                    #suma480 = np.sum( frame, axis = 1)
                    #suma640 = np.sum( frame, axis = 0)
                    #suma480 =suma480/len(suma480)/3
                    #suma640 =suma640/len(suma640)/3
                    # print(   len(suma480) ,  suma480[100] , np.sum( suma480[100]  ) ) # ax 1 480
                    for i in range(len(suma480) ): # to 480
                        histogram_v.SetBinContent(i, np.sum( suma480[i] ) )
                    for i in range(len(suma640) ): # to 480
                        histogram_h.SetBinContent(i, np.sum( suma640[i] ) )
                        #histogram_v.SetBinContent(i, np.sum( frame, axis = 0)[i] )
                if not ret:
                    print("X... not good read 1 ()")
                    time.sleep(0.2)
                    if cap is not None:
                        ret, frame = cap.read() # ....................................... this may be READ
                    else:
                        print("X... cap is NONE1")
                    if not ret:
                        print("X... not good read 2")
                        time.sleep(0.2)
                        if cap is not None:
                            ret, frame = cap.read() # .................................... this may be READ
                        else:
                            print("X... cap is NONE2")
                        print(f"X... 3rd read result=={ret}")


                # SIMULATE A PI3B problem
                # frame = cv2.resize(frame, (640,480) )
                if frame is not None:
                    obtres = f"{frame.shape[1]}x{frame.shape[0]}"
                    sucres = obtres == config.CONFIG['resolution']
                    if not sucres:
                        #xzoom
                        #w,h = config.CONFIG['resolution'].split("x")
                        #dsize = ( int(w), int(h))
                        #frame = cv2.resize(frame, dsize )
                        frame[0:4,0:4] = [0,255,255] # set   ;;0 0 255 is RED
                        print(f" OBTAINed res {fg.red}{obtres}{fg.default} is not config res", end = "" )
                    BaseCamera.nframes+=1
                    BaseCamera.capture_time = dt.datetime.now().strftime("%H:%M:%S.%f")[:-4]

            except Exception as ex:
                print()
                print("X... SOME EXCEPTION ON cap.read (@real_cam)...", ex)
                config.CONFIG["camera_on"] = False
        # --- camera probably works ret True
        if not ret:
            time.sleep(0.5)
            config.CONFIG["camera_on"] = False
            print("x...  cap didnt go ok, graying... trying to acquire new cap")
            print("x...   here is something i dont get .....why Camera.init ca")
            # static method. should give 3 things
            #    I dont understand this
            #
            # CAINI 1 ?
            cap = Camera.init_cam( ) # WHAT IS THIS? the same?<= static?
            #
            print(f"?... {fg.red}  cap 1 return === {cap} {fg.default}")
            nfrm = 0
            if frame is None:
                height, width = 480, 640
                if config.generic_bg_image is None:
                    print(" ****************************")
                    config.fullpath_bg_fixed_image = f"{os.path.dirname(config.CONFIG['filename'])}/{config.CONFIG['defaultbg']}"
                    print("i... BG IMAGE PATH", config.fullpath_bg_fixed_image)
                    config.fullpath_bg_fixed_image = os.path.expanduser(config.fullpath_bg_fixed_image)
                    print("i... BG IMAGE PATH", config.fullpath_bg_fixed_image)
                    if config.fullpath_bg_fixed_image is not None:
                        print("i... BG IMAGE READING ")
                        config.generic_bg_image = cv2.imread( config.fullpath_bg_fixed_image)
                    print("i... BG IMAGE READ: ", config.fullpath_bg_fixed_image)
                #print("i... BG IMAGE GENE: ", config.generic_bg_image )
                if config.generic_bg_image is not None:
                    frame = config.generic_bg_image
                else:
                    frame = np.zeros((height,width,3), np.uint8)
                frame = cv2.resize(frame, (width,height) )
                # blank_image = np.zeros((height,width,3), np.uint8)
                # # GRAY GREY 255 128 ---- half split image in a case ....happens too frequent..
                # blank_image[:,0:width//2] = (10,10,10)      # (B, G, R)
                # blank_image[:,width//2:width] = (30,30,30)
                #frame = blank_image

            overtext = "XXXXXXXXXXX"
            overtext = get_ip( "" ) # crash when no net
            overtext = f"Device lost on {overtext}"
            frame = force_center_text( frame, overtext, posy = 200, fg_bgr=(0, 0, 255) )
            print(f"i... FrAmE {BaseCamera.nframes:8d}  {BaseCamera.capture_time}   ", end="\r" )
            #
        return frame, cap




    @staticmethod
    def camera_or_image( cap, vidnum):
        """
        THIS RUNS WHEN CLOCK OR BEAMON IS demanded---------------
        vidnum None or -1 ...   check cap for filenames
        """
        #print("************************ IN")
        #config.fullpath_bg_fixed_image = "~/.config/flashcam/monoskop.jpg"
        #config.fullpath_bg_fixed_image = "~/.config/flashcam/ubu_2204.jpg"
        if config.fullpath_bg_fixed_image is None:
            config.fullpath_bg_fixed_image = f"{os.path.dirname(config.CONFIG['filename'])}/{config.CONFIG['defaultbg']}"
            config.fullpath_bg_fixed_image = os.path.expanduser( config.fullpath_bg_fixed_image)
            # debug print( cap, vidnum)
            if not os.path.exists(config.fullpath_bg_fixed_image):
                print("X...  config.fullpath_bg_fixed_image  doesnt exist")
                config.fullpath_bg_fixed_image = None

        if not (vidnum is None) and (vidnum==-1):
            #
            # No videodevice
            #
            # print("i... camera mode : cam-or-image ...  image mode", type(cap), cap, vidnum)
            #print("************************  NO DEV -  when image or clock...........")

            i = 0
            image = None
            if cap is not None and ((cap.find("screenshot.jpg")==0) or (cap.find("screenshot")==0) ) :#and ('pyautogui' in globals()):
                print("i... NOT screenshot mode")
                WAY =  os.getenv("XDG_SESSION_TYPE") == "wayland"
                if WAY:
                    if random.random() < 0.05:
                        image = shot()
                        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    #else:
                    #    image = pyautogui.screenshot()
                    #    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                #image = pyautogui.screenshot()
                #image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                if image is None: return None, None, cap

                # scale_percent = 50
                # width = int(image.shape[1] * scale_percent / 100)
                # height = int(image.shape[0] * scale_percent / 100)
                # # dsize
                # dsize = (width, height)

                # # resize image
                # frame = cv2.resize(image, dsize)

                # Resize the image to 640x480
                dsize = (640, 480)
                frame = cv2.resize(image, dsize)

                time.sleep(0.3) # from 85%cpu to 20% ??????
                return "image", frame, cap # repeat cap==image

            elif cap is not None and cap.find("clock")==0:
                """
                clock clocks clocks.jpg .....
                """
                #
                # demanded 'living' jpg
                #
                height, width = 480, 640
                blank_image = np.zeros((height,width,3), np.uint8)
                blank_image[0:height//2,0:width//2] = (25,15,15)      # (B, G, R)
                blank_image[0:height//2,width//2:width] = (15,25,15)
                blank_image[height//2:height,width//2:width] = (15,15,25)
                blank_image[height//2:height,0:width//2] = (25,15,25)
                position = (10, 320)
                drtext = dt.datetime.now().strftime("%H:%M:%S.%f")[:-5]
                frame = iprint( blank_image, drtext,
                                "di90" , position,  color_rgb=(0,255,0)  ) # green LED

                time.sleep(0.1) # from 85%cpu to 20% with 0.1;
                return "image", frame, cap # repeat cap==image

            elif cap is not None and cap.find(".jpg")>=0:
                if cap.find("win_rain1.jpg") > 0:
                    cap = "win_rain2.jpg"
                elif cap.find("win_rain2.jpg") > 0:
                    cap = "win_rain3.jpg"
                elif cap.find("win_rain3.jpg") > 0:
                    cap = "win_rain1.jpg"
                #------------------------
                #
                # any JPG   cap is what is demanded.....    config.generic_bg_image is None: Serves as RETRIGGER for LOAD
                #
                #print("i... ***************   static image mode", cap) # show jpg in cap (tripwire is generic_bg!!)
                capfull = os.path.expanduser( f"~/.config/flashcam/{cap}" )
                if  os.path.exists(capfull):
                    config.fullpath_bg_fixed_image =  capfull
                    #print("W... image        exist", cap, " OK")
                    print("D...", capfull)

                else:
                    print("X... image doesnt exist", cap, "using monoskop/ubu_2204")
                    cap = "monoskop.jpg"
                    capfull = os.path.expanduser( f"~/.config/flashcam/{cap}" )
                    config.fullpath_bg_fixed_image =  capfull

                time.sleep(0.3) # from 85%cpu to 20% with 0.1
                if config.generic_bg_image is None or config.fullpath_bg_fixed_image.find("win_rain") >= 0:
                    config.generic_bg_image = cv2.imread( config.fullpath_bg_fixed_image)
                retimg = cv2.resize(config.generic_bg_image, (640,480) )
                return "image", retimg, cap # repeat cap==image
        else:
            #==================================== monoskop added with IP ADDRESS in black
            # print("i...  camera mode .....   cap-or-image",type(cap), cap, vidnum)
            if cap is None and vidnum is None:
                #print("X... camera not accessible ... NO CAMERA FOUND ")
                time.sleep(0.2) # decrease framerate to 5fps
                if config.fullpath_bg_fixed_image is None:
                    if config.fullpath_bg_fixed_image is not None:
                        print("i... BG IMAGE READING ")
                        config.generic_bg_image = cv2.imread( config.fullpath_bg_fixed_image)
                frame = cv2.resize(cv2.imread( config.fullpath_bg_fixed_image), (640,480) )
                overtext = "XXXXXXXXXXX"
                overtext = get_ip("")
                overtext = f"No camera found on {overtext}"
                frame = force_center_text(frame, overtext , posy = 35, fg_bgr=(0, 0, 255))
                txt_img = "xxxxxxxxxxx"

                return "image_forced",  frame, cap # repeat cap==image
            # if there is a new cap => propagate it upsrtream
            frame, newcap = Camera().acquire_one_frame(cap)
            return "camera", frame, newcap
        print("X... NEVER GET HERE..................")
        return None, None, None


    # ================================================================================
    #    FRAMES ..... MAIN FUNCTION
    # --------------------------------------------------------------------------------

    @staticmethod
    def frames( ):
        """
        product= ... uses the recommend_video to restart the same cam; THIS OVERRIDES THE BASECAMERA;
        """
        # i need these to be in globals() ----evaluate from web.py
        #                                 ---- OR FROM seread
        global substract_background,save_background
        global save_image_decor, save_image_png # save camera_screenshot - web feature - unlike savebg - it saves with all decorations
        global mix_foreground,save_foreground
        global send_telegram, telegramlast

        global speedx, speedy, restart_translate, average
        # try to gaint .... directs
        global gaint, expot, gammat # I have global one-shot Nones....
        global gaintv, expotv, gammatv # I have global values....
        global gamma_divide, gamma_multiply,gamma_setdef
        global gain_divide,gain_multiply,gain_setdef
        global expo_divide,expo_multiply,expo_setdef# ,  expovalue, gainvalue
        global timelaps, timelaps_triggered, rotate180
        global fixed_image # show not camera but image
        global zoom
        global resozoom
        global pausedMOTION
        global overtext, overtextalpha, baduser
        global framekind


        global s9009
        gaint = None # direct set of values
        expot = None
        gammat = None
        # print("i... staticmethod frames @ real -  enterred; target_frame==", target_frame)
        # ----- I need to inform SENH about the resolution


        #
        #  DEFINE INPUT Processing
        #           and relative dimensions and positions, to be seen at higher resolutions
        yresolution = int(config.CONFIG["resolution"].split("x")[1])
        xresolution = int(config.CONFIG["resolution"].split("x")[0])
        widg_bias = int(0.1 * yresolution) # 50
        widg_skip = int(0.195 * yresolution) # 100
        widg_tail = int(0.91 * xresolution) # 585
        widg_trail = int(0.2 * xresolution) # 100 for sub(title)
        widg_radi = int( 0.0625 * yresolution) # 30 -dial-tacho-signal

        # for different port than config netport: I can detect a change and use inputi 11-16
        mywidgets = []
        MAX_WIDGETS = 6 # really 5 + sub
        CURRENT_PORT = int(config.CONFIG['netport']) # it will return 5000 if "-n 5000"
        STARTUP_PORT = int(config.CONFIG['startupport']) # original CONFG value is stored here OR ZERO if Gunicorn
        joffset = 0
        if STARTUP_PORT != 0 and CURRENT_PORT != STARTUP_PORT:   joffset = 10
        for i in range(1, MAX_WIDGETS):
            j = i + joffset
            mywidgets.append( widget(j,pos=(widg_tail, widg_bias + (i - 1)* widg_skip ), typ = "dial", radius=widg_radi) )
        mywidgets.append( widget(joffset + MAX_WIDGETS ,pos=(widg_trail, widg_bias + (i - 1)* widg_skip ), typ = "sub", radius=widg_radi) )

        # mywidgets.append( widget(2,pos=(585,150), typ = "dial") )
        # mywidgets.append( widget(3,pos=(585,250), typ= "tacho" ) )
        # mywidgets.append( widget(4,pos=(585,350), typ = "box" ) )
        # mywidgets.append( widget(5,pos=(220,450), typ = "sub" ) )

        senh = Stream_Enhancer( resolution = config.CONFIG["resolution"] ) # i take care inside

        senh.zmqtarget = None # initially
        if 'imagezmq' in config.CONFIG:
            senh.zmqtarget = config.CONFIG['imagezmq']
            if senh.zmqtarget=="None":
                senh.zmqtarget = None
        else:
            print("X... need to update config for imagezmq")
            senh.zmqtarget = None

        if 'jtelegram' in config.CONFIG:
            senh.jtelegram = config.CONFIG['jtelegram']
            if senh.jtelegram=="false":
                senh.jtelegram = False
        else:
            print("X... need to update config for imagezmq")
            senh.jtelegram = False


        # === I must have these GLOBAL and PREDEFINED HERE <= web.py
        # --------------------------------  control
        # -----------get parameters for DetMot, same for web as for all
        #print(config.CONFIG)
        #print( "AVERAGE I AM HAVING ",config.CONFIG['average'] )
        framekind    = config.CONFIG['framekind']
        average      = int(config.CONFIG['average'])
        #gaint        = None # int(config.CONFIG['gaint']) # initial gain value 1st TRY
        #expot = None
        #gammat = None
        threshold    = int(config.CONFIG['threshold'])
        blur         = int(config.CONFIG['blur'])
        timelaps     = config.CONFIG['laps']
        timelaps_triggered = False
        histogram    = config.CONFIG['Histogram']
        res          = config.CONFIG['resolution']
        speedx       = float(config.CONFIG['x'])
        speedy       = float(config.CONFIG['y'])
        rotate180    = int(config.CONFIG['otate'])
        zoom         = int(config.CONFIG['zoom'])
        resozoom     = False # trying to play on resolution

        MODE_DMbase = "MODE DM"
        MODE_DM = "MODE DM"

        #imagezmq = None # I use senh.zmqtarget....
        #if 'imagezmq' in config.CONFIG:
        #    imagezmq     = config.CONFIG['imagezmq']

        print( "XY: ", config.CONFIG['x'] ,  config.CONFIG['y']  , speedx, speedy)

        # ------------------    to evaluate commands from web.py
        # ------------------    or searead
        # ------------------    these commands need to be declared here
        #                       AND in globals
        substract_background = False
        save_background = False
        save_image_decor = False # save camera_screenshot
        save_image_png = False # save camera_screenshot
        mix_foreground = False
        save_foreground = False

        send_telegram = None # i hope this is ok too...
        telegramlast = dt.datetime.now()

        restart_translate = False

        gamma_divide = False
        gamma_multiply =False
        gamma_setdef =False

        gain_divide = False
        gain_multiply =False
        gain_setdef =False

        expo_divide = False
        expo_multiply =False
        expo_setdef =False
        exposet = False # not used..
        #expovalue = -999. # initial
        #gainvalue = -999. # initial

        # rotate180 = False # i define earlier from CONFIG

        fixed_image = None # just camera.

        # --- 433MHz
        pausedMOTION = False
        overtext = None
        overtextalpha = 0
        baduser = None


        switch_res = False # testing
        switch_res_pos = ["C","C"] # initial position of xzoom

        # ==================== GO TO CAMERA AND IMAGE PROCESSING ==============

        camera = Camera(  )
        vidnum = None # it will be re-asked gain and again

        # CAINI 2
        cap, vidnum, s9009 = camera.init_cam(  ) # can return None,None; of jpg,-1
        print("D... CAINI 2 '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        # Get the current FPS from the camera
        webcam_fps = 10
        try:
            webcam_fps = cap.get(cv2.CAP_PROP_FPS)
        except:
            print("X... no fps available")
        if not webcam_fps or webcam_fps <= 0:
            webcam_fps = 10.0  # Fallback FPS if the camera does not return a valid FPS







        # *********  video works,  get capacities and go with EXPO GAIN
        if not( (vidnum is None) or (vidnum == -1) ):

            cc = v4lc.V4L2_CTL("/dev/video"+str(vidnum))
            capa = cc.get_capbilities()


            #--- INITIATION...... collecting???

            exposuredef = True
            gammadefX = True
            gaindefX = True

            cc.autoexpo_on("autoexpo")
            if (capa is not None) and "gain" in capa:
                gain = cc.get_gain()
                print(f"========={bg.orange}{fg.black} GAIN INIT  {gain}{fg.default}{bg.default} =","="*40)
                gaindef = cc.getdef_gain()
                if gaindef == gain:
                    gaindefX = True
                else:
                    gaindefX = False

            if (capa is not None) and "gamma" in capa:
                gamma = cc.get_gamma()
                gammadef = cc.getdef_gamma()
                if gammadef == gamma:
                    gammadefX = True
                else:
                    gammadefX = False

            aea,aex,aga,agm = get_gem(cc, capa)
            if aex!=None: ex,exd,mine,maxe,ex10 = aex
            if agm!=None: gm,gmd,minm,maxm,gm10 = agm
            if aga!=None: ga,gad,ming,maxg,ga10 = aga

            # very stupid camera    ZC0303 Webcam
            if (capa is not None) and "exposure" in capa:
                exposure = cc.get_exposure()
                exposuredef = cc.getdef_exposure()
                #?????
                #auto_exposuredef = cc.getdef_exposure()
                print(f"i... EXPOAUTO (top) == {exposure} vs def={exposuredef}; ")
                # it seems I lost autoexposure in one RPI4 imx  camera...




            nfrm = 0
            # if config.CONFIG["product"]:
            #     wname = "none "
            # else:
            #     wname = config.CONFIG["product"]
        # ___ exposure and gain stuff here... done _____



        # *********************** INFINITE UNCONDITIONAL LOOP  ****
        # *********************** INFINITE UNCONDITIONAL LOOP  ****
        # *********************** INFINITE UNCONDITIONAL LOOP  ****
        # *********************** INFINITE UNCONDITIONAL LOOP  ****
        frame_prev = None
        capa = None # prevent fail when switching to from image to occupied live ???
        while True:
            #print("D... WHILE ****  TRUE")
            #capa = None # prevent fail when switching to from image to occupied live ???

            timeoutok = False
            ret = False
            frame = None

            # can change cap to a new one
            ccoi1, frame, cap = camera.camera_or_image(cap, vidnum)

            #print( frame.shape )
            #print( ccoi1 * 30 )
            ret = True # for the next


            #print(f"D...   mode: {ccoi1}    ")
            if ccoi1 == "camera" and frame is None:
                #print("D... ... but frame None    ")
                ret = False
            elif (ccoi1 == "camera") and (frame is not None) and (capa is None):
                print(f"D... ...  mode: {ccoi1}   AND LOADING CAPAbilities!!! ")
                capa = cc.get_capbilities()
            elif ccoi1 == "image_forced":
                #print("D... ... but image_forced   ")
                # CAINI 3
                if random.random() < 0.1:
                    print("D... ... ... but sometimes i try to init....   ")
                    cap, vidnum, s9009 = camera.init_cam()
                    print("D... init cam tried'''''''''''''''''''''''''''", end="\r")
                else:
                    print("D... init cam skipped'''''''''''''''''''''''''", end="\r")

                # *********  video works,  get capacities and go with EXPO GAIN
                if not( (vidnum is None) or (vidnum == -1) ):
                    cc = v4lc.V4L2_CTL("/dev/video"+str(vidnum))
                    capa = cc.get_capbilities()

                    # WHEN switching to occupied LIVE...... i try this
                    #if capa is None:
                    #    ret = False

                    exposuredef = True
                    gammadefX = True
                    gaindefX = True

            #print("D... ret==", ret)
            if ret: #********************************************************* operations


                #=====================================================
                #  FIRST OPERATION ON FRAME ...  xzoom  switchresolution
                #  if not 640x480 =>  CUT FROM IT .... when ZoomResolution option is True
                #  ::  xtend extended extra resolution switch resolution ::
                #=====================================================
                if frame is not None and  frame.shape[0]!=480 and config.CONFIG['ZoomResolution']:
                    # DO CUT FROM LARGER IMAGE
                    # xzoom thing
                    # print( frame.shape)
                    h,w = frame.shape[:2]  # from 3
                    # get the middle
                    ch = int(h/2)
                    cw = int(w/2)
                    #print(f"D...  xzooming  {switch_res_pos}   " , end="\r")
                    if switch_res_pos[0]=="L": cw=320
                    if switch_res_pos[1]=="U": ch=240

                    if switch_res_pos[0]=="R": cw=w-320
                    if switch_res_pos[1]=="D": ch=h-240

                    # make it 640x480 again :  0:480   0:640    h-480:h  w-640:w
                    frame = frame[ch-240:ch+240, cw-320:cw+320]
                    #else nothing
                frame_prev = frame



                #================================================================
                #
                # all the rest comes under this senh.add_frame
                #
                #================================================================
                if frame is not None and senh.add_frame(frame):  # it is a proper image....

                    # 1. rotate (+translate of the center)
                    # 2. zoom (+translate the center)
                    # 3. histogram !!!here
                    # 4. speed x,y
                    # 5. web command execution
                    # . others

                    # ================================================== ROTATE / priority #1
                    if rotate180!=0:   # rotate earlier than zoom
                        senh.rotate180( rotate180 ) #arbitrary int angle

                    # ================================================== ZOOM   / priority #2
                    if zoom!=1:
                        try:
                            crocfg = os.path.expanduser("~/.config/flashcam/cross.txt")
                            cross_dx, cross_dy  = None, None
                            if os.path.exists(crocfg):
                                with open(crocfg) as f:
                                    cross_dx, cross_dy  = [int(x) for x in next(f).split()]
                                    #senh.zoom( zoom ,0,0 )
                                    senh.zoom( zoom ,cross_dx, cross_dy )
                        except Exception as e:
                            print("!... Problem ar cross.txt file:",e)

                    # ================================================== calc his priority #3
                    if histogram: # just calculate a number on plain frame
                        #hmean = senh.histo_mean( ) # hmean STRING NOW
                        hmean = senh.histo_medi( ) # hmean STRING NOW
                        # print("i... histo value:", hmean)
                        ##tune_histo(cc, hmean )

                    # ---------- before anything - we decode the web command EXECUTE EXECUTION

                    # ================================================== x,y move priority #4
                    # - compensate for speed of the sky -  not used anymore
                    if ((speedx!=0) or (speedy!=0)) \
                    and ((abs(speedx)>1) or (abs(speedy)>1)):
                        senh.translate( speedx, speedy)

                    if restart_translate:
                        senh.reset_camera_start()
                        restart_translate = False


                    # ================================================== x,y move priority #5
                    # ------------- commands comming from web.py----------------
                    #  expressions     external commands
                    # ------------- COMMANDS COMMING FROM WEB.PY----------------
                    #  expressions
                    # ------------- commands comming from web.py----------------
                    #           -------------- or from seread (fixed_image ...)
                    expression,value = mmread_n_clear( )

                    if expression[:5] != "xxxxx":          # command  execution expression
                        print(f"i...  *received  EXPRESSION:    /{expression}/ == /{value}/")
                        print(f"i...  *received  EXPRESSION:    /{expression}/ == /{value}/")

                        # -------------------- conversions without eval inf float bool, string
                        if is_int(value):
                            print("i... ... ",value, 'can be safely converted to an integer.')
                            value = int(float(value)) # 1.0 => int crashes
                        elif is_float(value):
                            print("i... ... ",value, 'is a float with non-zero digit(s) in the fractional-part.')
                            value = float(value)
                        elif is_bool(value):
                            #print("i... ",value, 'is true or false.')
                            print("i... ... ",value, 'is boolean ')
                            if value=="True":
                                value = True
                            else:
                                value = False
                        else:
                            print(f"i... ... /{value}/ is string, quotes removed.")
                            value = str(value) # i dont care anyway
                            value = value.strip('"').strip("'")

                        # AVOID CHANGING AVERAGE WHEN DETMO -----------------------
                        if (threshold>0) and (expression == "average"):
                            expression = None
                            value = None

                            #################################################################
                        try: ################################################################
                            # eval makes float float and int int
                            #print("o... evaluating")
                            globals()[expression] = value  #was  eval(value)
                            print("i...             expression evaluated2globals:",  globals()[expression])
                            #  the expression MUST BE decleared   in    globals
                        except:
                            print("X... ... globals expression FAIL",expression,value)

                    # ==============================================================================
                    #
                    #  START OF EXPRESSIONS -------- IMMEDIATE  EVALUATIONS ------------------------
                    #
                    # ==============================================================================
                        # I need a crosscheck here on terminal screen
                        if expression=="overtext":
                            overtextalpha = 0
                        #if expression=="gaint": # it works normally
                        #    gaint = float(value)
                        if expression=="baduser":
                            print(f"X... realcam received info: baduser=={value}")
                            baduser = str(value)
                        if (expression=="fixed_image"):
                            if (value is not None) and (value != "None"):
                                print("============== GO TO FIXED IMG ===================",value)
                                fixed_image = value # doesnt worjk anymore
                                config.CONFIG["product"] = value # this may help to switch LIVE to IMG
                                ##camera.init
                                # CAINI 4
                                cap, vidnum, s9009 = camera.init_cam() # cap==jpg
                                print("D... CAINI 4 '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''", cap)

                            else:
                                print("============== RESTOR FROM FIXED IMG ===================")
                                fixed_image = None #value # doesnt worjk anymore
                                config.CONFIG["product"] = "" # this may help to switch LIVE to IMG
                                # CAINI 5
                                cap, vidnum, s9009 = camera.init_cam(  )
                                print("D... CAINI 5 '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")



                        if expression=="pausedMOTION":
                            if value is True:
                                print("===================== DM is going STANDBY  ==================************==")
                                senh.save_avi_close_dm()  # closing DM - May be Crash??
                                if config.CONFIG["cmatrixkill"]:
                                    CMD = "killall cmatrix &"
                                    try:
                                        print("D... killing cmatrix .... there might be no process like that ...")
                                        sp.Popen( CMD, shell=True)
                                    except:
                                        print("X.... cannot kill cmatrix &")
                                else:
                                    print("i... cmatrix is not run nor killed - see the config cfg.json")
                            if value is False:
                                print("--------------------- DM is going to RUN RUN RUN ----------**************--")
                                print(f"i... {bg.green}DetMo skwriter  OPENS{bg.default}")
                                if config.CONFIG["cmatrixkill"]:
                                    CMD = "xterm -fullscreen -e /usr/bin/cmatrix &"
                                    #CMD = "xterm  -e /usr/bin/cmatrix &"
                                    try:
                                        sp.Popen( CMD, shell=True)
                                    except:
                                        print("X.... cannot xterm  cmatrix")
                                else:
                                    print("i... cmatrix is not run nor killed - see the config cfg.json")



                        if expression=="telegram":
                            print("i... telegram test******************************* value=",value)
                            senh.telegram_send_image(blocking= False) # it has an internal block (300sec)

                        if expression=="timelaps":
                            print("i... TIMELAPS expression******************************* value=",value)
                            #senh.telegram_send_image(blocking= False) # it has an internal block (300sec)

                        # =====================   two possibilities for switch resolution / show max-resolution /  show a viewport 640x480
                        if expression == "switch_res":
                            #xzoom
                            if not config.CONFIG["ZoomResolution"]: # kick it immediatelly when not allowd in config
                                print(f"X... {fg.red} === zoomresolution not allowed in config {fg.default}")
                            elif type(value)==bool:
                                switch_res = value #not(switch_res)
                                print("i... ok ...ON/OFF")

                                print(f"i...       {fg.orange}   EXPERIMENTAL SWITCH RESOLUTION now=", switch_res,fg.default)
                                print("i...   if it doesnt work check in conf.json config:              ")
                                print("i...           'ZoomResolution':True                             ")
                                print("i...           'Maxresolution':'1280x720' or '1920x1080          ")
                                print("i...            'PIXELFORMAT':'MJPG' and not 'YUYV'              ")
                                print("i...                                                             ")
                                if switch_res:
                                    #maxres = "640x480"
                                    maxres = get_resolutions( vidnum )[-1] # from usb_check
                                    config.CONFIG['resolution'] = maxres
                                    print("D.... resolutionswitching to the MAX:", maxres)
                                    try:
                                        width,height = maxres.split("x")
                                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(width) )
                                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))
                                        print("D.... resolutionswitching to the MAX done:", width,height)
                                    except:
                                        print("X... problem on setting  maxres resolution:", maxres)


                                else:
                                    #xzoom ------ it seemd I am going back to standard resolution -----------------
                                    config.CONFIG['resolution'] = "640x480"
                                    print("D.... resolution to 640x480")
                                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                                    switch_res_pos = ["C","C"] #"CC" # I just reset the CC position to ease the NGuniwrec handling

                                res = config.CONFIG['resolution']


                            else:
                                #print(f"D...  /{value}/ switch_res  is type",type(switch_res), switch_res, switch_res_pos, switch_res_pos[0], switch_res_pos[1] )
                                if value=="L":
                                    print("val L")
                                    if switch_res_pos[0] == "R":
                                        switch_res_pos[0] = "C"
                                    else:
                                        switch_res_pos[0] = "L"
                                        #print("D... reset sw-re-po:",switch_res_pos[0], switch_res_pos)
                                if value=="R":
                                    if switch_res_pos[0] == "L":
                                        switch_res_pos[0] = "C"
                                    else:
                                        switch_res_pos[0] = "R"

                                if value=="U":
                                    if switch_res_pos[1] == "D":
                                        switch_res_pos[1] = "C"
                                    else:
                                        switch_res_pos[1] = "U"

                                if value=="D":
                                    if switch_res_pos[1] == "U":
                                        switch_res_pos[1] = "C"
                                    else:
                                        switch_res_pos[1] = "D"
                                print("D...  new  switch_res position is ", switch_res_pos )
                                switch_res = True#False # do not imply res.

                            #break # THIS BEAKS INIT, work on PC, not well on RPI


                    # ==============================================================================
                    #
                    #  END OF EXPRESSIONS -------- IMMEDIATE  EVALUATIONS --------------------------
                    #
                    # ==============================================================================


                    # ====================== BOTH KINDS OF LAPS SAVING AVI  ====================== ASTRO KIND HERE
                    if timelaps<0: # NEW...Save Every frame .. timelaps value is different from seconds value
                        mycodec=config.CONFIG['FOURCC']
                        # every frame AND take care of accumulation
                        senh.save_avi( seconds = 0.001, # ASTRO
                                       basecamera_string=f"{BaseCamera.nframes:07d} / {BaseCamera.capture_time} A",
                                       mycodec = mycodec, frnum= BaseCamera.nframes)

                    # ===========  SAVE PNG BEFORE OTHER interventions ============================
                    #    evidently on network command....  it is useless like this .......
                    if save_image_png:  # camera_screenshot PNG Full quality
                        print("D... HERE I SAVE  image camera_screenshot_PNG Full Quality")
                        if config.CONFIG['datapath'][-1] == "/":
                            pngname = dt.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
                            pngname = pngname[:-5].replace(".","_")
                            cv2.imwrite( config.CONFIG['datapath']+f"camera_screenshot_{pngname}.png" , frame ) # nicely saved
                        else:
                            print("X... You need to specify datapath ending with '/' . No screenshot saved")
                        save_image_png = False


                    if save_background:
                        print("D... HERE I SAVE save_background of mask")
                        print("D... HERE I SAVE save_background of mask")
                        print("D... HERE I SAVE save_background of mask")
                        senh.save_background()
                        save_background = False  # ONE SHOT

                    if substract_background:
                        # print("D... HERE I MUST DO subtraction of mask")
                        # print("D... HERE I MUST DO subtraction of mask")
                        # print("D... HERE I MUST DO subtraction of mask",speedx, speedy)
                        senh.subtract()



                    if save_foreground:
                        print("D... HERE I SAVE save_foreground ")
                        print("D... HERE I SAVE save_foreground ")
                        print("D... HERE I SAVE save_foreground ")
                        senh.save_foreground()
                        save_foreground = False  # ONE SHOT


                    if mix_foreground:
                        # print("D... HERE I mix the foreground")
                        senh.mix()

                    # done ALREADY ????---------------------------------
                    # # - compensate for speed of the sky
                    # if ((speedx!=0) or (speedy!=0)) and ((abs(speedx)<1) and (abs(speedy)<1)):
                    #     print(f"speed translate {speedx} {speedy}")
                    #     senh.translate( speedx, speedy)
                    # if restart_translate:
                    #     senh.reset_camera_start()
                    #     restart_translate = False


                    # average  THIS IS HERE to be changed TOO (ACCUM)
                    # print("i.... average", average)

                    #print("i... GAMMAS ", gamma, gammadef )

                    if ccoi1 == "camera":

                        if (capa is not None) and (gammat is not None) and "gamma" in capa:
                            gamma_divide = False
                            gammadefX = False
                            if gammat >= 0.0 and gammat <= 1.0:
                                gammatv = gammat # global v
                                gamma = gammat
                                cc.gamma(gamma  )
                                gamma = cc.gamma_get("gamma")
                                v4lc.mk_table(cc)
                            else:
                                gammatv = -1
                                gamma_setdef = False
                                gammadefX = True
                                gamma = gammadef
                                #if "gamma" in capa:
                                cc.setdef_gamma( )
                            gammat = None

                        if (capa is not None) and  gamma_divide and "gamma" in capa:
                            gamma_divide = False
                            gammadefX = False
                            gamma = cc.gamma_get("gamma")
                            gamma-=0.1
                            cc.gamma(gamma  )
                            gamma = cc.gamma_get("gamma")
                            v4lc.mk_table(cc)

                        if (capa is not None) and gamma_multiply and "gamma" in capa:
                            gamma_multiply = False
                            gammadefX = False
                            #if "gamma" in capa:
                            gamma = cc.gamma_get("gamma")
                            gamma+=0.1
                            cc.gamma( gamma )
                            gamma = cc.gamma_get("gamma")
                            v4lc.mk_table(cc)
                            # if gamma!=0:
                            #     newgamma =  int(gamma*2)
                            # else:
                            #     newgamma =  int(1)
                            # cc.set_gamma( newgamma )
                            # gamma = newgamma
                        if (capa is not None) and gamma_setdef and "gamma" in capa:
                            gamma_setdef = False
                            gammadefX = True
                            gamma = gammadef
                            #if "gamma" in capa:
                            cc.setdef_gamma( )
                            #    gamma = gammadef


                        # NEW TRY
                        if (capa is not None) and (gaint is not None) and "gain" in capa:
                            gain_divide = False
                            gaindefX = False
                            #gain = cc.gain_get("gain")
                            if gaint >= 0 and gaint <= 1.0:
                                gaintv = gaint # global v
                                gain = gaint
                                cc.gain(gain)
                                gain = cc.gain_get("gain")
                                v4lc.mk_table(cc)
                            else:
                                gaintv = -1
                                gain_setdef = False
                                gaindefX = True
                                gaindef = cc.getdef_gain()
                                gain = gaindef
                                print(f"========={bg.orange}{fg.black} GAIN SETDEF {gain} {fg.default}{bg.default} =","="*40)
                                cc.setdef_gain( )
                            gaint = None

                        if (capa is not None) and gain_divide and "gain" in capa:
                            gain_divide = False
                            gaindefX = False
                            gain = cc.gain_get("gain")
                            gain-=0.1
                            cc.gain(gain)
                            gain = cc.gain_get("gain")
                            v4lc.mk_table(cc)


                        if (capa is not None) and  gain_multiply and "gain" in capa:
                            gain_multiply = False
                            gaindefX = False
                            gain = cc.gain_get("gain")
                            gain+=0.1
                            cc.gain(gain)
                            gain = cc.gain_get("gain")
                            v4lc.mk_table(cc)

                        if (capa is not None) and gain_setdef and "gain" in capa:
                            gain_setdef = False
                            gaindefX = True
                            gain = gaindef
                            print(f"========={bg.orange}{fg.black} GAIN SETDEF {gain} {fg.default}{bg.default} =","="*40)
                            # if "gain" in capa:
                            cc.setdef_gain( )
                            #   gain = gaindef

                        ###print("D... XXX", capa)
                        if (capa is not None) and  ( "exposure_time_absolute" in capa or "exposure_absolute" in capa):
                            if histogram:
                                if hmean<5:
                                    #print(f"i... BOOSTING EXPOSURE TO 100%")
                                    cc.autoexpo_off( "autoexpo")
                                    cc.expo( 1 ,'expo')     # 0-1 log
                                    print("****** -H param => autoex  ************************ OFF")

                                if hmean>240:
                                    #print(f"i... KILLING MAN EXPOSURE ** TO AUTO,  gain too to avoid problem")
                                    cc.autoexpo_on( "autoexpo")
                                    if "gain" in capa:
                                        cc.setdef_gain()
                                    #exposure = -0.1 + exposure
                                    print("****** -H param => autoex  ********************** ON") # e-a-priority problem

                            if expot is not None:
                                #print(" ", expot) - it exists here
                                if expot >= 0 and expot <= 1.0:
                                    expotv = expot
                                    #v4lc.mk_table(cc)
                                    exposuredef = False
                                    cc.autoexpo_off( "autoexpo")
                                    exposure = expot  #cc.expo_get("expo_get")
                                    cc.expo( exposure ,'expo')     # 0-1 log
                                    v4lc.mk_table(cc)
                                else:
                                    expotv = -1
                                    exposuredef = True
                                    v4lc.mk_table(cc)
                                    exposure = cc.expo_get("expo_get")
                                    print(f"i ... AUTO  was;   exposure = {exposure} ")
                                    cc.autoexpo_on()
                                    exposure = cc.expo_get("expo_get")
                                    print(f"i ... AUTO   is;   exposure = {exposure} ")
                                    exposure = 0
                                    #senh.setbox(f"expo {exposure:.4f}",  senh.expo)
                                    v4lc.mk_table(cc)
                                expot = None # this is one-shot


                            if expo_divide:
                                expo_divide = False
                                v4lc.mk_table(cc)
                                exposuredef = False

                                cc.autoexpo_off( "autoexpo")

                                exposure = cc.expo_get("expo_get")
                                #print(f"i ... exposure- = {exposure} ")
                                exposure = -0.1 + exposure
                                cc.expo( exposure ,'expo')     # 0-1 log
                                v4lc.mk_table(cc)

                            if expo_multiply:
                                expo_multiply = False
                                v4lc.mk_table(cc)

                                exposuredef = False

                                # ra = random.uniform(0,1)
                                # print("\n\n", round(ra,3) )
                                cc.autoexpo_off( "autoexpo")
                                exposure = cc.expo_get( 'expo_get')     # 0-1 log
                                #print(" I found exposure === ", exposure)
                                cc.expo( exposure + 0.1 ,'expo')     # 0-1 log
                                v4lc.mk_table(cc)

                            if expo_setdef:
                                expo_setdef = False
                                exposuredef = True
                                v4lc.mk_table(cc)
                                exposure = cc.expo_get("expo_get")
                                print(f"i ... AUTO  was;   exposure = {exposure} ")
                                cc.autoexpo_on()
                                exposure = cc.expo_get("expo_get")
                                print(f"i ... AUTO   is;   exposure = {exposure} ")
                                exposure = 0
                                #senh.setbox(f"expo {exposure:.4f}",  senh.expo)
                                v4lc.mk_table(cc)




                            if not exposuredef: senh.setbox(f"exp {exposure:.3f}",  senh.expo)
                            if not gaindefX: senh.setbox(f"gai {gain:.3f}",  senh.gain)
                            if not gammadefX: senh.setbox(f"gam {gamma:.3f}",  senh.gamma)
                            #if  'exposure' in locals() and exposure != exposuredef:
                            #senh.setbox(f"expo {exposure:.4f}",  senh.expo)
                        #-----------exposure in capa
                    # ______________________ section with capa for camera _____________________


                    #--------------- now apply labels ------i cannot get rid in DETM---
                    #--------- all this will be on all rames histo,detect,direct,delta
                    senh.setbox(" ", senh.TIME, kompr=config.CONFIG['kompress'])
                    if config.CONFIG['resolution'] != "640x480" and config.CONFIG['ZoomResolution']:
                        #xzoom
                        senh.setbox(f"xz{switch_res_pos[0]}{switch_res_pos[1]}", senh.xzoom)

                    #senh.setbox(" ", senh.TIME, kompr= frame.shape[1])

                    if framekind in ["detect","delta","histo"]:
                        senh.setbox(f"DISP {framekind}",senh.DISP)
                    if average>0:
                        senh.setbox(f"a {average}",  senh.avg)
                    if blur>0:
                        senh.setbox(f"b  {blur}",  senh.blr)
                    if threshold>0:
                        senh.setbox(f"t  {threshold}",  senh.trh)

                    # two ways of timelaps ********************** SetBOX here
                    if timelaps>0:
                        timelaps_triggered = True
                        mycodec=config.CONFIG['FOURCC']
                        if mycodec == "DIVX":  #
                            senh.setbox(f"ld {timelaps}",  senh.lap)
                        elif mycodec == "XDIV":  # not  mkv
                            senh.setbox(f"lx {timelaps}",  senh.lap)
                        elif mycodec == "IYUV":
                            senh.setbox(f"lY {timelaps}",  senh.lap)
                        else:
                            senh.setbox(f"l  {timelaps} {mycodec}",  senh.lap)
                    if timelaps<0:
                        timelaps_triggered = True
                        senh.setbox(f"l AS",  senh.lap)
                    if timelaps == 0 and timelaps_triggered:
                        print("D... timelaps was switched off now")
                        senh.save_avi_close_laps()  # i need same for detm
                        timelaps_triggered = False


                    if histogram:
                        senh.setbox(f"h {hmean}",  senh.hist)
                    if speedx!=0:
                        #print(speedx)
                        senh.setbox(f"x {speedx:.3f}",  senh.speedx)
                    if speedy!=0:
                        senh.setbox(f"y {speedy:.3f}",  senh.speedy)
                    if zoom!=1:
                        senh.setbox(f"z {zoom:1d}x", senh.scale)

                    if substract_background and not mix_foreground:
                        senh.setbox("-BCKG",  senh.SUBBG )
                    if not substract_background and mix_foreground:
                        senh.setbox("*MIXFG",  senh.SUBBG )
                    if substract_background and mix_foreground:
                        senh.setbox("-BG*FG",  senh.SUBBG )

                    if rotate180!=0:
                        senh.setbox("ROT",  senh.rot )



                    # # ----------------expo gain gamma
                    # # very stupid camera    ZC0303 Webcam
                    # # print(capa, exposure,exposuredef) # crashes
                    # if "exposure" in capa:
                    #     if exposure!=exposuredef: # manual
                    #         senh.setbox(f"expo {exposure}",  senh.expo)

                    # if "auto_exposure" in capa:
                    #     if expo_auto!=expo_autodef: # manual
                    #         senh.setbox(f"expo {exposure_time_absolute}",  senh.expo)

                    # if ("gain" in capa) and (gain!=gaindef): # gain is not frequently tunable
                    #     senh.setbox(f"g {gain}",  senh.gain)

                    # if ("gamma" in capa):
                    #     if (gamma!=gammadef): # manual
                    #         senh.setbox(f"m {gamma}",  senh.gamma)




                    # ---draw histogram
                    #print("                               --- ",framekind)
                    if framekind == "histo":
                        senh.histo( )




                    # ====================================================== DETMO  ADN  LOOP SAVING =================================
                    # ====================================================== DETMO  ADN  LOOP SAVING =================================
                    # ====================================================== DETMO  ADN  LOOP SAVING =================================
                    # delayed telegram - preset in DM ========================
                    if not(type(senh.telegramtrigger))==bool:
                        if dt.datetime.now()>senh.telegramtrigger:
                            print("i... telegram time tripped the  2s wire:", senh.telegramtrigger.strftime("%H:%M:%S"), "NOW=",dt.datetime.now().strftime("%H:%M:%S") )
                            senh.telegramtrigger = False
                            senh.telegram_send_image() # it has an internal block (300sec)

                    # ----  for DetMo ---- work with detect motion----------------
                    #   telegram and imagezmq are active only here
                    if (threshold>0) :
                        # here there was MODE DM.
                        # but with imageZMQ and Telegram ALERT....
                        #
                        if not senh.zmqtarget is None:
                            MODE_DM=MODE_DMbase+"z"
                            if senh.jtelegram:
                                MODE_DM=MODE_DM+"T"
                        elif (senh.jtelegram):
                            MODE_DM=MODE_DMbase+"T"


                        senh.setbox(MODE_DM, senh.MODE, grayed = pausedMOTION) #---push UP to avoid DetMot
                        #print(f"MODE_DM /{MODE_DM}/  /{senh.MODE}/")
                        #print("D... detecting motion")
                        senh.detmo( average, blur)
                        senh.chk_threshold( threshold , framekind=framekind)
                        #
                        # I need a way to block DETMO ....
                        # ??? BLUETOOTH ------- see later
                        #
                        if senh.motion_detected: # saving avi on mation detect
                            # print("D... sav mot", senh.motion_detected)
                            if not pausedMOTION:
                                senh.save_avi( seconds = -1, name = "_dm" , mycodec = config.CONFIG['FOURCC'], container =  config.CONFIG['container'] , basecamera_string=f"{BaseCamera.nframes:07d} / {BaseCamera.capture_time} M" )

                    else:
                        senh.setaccum( average  )
                        senh.setblur( blur )
                        #senh.setbox("MODE  ", senh.MODE)



                    #------------yield the resulting frame----------------------------- NO MORE SENH!!!!
                    if framekind in ["detect","delta","histo"]:
                        frame = senh.get_frame(  typ = framekind)
                    else:
                        frame = senh.get_frame(  )



                    # ======== DECORATION =================
                    if overtext is not None:
                        frame = force_center_text( frame, overtext, posy = 400, fg_bgr= (0,255, 0) ) #
                        # DIAL --------
                        post = (590,430)
                        frame = dial(frame,post ,
                                     color=(0,255,0) ,
                                     radius = 30,
                                     thickness = 15,
                                     percentage= 100*overtextalpha/255 )
                        frame = signal_strength( frame, position=(580,60) , percentage= 100*overtextalpha/255  )
                        frame = text_box( frame, position=(320,240) )


                        if overtextalpha<255:
                            overtextalpha+=1.2
                        else:
                            overtext = None

                    # ======== DECORATION =================
                    if baduser is not None:
                        frame = force_center_text( frame, f"error! => {baduser}", posy = 440, fg_bgr= (0,0,255 ), fosize = 32 )


                    # ======== DECORATION =================
                    for i in mywidgets:
                        i.refresh()
                        if i.is_active():
                            frame = i.display(frame)



                    # ====================== BOTH KINDS OF LAPS SAVING AVI  ====================== ONE KIND HERE
                    if timelaps>0:
                        mycodec=config.CONFIG['FOURCC']
                        senh.save_avi( seconds = timelaps,
                                       basecamera_string=f"{BaseCamera.nframes:07d} / {BaseCamera.capture_time} L",
                                       mycodec = mycodec, frnum= BaseCamera.nframes)


                    # # not used???---------------------------------------------
                    # if save_image_decor:  # camera_screenshot with all decor
                    #     print("D... HERE I SAVE  image camera_screenshot_decor")
                    #     if config.CONFIG['datapath'][-1] == "/":
                    #         cv2.imwrite( config.CONFIG['datapath']+"camera_screenshot.jpg" , frame ) # nicely saved
                    #     else:
                    #         print("X... You need to specify datapath ending with '/' . No screenshot saved")
                    #     save_image_decor = False  # ONE SHOT


            yield frame
