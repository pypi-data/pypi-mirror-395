#!/usr/bin/env python3
"""
   SUMMARY POST MORTEM SUMMARY ==============================================================
 Motivations:
  1)  I need to receive UDP data on port 81000 : special VG format
      - hpgecontrol
      - nfsrpi
      - iccontrol
  2)  I need to respond with:
      - show the colored image on camera (simplest :  iccontrol)
      - save in influxdb (most IMPORTANT : nfsrpi)
      - control GREGORY (can become critical in long term measurements : hpgecontrol )

  OVERKILL
  3) starts ports 8001-8007 (MAX_PORTS+1) (TCP by default)
  4) see named pipes for 8001-8007 ()
  CALL
  5) process_data - mmwrite to the files defined in cfg.json of flashcam
  N.B.   ## WRITE TO INFLUX COMMENTED!!

  TEMPORARY HACK
  6) listens MQTT  - what TOPICS?
     - TOPIC - some from mminput{widget}_cfg => process_data
     - TOPIC - tele                 => INFLUXDB
     - TOPIC - hpgecontrol/runoff   => NOT DEFINED YET
     - TOPIC - iccontrol/status     => MMWRITE
     - TOPIC - flashcam_daq XXXXX
     - TOPIC - flashcam_cmd XXXXX
     - TOPIC - ALLTOPICS ENABLED....process_data => to flashcam to display
  7) if tele:
     - save to influxdb
 ________________________________________________________________________end of summary _____

INFLUX :
    -    watch_8100 - multi
    -
10/2024  I cannot have calibrations here.... At least in the 1st approximation...
 -  BUT still cfg.json TITLE points out which MQTT-TOPIC is WHERE (index and >10==port5000)


yellow port 81000 ... muolti information from Vadim
green  PIPE
violet MQTT

TESTING 3 VARIANTS:


1. watch -n 10 'echo "iccontrol status= 3 _ rabbit= 21 _ DetPos= -1 _ DGR= 00"  | nc -w 1 -u 127.0.0.1 8100 ;  sleep 3; echo "iccontrol status= 1 _ rabbit= 21 _ DetPos= -1 _ DGR= 00"  | nc -w 1 -u 127.0.0.1 8100 ;  '

2. watch -n 10 'echo "hpgecontrol runonoff=0_runnum=01_rabbit=99_pos=5_name=A1B2C3D4"  | nc -w 1 -u 127.0.0.1 8100 ;   sleep 5; echo "hpgecontrol runonoff=1_runnum=01_rabbit=99_pos=5_name=A1B2C3D4"  | nc -w 1 -u 127.0.0.1 8100 '

3. watch -n 35 'echo  "nfsrpi P1= 0.00E+0 _ P2= 0.00E+0 _ FL= 0.00E+0 _ CU= 0.00E+0 _ SP= 2.00E+0 _ PO= 1.00E+0" | nc -w 1 -u 127.0.0.1 8100'


"""

from fire import Fire
from flashcam.version import __version__
from flashcam.mmapwr import mmwrite # for daq
from console import fg, bg
import os
from flashcam import config
import time
import datetime as dt
#
import tdb_io.influx as influx
import sys
import signal
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import logging
import re
import json



TOPICS = {} # contains all topics for later maping


logging.basicConfig(
    filename=os.path.expanduser("~/flashcam_daq.log"),
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,

)
logger = logging.getLogger(__name__)


"""
The idea is
 1/ to take care about PORTS and PIPES, accept just a number (ideally)
 2/ use cfg.json to understand the number
 3/  PIPE is defined HERE like /tmp/flashcam_fifo_x001 ....
"""

PRIMARY_PORT = None # on startup - port is correct, with load_config - can change
MAX_PORTS = 6 # this is UNO+Shield limit to plugin

