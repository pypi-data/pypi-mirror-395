#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
"""
??? I saw an error with this... sudo apt-get install python3-smbus

"""
#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="flashcam",
    description="Composition of scripts to control a web camera",
    url="https://gitlab.com/jaromrax/flashcam",
    author="jaromrax",
    author_email="jaromrax@gmail.com",
    license="GPL2",
    version=get_version("flashcam/version.py"),
    packages=['flashcam'],
    package_data={'flashcam': [

        'data/coders_crux.ttf',
        'data/CONTFO__.ttf',
        'data/CONTF___.ttf',
        'data/CONTFU__.ttf',
        'data/digital-7.mono.ttf',
        'data/digital-7.regular.ttf',
        'data/good_times_rg.otf',
        'data/hemi_head_bd_it.otf',
        'data/OpenSans-BoldItalic.ttf',
        'data/OpenSans-Bold.ttf',
        'data/OpenSans-ExtraBoldItalic.ttf',
        'data/OpenSans-ExtraBold.ttf',
        'data/OpenSans-Italic.ttf',
        'data/OpenSans-LightItalic.ttf',
        'data/OpenSans-Light.ttf',
        'data/OpenSans-Regular.ttf',
        'data/OpenSans-SemiboldItalic.ttf',
        'data/OpenSans-Semibold.ttf',
        'data/pixelFJ8pt1__.TTF',
        'data/PixelFJVerdana12pt.ttf',
        'data/prstartk.ttf',
        'data/prstart.ttf',
        'data/px10.ttf',
        'data/retganon.ttf',
        'data/small_pixel.ttf',
        'data/square_pixel-7.ttf',
        'data/TypographerFraktur-Bold.ttf',
        'data/TypographerFraktur-Contour.ttf',
        'data/TypographerFraktur-Medium.ttf',
        'data/TypographerFraktur-Shadow.ttf',
        'data/Uni_Sans_Heavy_Italic.otf',
        'data/Uni_Sans_Heavy.otf',
        'data/Uni_Sans_Thin_Italic.otf',
        'data/Uni_Sans_Thin.otf',
        'data/visitor1.ttf',
        'data/visitor2.ttf',
        'data/VT323-Regular.ttf',
        'data/BEAM_OFF.jpg',
        'data/BEAM_ON_.jpg',
        'data/DET_NRDY.jpg',
        'data/DET_RDY_.jpg',
        'data/windows.jpg',
        'data/win_rain.jpg',
        'data/win_skull.jpg',
        'data/win_storm.jpg',
        'data/win_winter.jpg',
        'data/ubu_2204.jpg',
        'data/pattern_acircles.png',
        'data/pattern_chessboard.png',
        'data/monoskop.jpg'
    ]},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/flashcam','bin/flashcamg','bin/flashcam_join','bin/flashcam_rep','bin/flashcam_org'],
    install_requires = ['opencv-python','fire','v4l2py','flask_httpauth','gunicorn','numpy','imutils','pandas','matplotlib','psutil','pyserial-asyncio', 'imagezmq','notifator','pyautogui','importlib_resources','requests','pynput','console','pillow','scikit-video', 'tdb_io', 'paho-mqtt','screeninfo'],
)
