# to override print <= can be a big problem with exceptions
#from __future__ import print_function # must be 1st
#import builtins
'''
This is flask interface
'''
from flashcam.version import __version__
from fire import Fire
import sys

import xml.etree.ElementTree as ET # decoding s

#
# ======================== FIRST THING!!!!!!!!!!!!!!!!!!
#
from flashcam import config

config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"


if not config.load_config( create_if_nex=True ):
    print("X.... NO CONFIG LOADED OR ERROR IN LOAD")
    sys.exit(1)
print("---------------------------------------- LOADED Config INSIDE WEBPY")
print(f"         (net)port == {config.CONFIG['netport']}               ")
print("---------------------------------------- LOADED Config INSIDE WEBPY")
# print(config.CONFIG)
# print(config.CONFIG["Histogram"], "==histo in web")

if  not("debug" in config.CONFIG):
    config.CONFIG['debug'] = True
config.CONFIG['camera_on'] = False # for everyone -
#               nobodyhas the camera at this point
#               ?? it is used in real_camera.py ...




#### from flask_api import status
from flask import send_from_directory

# for regex
from werkzeug.routing import BaseConverter

from flashcam.usbcheck import get_v_m_r
from console import fg,bg

import glob



class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]



from importlib import import_module
import os
import sys  #exit
from flask import Flask, render_template, render_template_string, Response, url_for
from flask import request
from flask import jsonify

import getpass

import datetime as dt
import time

from flask import request
#===== another auth.
from flask_httpauth import HTTPBasicAuth

# import pantilthat

# block stuff depending on PC
import socket

import random

import cv2
import numpy as np

from flashcam.real_camera import Camera
from flashcam import real_camera # for is_int()

#----------------------------------------------
from flashcam.mmapwr import mmwrite

# from 2024/4- i consider it crap and not use it
PANTILTHAT = False
# instead I want it for xzoom positioning
xzoom_is_set = False
timelaps_ptz = None
try:
    import pantilthat
except:
    class pantilthat:
        @classmethod
        def tilt(self,a):
            print("D... fake pantilt")
            return
        @classmethod
        def pan(self,a):
            print("D... fake pantilt")
            return
        @classmethod
        def get_tilt(self):
            print("D... fake pantilt")
            return 0
        @classmethod
        def get_pan(self):
            print("D... fake pantilt")
            return 0



# ------------------------------------------------------
# ------------------------------------------------------
# ------------------------------------------------------


app = Flask(__name__)

# for regex
app.url_map.converters['regex'] = RegexConverter




#==================== ALL config changes must be here ============
#
#  1st   'filename'     2nd load config       !!!!!!!!!!!!!!!!!
#
#config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"
#config.load_config()

#



#config.show_config()
# CONFIG WILL BE SAVED WHEN RUN FROM MAIN

# Camera = Camera #  This was a lucky error.... CLass from Class
# it appears - flask works when I run directly the class .....


cross_dx, cross_dy = 0,0
cross_on = False
zoom2_on = 1

save_fg = False
mix_fg = False
save_bg = False
sub_bg = False

frame_fg = None
frame_fg2 = None
frame_bg = None
frame_bg2 = None
frame_mask = None
frame_mask_inv = None

# background path
BGFILE = os.path.expanduser('~/.config/flashcam/background.jpg')
FGFILE = os.path.expanduser('~/.config/flashcam/foreground.jpg')


aboutpage = """
<html>
<h1 id="camera-details">CAMERA DETAILS</h1>
<p><em>Mon 7 Aug 18:55:59 CEST 2023</em></p>
<ul>
<li>NAME: <strong>Azurewave<sub>USB2</sub>.0<sub>HDIRUVCWebCam200901010001</sub></strong></li>
<li>lsusb: 13d3:56cb IMC Networks USB2.0 HD IR UVC WebCam</li>
<li>V-M-R: 13d3 56cb 1862</li>
<li>Price:</li>
<li>Controls: 19
<ul>
<li>AE -&gt; auto<sub>exposure</sub></li>
<li>Gi -&gt;</li>
<li>Gm -&gt; gamma</li>
</ul></li>
</ul>
<hr />
<h2 id="look">Look:</h2>
<p><img src="13d3_56cb_1862.png" /></p>
<hr />
<h2 id="controls-detailed">Controls detailed</h2>
<pre class="example"><code>
User Controls

                     brightness 0x00980900 (int)    : min=-64 max=64 step=1 default=0 value=0
                       contrast 0x00980901 (int)    : min=0 max=100 step=1 default=50 value=50
                     saturation 0x00980902 (int)    : min=0 max=100 step=1 default=64 value=64
                            hue 0x00980903 (int)    : min=-180 max=180 step=1 default=0 value=0
        white_balance_automatic 0x0098090c (bool)   : default=1 value=1
                          gamma 0x00980910 (int)    : min=100 max=500 step=1 default=300 value=300
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=2 value=2 (60 Hz)
      white_balance_temperature 0x0098091a (int)    : min=2800 max=6500 step=10 default=4600 value=4600 flags=inactive
                      sharpness 0x0098091b (int)    : min=0 max=100 step=1 default=50 value=0
         backlight_compensation 0x0098091c (int)    : min=0 max=2 step=1 default=0 value=0

Camera Controls

                  auto_exposure 0x009a0901 (menu)   : min=0 max=3 default=3 value=3 (Aperture Priority Mode)
         exposure_time_absolute 0x009a0902 (int)    : min=50 max=10000 step=1 default=166 value=9931 flags=inactive
     exposure_dynamic_framerate 0x009a0903 (bool)   : default=0 value=1
</code></pre>
<hr />
<h2 id="example-captures">Example captures:</h2>
<p><img src="13d3_56cb_1862_20230807_185559.jpg" /> <img src="13d3_56cb_1862_20230807_182114.jpg" /></p>
<div style="height: 10px;"></div>

<hr />
<p><em>Created by: zen</em></p>
  </body>
</html>
"""


def logthis( ttt, silent=False):
    sss=dt.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S")+" "+ttt+"\n"
    if not silent:
        print("L...", sss)
    with open( os.path.expanduser("~/flashcam.log") ,"a+") as f:
        f.write( sss )


logthis("Started") #-------- keep track on logins ---------
remote_ip=""
auth = HTTPBasicAuth()

#---not fstring- {} would colide