def test():
    #cmd_ls( ip = ip,db = i['name'], series="all", qlimit = qlimit, output =output)
    if influx.check_port() :
        print("i... influx port present localy")
        commavalues = "a=1,b=2"
        influx.influxwrite( DATABASE="local", MEASUREMENT="flashcam",
                 values=commavalues,
                 IP="127.0.0.1"
                 )
    sys.exit(0)


def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n



import socket
import threading

def is_float(n):
    if n is None:return False
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


########################################################
#
#   recalculate if flashcam knows the calib system.... TEMP_phid HUMI_phid
#
######################################################3

def recalibrate(d ):#, title ):
    """
    NO RE CALIB  2024 - 10
    d comes as string BUT is sure it is a number; whatever happens, return rounded thing
    """
    res = d
    #newtitle = title
    #logger.info(f"D...RECAL  {d} ... {type(d)}   /{float(d)}/    /{title}/ ")
    #print(f"D... Before : {d}  ->   /{float(d)}/    /{title}/ ")
    # *********************************
    # if title.endswith("TEMP_phid"):
    #     res =  float(d) / 1024* 222.2 - 61.111
    #     if title != "TEMP_phid": newtitle = title.replace("TEMP_phid", "")
    # # ************************************
    # elif title.endswith("HUMI_phid"):
    #     res =  float(d) / 1024* 190.6 - 40.2
    #     if title != "HUMI_phid": newtitle = title.replace("HUMI_phid", "")
    # # ********************************************************************** END
    # else:
    #     res = d
    if len(str(round( float(res), 1))) < 4:
        res = round( float(res), 2)
    else:
        res = round( float(res), 1)
    #print(f"D... After  :  {res}   {type(res)}  ")
    #if newtitle[-1] == "_" and len(newtitle) > 2:
    #    newtitle = newtitle[:-1]
    #logger.info(f"D...RECALfin  {res} ... {newtitle}")
    return res#, newtitle


