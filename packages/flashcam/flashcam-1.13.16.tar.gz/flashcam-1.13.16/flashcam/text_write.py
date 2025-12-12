
#!/usr/bin/env python3

#from fire import Fire
from flashcam.version import __version__
import os
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import sys

#  Code:  ttfname, FSize(pt), KERN, FHieght, FWidth
#Fheight=>shiftUP txt by it
# default  10,0,10,5
fonts_available = {
    "s8":["small_pixel.ttf",8,0,7,5],
    "s6":["small_pixel.ttf",6,0,6,5],
    "pr":["prstartk.ttf",6,-1,6,5],
    "pr4":["prstartk.ttf",10,-1,10,9],
    "fj":["PixelFJVerdana12pt.ttf",4,0,6,5],
    "fj6":["PixelFJVerdana12pt.ttf",6,0,12,6],
    "re":["retganon.ttf",12,0,9,4],
    "p8":["pixelFJ8pt1__.TTF",8,0,6,5] ,
    "p7":["pixelFJ8pt1__.TTF",7,0,6,5] ,
    "ty":["TypographerFraktur-Medium.ttf",14,0,16,7],
    "v1":["visitor1.ttf",10,0,7,5],
    "v14":["visitor1.ttf",14,0,10,7 ],
    "v18":["visitor1.ttf",18,0,13,9 ],
    "v2":["visitor2.ttf",12,0,6,5],
    "co":["coders_crux.ttf",16,-1,7,5],
#    "ji":["JikiTourai.ttf",10,0,10,6],
#    "ca":["Caracas.ttf",10,0,10,7],
#    "sa":["SAIBA-45.ttf",12,0,10,7],
#    "ni":["NimbusMono-Regular.otf",12,0,9,7],
#    "nib":["NimbusMono-Bold.otf",12,0,9,7],
#    "li":["LiberationMono-Regular.ttf",12,0,10,7],
#    "cu":["COURIERO.TTF",10,0,8,7],
    "di":["digital-7.mono.ttf",10,0,8,5],
    "di2":["digital-7.mono.ttf",20,0,16,10],
#    "di":["digital-7.mono.ttf",9,0,7,6],
    "di99":["digital-7.mono.ttf",120,0,170,15],
    "di90":["digital-7.mono.ttf",110,0,155,14],
    "vt":["VT323-Regular.ttf",12,-1,6,5],
    "vt4":["VT323-Regular.ttf",14,-1,13,5],
    "utfu":[ "Uni_Sans_Thin.otf", 24, 0, 24, 8 ],  # uppercase thin
    "utfo":[ "OpenSans-Regular.ttf", 24, 0, 30, 12 ],
    "utfg":[ "good_times_rg.otf", 24, 0, 24, 8 ], # uppercase - broad
#    "utfp":[ "pricedown_bl.otf", 24, 0, 24, 8 ], # uppercase BoldSignature
    "utfh":[ "hemi_head_bd_it.otf", 24, -2, 24, 14 ]
}

LAST_FONT = None

MSG_FONT = "v14"
WIDGET_DEFAULT_GREEN = (0, 255, 0)
WIDGET_DEFAULT_ALERTRED = (50, 50, 255)
#
WIDGET_DEFAULT_DGREEN = (0, 120, 0)
WIDGET_DEFAULT_YELLOW = (0, 255, 255) #(100, 255, 185)
#WIDGET_DEFAULT_COLOR = (255, 250, 255) # BGR
#WIDGET_DEFAULT_COLOR = (255, 0, 0) # blu
#WIDGET_DEFAULT_COLOR = (0, 255, 255) # yell
#WIDGET_DEFAULT_COLOR = (100, 205, 105) #
WIDGET_DEFAULT_COLOR = WIDGET_DEFAULT_YELLOW
WIDGET_DEFAULT_COLOR_DARK = WIDGET_DEFAULT_DGREEN
WIDGET_DEFAULT_COLOR_BLACK = (0, 0, 0)
WIDGET_DEFAULT_COLOR_WHITE = (255, 255, 255)
# for auto color
WIDGET_COLOR_THRESHOLD = 210
WIDGET_COLOR_THRESHOLD_LOW = 140

def set_def_font( font ):
    global LAST_FONT
    if font is None: LAST_FONT = "p8"
    if font in fonts_available.keys():
        LAST_FONT = font
    else:
        LAST_FONT = "p8"


def get_def_font():
    global LAST_FONT
    return LAST_FONT