index_page = """
 <!--meta http-equiv="refresh" content="5";-->

<html>
<script>
function doDate()
{
    var str = "";

    var days = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");
    var months = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

    var now = new Date();

    str += " &nbsp; &nbsp;&nbsp;&nbsp;" +  now.getHours() +":" + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes() + ":" + (now.getSeconds() < 10 ? '0' : '') + now.getSeconds() ;
    document.getElementById("todaysDate").innerHTML = str;
}

setInterval(doDate, 200);
</script>
  <head>
    <title>Video Streaming</title>
  </head>
  <body>


<div id="todaysDate"></div>

    <img src="{{url}}">
<br>
<form method="post" action="/cross">
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="up2" value="UP2">up2</button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="up" value="UP">up</button>
      <button style="width:10%" name="crosson" value="CROSSON">crossON</button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:3%" name="left2" value="LEFT2"> << </button>
      <button style="width:3%" name="left" value="LEFT"> < </button>
      <button style="width:3%" name="center" value="CENTER"> o </button>
      <button style="width:3%" name="right" value="RIGHT"> > </button>
      <button style="width:3%" name="right2" value="RIGHT2"> >> </button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="down" value="DOWN">down</button>
      <button style="width:10%" name="crossoff" value="CROSSOFF">crossOFF</button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="down2" value="DOWN2">down2</button>
<button style="width:10%" name="zoom2" value="ZOOM2">ZOOM2</button> </div>
<hr>

<table>
<tr>
<td>
   <button style="width:100%" name="savebg" value="SAVEBG">saveBG</button>
    <button style="width:100%" name="savefg" value="SAVEFG">saveFG</button>
</td>
 <td align="left" rowspan="2">
    <img src="{{url_bg}}" alt="Smiley face"  height="120" width="160" />
 </td>
 <td align="left" rowspan="2">
    <img src="{{url_fg}}" alt="Smiley face"  height="120" width="160" />
 </td>


 <td>
   <button style="width:100%" name="timelaps" value="TIMELAPS">LAPS</button> <input type = "text" name = "timelaps_input" size="5"  placeholder="0" />
 </td>
</tr>





<tr>
 <td>
    <button style="width:100%" name="subbg" value="SUBBG">subBG</button>
    <button style="width:100%" name="mixfg" value="MIXFG">mixFG</button>
 </td>
 <td> </td>
 <td>
   <button style="width:100%" name="rot0" value="ROT0">rot0</button>
   <button style="width:100%" name="rot180" value="ROT180">rot180</button>
 </td>
 <td>
   <button style="width:100%" name="live" value="LIVE">live</button>
   <button style="width:100%" name="fixed" value="FIXED">fixed</button>
 </td>
</tr>
</table>





<hr>
      <button style="width:3%" name="speedx" value="SPEEDX">dX</button>
    <input type = "text" name = "inputx"  size="5" />
      <button style="width:3%" name="speedy" value="SPEEDY">dY</button>
    <input type = "text" name = "inputy" size="5" />

      <button style="width:6%" name="restart_translate" value="RESTART_TRANSLATE">restart</button>
      <button style="width:4%" name="zero_translatex" value="ZERO_TRANSLATEX">zeroX</button>
      <button style="width:4%" name="zero_translatex" value="ZERO_TRANSLATEX">zeroY</button>
      <button style="width:5%" name="accum" value="ACCUM">Accum</button>
      &nbsp; &nbsp;&nbsp; <input type = "text" name = "accumtxt" size="6" />
<hr>
      <button style="width:6%" name="gamma2" value="GAMMA2">gm x2</button>
      <button style="width:6%" name="gamma05" value="GAMMA05">gm /2</button>
      <button style="width:6%" name="gamma" value="GAMMA">gm def</button>
      <button style="width:6%" name="gain2" value="GAIN2">ga x2</button>
      <button style="width:6%" name="gain05" value="GAIN05">ga /2</button>
      <button style="width:6%" name="gain" value="GAIN">ga def</button>

      <button style="width:5%" name="gaint" value="GAINT">Gain</button>
      &nbsp; &nbsp;&nbsp; <input type = "text" name = "gaintxt" size="6" />

      <button style="width:5%" name="gaint" value="EXPOT">Expo</button>
      &nbsp; &nbsp;&nbsp; <input type = "text" name = "expotxt" size="6" />

      <button style="width:5%" name="gaint" value="GAMMAT">Gamma</button>
      &nbsp; &nbsp;&nbsp; <input type = "text" name = "gammatxt" size="6" />

      <button style="width:6%" name="expo05" value="EXPO05">ex /2</button>
      <button style="width:6%" name="expo2" value="EXPO2">ex x2</button>
      <button style="width:6%" name="expo" value="EXPO">ex def</button>

  <!--/div-->
<hr>
      <button style="width:6%" name="switch_res_on" value="SWITCH_RES_ON">RESOL TO 1920x1080 and CROP</button>
      <button style="width:6%" name="switch_res_off" value="SWITCH_RES_OFF">RESOL BACK TO 640x480</button>

</form>

<hr>
<a href=/about> About camera</a>


  </body>
</html>

"""
#    <img src="{{ url_for('video') }}">

def crossonw( img,  dix, diy):
    """
    duplicite with senh cross;  dix diy are dist from center
    """
    crotype = "box"
    lcolor = (0,255,55)
    RADIUS=63
    y = int(img.shape[0]/2)
    x = int(img.shape[1]/2)

    #if y<0:y=0
    #if x<0:x=0

    #if y>img.shape[0]:y=img.shape[0]
    #if x>img.shape[1]:x=img.shape[1]

    ix = x+dix
    iy = y+diy

    if ix<0 or iy<0 or ix>img.shape[1] or iy>img.shape[0]:
        print(f"|green cross: {ix},{iy}|" )

    if iy<0:iy=0
    if ix<0:ix=0
    if iy>img.shape[0]:iy=img.shape[0]
    if ix>img.shape[1]:ix=img.shape[1]


    i2=cv2.circle( img, (ix,iy), RADIUS, lcolor, 1)
    i2=cv2.line(i2, (ix-RADIUS+5,iy), (ix-5,iy), lcolor, thickness=1, lineType=8)
    i2=cv2.line(i2, (ix+RADIUS-5,iy), (ix+5,iy), lcolor, thickness=1, lineType=8)

    i2=cv2.line(i2, (ix,iy-RADIUS+5), (ix,iy-5), lcolor, thickness=1, lineType=8)
    i2=cv2.line(i2, (ix,iy+RADIUS-5), (ix,iy+5), lcolor, thickness=1, lineType=8)

    i2=cv2.line(i2, (ix,iy), (ix,iy), lcolor, thickness=1, lineType=8)
    # from senh
    if crotype == "box":
        #corners  #  position 0.5deg from 11 deg. OK
        crscal = 4
        crnx,crny = int(64/crscal),int(48/crscal)

        i2=cv2.line(i2, (ix-crnx,iy-crny), (ix+crnx,iy-crny), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix+crnx,iy-crny), (ix+crnx,iy+crny), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix+crnx,iy+crny), (ix-crnx,iy+crny), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix-crnx,iy+crny), (ix-crnx,iy-crny), lcolor, thickness=1, lineType=8)

    return img