# #########################################################################
#
#                      Process DATA
#
#   called from    serve_port 8001-8006     and    mqqt_on_message
#
#############################################################################
def process_data(data, index, CAM_PORT, OVR_LABEL=None):  #no OVR_LABEL!~!!!!
    """
10/2024 **** I cannot CALIBRATE HERE>..... just route

    fit the incomming data into the format template
    AND - possibly recalculate raw data :)!
 "mminput1_cfg": "dial xxx;22;28;5;signal1",
 "mminput2_cfg": "dial xxx;22;28;5;dial2",
 "mminput3_cfg": "dial xxx;22;28;5;tacho3",
 "mminput4_cfg": "dial xxx;22;28;5;box4",
 "mminput5_cfg": "sub xxx;22;28;5;title5"

    """
    global PRIMARY_PORT
    # DATA ---------------------------
    d = None
    try:
        d = data.decode('utf8').strip()
    except:
        d = str(data).strip()
    #print(f"i...  {bg.wheat}{fg.black}   receivd: /{d}/  on index /{index}/ CAMPORT={CAM_PORT} {bg.default}{fg.default}")
    #logger.info(f"D...  PDa receivd: /{d}/  on index {index} ")

    # without port - they are normal mminput1 and  mminput1_cfg # ************************
    item_file = f"mminput{index}"
    item_cfg = f"mminput{index}_cfg"

    # ***************2024/10 i display just what index and port say *****************
    #if PRIMARY_PORT != CAM_PORT: # one more set of conncetors defined in config
    #    item_file = f"mminput{index+10}"
    #    item_cfg = f"mminput{index+10}_cfg"

    if not item_file in config.CONFIG:
        print(fg.red, f"X... MMAP file {index} - {item_file} not defined in {config.CONFIG['filename']}  ",  fg.default)
        return
    if not item_cfg in config.CONFIG:
        print(fg.red, f"X... template {index} - {item_cfg} not defined in {config.CONFIG['filename']}  ",  fg.default)
        return

    mmfile = config.CONFIG[ item_file ]
    mmtemplate = config.CONFIG[item_cfg ]

    # ------------------  MMAP file and TEMPLATE defined from here ======================================


    # prepare re calibration, you need to know title/label ....... Also - IF  number => write to INFLUX
    #
    if is_float(d) or is_int(d):
        # extract LABEL/TITLE that is crutial for re calibration
        mytitle = " ".join(mmtemplate.split(" ")[1:]).split(";")[4]

        #if OVR_LABEL is None: # MQTT  override label
        #    #  re calibrate by label
        d = recalibrate( d)#, mytitle ) #  d goes as string returns as float
        #else:
        #    # no recal!
        #    d, newtitle= re calibrate( d, "placeholder" ) #  d goes as string returns as float

        #if OVR_LABEL is not None: newtitle = OVR_LABEL
        #mmtemplate = mmtemplate.replace(mytitle, newtitle ) # FIT THE DATA INTO THE FIELD

        mmtemplate = mmtemplate.replace("xxx", str(d) ) # FIT THE DATA INTO THE FIELD
        #print(f"DEBUG4 {d} ### {mmtemplate} ", flush=True)
        #logger.info(f"D...  mmwrite: {mmtemplate}  ")
        # *******************
        mmwrite( mmtemplate, mmfile, debug=False, PORT_override=CAM_PORT )
        # *******************
        print(f"i... SUCCESS  MMWRITE ----- #{CAM_PORT}#  ", bg.white, fg.black, mmtemplate, fg.default, bg.default)

        # if influx.check_port():
        #     #print("i... influx port present localy")
        #     #if OVR_LABEL is not None: #  override label
        #     #    commavalues = f"{OVR_LABEL}={d}"
        #     #else:
        #     commavalues = f"{mytitle}={d}"
        #         #if CAM_PORT != PRIMARY_PORT: # RE CALIBRATION AND TRUNC Only for main port.....
        #         #    commavalues = f"{mytitle}_{CAM_PORT}={d}"
        #     try:
        #         influx.influxwrite( DATABASE="local",
        #                             MEASUREMENT=f"flashcam{CAM_PORT}",
        #                             values=commavalues,
        #                             IP="127.0.0.1" )
        #         print(f"i... OK      WRITING  INFLUX => DB:flashcam{CAM_PORT}  ")
        #         logger.info(f"D...  PDa  InOK /{commavalues}/  on index {index} ")
        #     except:
        #         logger.info(f"D...  PDa  InXX /{commavalues}/  on index {index} ")
        #         print("X... ERROR  WRITING  INFLUX")

    else:# if not float.... make it a box and dont write INFLUX***************************
        mmtemplate = mmtemplate.replace("xxx", d ) # FIT THE DATA INTO THE FIELD
        mmtemplate = mmtemplate.replace("signal", "box" )
        mmtemplate = mmtemplate.replace("dial", "box" )
        mmtemplate = mmtemplate.replace("tacho", "box" )
        logger.info(f"D...  MMAP  /{mmtemplate}/  on index {index} ")
        # *****************
        mmwrite( mmtemplate, mmfile, debug=False, PORT_override=CAM_PORT )#PRIMARY_PORT) # this is a uniquZ
        #
        print(f"i... SUCCESS  MMWRITE ----- #{CAM_PORT}# noINFLUX ", bg.white, fg.black, mmtemplate, fg.default, bg.default)
    #print("_____________________________________", dt.datetime.now() )
    pass

############################################################3
#
#
#
#
##############################################################

