#!/usr/bin/env python3
'''
 on https://github.com/TheStaticTurtle/RemoteV4L2-CTL/blob/master/remote_v4l2ctl/utils.py
'''
from flashcam.version import __version__
from fire import Fire
from flashcam import config

#import v4l2py
#from v4l2py import Device

import subprocess as sp

import cv2

import matplotlib.pyplot as plt
import numpy as np
import json

import itertools # duplicite list removeal

import sys


import time # tuning has a delay from camera chip.... oscilates...

import random # i need to skip some tune frames


import math

from console import fg,bg
import datetime as dt

class V4L2_Control:
    """docstring for V4L2_CTL"""

    def is_int(self,n):
        if str(n).find(".")>=0:  return False
        if n is None:return False
        try:
            float_n = float(n)
            int_n = int(float_n)
        except ValueError:
            return False
        else:
            return float_n == int_n


    def is_float(self,n):
        if n is None:return False
        try:
            float_n = float(n)
        except ValueError:
            return False
        else:
            return True


    def __init__(self, control_group, name, addr, type, min=None, max=None, step=None, default=None, value=None, flags="none", access="local", device="/dev/video0", callback=None):
        super(V4L2_Control, self).__init__()
        self.control_group = control_group

        self.name = name
        self.addr = addr
        self.type = type
        self.min = min
        self.max = max
        self.step = step
        self.default = None # was not here...

        # RECOVER  DEFAULTS... SOLVE BOUNDS
        # the cheap sonix camera problem
        if self.is_int(max) and self.is_int(min) and self.is_int(default):
            if (default>max) or (default<min):
                print(f"X... CAM DEF {default} is out of min-max: {min}-{max} /{name}/")
                self.default = self.min
            else:
                self.default = default
        elif self.is_int(default):
            self.default = default


        self.value = value
        self.flags = flags

        self.access = access
        self.device = device
        self.callback = callback

        self.server = None

        #------- i add delay
        self.ctime = dt.datetime.now()


    def setServer(self, server):
        self.server = server

    def get_value(self, a2 = None):
        return self.value

    def get_value01(self, a2 = None):
        res =  (self.value - self.min)/(self.max- self.min)
        # res = 0-1
        # val2 = (math.exp(mul*value)-1)/math.exp(1*mul)
        #mul = 5
        #res = math.log( res* math.exp(mul)  +1 )/mul
        return res

    def get_value01log(self, a2 = None):
        res =  (self.value - self.min)/(self.max- self.min)
        # res = 0-1
        # val2 = (math.exp(mul*value)-1)/math.exp(1*mul)
        mul = 5
        res = math.log( res* math.exp(mul)  +1 )/mul
        return res

    def getmin_value(self):
        return self.min

    def getmax_value(self):
        return self.max

    def setdef_value(self):
        return self.change_value(self.default)

    # uuuuuiiiiiiiiii ---works
    def getdef_value(self):
        return self.default

    # hard way with autoexp
    def set3(self, a2 = None):
        now = dt.datetime.now()
        if (now - self.ctime).total_seconds()>1:
            print(f"X...  Setting 3 IN  {self.name}    {now}")
            self.ctime = now
            return self.change_value(3)
        return None

    def set1(self, a2 = None):
        now = dt.datetime.now()
        if (now - self.ctime).total_seconds()>1:
            print(f"X...  Setting 1 IN  {self.name}     {now}")
            self.ctime = now
            return self.change_value(1)
        return None

    def nonpres(self, a1=None, a2=None):
        print(f" ... ... /{a2}/ control not available")
        return False# elf.change_value(1)

    def change_value01log(self,value, a2 = None):
        #print("D... in value01log", value)
        if self.is_float(value):
            vv = value
            if vv<0: vv =0
            if vv>1: vv= 1
            mul=5 #2.71 # EMPIRICALLY ============5
            val2 = (math.exp(mul*vv)-1)/math.exp(1*mul)
            val2 = val2*(self.max-self.min)+self.min
            #print(" ... ... translates to ", self.name, round(val2,4))
            self.change_value(val2)

    def change_value01(self,value, a2 = None):
        print("D... in value01", value)
        if self.is_float(value):
            vv = value
            if value<0: vv=0
            if value>1: vv=1
            val2 = vv*(self.max-self.min)+self.min
            #print(" ... ... ", self.name, round(val2,4))
            self.change_value(val2)


    def change_value(self, value):
        try:
            if value> self.max:  value = self.max
            if value< self.min:  value = self.min
        except:
            print("X... some problem with minmax not defined, value=", value) # e-a-priority problem
        try:
            value = int(value)
            #print(" ... ... ... ... ",value)
        except Exception as e:
            print("change_value: Invalid input -> " + str(e))
            return -1

        if self.step is not None and value < self.min:
            print("change_value: Value too little", value," x ",self.min)
            return -1

        if self.step is not None and value > self.max:
            print("change_value: Value too big", value," x ",self.max)
            return -1

        if self.step is not None and value % self.step != 0:
            print("change_value: Invalid step number (Steps per " + str(self.step) + ")")
            return -1

        if self.type == "custom":
            if self.callback is not None:
                return self.callback(value)

        if self.access == "local":
            #print("Executing: " + ' '.join(['v4l2-ctl', '-d', self.device, '--set-ctrl=' + self.name + '=' + str(value)]))
            try:
                sp.check_output(['v4l2-ctl', '-d', self.device, '--set-ctrl=' + self.name + '=' + str(value)]).decode("utf-8")
                self.value = value
                time.sleep(0.1) # i want to see a blink ??
                return 0

            except sp.CalledProcessError as e:
                print(
                    "Failed to execute command" +
                    ' '.join(['v4l2-ctl', '-d', self.device, '--set-ctrl=' + self.name + '=' + str(value)]) +
                    " -> "+str(e)
                )
                print("!... you may need apt install v4l-utils")
                print("!... you may need apt install v4l-utils")
                print("!... ALSO - while default reported 0 it may be 1 ..." )
                print("!... you may need apt install v4l-utils")
                return -1
        elif self.access == "remote" and self.server is not None:
            print("Sending remote command: " + self.name + '=' + str(value))
            r = self.server.send_value_set(self.name, value)
            self.value = value
            return r

    def asdict(self):
        return {
            "control_group": self.control_group,
            "name": self.name,
            "addr": self.addr,
            "type": self.type,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "default": self.default,
            "value": self.value,
            "flags": self.flags
        }
    def __repr__(self):
        return str(self)

    def __str__(self):
        out = "V4L2_Control() -> " + self.name + " " + self.addr + " (" + self.type + ")  :  "
        # out += "min=" + str(self.min) + " " if self.min != -99 else ""
        # out += "max=" + str(self.max) + " " if self.max != -99 else ""
        # out += "step=" + str(self.step) + " " if self.step != -99 else ""
        # out += "default=" + str(self.default) + " " if self.default != -99 else ""
        # out += "value=" + str(self.value) + " " if self.value != -99 else ""
        # out += "flags=" + self.flags + " " if self.flags != "none" else ""
        return out





# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------



class V4L2_CTL():
    """docstring for V4L2_CTL... this is what I call from real_camera"""
    def is_int(self,n):
        if n is None:return False
        try:
            float_n = float(n)
            int_n = int(float_n)
        except ValueError:
            return False
        else:
            return float_n == int_n

    def int_or_none(self, ii ):
        if ii is None: return None
        if self.is_int(ii): return int(ii)
        return None



    def __init__(self, device="/dev/video0"):
        super(V4L2_CTL, self).__init__()
        self.device = device
        self.controls = self._list_controls()
        self.capabilities = []
        self.update_capabilities()

        AE = False
        EX = False
        GA = False
        GM = False
        for control in self.controls:
            # print(f"i... {bg.green}{fg.white} {control.name} {fg.default}{bg.default} ")
            #print(control.name)
            setattr(self, "set_" + control.name, control.change_value)
            setattr(self, "getmin_" + control.name, control.getmin_value)
            setattr(self, "getmax_" + control.name, control.getmax_value)
            setattr(self, "setdef_" + control.name, control.setdef_value)
            setattr(self, "get_" + control.name, control.get_value)
            setattr(self, "getdef_" + control.name, control.getdef_value)


            # here I want to extract 4 MAIN controls: *************************
            # autexp - Hard way 3 is always auto
            #
            #   ON PCU22: auto_exposure ... perfect
            #   ON PiU22: exposure_auto + exposure_auto_priority
            #
            if control.name.find("auto")>=0:
                if control.name.find("exposure")>=0: # On PI I see exposure_auto_priority !!!
                    if control.name.find("priority")>=0:
                        #
                        # notime: when auto==1 ... manual operation
                        #
                        print(f"i... {bg.red}{fg.white} {control.name}                   NOT {fg.default}{bg.default} ")
                        # setattr(self, "autoexpo_on", control.set3) # automat=3
                        # setattr(self, "autoexpo_off", control.set1) #manual==1
                        # AE = True

            if control.name.find("auto")>=0:
                if control.name.find("exposure")>=0: # On PI I see exposure_auto_priority !!!
                    if control.name.find("priority")<0:
                        #
                        # notime: when auto==1 ... manual operation
                        #
                        #print(f"i... {bg.blue}{fg.white} {control.name} {fg.default}{bg.default} ")
                        setattr(self, "autoexpo_on", control.set3) # automat=3
                        setattr(self, "autoexpo_off", control.set1) #manual==1
                        AE = True



            # exposure_absolute -     exposure_time_absolute
            if control.name.find("absolute")>=0:
                if control.name.find("exposure")>=0:
                    setattr(self, "expo", control.change_value01log)
                    setattr(self, "expo_get", control.get_value01log)
                    EX = True

            # here I want to extract 4 MAIN controls: *************************
            # gamma -
            if control.name.find("gamma")>=0:
                setattr(self, "gamma", control.change_value01)
                setattr(self, "gamma_get", control.get_value01)
                GM = True

            # here I want to extract 4 MAIN controls: *************************
            # gain -
            if control.name.find("gain")>=0:
                setattr(self, "gain", control.change_value01)
                setattr(self, "gain_get", control.get_value01)
                GA = True

        #------------------------------------------------------------- end for all contr

        empty = V4L2_Control(
                    "empty_control",
                    "w0",
                    "w1",
                    "w3",
                    min=0,
                    max=1,
                    step=1,
                    default=1,
                    value=1,
                    flags="none",
                    device=self.device
                )
        # it will not know its name, sinvce the control is not displaye
        if not AE: setattr(self, "autoexpo_on" , empty.nonpres )
        if not AE: setattr(self, "autoexpo_off", empty.nonpres )
        if not EX:
             setattr(self, "expo"  ,       empty.nonpres )
             setattr(self, "expo_get"  ,       empty.nonpres )
        if not GA: setattr(self, "gain"  ,       empty.nonpres )
        if not GM:
            setattr(self, "gamma" ,       empty.nonpres )
            setattr(self, "gamma_get"  ,       empty.nonpres )



    def get_capbilities_as_json(self):
        return json.dumps([x.asdict() for x in self.controls])

    def get_capbilities(self):
        li = [x.asdict() for x in self.controls]
        ca = []
        for i in li:
            ca.append( i["name"] )
        return ca


    def update_capabilities(self):
        self.capabilities = [x.name for x in self.controls]

    def has_capability(self,what):
        return what in self.capabilities

    def _list_controls(self):
        controls = []
        CMDL = ['v4l2-ctl', '-d', self.device, '-l']
        output = ""
        try:
            output = sp.check_output( CMDL ).decode("utf-8")  # TODO: Check if the output is valid
        except Exception as e:
            print("!... Exception when", CMDL)
            print("!... you may need apt install v4l-utils")
            print("!... you may need apt install v4l-utils")
            print("!... you may need apt install v4l-utils")

        if len(output) <2:
            #print("D... no output, returning")
            return []

        raw_ctrls = [x for x in output.split('\n') if x]  # TODO: Same

        last_control_group = "unknown"
        for raw_ctrl in raw_ctrls:
            if raw_ctrl[0] != ' ':
                last_control_group = ('_'.join(raw_ctrl.split(" ")[:-1])).lower()
                #print("Found new control group: " + last_control_group)
            else:
                # Remove double white spaces
                while "  " in raw_ctrl:
                    raw_ctrl = raw_ctrl.replace("  ", " ")

                raw_ctrl_what, raw_ctrl_values = raw_ctrl.split(":")
                raw_ctrl_what = [x for x in raw_ctrl_what.split(' ') if x and x != ' ']

                values = {
                    "min": None,
                    "max": None,
                    "step": None,
                    "default": None,
                    "value": None,
                    "flags": "none"
                }

                for name, value in [name_value_combo.split("=") for name_value_combo in raw_ctrl_values.split(" ") if
                                    "=" in name_value_combo]:
                    values[name] = value

                ctrlr = V4L2_Control(
                    last_control_group,
                    raw_ctrl_what[0],
                    raw_ctrl_what[1],
                    raw_ctrl_what[2].replace("(", "").replace(")", ""),
                    min=self.int_or_none(values["min"]),
                    max=self.int_or_none(values["max"]),
                    step=self.int_or_none(values["step"]),
                    default=self.int_or_none(values["default"]),
                    value=self.int_or_none(values["value"]),
                    flags=values["flags"],
                    device=self.device
                )

                #print("N..." + str(ctrlr))
                controls.append(ctrlr)


        return controls


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------