# ... this i dont remember
# --- probably a wrong guess ... @auth.verify_password
#
# i need  @auth.login_required
@auth.verify_password
@app.route("/cross", methods=['GET', 'POST'])
# @auth.login_required
def cross():
    global cross_dx, cross_dy, cross_on, save_bg, save_fg, mix_fg, sub_bg, zoom2_on
    global remote_ip
    global xzoom_is_set # for xzoom resolution and newpantilt
    # i will read it from file
    print(f"i... request (authenticated) on cross came on port {config.CONFIG['netport']}...")
    print(f"i ... FORM:",request.form)

    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis(f" @cross {remote_ip}/{request.remote_addr}  {request.form}")
    crocfg = os.path.expanduser("~/.config/flashcam/cross.txt")
    if os.path.exists(crocfg):
        with open(crocfg) as f:
           cross_dx, cross_dy  = [int(x) for x in next(f).split()]

    print(request.method)
    if request.method == 'POST':

        # ------------------------------------------- EXECUTE EXECUTION part for real_camera
        if request.form.get('savepn') == 'SAVEPN':
            print("i... saving PNG Full quality" )
            mmwrite(f"save_image_png {True}" )

        if request.form.get('saveim') == 'SAVEIM':
            print("i... saving IM camera-screenshot jpg" )
            mmwrite(f"save_image_decor {True}" )

        if request.form.get('savebg') == 'SAVEBG':
            print("i... saving BG" )
            save_bg = True
            mmwrite(f"save_background {save_bg}" )

        if request.form.get('savefg') == 'SAVEFG':
            print("i... saving FG" )
            save_fg = True
            mmwrite(f"save_foreground {save_fg}" )

        if request.form.get('subbg') == 'SUBBG':
            print("i... substracting  BG" )
            sub_bg = not( sub_bg)
            mmwrite(f"substract_background {sub_bg}" )

        if request.form.get('mixfg') == 'MIXFG':
            print("i... mixing FG" )
            mix_fg = not( mix_fg)
            mmwrite(f"mix_foreground {mix_fg}" )

        # ===================================================== BG FG

        if request.form.get('accum') == 'ACCUM':
            accum = request.form.get('accumtxt')
            try:
                accum = int(accum)
            except:
                accum = 0
            print("i...  ACCUM",  accum)
            mmwrite(f"average {accum}" )


        # ------------ first try to make exact gain expo values
        if request.form.get('gaint') == 'GAINT':
            gaint = request.form.get('gaintxt')
            try:
                gaint = float(gaint)
            except:
                gaint = 0.5
            print("i...  GAINT",  gaint)
            mmwrite(f"gaint {gaint}" )

        # ------------ first try to make exact gain expo values
        if request.form.get('expot') == 'EXPOT':
            expot = request.form.get('expotxt')
            try:
                expot = float(expot)
            except:
                expot = 0.5
            print("i...  EXPOT",  expot)
            mmwrite(f"expot {expot}" )

        # ------------ first try to make exact gain expo values
        if request.form.get('gammat') == 'GAMMAT':
            gammat = request.form.get('gammatxt')
            try:
                gammat = float(gammat)
            except:
                gammat = 0.5
            print("i...  GAMMAT",  gammat)
            mmwrite(f"gammat {gammat}" )



        if request.form.get('speedx') == 'SPEEDX':
            speedx = request.form.get('inputx')
            try:
                speedx = float(speedx)
                print("i...  X",  speedx)
                mmwrite(f"speedx {speedx}" )
            except:
                print("D... unknown value speedx")

        if request.form.get('speedy') == 'SPEEDY':
            #time.sleep(0.2)  #=============== PROBLEM FOR SLOW FRAMES!
            speedy = request.form.get('inputy')
            try:
                speedy = float(speedy)
                print("i...  Y",  speedy)
                mmwrite(f"speedy {speedy}" )
            except:
                print("D... unknown value speedy")

        if request.form.get('restart_translate') == 'RESTART_TRANSLATE':
            mmwrite(f"restart_translate True" )

        if request.form.get('zero_translatex') == 'ZERO_TRANSLATEX':
            mmwrite(f"speedx {0}" )
        if request.form.get('zero_translatey') == 'ZERO_TRANSLATEY':
            mmwrite(f"speedy {0}" )

        if request.form.get('gamma2') == 'GAMMA2':
            mmwrite(f"gamma_multiply True" )
        if request.form.get('gamma05') == 'GAMMA05':
            mmwrite(f"gamma_divide True" )
        if request.form.get('gamma') == 'GAMMA':
            mmwrite(f"gamma_setdef True" )

        if request.form.get('gain2') == 'GAIN2':
            mmwrite(f"gain_multiply True" )
        if request.form.get('gain05') == 'GAIN05':
            mmwrite(f"gain_divide True" )
        if request.form.get('gain') == 'GAIN':
            mmwrite(f"gain_setdef True" )

        if request.form.get('expo2') == 'EXPO2':
            mmwrite(f"expo_multiply True" )
        if request.form.get('expo05') == 'EXPO05':
            mmwrite(f"expo_divide True" )
        if request.form.get('expo') == 'EXPO':
            mmwrite(f"expo_setdef True" )

        # FOR THE MOEMNT - HIDDEN CAPABILITY
        if request.form.get('exposet') == 'EXPOSET':
            expovalue = request.form.get('expovalue')
            mmwrite(f"expovalue {expovalue}" )
        # FOR THE MOEMNT - HIDDEN CAPABILITY
        if request.form.get('gainset') == 'GAINSET':
            gainvalue = request.form.get('gainvalue')
            mmwrite(f"gainvalue {gainvalue}" )


        if request.form.get('timelaps') == 'TIMELAPS':
            timelaps = request.form.get('timelaps_input')
            try:
                print("i...  Y",  timelaps)
                # kill when not integer
                speedy = int(timelaps)
                mmwrite(f"timelaps {timelaps}" )
            except:
                print("D... unknown value timelaps")

        if request.form.get('rot0') == 'ROT0':
            mmwrite(f"rotate180 0" )
        if request.form.get('rot180') == 'ROT180':
            mmwrite(f"rotate180 180" )

        if request.form.get('live') == 'LIVE':
            mmwrite(f"fixed_image None" )
            # if request.form.get('fixed') == 'FIXED':
            #     mmwrite(f'fixed_image "BEAM_ON_.jpg"' )
            # added 2302 - directly image display possible via curl
        elif  (request.form.get('fixed') is not None) and \
          (request.form.get('fixed').find(".jpg")>1 or request.form.get('fixed').find("clock")==0):
            diimg = request.form.get('fixed')
            mmwrite(f'fixed_image "{diimg}"' )


        if request.form.get('overtext') is not None:
            digits = request.form.get('overtext')
            #print("D... writing:", digits)
            mmwrite(f"overtext {digits}" )



        if request.form.get('framekind') == "HISTOGRAM":
            mmwrite(f"framekind histo" )
        if request.form.get('framekind') == "DIRECT":
            mmwrite(f"framekind direct" )
        if request.form.get('framekind') == "DETECT":
            mmwrite(f"framekind detect" )




        # ---------------------------------------------- Cross controls
        if cross_on:
            # cross movement
            print("D... ARROWS (@web) cross is on" )
            if request.form.get('left2') == 'LEFT2':
                print("left2")
                cross_dx-= 50
            if request.form.get('left') == 'LEFT':
                print("left")
                cross_dx-= 4
            if request.form.get('center') == 'CENTER':
                print("center")
                cross_dx= 0
                cross_dy= 0
            elif  request.form.get('right') == 'RIGHT':
                print("right")
                cross_dx+= 4
            elif  request.form.get('right2') == 'RIGHT2':
                print("right2")
                cross_dx+= 50
            elif  request.form.get('up') == 'UP':
                print("up")
                cross_dy-= 4
            elif  request.form.get('up2') == 'UP2':
                print("up2")
                cross_dy-= 50
            elif  request.form.get('down') == 'DOWN':
                print("down")
                cross_dy+= 4
            elif  request.form.get('down2') == 'DOWN2':
                print("down2")
                cross_dy+= 50
        elif PANTILTHAT: # ---------------------------- PANTILT MODE
            # not using from 2024/4
            # sudo apt install python3-smbus
            if request.form.get('down') == 'DOWN':
                print("TILT v")
                if (pantilthat.get_tilt()-1)>=-85:
                    pantilthat.tilt( pantilthat.get_tilt()-1  )
            if request.form.get('up') == 'UP':
                print("TILT ^")
                if (pantilthat.get_tilt()+1)<=-32:
                    pantilthat.tilt( pantilthat.get_tilt()+1 )
            if request.form.get('right') == 'RIGHT':
                print("PAN ->")
                if (pantilthat.get_pan()-1)>=-90:
                    pantilthat.pan( pantilthat.get_pan()-1 )
            if request.form.get('left') == 'LEFT':
                print("PAN <-")
                if (pantilthat.get_pan()+1)<=90:
                    pantilthat.pan( pantilthat.get_pan()+1 )

            if request.form.get('down2') == 'DOWN2':
                print("PAN v")
                if (pantilthat.get_tilt()-8)>=-84:
                    pantilthat.tilt( pantilthat.get_tilt()-8  )
            if request.form.get('up2') == 'UP2':
                print("PAN ^")
                if (pantilthat.get_tilt()+8)<=-30:
                    pantilthat.tilt( pantilthat.get_tilt()+8 )
            if request.form.get('right2') == 'RIGHT2':
                print("PAN ->")
                if (pantilthat.get_pan()-8)>=-90:
                    pantilthat.pan( pantilthat.get_pan()-8 )
            if request.form.get('left2') == 'LEFT2':
                print("PAN <-")
                if (pantilthat.get_pan()+8)<=90:
                    pantilthat.pan( pantilthat.get_pan()+8 )
        elif xzoom_is_set: # I am in zoom-mode
            print("D... ARROWS(@web)  xzoom_is_set=TRUE (artif.zoom.ON)" )
            if request.form.get('down') == 'DOWN':
                print("xzoom v")
                mmwrite(f"switch_res D" )
            if request.form.get('up') == 'UP':
                print("xzoom ^")
                mmwrite(f"switch_res U" )
            if request.form.get('right') == 'RIGHT':
                print("xzoom ->")
                mmwrite(f"switch_res R" )
            if request.form.get('left') == 'LEFT':
                print("xzoom <-")
                mmwrite(f"switch_res L" )
        else:# i am not in zoom mode
            print("D... ARROWS(@web) xzoom_is_set=FALSE (no action)")
            if request.form.get('down') == 'DOWN':
                print("NO action v")
            if request.form.get('up') == 'UP':
                print("NO action ^")
            if request.form.get('right') == 'RIGHT':
                print("NO action ->")
            if request.form.get('left') == 'LEFT':
                print("NO action <-")



        if  request.form.get('external_signal') is not None:
            excommand = str( request.form.get('external_signal') )
            #print(f"**** external signal == {excommand} *****")
            #print(f"**** external signal == {excommand} *****")
            #print(f"**** external signal == {excommand} *****")
            print(f"**** external signal == {excommand} *****")
            if excommand == "pausedmON":
                print("i... unpause   - Detect Motion         unpause   - Detect Motion ")
                mmwrite(f"pausedMOTION False" )
            if excommand == "pausedmOF":
                print("i... pause - NO Detect Motion              pause - NO Detect Motion")
                mmwrite(f"pausedMOTION True" )


        if  request.form.get('crosson') == 'CROSSON':
            print("green cross ON")
            cross_on = True
        elif  request.form.get('crossoff') == 'CROSSOFF':
            print("green cross OFF")
            cross_on = False

        if  request.form.get('zoom2') == 'ZOOM2':
            if zoom2_on==1:
                print("ZOOM2 ->2")
                zoom2_on = 2
                mmwrite(f"zoom 2" )
            elif zoom2_on==2:
                print("ZOOM2 ->4")
                zoom2_on = 4
                mmwrite(f"zoom 4" )
            elif zoom2_on==4:
                print("ZOOM2 ->6")
                zoom2_on = 8
                mmwrite(f"zoom 8" )
            else :
                print("ZOOM2 ->1")
                zoom2_on = 1
                mmwrite(f"zoom 1" )

        #---------------- I am blindly adding functionality ... compression now
        if  request.form.get('kompress') == 'KOMPRESS':
            kompressvalue = request.form.get('kompressvalue')
            if real_camera.is_int(kompressvalue):
                kompressvalue = int(kompressvalue)
            else:
                kompressvalue = 85
            print("kompress asked  ....... with value=", kompressvalue)
            config.CONFIG['kompress'] = kompressvalue
            # if config.CONFIG['kompress']>90:
            #     config.CONFIG['kompress'] = 9
            #     print("i... KOMPRESS", config.CONFIG['kompress'] )
            # else:
            #     config.CONFIG['kompress'] = 99
            #     print("i... KOMPRESS", config.CONFIG['kompress'] )
            #     #mmwrite(f"zoom 2" ) # not here...

        #---------------- TELEGRAM TEST
        if  request.form.get('telegram') == 'TELEGRAM':
            print("i...  telegram asked  ....... ")
            mmwrite(f"telegram TELEGRAM" )


        # ------------------------------------------------
        if  request.form.get('switch_res_on') == 'SWITCH_RES_ON':
            print("switch-res trig ON")
            xzoom_is_set = True
            mmwrite(f"switch_res True" )
        if  request.form.get('switch_res_off') == 'SWITCH_RES_OFF':
            print("switch-res trig OFF")
            mmwrite(f"switch_res False" )
            xzoom_is_set = False
            #cross_on = True




        # .... save cross x and y inside a file at ~/.config/flashcam/
        with open(crocfg,"w") as f:
            f.write(f"{cross_dx} {cross_dy}")

    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " @cross2 / remote      = "+request.remote_addr, silent=True)
    logthis( " @cross2 / remote xreal= "+remote_ip , silent=True)
    print(f"i...  request @cross :  {request.remote_addr} , xreal={remote_ip}  ")
    url = url_for('video')
    url_bg = url_for('background')
    url_fg = url_for('foreground')
    #time.sleep(0.5)
    return render_template_string(index_page, url=url, url_bg  = url_bg, url_fg  = url_fg)







