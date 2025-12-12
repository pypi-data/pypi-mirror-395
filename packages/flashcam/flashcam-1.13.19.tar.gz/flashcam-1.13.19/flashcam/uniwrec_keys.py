#!/usr/bin/env python3

# NOT IN UBUNTU22
def kb_on_press(key, SHIFT=False, CTRL=False):
    """
NOT USED????
    """
    #global SHIFT, CTRL
    print("                                              =v=")
    try:
        a = key.char
        # print('alphanumeric key {0} pressed'.format( key.char))
        # CTRL  = False
    except AttributeError:
        print('special key {0} pressed'.format(  key))
    if key == Key.alt:
        CTRL = True
    if key == Key.shift:
        SHIFT = True
    return SHIFT, CTRL

# NOT ON UBUNTU22
def kb_on_release(key, SHIFT, CTRL):
    """
    NOT USED
    """
    #global SHIFT, CTRL
    print("                                              =^=")
    if key == Key.alt:
        CTRL = False
    if key == Key.shift:
        SHIFT = False
    print('{0} released'.format( key))
    if key == Key.esc:
        # Stop listener
        return False, False # NOT USED
    return SHIFT, CTRL


def remap_keys(key, CTRL=False):
    """
    Problem - THIS TABLE WORKS ON  gigajm
        , while zen : 65505
    """
    #global CTRL
    CTRL=False
    print(f" ... remap_keys()1  KEY==/{key}/  ", CTRL)
    if key>=262241 and key<=262266:CTRL=True  # zen
    if key>=1310817 and key<=1310842:CTRL=True # zaba

    print(f" ... remap_keys()2  KEY==/{key}/  ", CTRL)
    table = {
        262241: "a", # zen ctrl
        262242: "b", # zen ctrl
        262243: "c", # zen ctrl
        262244: "d", # zen ctrl
        262245: "e", # zen ctrl
        262246: "f", # zen ctrl
        262247: "g", # zen ctrl
        262248: "h", # zen ctrl
        262249: "i", # zen ctrl
        262250: "j", # zen ctrl
        262251: "k", # zen ctrl
        262252: "l", # zen ctrl
        262253: "m", # zen ctrl
        262254: "n", # zen ctrl
        262255: "o", # zen ctrl
        262256: "p", # zen ctrl
        262257: "q", # zen ctrl
        262258: "r", # zen ctrl
        262259: "s", # zen ctrl
        262260: "t", # zen ctrl
        262261: "u", # zen ctrl
        262262: "v", # zen ctrl
        262263: "w", # zen ctrl
        262264: "x", # zen ctrl
        262265: "y", # zen ctrl
        262266: "z", # zen ctrl


        1310817: "a", #ctrl zaba
        1310818: "b", #ctrl zaba
        1310819: "c", #ctrl zaba
        1310820: "d", #ctrl
        1310821: "e", #ctrl
        1310822: "f", #ctrl zaba
        1310823: "g", #ctrl zaba
        1310824: "h", #ctrl zaba
        1310825: "i", #ctrl zaba
        1310826: "j", #ctrl zaba
        1310827: "k", #ctrl zaba
        1310828: "l", #ctrl zaba
        1310829: "m", #ctrl zaba
        1310830: "n", #ctrl zaba
        1310831: "o", #ctrl zaba
        1310832: "p", #ctrl zaba
        1310833: "q", #ctrl zaba
        1310834: "r", #ctrl zaba
        1310835: "s", #ctrl zaba
        1310836: "t", # ctrl
        1310837: "u", # ctrl
        1310838: "v", # ctrl
        1310839: "w", # ctrl
        1310840: "x", # ctrl
        1310841: "y", # ctrl
        1310842: "z", # ctrl

        1114175: "?", # zaba
        65599: "?", # zen

        1048673: "a",
        1048674: "b",
        1048675: "c",
        1048676: "d",
        1048677: "e",
        1048678: "f",
        1048679: "g",
        1048680: "h",
        1048681: "i",
        1048682: "j",
        1048683: "k",
        1048684: "l",
        1048685: "m",
        1048686: "n",
        1048687: "o",
        1048688: "p",
        1048689: "q",
        1048690: "r",
        1048691: "s",
        1048692: "t",
        1048693: "u",
        1048694: "v",
        1048695: "w",
        1048696: "x",
        1048697: "y",
        1310841: "y", #ctrl
        1048698: "z",
        1114177: "A",
        1114178: "B",
        1114179: "C",
        1114180: "D",
        1114181: "E",
        1114182: "F",

        65601: "A", # zen
        65602: "B", #zen
        65603: "C", # zen
        65604: "D",
        65605: "E",
        65606: "F", # zen
        65607: "G",
        65608: "H",
        65609: "I",
        65610: "J",
        65611: "K",
        65612: "L",
        65613: "M",
        65614: "N",
        65615: "O",
        65616: "P",
        65617: "Q",
        65618: "R",
        65619: "S",
        65620: "T",
        65621: "U",
        65622: "V",
        65623: "W",
        65624: "X",
        65625: "Y",
        65626: "Z",

        1114183: "G",
        1114184: "H",
        1114185: "I",
        1114186: "J",
        1114187: "K",
        1114188: "L",
        1114189: "M",
        1114190: "N",
        1114191: "O",
        1114192: "P",
        1114193: "Q",
        1114194: "R",
        1114195: "S",
        1114196: "T",
        1114197: "U",
        1114198: "V",
        1114199: "W",
        1114200: "X",
        1114201: "Y",
        1114202: "Z",
    }
    # 1.  I deactivate ALL above keys to avoid duplicity for arrows etc...
    #
    #
    # 2. I use these ctrl-
    # ctrle     1310821:''
    # (key == 1310823): # ctrlg
    #         1310841): #ctrly
    # ctrla

    # ####return table[key]
    keynew = None
    if key in table:
        keynew = ord(table[key])
        # keynew = table[key]
        print(f"D... @remaping-keys: {key} -> {chr(keynew)}  (ctrl=={CTRL})")
        # #return keynew
    else:
        keynew = key
    return keynew, CTRL