def get_gem( cc, capa ):
    # capa = cc.get_capbilities()

    agm = None
    aex = None
    aea = None # auto_exposure (exposure_auto for <ubu22)
    aga = None

    if "gamma" in capa:
        gm = cc.get_gamma()
        gmd = cc.getdef_gamma()
        minm = cc.getmin_gamma()
        maxm = cc.getmax_gamma()
        gm10 = (gm-minm)/(maxm-minm)
        agm = (gm,gmd,minm,maxm,gm10) # gamma, defa, min, max, divided-0-1
        print(f"I... gamma                  {gm:5d}; range({minm:4d},{maxm:5d}) def: {gmd} {gm10:.5f}")

    if "exposure_time_absolute" in capa:
        ex = cc.get_exposure_time_absolute()
        exd=  cc.getdef_exposure_time_absolute()
        mine = cc.getmin_exposure_time_absolute()
        maxe = cc.getmax_exposure_time_absolute()
        ex10 = (ex-mine)/(maxe-mine)
        aex = (ex,exd,mine,maxe,ex10)
        print(f"I... exposure_time_absolute {ex:5d}; range({mine:4d},{maxe:5d}) def: {exd} {ex10:.5f}")

    if "auto_exposure" in capa:
        ea = cc.get_auto_exposure()
        ead=  cc.getdef_auto_exposure()
        minea = cc.getmin_auto_exposure() # I think IT IS 1
        minea = 1
        maxea = cc.getmax_auto_exposure()
        aea = (ea,ead,minea,maxea)
        print(f"I... exposure auto          {ea:5d}; range({minea:4d},{maxea:5d}) def: {ead}")

    # A STRANGE CAMERA
    if "exposure" in capa:
        ex = cc.get_exposure()
        exd=  cc.getdef_exposure_time_absolute()
        mine = cc.getmin_exposure()
        maxe = cc.getmax_exposure()
        gm10 = (ex-mine)/(maxe-mine)
        aex = (ex,exd,mine,maxe,ex10)
        print(f"I...  exposure              {ex:5d}; range({mine:4d},{maxe:5d}) def: {exd} {ex10:.5f}")


    # bad sonix camera- crazy default values...
    if "gain" in capa:
        ming = cc.getmin_gain()
        maxg = cc.getmax_gain()
        ga = cc.get_gain()
        if (ga>maxg)or (ga<ming): ### if bad values
            ga=ming
        gad = cc.getdef_gain()
        if (gad>maxg)or (gad<ming): ### if bad values
            gad=ming
        ga10 = (ga-ming)/(maxg-ming)
        aga = (ga,gad,ming,maxg,ga10)


        print(f"I...  gain                  {ga:5d}; range({ming:4d},{maxg:5d}) def: {gad} {ga10:.5f}")

        # aea - expoauto;  exposure; gain;  gamma
    return aea,aex,aga,agm