@auth.verify_password
def verify_password(username, password):
    global remote_ip
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
#    user = User.query.filter_by(username = username).first()
#    if not user or not user.verify_password(password):
#        return False
#    g.user = user
    # config.load_config() # IMPLIES THAT ALL changes in 'bin flask500' are lost
    # config.show_config()
    u = config.CONFIG["user"]
    p = config.CONFIG["password"]
    #u=getpass.getuser()
    #p=u+u
    # try:
    #     with open( os.path.expanduser("~/.pycamfw_pass") ) as f:
    #         print("YES---> FILE  ","~/.pycamfw_pass")
    #         p=f.readlines()[0].strip()
    # except:
    #     print("NO FILE  ","~/.pycamfw_pass")

    if (username==u) and (password==p):
        # logthis( "   TRUE  checking userpass (client)"+username+"/"+password+"/")
        logthis( f" PASS-OK   {request.remote_addr:15s} {remote_ip:15s}: /{u}/{p}/")
        return True
    else:
        logthis( f" PASS-Fail {request.remote_addr:15s} {remote_ip:15s}: /{username}/{password}/")
        print(f"X... {bg.red}{fg.white} WRONG PASS {fg.default}{bg.default} {request.remote_addr:15s} {remote_ip:15s}: /{username}/{password}/" )
        mmwrite(f"baduser {username}" )
        return False




