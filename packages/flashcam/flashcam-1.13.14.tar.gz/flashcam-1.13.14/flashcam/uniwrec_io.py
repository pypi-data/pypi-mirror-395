import datetime as dt
import socket
import os
import cv2

import getpass
import urllib.request
#import pyautogui
import base64

# ---------- files:
FILE_USERPASS = "~/.config/flashcam/.flashcam_upw"  # will extend
FILE_REDCROSS0 = "~/.config/flashcam/crossred"  # will extend
FILE_REDCROSS = "~/.config/flashcam/crossred"  # will extend



def get_passfile( videodev ):
    """
    only initial part of passfile.... useful for redcross
    """
    if "passfile" in locals():
        if passfile is None:
            print(f"i... nO passfile...trying {videodev} , {passfile}")
            passfile = videodev.strip("http://")
            print("i... TRYING", passfile)
    else:
        passfile = videodev.strip("http://")
        passfile = passfile.strip("/video")
        passfile = passfile.split(":")[0]

        ### WITH A HACK  -  I REDEFINE REDCROSS too
        ###FILE_REDCROSS = f"{FILE_REDCROSS0}_{passfile}.txt"

        # maybe not needed here
        #FILE_REDCROSS = get_FILE_REDCROSS(passfile)

    return passfile




def get_FILE_REDCROSS( videodev ):
    """
    used to save coordinates few times...
    """
    passfile = get_passfile( videodev)
    FILE_REDCROSS = f"{FILE_REDCROSS0}_{passfile}.txt"
    return FILE_REDCROSS




def get_stream( videodev="" ):# , FILE_USERPASS, FILE_REDCROSS,FILE_REDCROSS0 ):
    # global CTRL, SHIFT
    # localuser
    #global FILE_USERPASS, FILE_REDCROSS,FILE_REDCROSS0
    stream = None  # i return
    u, p = getpass.getuser(), "a"

    # this is bug.... never find passfile
    passfile = get_passfile( videodev )
    passfile = f"{FILE_USERPASS}_{passfile}"
    print(f"i... TRYING {videodev} PASSFILE: {passfile}")

    nopass = True
    try:
        with open(os.path.expanduser(passfile)) as f:
            print("YES---> PASSWORD FILE  ", passfile)
            w1 = f.readlines()
            u = w1[0].strip()
            p = w1[1].strip()
            nopass = False
    except:
        print("NO PASSWORD FILE (gs) ")
        nopass = True
    if nopass:
        print("X....  input user pass here...... exiting")
        sys.exit(1)
        #u = pyautogui.prompt("User:")
        #p = pyautogui.prompt("User:")

        with open(os.path.expanduser(passfile), "w") as f:
            f.write(u)
            f.write("\n")
            f.write(p)
            f.write("\n")


    print("D... capturing from: /{}/".format(videodev))
    # cam = cv2.VideoCapture( videodev )
    # stream = urllib.request.urlopen( videodev )

    request = urllib.request.Request(videodev)
    print("D... USER/PASS", u, p)
    base64string = base64.b64encode(bytes("%s:%s" % (u, p), "ascii"))
    print("D... stream ok1", base64string)
    request.add_header("Authorization", "Basic %s" % base64string.decode("utf-8"))

    # request.add_header("Authorization", "Basic %s" % base64string)
    print("D... stream ok2 - request.urlopen (disp)")
    ok = False
    try:
        stream = urllib.request.urlopen(
            request, timeout=3
        )  # timeout to 7 from 5 sec.
        ok = True
        filesource = True
        print("D... stream ok3")
    except urllib.error.HTTPError as e:
        print("Server Offline1? Http error", e)
        print(videodev)
        # do stuff here
    except urllib.error.URLError as e:
        print("Server Offline2?  URL error", e)
        print(videodev)
        # do stuff here
    except:
        ok = False
        stream = None
        print("X.... Timeouted on URLOPEN")

    return stream, u, p







def setupsave(resolution=(640, 480),  videodev="xxx" ):
    sname = "rec"
    sname = videodev
    sname = sname.replace("http", "")
    sname = sname.replace("//", "")
    sname = sname.replace(":", "")
    sname = sname.replace("5000/video", "")
    sname = sname.replace("8000/video", "")

    sfilenamea = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    sme = socket.gethostname()
    sfilenamea = f"{sme}_{sname}_{sfilenamea}"
    #
    # DEFINE EXTENSION : avi+xvid     mov  mp4 mpg
    #   avi+x264
    #
    # sfilenamea = f"{sfilenamea}.mp4"
    # sfilenamea = f"{sfilenamea}.mp4"
    sfilenamea = f"{sfilenamea}.mkv"

    # XVID-works     LAGS   X264    MP4V? mp4v-new,ubu22    IYUV-huge
    CODEC = "mp4v"

    dir2create = os.path.expanduser("~/DATA/")
    if not os.path.isdir(os.path.expanduser(dir2create)):
        print(f"D... trying to create directory {dir2create} for saving")
        # result = False
        os.mkdir(os.path.expanduser(dir2create))

    sfilenamea = os.path.expanduser("~/DATA/" + sfilenamea)
    # codec
    # sfourcc = cv2.VideoWriter_fourcc(*'XVID')
    # ### sfourcc = cv2.VideoWriter_fourcc(*'LAGS') # lossless NOT mkv,avi
    # sfourcc = cv2.VideoWriter_fourcc(*'X264') # +avi small NOTubu22
    # sfourcc = cv2.VideoWriter_fourcc(*'mp4v') # works on UBU22 clean inst
    # ####sfourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # ####sfourcc = cv2.VideoWriter_fourcc(*'IYUV') # huge + avi

    sfourcc = cv2.VideoWriter_fourcc(*f"{CODEC}")  #

    #  25 FPS
    saviout = cv2.VideoWriter(sfilenamea, sfourcc, 25.0, resolution)
    for i in range(4):
        print(f"SAVE={sfilenamea} ---  FOURCC={CODEC}")
    return sfilenamea, saviout