# -------- set range 0-1 ---------------
def set_gem(cc, gain=None, expo=None, mmaga=None):

    capa = cc.get_capbilities()
    aea,aex,aga,agm = get_gem(cc, capa)
    if aex!=None: ex,exd,mine,maxe,ex10 = aex  #
    if agm!=None: gm,gmd,minm,maxm,gm10 = agm  #  gamma
    if aga!=None: ga,gad,ming,maxg,ga10 = aga  # gain


    if not "ex" in locals():  return

    print(f"i1... in set_gem: ex={ex}")
    if not expo is None:
        print(f"ix... expo demand {expo}")
        if (expo == "auto"):
            if "exposure_time_absolute" in capa:
                print("D... AUTO EXPOSURE ON")
                cc.setdef_auto_exposure()  # i thik he knows what is auto
        elif expo !=-1:
            if "exposure_time_absolute" in capa:
                if "auto_exposure" in capa:
                    print("D... AUTO EXPOSURE OFF")
                    cc.setdef_auto_exposure() # doesnt do default 3
                    #print("ex def",cc.get_auto_exposure())
                    cc.set_auto_exposure(1)  # I just a guess, 1 may be manual, 3


                    ex = cc.get_exposure_time_absolute()
                    mine = cc.getmin_exposure_time_absolute()
                    maxe = cc.getmax_exposure_time_absolute()
                    print(f"i... current exposure {ex}   range {mine}, {maxe}")

                    if (expo == "def"):
                        cc.setdef_exposure_time_absolute()
                        print("i... new ex= default")
                    else:
                        ex = int( expo * (maxe-mine)+mine)
                        if expo>1: ex+=1
                        if expo<1: ex-=1
                        if ex>maxe: ex=maxe
                        if ex<mine: ex=mine
                        print(f"i... new ex1= {ex};   {expo}")

                    cc.set_exposure_time_absolute(ex)
            # very stupid wabcam
            elif "exposure" in capa:
                ex = cc.get_exposure()
                mine = cc.getmin_exposure()
                maxe = cc.getmax_exposure()
                print(f"i... current exposure {ex}   range {mine}, {maxe}")

                ex = int( expo * (maxe-mine)+mine)
                if expo>1: ex+=1
                if expo<1: ex-=1
                if ex>maxe: ex=maxe
                if ex<mine: ex=mine
                print("i... new ex2= ",ex)

                cc.set_exposure(ex)
            else:
                print("X... exposure_time_absolute NOR exposure not in capacities")

    print(f"i2... in set_gem: ex={ex}")

    if not gain is None:
        if gain == "def":
            if "gain" in capa:
                print("Q... messing with default gain")
                print("Q... messing with default gain")
                cc.setdef_gain()
        elif gain !=-1:
            if "gain" in capa:
                #ga,gad,ming,maxg,ga10
                #ming = cc.getmin_gain()
                #maxg = cc.getmax_gain()
                #ga = cc.get_gain()
                #if (ga>maxg) or (ga<ming):
                #    ga = ming
                print(f"i... current gain {ga}   range {ming}, {maxg}")

                ga = int( gain * (maxg-ming)+ming)
                if gain>1: ga+=1
                if gain<1: ga-=1
                if ga>maxg: ga=maxg
                if ga<ming: ga=ming
                print("i... new ga = ",ga)
                cc.set_gain(ga)
            else:
                print("X... gain noit in capacities")

    #if not mmaga is None: # formelly, but from 2206 - I dont want to play gamma
    # ------------!!!!!!!!!!!------------
    if False: #not mmaga is None:
        if mmaga == "def":
            if "gamma" in capa:
                cc.setdef_gamma()
        elif mmaga !=-1:
            if "gamma" in capa:
                gm = cc.get_gamma()
                minm = cc.getmin_gamma()
                maxm = cc.getmax_gamma()
                print(f"i... current gamma {gm}   range {minm}, {maxm}")

                gm = int( mmaga * (maxm-minm)+minm)
                if gm>maxm: gm=maxm
                if gm<minm: gm=minm
                print("i... new gm= ",gm)

                cc.set_gamma(gm)
            else:
                print("X... gamma not in capacities")

    #------------------------------------------end of function--- SET_GEM