@app.route('/about')
@auth.login_required
def about():
    global remote_ip
    """about page.  Returns html from .config on cam"""
    vmr = get_v_m_r("/dev/video0")
    vmr = vmr.replace(":","_")

    # aboutpage="13d3_56cb_1862.html"
    aboutfilename=f"{vmr}.html"
    path,filen = os.path.split( config.CONFIG['filename'] )
    path = os.path.expanduser( path )


    with open( f"{path}/web/{aboutfilename}") as f:
        aboutpage = f.readlines()

    for i in range(len(aboutpage)):
        if aboutpage[i].find("Example captures")>=0:
            relev = glob.glob( f"{path}/web/{vmr}_*.jpg")

            for j in sorted(relev):
                aboutpage.insert(i+1,f'  <img src="{os.path.basename(j)}"  width="640"  height="480"> {os.path.basename(j)} </img> <hr>\n\n')
    aboutpage = "\n".join( aboutpage )
    print(f"i... sending ABOUT {vmr} ")

    # face = f"web/{vmr}.png" # Face is defined inside HTML - unique JPG filename as the HTML
    return render_template_string(aboutpage  );

    #path,filen = os.path.split( config.CONFIG['filename'] )
    #path = os.path.expanduser( path )
    #return  send_from_directory( f"{path}/web/", aboutpage  )





@app.route('/')
@auth.login_required
def index():
    global remote_ip
    """Video streaming home page."""
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " @index / remote      = "+request.remote_addr, silent=True)
    logthis( " @index / remote xreal= "+remote_ip, silent=True)
    print(f"i...  request @index :  {request.remote_addr} , xreal={remote_ip}  ")

    url = url_for('video')
    print(f"W... ... {request.remote_addr}   {remote_ip}   {url}")
    print(url)
    url_bg = url_for('background')
    url_fg = url_for('foreground')
    return render_template_string(index_page, url=url, url_bg  = url_bg, url_fg  = url_fg)




@app.route('/refresh30')
@auth.login_required
def index30():
    global remote_ip
    """Video streaming home page."""
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " @index30 / remote      = "+request.remote_addr, silent=True)
    logthis( " @index30 /  remote xreal= "+remote_ip, silent=True)
    print(f"i...  request @index30 :  {request.remote_addr} , xreal={remote_ip}  ")
    url = url_for('video')
    print(url)
    url_bg = url_for('background')
    url_fg = url_for('foreground')
    return render_template_string(index_page_refresh30, url=url, url_bg  = url_bg, url_fg  = url_fg)