def get_f_width(font = None):
    global LAST_FONT
    mfont = font
    if mfont is None: mfont = LAST_FONT
    if mfont is None: return 5
    if mfont in fonts_available.keys():
        #LAST_FONT = mfont
        return fonts_available[mfont][4]
    else:
        return 5

def get_f_height(font = None):
    global LAST_FONT
    mfont = font
    if mfont is None: mfont = LAST_FONT
    if mfont is None: return 25
    if mfont in fonts_available.keys():
        #LAST_FONT = mfont
        return fonts_available[mfont][3]
    else:
        return 25

#def iprint( frame, drtext, font, position , color_bgra=(100,0,0,0)  ):
# mess - it seems RGB is needed
#
def iprint( frame, drtext, font, position , color_rgb=(0,255,0)  ):
    global LAST_FONT

    if drtext is None: return
    if type(drtext) is not str:
        drtext = str(drtext)
    mfont = font
    if mfont is None: mfont = LAST_FONT
    if mfont is None: return frame
    if mfont in fonts_available.keys():
        #print("D.... FONT ACCEPTED:", mfont )
        #print("D.... FONT ACCEPTED:", fonts_available[mfont][0] )
        #LAST_FONT = mfont
        # prepare font
        fname = fonts_available[mfont][0]
        fsize = fonts_available[mfont][1]
        fkern = fonts_available[mfont][2]
        fheig = fonts_available[mfont][3]
        fontpath = os.path.expanduser(f"~/.config/flashcam/{fname}")
        try:
            font = ImageFont.truetype(fontpath, fsize)
        except Exception, e:
            print(e)
            sys.exit(1)


        #### draw
        #### img_pil = Image.fromarray(frame.astype('uint8'), 'RGB') # sometimes crashes
        # img_pil = Image.fromarray(frame) ##### BUGBUG !!!!!!!!!!!!!!!!

        # Tying to repair:
        # Ensure the frame has correct data type
        if frame.dtype != np.uint8:
            frame = (255 * frame).astype(np.uint8) if frame.max() <= 1 else frame.astype(np.uint8)
        img_pil = Image.fromarray(frame)  # Correct data type
        # emd of repair

        draw = ImageDraw.Draw(img_pil )

        letter_spacing = fkern
        x,y=position
        # Draw each character with custom spacing
        for chara in drtext:
            #print(f"D... #fill@draw.text: {frame.shape} {color_rgb} {type(color_rgb)} CHAR={chara}/{ord(chara)}/; {(x, y-fheig)}")
            #color_rgb = (255,255,255)

            try:
                draw.text((x, y-fheig), str(chara), fill=color_rgb, font=font, align="left")
            except:
                draw.text((x, y-fheig), chara,  font=font, align="left")

            # THIS WORKS ONLY WITH    pillow==9.0.1 ####################
            #char_width, _ = draw.textsize(chara, font=font)
            #char_width, _ = draw.textsize(chara, font=font)
            #x += char_width + letter_spacing
            # replacing with
            bbox = draw.textbbox((0, 0), chara, font=font)
            char_width = bbox[2] - bbox[0]
            x += char_width + letter_spacing

        frame = np.array(img_pil)
    return frame