def func(debug = False):

    print("D... in unit unitname function func DEBUG may be filtered")
    print("i... in unit unitname function func - info")
    print("X... in unit unitname function func - ALERT")
    return True


def test_func():
    print("i... TESTING function func")
    assert func() == True








#------------------------------------------------------------------------------------------------

def get_resolutions(vidnum):
    if vidnum >= 0:
        CMD = ['v4l2-ctl', '-d', "/dev/video"+str(vidnum),  "--list-formats-ext"]
        print(f"i... cmd = {CMD}")
        try:
            output = sp.check_output(CMD).decode(
                "utf-8")  # TODO: Check if the output is valid
            output = output.split("\n")
            output = sorted( [ x.split("Discrete ")[-1] for x in output if x.find("Size: Discrete")>0 ])

            output = [tupl for tupl in {item for item in output }]
            output = sorted( output, key = lambda x: int(x.split("x")[0]) * int(x.split("x")[1]) )
        except:
            print("!... you may need apt install v4l-utils")
            print("!... you may need apt install v4l-utils")
            print("!... you may need apt install v4l-utils")
            output = "640x480"
        #o = [ float(o.split("x")[0]+"."+o.split("x")[1]) for o in output]
        # print(output)
    else:
        print("i... vidnum is < 0 ... means jpg file/clock/something else")
        output = ["640x480"]
    mxr = config.CONFIG['Maxresolution']
    mxr2 = int(mxr.split("x")[0])
    newout = []
    for i in output:
        #print(i)
        try:
            x = int(i.split("x")[0])
        except:
            x = 640
        if x<=mxr2:
            newout.append(i)
        else:
            print(f"D... dropping {i} resolution" )
    print("i... new allowed resolutions:",newout)
    return newout






