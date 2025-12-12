# Project flashcam

`FLASk powered Hybrid webCAM`

*IN DEVELOPMENT*

## Why

Because any idea can be implemented in the code without a dependence on
a closed source. And there are few ideas implemented by now.

## Start

Production web interface:

``` {.bash org-language="sh"}
export PATH=$PATH:$HOME/.local/bin
export DISPLAY=:0
killall -9 gunicorn
$( sleep 5;flashcam ask;)&
flashcamg
```

Just run on local network, force a port 8000

``` {.bash org-language="sh"}
export PATH=$PATH:$HOME/.local/bin
flashcam flask -n 8000 # -p  00.0-usb-0:1.3:1.0
```

### Select a camera

If there are two or more connected, try `flashcam ls` and select a
proper `IDpath` like `flashcam flask -p 00.0-usb-0:1.3:1.0`.

It is possible to run with two cameras, but with local network mode and
pay attention to MJPG pixelformat and using different ports.

### When config is already fine-tuned for something else

Deactivate blur, accumulate, threshold, telegram, set basic resolution,
another port:

``` {.bash org-language="sh"}
flashcam flask -p clock -a 10 -b 3  -r 640x480 -n 5000 -j False -t 0 -a 0 -b 1
```

## Config

Located at `$HOME/.config.flashcam/cfg.conf` it allows to setup
basically everything.

A lot of options is possible to set and override from commandline.

## Basic scenarios

### Just use

Probably the option `'PIXELFORMAT':'MJPG'` to read physical camera as
mjpg is fine.

### High quality

When trying e.g. for astrophotography, you may prefer
`'PIXELFORMAT':'YUYV'` to read camera without artifacts. While it works
for 640x480, this may not be possible for higher resolution.

### Motion detection

# Technical details

-   *web.py* module is the one that is called by *gunicorn* and provides
    the interface. See *frames()*, where *Camera()* class (defined in
    *real~camera~.py*) is called first.

## Development with pip and uv

Definitely things turned to `uv` and `uvx` from `astral.sh`{.verbatim}

`requirements.txt` is now kept actual, own venv works (`uv venv`;
`uv pip install -r requirements.txt`) and setup should contain correct
info too - `uvx flashcam flask -p win_rain.jpg` works.

This is a big deal because of PEP668.

# Usage

See README.howto.org

# Some references that may or may not be related

<https://longervision.github.io/2017/03/12/ComputerVision/OpenCV/opencv-external-posture-estimation-ArUco-board/>

<https://github.com/LongerVision/Examples_OpenCV/blob/master/01_internal_camera_calibration/chessboard.py>

<https://markhedleyjones.com/projects/calibration-checkerboard-collection>