###################################################
#             ONE FRAME ONLY
#################################################
@app.route('/singleframe.jpg')
@auth.login_required
def one_frame():
    print("i... ******************************* SINGLE FRAME ***********", flush=True)
    camera = Camera()
    print("i... ******************************* SINGLE FRAME ***********", camera, flush=True)
    frame,b_nframes,b_capture_time = camera.get_frame() # This is BaseCamera method, inherited in Camera
    print("i... ******************************* SINGLE FRAME ***********", b_nframes, len(frame), type(frame), flush=True)
    print("i... ******************************* SINGLE FRAME ***********", b_nframes, len(frame), frame.shape, flush=True)
    if not(frame is None):  # 95 is default quality
        #            frame=cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])[1].tobytes()
        COMPR = config.CONFIG['kompress']
        # 480,640 --- print(frame.shape)
        jpg=cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, COMPR])[1].tobytes()
        print("i... ******************************* SINGLE FRAME ********JPG",  type(jpg), flush=True)

    else:
        print("i... ******************************* SINGLE FRAME **NONE*****",  flush=True)
        blackframe = np.zeros((480,640,3), np.uint8)
        jpg=cv2.imencode('.jpg', blackframe )[1].tobytes()
    TTAG = f"{b_nframes:07d}#{b_capture_time}#"
    print(TTAG, 'returning')
    # from foregroung.jpg
    return Response( jpg + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

    return Response( jpg.tobytes() , direct_passthrough= True)

    return (b'--frame\r\n' # ---- JPEG
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n' )# + b'#FRAME_ACQUISITION_TIME#' + TTAG.encode("utf8") )









#
#  all PNG with structure (/about)
#
@app.route('/<regex("[abcdef0-9]{4}_[abcdef0-9]{4}_[abcdef0-9]{4}"):uid>.png')
@auth.login_required
def hexa_png(uid):
    return None
    # global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE
    # print("i...  REGEX PAGE JPG ",uid)
    # print("i...  REGEX PAGE JPG ",uid)
    # blank = np.zeros((480,640,3), np.uint8)
    # frame_fg = blank.copy() # propagate to the system
    # r, jpg = cv2.imencode('.jpg', blank)
    # print("i... NO  - black image",r)

    # path,filen = os.path.split( config.CONFIG['filename'] )
    # path = os.path.expanduser( path )

    # FGFILE=f"{path}/web/{uid}.png"
    # print(f"i... CHECKING EXISTENCE :  {FGFILE}")
    # if os.path.exists( FGFILE):
    #     print(f"i... OPENING :  {FGFILE}")
    #     blank = cv2.imread( FGFILE )
    #     frame_fg = blank.copy() # propagate to the system
    #     r, jpg = cv2.imencode('.jpg', blank)
    #     print(f" {FGFILE} IMAGE FOUND: ",r, frame_fg.shape)
    # else:
    #     print(f"i... PROBLEM OPENING :  {FGFILE}")


    # # send direct JPG
    # return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    # #return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')




#
#  all JPG with structure (/about)
#
@app.route('/<regex("[abcdef0-9]{4}_[abcdef0-9]{4}_[abcdef0-9]{4}"):uid>.jpg')
@app.route('/<regex("[abcdef0-9]{4}_[abcdef0-9]{4}_[abcdef0-9]{4}_[0-9_]+"):uid>.jpg')
@auth.login_required
def hexa_jpg(uid):
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE
    print("i...  REGEX PAGE JPG ",uid)
    print("i...  REGEX PAGE JPG ",uid)
    blank = np.zeros((480,640,3), np.uint8)
    frame_fg = blank.copy() # propagate to the system
    r, jpg = cv2.imencode('.jpg', blank)
    #print("i... NO  - black image",r)

    path,filen = os.path.split( config.CONFIG['filename'] )
    path = os.path.expanduser( path )

    FGFILE=f"{path}/web/{uid}.jpg"
    print(f"i... CHECKING EXISTENCE :  {FGFILE}")

    if os.path.exists( FGFILE):
        print(f"i... OPENING :  {FGFILE}")
        blank = cv2.imread( FGFILE )
        new = blank.copy() # propagate to the system
        new = cv2.resize(new, (640,480) )
        r, jpg = cv2.imencode('.jpg', new)
        print(f" {FGFILE} IMAGE FOUND",r, blank.shape)
    else:
        print(f"i... PROBLEM OPENING :  {FGFILE}")


    # send direct JPG
    print("i... RETURNING JPG:", blank.shape )
    #
    # i cannot return....
    #
    #return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    #
    # this returns img alone
    #
    # TADAAAAAAAAAAAAAAAAAAAAAAAAAAAA  TADAAAAAAAAAAAAAAAAAAA  ON FIREFOX!
    #
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    # THIS WORKS IN BRAvE
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')






#('index.html')
@app.route('/foreground.jpg')
@auth.login_required
def foregroundjpg():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    if os.path.exists( FGFILE):
        blank = cv2.imread( FGFILE )
        frame_fg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD FOREGROUND IMAGE FOUND",r, frame_fg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_fg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO FOREGROUND - black image",r)

    # send direct JPG
    # return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    # <img>
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/foreground')
@auth.login_required
def foreground():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    if os.path.exists( FGFILE):
        blank = cv2.imread( FGFILE )
        # print( blank )
        # # frame_bg = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        frame_fg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD FOREGROUND IMAGE FOUND",r, frame_fg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_fg = blank.copy() # propagate to the system
        #frame = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO FOREGROUND - black image",r)

    # send direct JPG
    return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/background.jpg')
@auth.login_required
def backgroundjpg():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    if os.path.exists( BGFILE):
        blank = cv2.imread( BGFILE )
        frame_bg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD BACKGROUND IMAGE FOUND",r, frame_bg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_bg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO BACKGROUND - black image",r)

    # send direct JPG
    #return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    # jpg direct?
    return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    # with <img>
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/background')
@auth.login_required
def background():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE


    #if not(frame_bg is None):
    #    # print(frame_bg, "BGFRAME")
    #    # # frame = cv2.imdecode(frame_bg, cv2.IMREAD_COLOR)
    #    r, jpg = cv2.imencode('.jpg', frame_bg)
    #    # print("RESPONSE BACKGROUND",r)
    #else:
    if os.path.exists( BGFILE):
        blank = cv2.imread( BGFILE )
        # print( blank )
        # # frame_bg = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        frame_bg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD BACKGROUND IMAGE FOUND",r, frame_bg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_bg = blank.copy() # propagate to the system
        #frame = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO BACKGROUND - black image",r)

    # create mask----------------- appears not usefull-----
    # frame_mask = np.random.randint(2,
    #                                size = (frame_bg.shape[0],frame_bg.shape[1] ),
    #                                dtype=np.uint8) #
    # frame_mask = 255 *np.ones( (frame_bg.shape[0],frame_bg.shape[1] ),
    #                                dtype=np.uint8) #
    # frame_mask[:230,:] = 0
    # frame_mask[-20:-1,:] = 0
    # frame_mask_inv = 255 - frame_mask
    # r, jpg = cv2.imencode('.jpg', frame_mask)

    # send direct JPG
    return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')






######################################################################################
######################################################################################
#
#      PTZ BUT FOR Swann  DVR16-1599    -----------
#
######################################################################################
######################################################################################

def extract_value(data, tag, make_int=False, invert_int=False):
    try:
        root = ET.fromstring(data)
        value = root.find(f'.//{tag}')
        vt = value.text
        if make_int:
            vt = int(vt)
            if invert_int:
                vt = -vt
        if (vt == "0") or (vt == 0):
            return None
        return vt if value is not None else None
    except ET.ParseError:
        return None
    except:
        return None


@app.route('/ISAPI/PTZCtrl/channels/<regex("[1-9]+"):channel>/continuous', methods = ['GET', 'POST', 'PUT'])
@app.route('/ISAPI/System/Video/inputs/channels/<regex("[1-9]+"):channel>/focus', methods = ['GET', 'POST', 'PUT'])
@app.route('/ISAPI/System/Video/inputs/channels/<regex("[1-9]+"):channel>/iris', methods = ['GET', 'POST', 'PUT'])
@app.route('/ISAPI/Image/channels/<regex("[1-9]+"):channel>/ircutFilter', methods = ['GET', 'POST', 'PUT'])
@app.route('/ISAPI/PTZCtrl/channels/<regex("[1-9]+"):channel>/presets/<regex("[1-9]+"):preset>/goto', methods = ['GET', 'POST', 'PUT'])
#  <PTZData><zoom>0</zoom></PTZData>b'<FocusData><focus>-60</focus></FocusData>'
# b'<IrisData><iris>60</iris></IrisData>'
# b'<PTZData><pan>60</pan><tilt>60</tilt></PTZData>'
@auth.login_required

