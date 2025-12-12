#!/usr/bin/env python3


from flashcam.version import __version__
from fire import Fire
from flashcam import config
import os

import mmap
import time
import sys

MMAPFILE = os.path.expanduser("~/.config/flashcam/mmapfile")
MMAPSIZE = 1000

# -------------------------------------------------------------------------

def mmcreate(filename=MMAPFILE, add_port=False):#, PORT_override=None):
    """
    Two variants * things:
    1/ just create nonexisting file (PORT is already there)
    2/for widgets - distinguish by PORT
    """
    # # PORT should be known here I hope
    PORT=config.CONFIG['netport']
    if add_port:
        filename1 = f"{os.path.expanduser(filename)}{PORT}"
    # #if os.path.exists(filename1):
    # #    os.remove(filename1)

    filename1 = filename
    print(f"*********{filename1}***************")
    with open(filename1, "w") as f:
        f.write("-"*MMAPSIZE)
    if add_port:
        return PORT


def mmwrite(text, filename = MMAPFILE, debug=False, PORT_override=None):
    """
    write text to filename
    """
    # PORT should be known here I hope
    if PORT_override is None:
        PORT=config.CONFIG['netport']
    else:
        PORT = PORT_override
    filename1 = f"{os.path.expanduser(filename)}{PORT}"

    # --- no ports now - filename1 IS FIXED..........
    if not os.path.exists(filename1):
        print(f"W...   {filename1} no found ... creating now. ")
        mmcreate(filename1 )#, PORT_override=PORT_override )
    else:
        file_size = os.path.getsize( filename1 )
        if file_size!=MMAPSIZE:
            print(f"X... File Size IS== {file_size}, should be {MMAPSIZE} ")
            sys.exit(0)

    with open(filename1, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            if debug:
                print(f"D... (mmap) WRITING: {text}  # {str(text).encode('utf8')}   ==> {filename1}")
            mmap_obj.write(str(text).encode("utf8") )  # 2ms
            mmap_obj.flush()





# -------------------------------------------------------------------------

def mmread(filename = MMAPFILE, PORT_override=None):
    """
TO DEBUG ONLY
    """
    # PORT should be known here I hope
    if PORT_override is None:
        PORT=config.CONFIG['netport']
    else:
        PORT = PORT_override
    filename1 = f"{os.path.expanduser(filename)}{PORT}"

    print(filename1)
    print(filename1)
    print(filename1)
    print(filename1)
    print(filename1)
#    with open(filename, mode="r", encoding="utf8") as file_obj:
#        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
#            text = mmap_obj.read()
#            print("READTEXT =",text)

    with open(filename1, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            text = mmap_obj.read().decode("utf8").strip()
            print(text)
            print(text)
            print(text)
            print(text)
            return text



def mmread_n_clear(  filename = MMAPFILE , PORT_override=None):
    """
    read and clear  filename
    """
    # PORT should be known here I hope
    if PORT_override is None:
        PORT=config.CONFIG['netport']
    else:
        PORT = PORT_override
    filename1 = f"{os.path.expanduser(filename)}{PORT}"
    #    PORT=config.CONFIG['netport']
    #    filename1 = f"{os.path.expanduser(filename)}{PORT}"

    # print("D... MMRC")
    if os.path.exists(filename1):
        file_size = os.path.getsize( filename1 )
        if int(file_size) != int(MMAPSIZE):
            print(f"! File Size  {filename1} == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size  {filename1} == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size  {filename1} == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size  {filename1} == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size  {filename1} == {file_size}, should be {MMAPSIZE}")
            os.remove( filename1 )
            #sys.exit(0)
            mmcreate(filename)

    if not os.path.exists(filename1):
        print( f"xxxxxx ... {filename1} not found... creating now.")
        mmcreate(filename1)
        #return  "xxxxxx","1"


    with open(filename1, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            text = mmap_obj.read().decode("utf8").strip()
            # print("READTEXT: ",text)


            # execute(text.decode("utf8"))
            if text[0] == chr(0): # "*":
                response = "xxxxxx","1"
            elif chr(0) in text:
                # AHAAAAAA - I need to have at least some *
                response = text.split( chr(0) )[0]
                if len(response.split())>1:
                    spl01 = response.split()[0].strip()
                    spl02 = " ".join(response.split()[1:])
                    spl02 = spl02.strip()
                    response = f"{spl01}",f"{spl02}"
                    print("i... mmapread'nclear returning ", response)
                else:
                    response = "xxxxxx","1"
            else:
                response = "xxxxxx","1"

                # print("i... mmapread'nclear returning ", response)
                # print("i... mmapread'nclear returning ", response)

            # ------------------ this is strange: short *** block some longer texts to be disp
            #text = "*"*990
            text = chr(0)*990
            # print("CLEARING: ",text)



            mmap_obj[:MMAPSIZE] = str(" "*MMAPSIZE).encode("utf8")
            mmap_obj[:len(text)] = str(text).encode("utf8")
            mmap_obj.flush()
            return response
# -------------------------------------------------------------------------

if __name__ == "__main__":
    Fire(mmwrite)
    print("... finished ")
    # time.sleep(2)