#==================================== WORKS

def tune_histo(cc, h_avg, limitgamma=150):

    glow,ghigh = 16,28

    dg= (ghigh-glow)/2
    med = (ghigh+glow)/2

    if (h_avg>=glow) and (h_avg<=ghigh):
        return
    h_avg= int(h_avg)

    dist = (h_avg- med)/dg # distance in #of sigma
    if abs(dist)<=1:
        return

    capa = cc.get_capbilities()
    aea,aex,aga,agm = get_gem(cc, capa)
    if aex!=None: ex,exd,mine,maxe,ex10 = aex
    if agm!=None: gm,gmd,minm,maxm,gm10 = agm
    if aga!=None: ga,gad,ming,maxg,ga10 = aga


    ok = False
    if dist<-1:
        if (ex<0.2) and(random.randint(0,10)<7): # I skip   frames to stop oscilation
            return
        if aex!=None:
            if ex10<1:
                set_gem(cc, expo=ex10*1.01+0.001)
                ok = True
        if not ok:
            if aga!=None:
                if ga10<1:
                    set_gem(cc, gain=ga10*1.01+0.001)
                    ok = True

    if dist>1:
        if (ex10<0.2) and (random.randint(0,10)<2): # I skip   frames to stop oscilation
            return
        if aex!=None:
            if ex10>0:
                set_gem(cc, expo=ex10*0.99-0.001)
                ok = True
        if not ok:
            if aga!=None:
                if ga10>0:
                    set_gem(cc, gain=ga10*0.99-0.001)
                    ok = True


    # time.sleep(0.2)
    return

    # 48 - 20 = 28;  28/4 ... 6x
    maxg,gg,ming = 2,1,0
    gg,mg,ex = 0,0,0
    defg,defm = 0,0
    maxe,ex,mine = 500,100,100
    maxg,ex,minm = 500,100,100
    maxm,ex,minm = 500,100,100

    if "gain" in capa:
        gg = cc.get_gain()
        maxg = cc.getmax_gain()
        ming = cc.getmin_gain()

    if "gamma" in capa:
        mg = cc.get_gamma()
        maxm = cc.getmax_gamma()
        minm = cc.getmin_gamma()
        defm = cc.getdef_gamma()
        maxm = limitgamma # terrible result if too much


    if "exposure_time_absolute" in capa:
        ex = cc.get_exposure_time_absolute()
        mine = cc.getmin_exposure_time_absolute()
        maxe = cc.getmax_exposure_time_absolute()


    if dist<-1:
        if "auto_exposure" in capa:
            auto_exposure = cc.get_auto_exposure()
            #if auto_exposure!=1:
            cc.set_auto_exposure(3)
        else:
            print("X... cannot tune the exposure (no auto)")
            return
        return

    elif dist>4:
        FAC = 0.5
    elif dist>3:
        FAC = 0.7
    elif dist>2:
        FAC = 0.9
    elif dist>1:
        FAC = 0.98
    #print(FAC)
    #print(FAC)
    # no caf     CAF = 1/FAC

    # CAF = 1/FAC_BASE # I override the speed from bottom to up

    print(f"i...  {med} +- {dg}  <{h_avg}>  {dist:4.1f}sigma  {FAC:5.2f}x")


    if "exposure_time_absolute" in capa:
        exposure_time_absolute = cc.get_exposure_time_absolute()
        if exposure_time_absolute!=1:
            cc.set_auto_exposure(1)
    else:
        print("X... cannot tune the exposure (no auto)")
        return


    gg2,ex2,mg2 = gg,ex,mg

    #print(f"                   {ming} - {gg} - {maxg} ; {mine}-{ex}-{maxe} ")
    if h_avg<glow: #------------------ increase
        ex2 = int(FAC*ex)
        gg2 = int(FAC*gg)
        mg2=mg # tune separate
        #mg2 = int(1.1*mg)
        #print(f"increasing {ex} to {ex2}")
        if gg2==gg:
            gg2+=1
        #if mg2==mg:
        #    mg2+=1
        if ex2==ex:
            ex2+=1
        #print(f"increasing {ex} to {ex2}")
    elif h_avg>ghigh:
        ex2 = int(FAC*ex)
        gg2 = int(FAC*gg)
        mg2 = defm # int(0.9*mg)
        if gg2==gg:
            gg2-=1
        #if mg2==mg:
        #    mg2-=1
        if ex2==ex:
            ex2-=1

    gg,ex,mg = gg2,ex2,mg2


    if gg>maxg: gg=maxg
    if gg<ming: gg=ming

    if ex>maxe: ex=maxe
    if ex<mine: ex=mine

    if (ex==maxe) and (gg==maxg):
        print("!... on max")
        mg2=mg
        if h_avg<glow: #------------------ increase
            print("inc gamma now")
            mg2 = int(1.1*mg)
            #print(f"increasing {mg} to {mg2}")
            if mg2==mg:
                mg2+=1
            if mg2>maxm: mg2=maxm
            if mg2<minm: mg2=minm
    else:
        mg2=defm





    #print(f"                   gain {gg}  expo {ex} gamma {mg} ")
    #print(f"                   gain {gg}  expo {ex} gamma {mg} ")
    print(f"        gain {gg} ({ming}/{maxg})  expo {ex} ({mine}/{maxe}) gamma {mg} ({minm}/{maxm}) ")
    time.sleep(0.6)

    if "exposure_time_absolute" in capa: cc.set_exposure_time_absolute(ex)
    if "gain" in capa: cc.set_gain(gg)
    if "gamma" in capa: cc.set_gamma(mg2)

    # if gg>maxg:
    #     if h_avg<glow:
    #         ex+=2
    #         cc.set_exposure_time_absolute(ex)
    #     elif h_avg>ghigh:
    #        gg-=2
    #        if "gain" in capa: cc.set_gain(gg)
    # elif gg<ming:
    #     if h_avg>ghigh:
    #        ex-=2
    #        cc.set_exposure_time_absolute(ex)
    #     if h_avg<glow:
    #        gg+=2
    #        if "gain" in capa: cc.set_gain(gg)
    # else:
    #     if h_avg<glow:
    #         gg+=2
    #         if "gain" in capa: cc.set_gain(gg)
    #     elif h_avg>ghigh:
    #         gg-=2
    #         if "gain" in capa: cc.set_gain(gg)
    #res = cc.set_exposure_time_absolute(ex)
    return gg,ex