def get_color_based_on_brightness(frame,     left_up_point , right_down_point):
    (x1, y1) = left_up_point
    (x2, y2) = right_down_point
    x1 = max(0, x1)
    x2 = min( frame.shape[1], x2)
    y1 = max(0, y1)
    y2 = min(frame.shape[0], y2)
    # Extract the region of interest (ROI)
    roi = frame[y1:y2, x1:x2]

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Calculate the average brightness - no, maximum!
    avg_brightness = int(np.mean(gray_roi))
    max_brightness = int(np.max(gray_roi))

    # if average_brightness < WIDGET_COLOR_THRESHOLD:
    if max_brightness < WIDGET_COLOR_THRESHOLD:
        return tuple( WIDGET_DEFAULT_COLOR )
    else:
        # it is bright
        min_brightness = int(np.min(gray_roi))
        avg_brightness = int(np.mean(gray_roi))
        #print(f"------{min_brightness}   {avg_brightness}  {max_brightness}----")
        if (min_brightness > 40) and (avg_brightness < 150):
            return tuple(WIDGET_DEFAULT_COLOR_BLACK)
        if (min_brightness > 40) and (avg_brightness >= 150):
            return tuple(WIDGET_DEFAULT_COLOR_DARK)
        if (min_brightness <=  40) and (avg_brightness >= 100):
            return tuple(WIDGET_DEFAULT_COLOR_DARK) #?
        if (min_brightness <=  40) and (avg_brightness < 100):
            return tuple(WIDGET_DEFAULT_COLOR_WHITE)
    return tuple(WIDGET_DEFAULT_COLOR_WHITE)

    # # Convert the ROI to HSV color space
    # hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # # Extract the Hue channel
    # hue_channel = hsv_roi[:, :, 0]
    # # Calculate the average hue
    # average_hue = np.mean(hue_channel)
    # # Calculate the contrasting hue
    # contrasting_hue = (average_hue + 20) % 180  # Adding 90 for a contrasting color in OpenCV's 0-180 range
    # #contrasting_hue = average_hue
    # print( int(average_hue), " ",int(contrasting_hue) , end="  ")
    # # Define the allowed hue ranges (in OpenCV's 0-180 hue range)
    # allowed_ranges = [(20, 40), (40, 80), (140, 160), (80, 100)]  # Yellow, green, pink, cyan
    # allowed_ranges = [(0, 180)]  # Yellow, green, pink, cyan
    # allowed_ranges = [(4, 25)]  # Yellow, green, pink, cyan
    # allowed_ranges = [(6, 255)]  # Yellow, green, pink, cyan

    # # Define the ranges to avoid (in OpenCV's 0-180 hue range)
    # avoid_ranges = [(0, 15), (165, 180), (105, 135)]  # Deep red, deep blue, violet

    # # Adjust the contrasting hue to fall within the allowed ranges
    # for low, high in allowed_ranges:
    #     if low <= contrasting_hue <= high:
    #         break
    #     else:
    #         # If the initial contrasting hue is not in any allowed range, pick the closest allowed range
    #         closest_range = min(allowed_ranges, key=lambda r: min(abs(contrasting_hue - r[0]), abs(contrasting_hue - r[1])))
    #         contrasting_hue = (closest_range[0] + closest_range[1]) // 2

    # # # Adjust the contrasting hue to avoid the specified ranges
    # # for low, high in avoid_ranges:
    # #     if low <= contrasting_hue <= high:
    # #         contrasting_hue = (high + 15) % 180
    # #         break

    # # Create an HSV image with the contrasting hue
    # hsv_contrasting = np.zeros((1, 1, 3), dtype=np.uint8)
    # hsv_contrasting[0, 0, 0] = contrasting_hue
    # hsv_contrasting[0, 0, 1] = 245  # Full saturation
    # hsv_contrasting[0, 0, 2] = 255  # Full value (brightness)

    # floor = 70 # base green
    # tresh = 150
    # if average_brightness>tresh:
    #     nc = floor
    # else:
    #     nc =     (tresh-average_brightness)/(tresh)
    #     nc = int((255-floor)*nc*nc)+floor
    #     #nc = 255 - average_brightness
    # if nc>255:nc=255
    # if nc<60:nc=60
    # hsv_contrasting[0, 0, 2] = nc  # Full value (brightness)

    # # Convert the HSV image to BGR
    # bgr_contrasting = cv2.cvtColor(hsv_contrasting, cv2.COLOR_HSV2BGR)
    # # Get the BGR values
    # bgr_values = bgr_contrasting[0, 0]

    # # # # Find the maximum component value
    # #max_component = np.max(bgr_values) # Calculate the scaling factor to make the maximum component 255
    # #scaling_factor = 255 / max_component # Scale the color components
    # #bgr_values = np.clip(bgr_values * scaling_factor, 0, 255).astype(np.uint8)


    # #print(f"      {bgr_values}    avgb= {average_brightness} x trsh={tresh}   /FLO{floor}     NC={nc}    ")
    # return tuple(bgr_values)