def serve_port( PORT, TCP=True):  # ++++++++++++++++++++++++++++++++++++++++++++ THREAD
    """
    PORTS ********************************
    watch on PORT
    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    s = None
    if TCP:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ok = False
    try:
        s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
        ok = True
    except:
        print(f"X... {bg.orange}{fg.black} DaQ PORT NOT ALLOCATED {PORT} {bg.default}{fg.default} ")

    if not ok:
        try:
            time.sleep(6)
            if TCP:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
            ok = True
        except:
            print(f"X...   {bg.red} DaQ PORT NOT ALLOCATED {PORT} {bg.default} ")

    if not ok: return
    s.listen(5)
    print(f"i...   {bg.blue} Data Acquisition Server started on port {PORT} ;  TCP{TCP} / UDP{not TCP}  {bg.default}")
    while True:


        conn, addr = s.accept() # I hope this is waiting, else 12% of procssor taken by load_config
        with conn:
            data = conn.recv(1024)
            if data:
                config.load_config()
                print(f'i...  {fg.blue}port data Received: {data};  config reloaded{fg.default}')
                # create index in place ; communication port
                process_data(data, PORT - int(PRIMARY_PORT), CAM_PORT=int(PRIMARY_PORT) )


# ************************************************************************
#
# NAMED PIPES
#
# ************************************************************************

def watch_named_fifo(PORT, fifon = '/tmp/flashcam_fifo'):  # ++++++++++++++++++++++++++++++++++++++++++++THREAD
    """
    NAMED PIPES ************
    In client - use `os.path.exists` to check if the named pipe exists and `os.open` with `os.O_NONBLOCK` to check if it's open:
    """
    global PRIMARY_PORT
    fifoname = f"{fifon}_{PORT}"
    print(f"i...   {bg.darkgreen} Data Acquisition PIPE  started on {fifoname}   {bg.default}")
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)
    # Wait for the named pipe to be created
    #while not os.path.exists(fifo):
    #    time.sleep(1)
    with open(fifoname, 'r') as fifo_file:
        while True:
            data = fifo_file.readline().strip() # get what comes to PIPE
            if data:
                index = PORT - int(PRIMARY_PORT)
                logger.info(f"*** fifo-readline data=={data} on PORT {PORT} ")
                print(f'i... {fg.green}named pipe Received: {data} on index {index} {fg.default}')
                publish.single(f"fifo/i{index}", data, hostname="localhost") # PUBLISH; I see the whole takes ~4-5ms

                #config.load_config()
                #
                #process_data(data, PORT - int(PRIMARY_PORT), CAM_PORT=int(PRIMARY_PORT) )
                time.sleep(0.1) # it runs all time.......
            else:
                time.sleep(0.1) # it runs all time.......





# ************************************************************************
#
#                                              MQTT --------------------
#
# ************************************************************************

def extract_numbers(s, topic="flashcam_daq"): # JUST widget and port
    #match = re.match(fr'^{topic}/widget(\d+)port(\d+)([A-Za-z]*)$', s)
    match = re.match(fr'^{topic}/widget(\d+)port(\d+)$', s)
    #print("D... ... matching ", match, s)
    if match:
        num1, num2 = match.groups()
        #print( match.groups() )
        return int(num1), int(num2) #, label if label else "dial"
    return None


# Define the callback for when a message is received
def mqtt_on_message(client, userdata, msg):
    global PRIMARY_PORT
    global TOPICS
    data = msg.payload.decode()
    topic = msg.topic
    #print(f"D... MQTT.Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    #logger.info(f"*** mqtt         data=={data} on /{msg.topic}/ ")
    #print(f"i... MQTT       {fg.violet}Received: {data};  on topic '{msg.topic}' rel-config {fg.default}")

    #print(topic)
    if not topic in TOPICS:
        TOPICS[topic] = None
    #print( "i...  topics#==", len(TOPICS) )

    # thinks around  CONFIG ***********************
    AllTopicsMmapCfg = None # There might be one with all topics "#"
    config.load_config()
    for widget in range(1, 17): # parse all channels to widgets
        key = f"mminput{widget}_cfg"
        if key in config.CONFIG: # mm_cfg is there in cfg ....
            title = config.CONFIG[key].split(";")[-1] # extract Title
            if title == "#": AllTopicsMmapCfg = int(widget)
            #print(title, topic)
            if topic == title: # TOPIC IS IDENTICAL WITH TITLE@FLASHCAM CFG ****

                #print( f"i...  topics#=={len(TOPICS)} total seen,   topic {topic} in cfg.json")
                mmkey = key.split("_")[0]
                mmfile = config.CONFIG[mmkey]
                port = 8000
                if widget > 10: port = 5000
                process_data(data, widget, CAM_PORT=port )

    # aftermath.... ---- LIKE INFLUX SOME SPECIFIC TOPICS -----------------------
    #              ----- REACT ON SOME SPECIFIC TOPICS -------------------------
    if topic.find("tele/") == 0:  # TELEMATIX - SAVE in any case
        if influx.check_port():
            topic2 = topic.split("tele/")[-1]
            #print("i... influx port present localy")
            commavalues = f"{topic2}={data}"
            try:
                influx.influxwrite( DATABASE="local",
                                    MEASUREMENT=f"telematix",
                                    values=commavalues,
                                    IP="127.0.0.1" )
                print(f"i...  {fg.violet}{fg.black}  INFLUX => DB:telematix  {fg.default}{fg.default}")
            except:
                print(f"X... {fg.violet}{fg.black}ERROR  WRITING  INFLUX {fg.default}{fg.default}")

    # HERE I DONT KNOW WHICH CAMERA CAN ACCEPT THIS **********  BEAM ON OFF STATUS
    # what about "#" as a topic?
    if topic.find("iccontrol/status") == 0:  # Special Reaction
        #print(f"D... {bg.green} SCREEN: AllTopicsMmapCfg   {AllTopicsMmapCfg} ... data={type(data)} {data} {bg.default}")
        if AllTopicsMmapCfg is not None: # the number!
            if AllTopicsMmapCfg < 11:
                CAM_PORT = 8000 # BAD THING, HARDCODED
            else:
                CAM_PORT = 5000
            #STARTUP_PORT = int(config.CONFIG['startupport']) # 0 ... original CONFG value OR ZERO if Gunicorn
            #if STARTUP_PORT != 0 and CURRENT_PORT != STARTUP_PORT:
            mmfile = f"{os.path.dirname(config.CONFIG['filename'])}/mmapfile"
            print(f"i... ...                             {bg.cyan}{fg.black}MQTT IC STATUS ==  {data}  Port {CAM_PORT} Index={AllTopicsMmapCfg}{fg.default}{bg.default}")
            if data == str(3):
                mmwrite( f"fixed_image BEAM_ON_.jpg", mmfile, debug=False, PORT_override=CAM_PORT )
            elif data == str(4):
                mmwrite( f"fixed_image BEAM_OFF.jpg", mmfile, debug=False, PORT_override=CAM_PORT )
            elif data == str(1):
                mmwrite( f"fixed_image DET_RDY_.jpg", mmfile, debug=False, PORT_override=CAM_PORT )
            elif data == str(2):
                mmwrite( f"fixed_image DET_NRDY.jpg", mmfile, debug=False, PORT_override=CAM_PORT )
            elif data == str(0):
                mmwrite( f"fixed_image clocks.jpg", mmfile, debug=False, PORT_override=CAM_PORT )
            elif int(data) >  9:
                config.load_config()
                defimg = config.CONFIG['defaultbg']
                mmwrite( f"fixed_image {defimg}", mmfile, debug=False, PORT_override=CAM_PORT )
        else:
            print("X...  NO '#' Title is defined in cfg.json Titles => no BEAMONOFF Screens")

    #
    #  I will not see the NAME and RUN in MQTT
    #
    if topic.find("hpgecontrol/runonoff") == 0:  #  NEW - Send Start/Stop *-----------------
        if data != str(0) and data != str(1):
            print("X...  NO '#' Title is defined in cfg.json Titles => no BEAMONOFF Screens")
        else:
            print(f"i... ...                             {bg.cyan}{fg.black}MQTT manual RUNONONFF ==  {data}  {fg.default}{bg.default}")


    # Show ALL TOPICS - MQTT messages... on "#" ****************************************
    if AllTopicsMmapCfg is not None: # the number!
        key = f"mminput{AllTopicsMmapCfg}_cfg"
        mmkey = key.split("_")[0]
        mmfile = config.CONFIG[mmkey]
        port = 8000
        if AllTopicsMmapCfg > 10: port = 5000
        displtxt = f"{topic} {data}"[:20]
        process_data(displtxt, AllTopicsMmapCfg, CAM_PORT=port )
    return
# **********************************************************************************************
# **********************************************************************************************
# **********************************************************************************************
# **********************************************************************************************
# **********************************************************************************************
# **********************************************************************************************

    if msg.topic.find("flashcam_daq") >= 0:  # numbers for widget and port
        result = extract_numbers(msg.topic, topic="flashcam_daq")     #= 'flashcam_daq/widget3port5000'
        if result:
            widget, port = result
            #print(f"D....    processing widget {widget} to port {port}  ********************************************")
            process_data(data, widget, CAM_PORT=port )      #PORT - int(PRIMARY_PORT))
            pass
        else:
            print(f"X... {fg.red}MQTT Format is NOT widgetXportY {result}  {fg.default}")

    if msg.topic.find("flashcam_cmd") >= 0 and msg.topic.find("status") >= 0:  #  -------------- just get the number HARDCODED BELLOW
        ok = False
        try:
            data = int(data)
            ok = True
        except:
            ok = False
        if not ok: return
        # no help, no cmdline override....
        CAM_PORT = config.CONFIG['netport'] # always 8000
        CAM_PORT = 5000 # BAD THING, HARDCODED
        STARTUP_PORT = int(config.CONFIG['startupport']) # 0 ... original CONFG value is stored here OR ZERO if Gunicorn
        #if STARTUP_PORT != 0 and CURRENT_PORT != STARTUP_PORT:

        mmfile = f"{os.path.dirname(config.CONFIG['filename'])}/mmapfile"
        print(mmfile)
        print(f"i... {bg.white}{fg.black}MQTT from flashcam_cmd ==  {data}  {fg.default}{bg.default}")
        if data == 3:
            mmwrite( f"fixed_image BEAM_ON_.jpg", mmfile, debug=True, PORT_override=CAM_PORT )
        elif data == 4:
            mmwrite( f"fixed_image BEAM_OFF.jpg", mmfile, debug=True, PORT_override=CAM_PORT )
        elif data == 1:
            mmwrite( f"fixed_image DET_RDY_.jpg", mmfile, debug=True, PORT_override=CAM_PORT )
        elif data == 2:
            mmwrite( f"fixed_image DET_NRDY.jpg", mmfile, debug=True, PORT_override=CAM_PORT )


def mqtt_on_disconnect(client, userdata, rc):
    print("Disconnected. Attempting to reconnect...")
    try:
        client.reconnect()
    except Exception as e:
        print(f"Reconnection failed: {e}")


def watch_mqtt(POPO, MACHINE="127.0.0.1", PORT=1883):  # ++++++++++++++++++++++++++++++++++++++++++++THREAD
    """
    MQTT  ************

    """
    fifoname = f"notnow_{PORT}"
    print(f"i...   {bg.violet}{fg.black} Data Acquisition MQTT started on {fifoname}   {bg.default}{fg.default}")

    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the on_message callback
    client.on_message = mqtt_on_message
    client.on_disconnect = mqtt_on_disconnect

    # Connect to the broker
    client.connect( MACHINE, PORT, 60)

    # Subscribe to a topic  ---   standard flashcam AND +++   trick ++++ IMGSWITCH
    client.subscribe("#")
    print(f"i...   {bg.violet}{fg.black} ... MQTT subscribing  ALL  #   {bg.default}{fg.default}")



    #client.subscribe("flashcam_daq/#")
    #print(f"i...   {bg.violet} ... subscribing  flashcam_daq/#   {bg.default}")
    #client.subscribe("flashcam_cmd/#")
    #print(f"i...   {bg.violet} ... subscribing  flashcam_cmd/#   {bg.default}")

    #client.subscribe("telemetrix/#")
    #client.subscribe("telemetix/temp2")

    # Start the loop to procss network traffic and dispatch callbacks
    client.loop_forever()



# ************************************************************************
#
#                                              8100 --------------------
#
# ************************************************************************

#================================================================== SERVER TCP/UDP/========start
def str_is_json(myjson):
    # print("D... my local jsontest:",myjson)
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        print("D... not loadable")
        return False
    return True


def watch_udp_8100():
    """
    echo "ahoj _p1=12_" | nc -u -w 1 127.0.0.1 8100"
    Q=`date +%s.%N` ;echo "merka0 _t=${Q}_p1=123" | nc -u -w 1 127.0.0.1 8100