def old_main( devid ):
    """
    Here it is a test to set exposure and gain by histogram
    """
    #cam = Device.from_id(0)
    #print( cam.info)
    #print()
    #print(cam.video_capture.get_format())
    cc = V4L2_CTL("/dev/video"+str(devid))
    vid = cv2.VideoCapture(devid)


    lw=1
    bins=256

    initme = True
    gain = 100
    capa = cc.get_capbilities()

    if "auto_exposure" in capa:
        print("D... AUTO EXPOSURE OFF")
        cc.setdef_auto_exposure() # doesnt do default 3
        print("i... v4l... ex def",cc.get_auto_exposure())
        cc.set_auto_exposure(1)

    #print("ex 3",cc.get_auto_exposure())
    if "gain" in capa:
        cc.setdef_gain()
        gg = cc.get_gain()
        print("defgain ",gg)

    if "exposure_time_absolute" in capa:
        ex = cc.get_exposure_time_absolute()
        cc.setdef_exposure_time_absolute()

    gain= 0

    #create two subplots
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    lineGray, = ax2.plot(np.arange(bins), np.zeros((bins,1)), c='r', lw=lw)
    ax2.set_xlim(-10, bins + 10)

    while(True):# https://github.com/nrsyed/computer-vision/blob/master/real_time_histogram/real_time_histogram.py
        #print(" ... gain,  exposure   ",cc.get_gain(), cc.get_exposure_time_absolute() )

        ret, frame = vid.read()
        # if initme:

        #     #ax2.set_ylim(0, 1)
        #     ax1.set_axis_off()
        #     ax2.spines['right'].set_visible(False)
        #     #ax.spines['bottom'].set_visible(False)
        #     ax2.spines['left'].set_visible(False)
        #     #ax2.set_axis_off()

        #     #create two image plots
        #     im1 = ax1.imshow(frame)

        #     #im2 = ax2.imshow(frame)
        #     #plt.autoscale(enable=True, axis='x', tight=True)
        #     #ax1 = plt.gca()  # only to illustrate what `ax` is
        #     #ax1.autoscale(enable=True, axis='both', tight=True)
        #     #ax2.autoscale(enable=True, axis='both', tight=True)
        #     plt.rcParams['axes.xmargin'] = 0
        #     plt.rcParams['axes.ymargin'] = 0
        #     plt.ion()
        #     ####print("i... plt show")
        #     #plt.show()
        #     #plt.pause(0.01)
        #     initme = False

        framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([framegray], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hist /= hist.sum()

        #h_avg = (hist*np.arange(bins)).sum()
        #h_std = ((hist*np.arange(bins)*np.arange(bins)).sum())**0.5


        #------------------ https://stackoverflow.com/questions/9390592/drawing-histogram-in-opencv-python
        #h = np.zeros((300,256,3))
        h = np.zeros((480,640,3))
        h = frame.copy()
        #h = np.flipud(h)

        BINS = 64
        bins = np.arange(BINS).reshape(BINS,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]

        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([frame],[ch],None,[BINS],[0,255])
            cv2.normalize(hist_item,hist_item, 0, 255, cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_item))
            pts = np.column_stack((bins*int(640/BINS),480-(hist*480/255).astype(int)))
            cv2.polylines(h,[pts],False,col)

        framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([framegray], [0], None, [BINS], [0, 255])
        cv2.normalize(hist_gray,hist_gray,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_gray))
        pts = np.column_stack((bins*int(640/BINS),480-(hist*480/255).astype(int)))
        cv2.polylines(h,[pts], False,  [255,255,255], thickness= 2 )


        #h=np.flipud(h)

        cv2.imshow('colorhist',h)
        #cv2.waitKey(1)


        #gg,ex = tune_histo(cc, h_avg)
        #print(f" g={gg} e={ex}   {h_avg:.1f} ({h_std:.1f}) ", end = "\r" )


        #im1.set_data(frame)
        #lineGray.set_ydata(hist)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def mk_table(cc):
    # -------------------------------------- NICE TABLE PRINT -----------
    capa = cc.get_capbilities()

    print("_"*77)
    for i in capa:
        if i in ["contrast","saturation","hue","power_line_frequency","sharpness","brightness"]: continue
        mi = getattr(cc,f"getmin_{i}")()
        ma = getattr(cc,f"getmax_{i}")()
        de = getattr(cc,f"getdef_{i}")()
        va = getattr(cc,f"get_{i}")()

        mi = "    ~" if mi is None else f"{mi:6d}"
        ma = "    ~" if ma is None else f"{ma:6d}"
        de = "    ~" if de is None else f"{de:6d}"
        va = "    ~" if va is None else f"{va:6d}"

        #print( type(mi) )
        #ma = i.getmax_value()
        #de = i.getdef_value()
        print(f"{i:30s} ... {mi:6s}   {va:6s} ({de:6s})    {ma:6s}")

    print("_"*77)
    # -------------------------------------- NICE TABLE PRINT -----------