def dial(frame, position, radius=30, thickness=10, color=WIDGET_DEFAULT_COLOR, percentage=100, value = 12.3, title=""):
    """
    AI generated: too many iterations
use with text:
     FO="v14"
     frame = iprint( frame,
             str(round(100*overtextalpha/255)),
             FO,
             position = (post[0]-2*get_f_width(FO)//2,
             post[1] +get_f_height(FO)//2 ),
             color_rgb= (0,255, 0, 255-int(overtextalpha))
            )

    """
    MY_CIRC_COLOR =  WIDGET_DEFAULT_GREEN
    #if percentage <= 0: MY_CIRC_COLOR = (100, 100, 255) # BGR
    if percentage >= 100:
        MY_CIRC_COLOR = WIDGET_DEFAULT_ALERTRED #(50, 50, 255) # BGR
    # Calculate the bounding box of the circle
    left_up_point = (position[0] - radius, position[1] - radius)
    right_down_point = (position[0] + radius, position[1] + radius)
    #ncolor = get_color_based_on_brightness( frame, left_up_point , right_down_point)
    ncolor = color

    # Convert the image to a PIL Image
    pil_img = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_img)





    # Calculate the start angle based on the percentage for clockwise drawing
    end_angle = 270  # Ending at the top (north)
    start_angle = end_angle - (360 * (percentage / 100.0))

    # Draw the partial circle (arc)
    draw.arc([left_up_point, right_down_point], start=start_angle, end=end_angle, fill=MY_CIRC_COLOR , width=thickness)

    # Draw a thin full circle as a guide
    guide_thickness = 1  # Set the thickness of the guide circle
    draw.ellipse([left_up_point, right_down_point], outline=MY_CIRC_COLOR , width=guide_thickness)

    # Convert back to OpenCV image


    frame = np.array(pil_img)
    FO="v14"
    FO=MSG_FONT
    frame = iprint( frame,
                    str( value),
                    FO,
                    position = (position[0]-2*get_f_width(FO)//2,
                                position[1] +get_f_height(FO)//2 ),
                    color_rgb= ncolor
                   )
    frame = iprint( frame,
                    str( title),
                    FO,
                    position = (position[0]-len(title)*get_f_width(FO)//2,
                                position[1] + radius + get_f_height(FO) ),
                    color_rgb= ncolor
                   )
    return frame


def tacho(frame, position, radius=30, thickness=10, color=WIDGET_DEFAULT_COLOR, percentage=100, value = 12.3, title=""):
    """

    """

    # Calculate the bounding box of the circle
    left_up_point = (position[0] - radius, position[1] - radius)
    right_down_point = (position[0] + radius, position[1] + radius)
    #ncolor = get_color_based_on_brightness( frame, left_up_point , right_down_point)
    ncolor = color

    # Convert the image to a PIL Image
    pil_img = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_img)



    # Calculate the start angle based on the percentage for clockwise drawing
    end_angle = 180  # Ending at the top (north)
    start_angle = end_angle - (180 * (percentage / 100.0))

    start_angle = 180  # 90 is bottom    180 is left
    end_angle = start_angle + (180 * (percentage / 100.0))  # Ending at the top (north)

    # Draw the partial circle (arc)
    draw.arc([left_up_point, right_down_point], start=start_angle, end=end_angle, fill=WIDGET_DEFAULT_GREEN , width=thickness)

    # Draw a thin full circle as a guide
    guide_thickness = 1  # Set the thickness of the guide circle
    draw.arc([left_up_point, right_down_point], start=start_angle, end=start_angle + 180, fill=WIDGET_DEFAULT_GREEN , width=1)
    #draw.ellipse([left_up_point, right_down_point], outline=WIDGET_DEFAULT_GREEN , width=guide_thickness)

    # Convert back to OpenCV image


    frame = np.array(pil_img)
    FO="v14"
    FO=MSG_FONT
    frame = iprint( frame,
                    str( value),
                    FO,
                    position = (position[0]-2*get_f_width(FO)//2,
                                position[1] +get_f_height(FO)//2 ),
                    color_rgb= ncolor
                   )
    frame = iprint( frame,
                    str( title),
                    FO,
                    position = (position[0]-len(title)*get_f_width(FO)//2,
                                right_down_point[1] - get_f_height(FO)),
                    color_rgb= ncolor
                   ) # tacho righd==lowlow
    return frame


def signal_strength(frame, position, radius=30, color=WIDGET_DEFAULT_COLOR, percentage=100, value = 0.0, title=""):
    """
    by AI:
    """
    ratio = 2.33
    # size = 50 # with this I started
    size = int(radius *  5 / 3) # To keep compatibility with dial+tacho
    #print( type(position), position[0], position[1] )
    # Calculate the vertices of the triangle
    bottom_left = (position[0] - int(size /  2), position[1] + int(size / 2) )

    bottom_right = (position[0] + int(size / 2), position[1] + int(size / 2) )

    top_right = (position[0] + int(size / 2), position[1] - int(size / ratio) )

    # Draw the hollow green triangle
    cv2.line(frame, bottom_left, bottom_right, WIDGET_DEFAULT_GREEN, 1)
    cv2.line(frame, bottom_right, top_right, WIDGET_DEFAULT_GREEN, 1)

   # print( bottom_left, " ___  ", bottom_right  )
   # print( bottom_right, " /// ", top_right )
    #cv2.line(image, top_right, bottom_left, (0, 255, 0), 1)

    # Calculate the fill level based on the percentage
    fill_level = int(  size * (percentage / 100.0))

    # Draw the filled part of the triangle
    if fill_level > 0:
        pts = np.array([[
            bottom_left,
            (bottom_left[0] + fill_level, bottom_left[1]),
            (bottom_left[0] + fill_level, bottom_left[1] - int(  fill_level  /ratio  )   )
        ] ],
            np.int32)

        cv2.fillPoly(frame, [pts], WIDGET_DEFAULT_GREEN )

    FO="v14"
    FO=MSG_FONT

    frame = iprint( frame,
                    str( value),
                    #str( round(percentage)),
                    FO,
                    position = (position[0] -get_f_width(FO)//2,
                                position[1] -get_f_height(FO) ),
                    color_rgb= ( color[0],color[1], color[2] )
                   )
    frame = iprint( frame,
                    str( title),
                    FO,
                    position = (position[0]-len(title)*get_f_width(FO)//2,
                                position[1] + size // 2 + get_f_height(FO) ),
                    color_rgb= ( color[0],color[1], color[2] )
                   ) # signal;   size//2==ontheline;  size==lowlow;
    return frame


def text_box(image, position,  color=WIDGET_DEFAULT_COLOR, split_height=20,  title="Title", values = "rate 123.2 uSv\n tot 220 mSv"):
    # Calculate the corners of the box
    FO="v14"
    FO=MSG_FONT

    maxw=0
    shift2left = 0
    xmargin = 30 # keep min

    #  ';' is already used for a standard  min;max;timeout
    # '# for lines SPLIT
    mylines = values.split("\n")
    if len(mylines) == 1:
        mylines = mylines[0].split("#")

    #print("D... box write:", mylines)
    for i in mylines:
        a = get_f_width(FO)*(len(str(i))+2)
        if a>maxw: maxw=a
    a = get_f_width(FO)*(len(str(title))+2)
    if a>maxw: maxw=a
    # I hava maxw == text wid


    startx = position[0] - maxw // 2

    if maxw + startx > image.shape[1]-xmargin:
        delta = maxw + startx - image.shape[1] + xmargin
        startx = startx - delta

    #xbox_size[1] = maxw
    if len(mylines)>0:
        xbox_size = [ maxw  , get_f_height(FO)* (len(mylines)+3)  ]
    else:
        xbox_size = [ maxw  , get_f_height(FO)* (len(mylines)+1)  ]

    top_left = ( startx  - shift2left,  position[1]  )
    bottom_right = (startx + xbox_size[0] - shift2left, position[1] + xbox_size[1]  )
    #bottom_left = (position[0], position[1] + xbox_size[1])
    #top_right = (position[0] + xbox_size[0], position[1])
    # Draw the rectangle for the text box in green


    cv2.rectangle(image, top_left, bottom_right, WIDGET_DEFAULT_GREEN , 1)

    # Draw the horizontal split line in green
    split_line_start = (startx -shift2left, position[1] + split_height)
    split_line_end = (startx + xbox_size[0]-shift2left, position[1] + split_height)

    if len(mylines)>0:
        cv2.line(image, split_line_start, split_line_end, WIDGET_DEFAULT_GREEN , 1)

    FO = "v14"
    image = iprint( image,
                    str( title ),
                    FO,
                    position = (startx  +get_f_width(FO)-shift2left,
                                position[1] + 1.2*get_f_height(FO) ),
                    color_rgb= ( color[0],color[1], color[2] )
                   )

    if len(title)>0:
        nsk=0
    else:
        nsk=-2

    if len(mylines) > 0:
        for i in mylines:
            image = iprint( image,
                            str( i),
                            FO,
                            position = (startx +get_f_width(FO)-shift2left,
                                        position[1] +(nsk+3)* get_f_height(FO) + int(split_height / 2) - 2),
                            color_rgb= ( color[0],color[1], color[2] )
                           )
            nsk+=1


    return image

def main():
    print()

if __name__=="__main__":
    main()