def api_echo(channel=None, preset=None):

    global xzoom_is_set # for xzoom resolution and newpantilt
    global timelaps_ptz # INDEX

    if request.method == 'GET':
        print( "ECHO: GET\n" )

    elif request.method == 'POST':
        print( "ECHO: POST\n")
        for i in request.args.keys():
            print(i)

    elif request.method == 'PATCH':
        print( "ECHO: PACTH\n")

    elif request.method == 'PUT':
        data = request.data.decode('utf-8')
        focus = iris = zoom = pan = tilt = irfilter = None

        preset1 = preset
        if (preset1 is not None) and (type(preset1) is str):
            preset1 = int(preset1)
        if '<FocusData>' in data:
            focus = extract_value(data, 'focus', make_int=True, invert_int=True)
        if '<IrisData>' in data:
            iris = extract_value(data, 'iris', make_int=True)
        if '<IrcutFilter>' in data:
            irfilter =  extract_value(data, 'IrcutFilterType' )
            # irfilter = extract_value(data, 'irfilter')
        if '<PTZData>' in data:
            zoom = extract_value(data, 'zoom', make_int=True)
            pan = extract_value(data, 'pan', make_int=True)
            tilt = extract_value(data, 'tilt', make_int=True)

        if not all(value is None for value in [focus, iris, zoom, pan, tilt, irfilter, preset1]):
            print("_______________________________________________________")
            print(f"  pan      tilt        zoom       iris       focus         irfilter     preset     ")
            print(f"  {pan}     {tilt}       {zoom}      {iris}         {focus}           {irfilter}        {preset1}     ")
            print(f"")

            switchzoom = 0

            if (config.CONFIG["ZoomResolution"]) and (zoom is not None) and (int(zoom) > 0):
                mmwrite(f"switch_res True" )
                print(f"i... {fg.orange} ZOOM IN {fg.default}")
                xzoom_is_set = True
            if (config.CONFIG["ZoomResolution"]) and (zoom is not None) and (int(zoom) < 0):
                mmwrite(f"switch_res False" )
                print(f"i... {fg.orange} ZOOM OUT {fg.default}")
                xzoom_is_set = False

            if (config.CONFIG["ZoomResolution"]) and ((pan is not None) or (tilt is not None)): # ONLY  while in xzoom
                if xzoom_is_set: # ---------- I am in xzoom  mode..... ------
                    print(f"i... {fg.orange} experimental remote ctrl.: arrows {fg.default}")
                    if (pan is not None) and (pan < 0):
                        print("xzoom <-")
                        mmwrite(f"switch_res L" )
                        time.sleep(0.4)
                    if (pan is not None) and (pan > 0):
                        print("xzoom ->")
                        mmwrite(f"switch_res R" )
                        time.sleep(0.4)
                    if tilt is not None and tilt > 0:
                        print("xzoom ^")
                        mmwrite(f"switch_res U" )
                        time.sleep(0.4)
                    if tilt is not None and tilt < 0:
                        print("xzoom v")
                        mmwrite(f"switch_res D" )
                        time.sleep(0.4)

            if (iris is not None):
                if iris > 0:
                    print("iris ^ /expo")
                    mmwrite(f"expo_multiply True" )
                if iris < 0:
                    print("iris v / expo")
                    mmwrite(f"expo_divide True" )
            if (focus is not None):
                if focus > 0:
                    print("focus ^ / gain")
                    mmwrite(f"gain_multiply True" )
                if focus < 0:
                    print("focus v / gain")
                    mmwrite(f"gain_divide True" )
            if (irfilter is not None):
                print("D.... TODO  day night")
                if irfilter == "auto":
                    print("reset iris and focus   / expo and gain")
                    mmwrite(f"gain_setdef True" )
                    time.sleep(0.4)
                    mmwrite(f"expo_setdef True" )


        # print( f"ECHO: PUT    * * * *      preset=={preset}  channel={channel}    ")
        # #print(request.json)
        # print(request.data)
        # #print(f"{request.json=}")
        # #print(f"{request.get_json()=}")
        # print("-------------------- ")

    elif request.method == 'DELETE':
        print( "ECHO: DELETE" )
    return "ok", 200