def main( devid = 0 ):
    """
    Here it is a test of class


    # very stupid camera    ZC0303 Webcam  ... only exposure!


    """
    cc = V4L2_CTL("/dev/video"+str(devid))

    mk_table(cc) # controls
    res = get_resolutions(devid)
    print(res)

    return
    cc.autoexpo_on("autoexpo")

    vid = cv2.VideoCapture(devid)
    cnt = 0
    while(True):
        cnt+=1
        ret, frame = vid.read()

        if cnt%40 == 0:
            ra = random.uniform(0,1)
            print("\n\n", round(ra,3) )

            cc.autoexpo_off( "autoexpo")
            a = cc.expo_get( 'expo_get')     # 0-1 log
            print("1I found exposure === ", a)
            cc.expo( ra ,'expo')     # 0-1 log
            a = cc.expo_get( 'expo_get')     # 0-1 log
            print("2I found exposure === ", a)
            cc.gamma( ra ,'gamma' )     # 0-1 log
            #print("gain...")
            cc.gain( ra , 'gain'  )     # 0-1 log
            mk_table(cc)

        if cnt%200 == 0:
            cc.autoexpo_on("autoexpo")
            print("ON")

        if cnt%200 == 100:
            cc.autoexpo_off("autoexpo")
            print("OFF")

        cv2.imshow('colorhist',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cc.autoexpo_on("autoexpo")
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("i... in the __main__ of unitname of flashcam")
    Fire(main)