watch -n 5 'echo  "nfsrpi P1= 0.00E+0 _ P2= 0.00E+0 _ FL= 0.00E+0 _ CU= 0.00E+0 _ SP= 2.00E+0 _ PO= 1.00E+0" | nc -w 1 -u 127.0.0.1 8100'


    """
    UPORT = 8100 # decided long time ago
    print(f"i...   {bg.yellow}{fg.black} Multi-info One-line Acquisition UDP {UPORT}   {bg.default}{fg.black}")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ok = False
    try:
        s.bind(('0.0.0.0', UPORT))  #
        ok = True
    except:
        print(f"X... {bg.orange}{fg.black} UDP {UPORT}  PORT NOT ALLOCATED  {bg.default}{fg.default} ")
    if not ok:
        return
    #s.listen(5)
    print(f"i...   {bg.yellow}{fg.black} Multi-info Data Acquisition Server started on UDP port {UPORT} ;   {bg.default}{fg.default}")

    while True:
        data, address = s.recvfrom(4096)
        data = data.decode('utf8').strip("\n")
        #print(f"{data} @{':'.join([str(i) for i in address])}")
        print(f"{fg.yellow}{fg.black}{data} @{address[0]}{fg.default}{fg.default}" )
        if data.find("nfsrpi") == 0 or \
           data.find("iccontrol") == 0 or \
           data.find("hpgecontrol") == 0:
            #print(fg.green, "recognized", fg.default)
            pass
        else:
            print(fg.red, "X... unknown data; no action", fg.default)
            continue

        measu,*allrest = data.split(" ") # name of measurement - and split
        measu = measu.replace("   ", "")
        measu = measu.replace("  ", "")
        measu = measu.replace(" ", "")

        allrest = "".join(allrest).strip().strip("_")
        allrest = allrest.replace("   ", "")
        allrest = allrest.replace("  ", "")
        allrest = allrest.replace(" ", "")
        allrest = allrest.split("_")
        #print( fg.gray, "allrest==",allrest, fg.default )


        # results contain measurements fo VADIM
        res = '"fields":{' # FULL JSON
        res = ""
        # JOIN ALL VALUES *****************  Joining and publishing  MQTT
        n_flds = 0
        for ar in allrest:
            skip = True
            try:
                var,val = ar.split("=")
                skip = False # no =
            except:
                print(f"X... unable to split /{ar}/  ")
            try:
                #res = f'{res}"{var}":{float(val)},'  # "fields":{ "var":float,
                res = f'{res}{var}={float(val)},'
                n_flds += 1
            except:
                print(f"X... {val} is not possible to interpres as float [udp8100]...")
                skip = True # no float
                pass

            # PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH
            if not skip:
                #print("i... publishing...", measu, var, val)
                #if measu == "iccontrol" and var == "status":
                #    print(f"i... {fg.green}SCREEN!{fg.default}")
                #    publish.single(f"flashcam_cmd/status", val, hostname="localhost") # PUBLISH;
                #else:
                publish.single(f"{measu}/{var}", val, hostname="localhost") # PUBLISH; I see the whole takes ~4-5ms
            # PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH PUBLISH

        #END OF CONSTRUCTION FOR INFLUX*******************
        #res=f'{res[:-1]}' + '}' # FULL JSON
        res=f'{res[:-1]}' # remove comma
        #print(res)
        if influx.check_port():
            #     commavalues = f"{var}={val}"
            try:
                influx.influxwrite( DATABASE="local",
                                    MEASUREMENT=measu, # nfsrpi,icconrol, hpgecontrol
                                    values=res,
                #                    values=commavalues,
                                    IP="127.0.0.1" )
                print(f"i... {fg.yellow}{fg.black}Influx  DB:{measu}{fg.default}{fg.default} ")
                logger.info(f"i... {measu}:  /{res}/  ")
            except:
                logger.info(f"X... {measu}:  /{res}/  ")
                print(f"{fg.red}NoInlfux{fg.default}")

        #     # print(f"i... {var} === {val}")
        # # REMOVE THE LAST COMMA
        # if n_flds < 1:
        #     print("X... NO VALUES TO WRITE TO INFLUX")
        # else:
        #     res=f'{res[:-1]}' + '}'
        #     res = 'influxme [{"measurement":"'+measu+'",'+res+'}]'
        #     # string
        #     r = res.split("influxme ")[-1].strip()
        #     print(f"D... {fg.grey}IFM: {r}{fg.default}" )
        #     #------ this is the last resort. Everything ends with list of dicts
        #     if str_is_json( r[1:-1] ): # check if in inner part of [] is json
        #         # print("D... GOOD , JSON inside")
        #         json_body=json.loads(r[1:-1])  # string loaded
        #         json_body=[json_body,]  # made list item
        #         # return this
        #         print("TO SEND2INFLUX", json_body )
        #     else:
        #         print("X...  NO JSON CREATED")
        #     # sendme=True
        time.sleep(0.01)

# ***************************************************
# ***************************************************
#
#                                               MAIN
#
# ***************************************************
# ***************************************************

def main():
    """
    I have :
    PORTS
    and
    NAMED PIPES
    and
    MQTT

    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    print()
    def signal_handler(sig, frame):
        print("Exiting with signal handler @bin...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


    # ***************************************************************** PORTS
    print("D... daq command - starting servers - start separatelly in FG")
    daq_threads = []
    for i in range(MAX_PORTS ):  # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1 #1-7  resp 8001-8007
        #print(f"D...   starting server {i} - port {P} *****************")
        daq_threads.append( threading.Thread(
            target=serve_port,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads[i].start()

    #***************************************************************** PIPES
    print("D... daq command - starting PIPES - start separatelly in FG")
    daq_threads_FF = []
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1
        #print(f"D...   starting PIPE {i} - port {P} ********************")
        daq_threads_FF.append( threading.Thread(
            target=watch_named_fifo,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads_FF[i].start()

    #print(fg.violet) **************************************************MQTT
    mqtt_thread = threading.Thread(
        target=watch_mqtt,  args=( P, )  )
    mqtt_thread.start()

    print("****************************** all prepared ")

    #print(fg.violet) ************************************************** UDP 8100
    udp_thread = threading.Thread(
        target=watch_udp_8100,  args=(  )  )
    udp_thread.start()

    print("****************************** all prepared ")

    # ************************************************ JOIN ALL AT THE END
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        daq_threads[i].join()
        daq_threads_FF[i].join()
        mqtt_thread.join()
    exit(0)

if __name__ == "__main__":
    Fire(test)
    Fire(main)