#   ENTRY POINT OF:                #   /tinycam ANDROID    application/
#   Camera Type:    windows -  webcamxp   jpg ............... ( Better is Swann / DVR16-1500 !!!)
#
@app.route('/ptz')
def ptz_windowsxp():
    """
    PTZ - 2 web variants , one is with real ptz (Crap) 2nd is a trick
    """
    global xzoom_is_set # for xzoom resolution and newpantilt
    global timelaps_ptz # INDEX

    # real time in seconds:
    timelapses = [15, 1, 0] #[0,1,15,60]

    mx = request.args.get('movex')
    my = request.args.get('movey')
    src = request.args.get('src')
    zoom = request.args.get('zoom')
    print(f"i... {fg.yellow}  DX={mx}   DY={my}  SRC={src}  ZOOM={zoom}  {fg.default}")

    # -------------------------------------------- try PTZ HAT, but deprecated.......
    ptz_ok = False
    try:
        pantilthat.show() # get_tilt()
        ptz_ok = True
    except:
        print("D... pt-hat not installed")

    if ptz_ok:
        print(f"i... {fg.white} ptz {fg.default}")
        if my is not None:
            if int(my)<0:
                print("TILT ^ - /ptz")
                if (pantilthat.get_tilt()-1)>=-85:
                    pantilthat.tilt( pantilthat.get_tilt()-1 )
            else:
                print("TILT v - /ptz")
                if (pantilthat.get_tilt()+1)<=-32:
                    pantilthat.tilt( pantilthat.get_tilt()+1 )
        if mx is not None:
            if int(mx)<0:
                print("PAN <- - /ptz")
                if (pantilthat.get_pan()+1)<=90:
                    pantilthat.pan( pantilthat.get_pan()+1 )
            else:
                print("PAN -> - /ptz")
                if (pantilthat.get_pan()-1)>=-90:
                    pantilthat.pan( pantilthat.get_pan()-1 )
    else:
        # ----------------------------------------------------------- CURRENT INTERPRETATION:
        #
        # checking timelaps here.....
        # I dont remember here what is the STATE
        #
        if xzoom_is_set: # ---------- I am in xzoom  mode..... ------
            print(f"i... {fg.orange} experimental remote ctrl.: arrows {fg.default}")
            if mx is not None and int(mx) == -1:
                print("xzoom <-")
                mmwrite(f"switch_res L" )
            if mx is not None and int(mx) ==  1:
                print("xzoom ->")
                mmwrite(f"switch_res R" )
            if my is not None and int(my) > 0:
                print("xzoom ^")
                mmwrite(f"switch_res U" )
            if my is not None and int(my) < 0:
                print("xzoom v")
                mmwrite(f"switch_res D" )
        else:
            print(f"i... {fg.orange} experimental remote ctrl.: dx=-1= laps 0s, 15s {fg.default}")
            #timelaps = 0
            #try:# ..... not sure about states of mx my......
            if mx is not None and int(mx) == -1:
                timelaps_ptz = None
                mmwrite(f"timelaps 0" ) # RESET LAPS
                time.sleep(0.4)
                mmwrite(f"expo_setdef True" ) # RESET EXP

            if mx is not None and int(mx) ==  1:
                if timelaps_ptz is None:
                    timelaps_ptz = 0 # index
                else:
                    timelaps_ptz += 1
                    if timelaps_ptz >= len(timelapses): timelaps_ptz = 0
                settimelaps = timelapses[timelaps_ptz] # real time in seconds
                mmwrite(f"timelaps {settimelaps}" )
                #
            if my is not None and int(my) > 0:
                print(f"i... {fg.orange} EXPO UP {fg.default}")
                mmwrite(f"expo_multiply True" )
            if my is not None and int(my) < 0:
                print(f"i... {fg.orange} EXPO DOWN {fg.default}")
                mmwrite(f"expo_divide True" )

            #except:
            #    pass
            # if mx is not None or my is not None: mmwrite(f"timelaps {timelaps}" )

        switchzoom = 0
        if zoom is not None and int(zoom) > 0:
            mmwrite(f"switch_res True" )
            print(f"i... {fg.orange} ZOOM IN {fg.default}")
            xzoom_is_set = True
        if zoom is not None and int(zoom) < 0:
            mmwrite(f"switch_res False" )
            print(f"i... {fg.orange} ZOOM OUT {fg.default}")
            xzoom_is_set = False

    return "ok", 200



#==================== IN FACT == THIS IS THE START OF THE CAMERA =====  REAL ENTRY @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#==================== IN FACT == THIS IS THE START OF THE CAMERA =====
#==================== IN FACT == THIS IS THE START OF THE CAMERA =====
#==================== IN FACT == THIS IS THE START OF THE CAMERA =====
#==================== IN FACT == THIS IS THE START OF THE CAMERA =====
#==================== IN FACT == THIS IS THE START OF THE CAMERA =====
# with asking Camera()    I create an "instance" (static!) of the class
# and call init_cam
#
# windows  webcamxp ...   jpg  only
##### @app.route('/cam_5.cgi')
@app.route('/video')
# widows / windowsXP /channel dependent
@app.route('/cam_5.jpg')
@app.route('/cam_2.jpg')
@app.route('/cam_3.jpg')
#@app.route('/cam_<int(cam_id):[0-9]{1,2}.jpg>')
@app.route('/cam_<regex("[0-9]+"):uid>.jpg')
# ================ Swann / DVR16-1500
@app.route('/Streaming/channels/<regex("[0-9]+"):uid>01/picture')
@auth.login_required
def video(uid=1):
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    now = dt.datetime.now().strftime("%m/%d %H:%M:%S")
    print(f"W... {now} ... web is asking VIDEO",request.remote_addr, "(",remote_ip,")", end="\n")
    logthis( " /video remote      = "+request.remote_addr, silent=True)
    logthis( " /video remote xreal= "+remote_ip, silent=True)
    print(f"i...  request @video :  {request.remote_addr} , xreal={remote_ip}  ")
    # i return JPG TO AXIS CAMERA....
    #---------------this is MJPEG-------------------------
    #config.CONFIG["product"] = "Webcam C270"
    # return Response(gen(Camera(config.CONFIG["product"], "640x480"),remote_ip),
    # --- i send here the CLASS ?????
    return Response(gen(Camera(),remote_ip),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



#========================================= CAMERA GEN ===
#========================================= CAMERA GEN ===
#========================================= CAMERA GEN === RESPONSE
#========================================= CAMERA GEN ===
#========================================= CAMERA GEN ===

def gen(camera, remote_ip, blend=False, bigtext=True):
    """ returns jpeg;
    MAY do modifications per USER ! BUT any fraME MOD => IS SENT TO ALL!
    can send only some frames
    at the end - it sends an extra info on acq time
    """
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    #print("D... entered gen(), camera = ", camera)
    framecnt = 0
    framecnttrue = 0
    ss_time = 0

    while True:
        time.sleep(0.1)
        framecnt+=1
        #print("D... get_frame (gen)")

        #print("D...  gen() - getframe ... ")
        frame,b_nframes,b_capture_time = camera.get_frame() # This is BaseCamera method, inherited in Camera
        #print("D...  gen() - gotframe  ")

        #print("i... got_frame (gen)", frame.shape )
        start = dt.datetime.now()
        blackframe = np.zeros((480,640,3), np.uint8)
        #frame = blackframe
        if blend:
            frame = 0.5*frame + 0.5*imgs[ random.randint(0,len(imgs)-1) ]

        if cross_on:
            if zoom2_on==1:
                crossonw( frame, cross_dx, cross_dy )
            else:
                crossonw( frame, 0,0  )

        if not(frame is None):  # 95 is default quality
#            frame=cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])[1].tobytes()
            COMPR = config.CONFIG['kompress']
            # 480,640 --- print(frame.shape)
            frame=cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, COMPR])[1].tobytes()
        else:
            continue

        stop = dt.datetime.now()
        ss_time = (stop-start).total_seconds()

        #===== MAYBE THIS IS WASTING - it should throw get_frame
        #  but with -k sync   it restarts

        #timetag = stop.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        #TTAG = f"{framecnt:07d}#{timetag}#"
        TTAG = f"{b_nframes:07d}#{b_capture_time}#"
        # print(TTAG)

        # yield ( frame)  #--------- JPEG vs MJPEG
        yield (b'--frame\r\n' # ---- JPEG
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n' + b'#FRAME_ACQUISITION_TIME#' + TTAG.encode("utf8") )




if __name__ == '__main__':

    print("i... APP RUN FROM WEB.PY")
    #
    #
    #
    #
    app.run(host='0.0.0.0', port=config.CONFIG['netport'], threaded=True)
