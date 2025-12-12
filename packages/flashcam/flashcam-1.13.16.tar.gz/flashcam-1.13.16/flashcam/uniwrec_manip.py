
import numpy as np

import cv2
import math




def matrix_undistort(frame):
    """
    if apply_distortion...
    not used now
    """
    #dist = np.zeros((5,1))
    dist = np.array([[ -8e-7, 4e-11, 0.0, 0.0, 0.0]])

    #mtx = np.eye(3)
    scale = 1.0
    mtx = np.array([[scale, 0, h/2], [0, scale, w/2], [0, 0, 1]])

    h, w = frame.shape[:2]

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # undistort
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    ### crop the image
    ##x, y, w, h = roi
    return dst
    #frame = dst#[y:y+h, x:x+w]




def img_estim(img, thrshld=127):
    """
    not used
    """
    res = np.mean(img)
    return res
    is_light = res > thrshld
    return "light" if is_light else "dark"
    # 40 -> 2.2



def adjust_gamma(image, gamma=1.0):
    """
    local gamma mapped to d shift-d  ctrl-d
    """
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)





def rotate_image(image, angle):
    if angle is None:     return image
    if abs(angle)<0.1:     return image
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    # print( "rotate", image_center, angle )
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    #print(rot_mat)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    #print("rotated by ", angle)
    return result




# -------------------- DISPLAY MULTITEXT ---------------------
def disp_mutext(lena, wrapped_text_o):
    lena = np.array(lena)  # I turn to np.array
    lena = lena / 255

    size = lena.shape
    wrapped_text = wrapped_text_o.split("\n")

    img = np.zeros(size, dtype="uint8")
    img = img + 0.0  # +0.9 # whitish
    # print("npzero",img.shape, img)

    height, width, channel = img.shape

    # never used text_img = np.ones((height, width))
    # print(text_img.shape)
    font = cv2.FONT_HERSHEY_SIMPLEX

    x, y = 10, 40
    font_size = 0.4
    font_thickness = 1

    i = 0

    textsize1 = 1
    textsize0 = 1

    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        if textsize[0] > textsize0:
            textsize0 = textsize[0]
        if textsize[1] > textsize1:
            textsize1 = textsize[1]

    #    wrapped_text.append( " "*textsize1+"[OK]" )
    # print(    wrapped_text )

    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        if textsize[0] > textsize0:
            textsize0 = textsize[0]
        if textsize[1] > textsize1:
            textsize1 = textsize[1]
    # ----- after finding the text sizes; define gap

    gap = textsize1 + 6

    nlines = len(wrapped_text)
    offx = 0 + int((img.shape[1] - textsize0) / 2)
    offy = 0 + int((img.shape[0] - gap * (nlines - 1)) / 2)

    pad = 10
    start_point = (offx - pad, offy - pad - textsize1)
    start_point2 = (offx - pad, offy - pad - textsize1 + int(pad / 2))
    end_point = (pad + offx + textsize0, offy + gap * len(wrapped_text))
    end_point2 = (pad + offx + textsize0, offy + gap * len(wrapped_text) - int(pad / 2))

    # i guess this is gray ...
    img = cv2.rectangle(img, start_point, end_point, (0.3, 0.3, 0.3), -1)
    # this is a frame and  topbar
    img = cv2.rectangle(img, start_point, end_point, (-1, -1, -1), 1)  # trick
    img = cv2.rectangle(img, start_point2, end_point2, (-1, -1, -1), 1)

    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        # print(textsize)
        # gap = textsize[1] + 5
        # gap = textsize1 # gap define earlier

        y = int((img.shape[0] + textsize[1]) / 2) + i * gap
        x = 10  # for center alignment => int((img.shape[1] - textsize[0]) / 2)
        x = offx
        y = offy + i * gap

        cv2.putText(
            img,
            line,
            (x, y),
            font,
            font_size,
            #                (255,255,255),
            (-1, -1, -1),  # BIG TRICK
            font_thickness,
            lineType=cv2.LINE_AA,
        )
        i += 1

    # -------------------- howto merge with frame........
    img = lena - img

    # print("min", img.min()  , "max=",img.max()  )
    img = np.clip(img, 0.0, 1.0, None)  # for dark img values, clip to 0
    # img = img / img.max()
    # print("min", img.min()  , "max=",img.max()  )

    img = img * 255  # i dont know how to make int
    img = img.astype(np.uint8)  # this makes negative to positive
    # print(img)
    return img



# ===================================== big mess


def make_measurements(frame, measure_fov, zoomme, measure, tracker1, tracker_list, cross):
    """
    fov...   measure ... parameters for measurement
    tracker1,_list. ... for speed measurement
    cross ... for movement of the point
    """
    h, w = frame.shape[0], frame.shape[1]
    # measure_fov = 110.5 # notebook

    # approximative, not precise... 5%
    radians_per_pixel = (measure_fov / 180 * math.pi) / w

    # rad per pix * unit distance * better
    # worked with zoom cameras????
    radians_per_pixel2 = math.tan(measure_fov / 180 * math.pi / 2 / w)

    # works with my 101deg camera---------------- and 55deg builtin ntbcam
    #           ..... for 0.5 tan and alpha have 10% diff (tan vs. atan)
    # measure_fov is TOTAL ANGLE
    # radians_per_pixel2 =  math.atan(measure_fov /180*math.pi/(2*w) )*2
    radians_per_pixel2 = math.atan(measure_fov / 180 * math.pi / w)
    # print( radians_per_pixel2 ) # GOOD .... 0.00275

    # radians_per_pixel2 =

    radians_per_pixel2 /= zoomme  # process with zoom

    # print(f"RPPX {radians_per_pixel}  {radians_per_pixel2} ")

    # now arbitrarily define 1 meter..like.. 100px =>
    # alpha = 100*radians_per_pixel
    # b = 1m / math.tan( alpha )

    def get_order(dist=1.7):  # determine order that fits
        # list of marks on the ruler
        wide = 0.001
        notfulrng = 1.0 # notfulrng==0.8; I want full range now..
        while True:
            wide *= 10
            pixwid = math.atan(wide / dist) / radians_per_pixel2
            alpha = pixwid * radians_per_pixel2
            if pixwid > w / 2 * notfulrng:  # not full rANGE
                wide /= 10
                pixwid = math.atan(wide / dist) / radians_per_pixel2
                alpha = pixwid * radians_per_pixel2
                break
        order = wide

        row = []

        while True:
            wide += order
            pixwid = math.atan(wide / dist) / radians_per_pixel2
            alpha = pixwid * radians_per_pixel2
            if pixwid > w / 2 * notfulrng:  # not full rANGE:
                wide -= order
                pixwid = math.atan(wide / dist) / radians_per_pixel2
                # neverused alpha = pixwid * radians_per_pixel2
                break
            else:
                row.append(wide)
        # -----
        # -----
        row.append(order)
        row = sorted(row)
        row = row[::-1]  # revert - we want Big to small
        # print( "TICKS... max:", row[0]  )

        base = 10**math.floor( math.log10( row[0]) )
        if row[0]/base<4:
            base = 10**math.floor( math.log10( row[0]/4) )

        minors = np.arange( base, row[0], base)
        minors = minors[::-1]
        #print(minors)
        if len(row) <= 2:
            in0 = row[0] / 2
            row.append(in0)
            in1 =  row[0] / 4
            row.append(in1)
        #     in2 = row[0] / 4 *3
        #     in3 = row[0] / 5
        #     #in2 = row[-1]/10
        #     row.append(in2)
        #     # row.append( in2 )
            # print("   > ",row)
        return row,minors  # Big to small


    def one_mark(dist=1.7, wide=[1, 2], speed=0, dispnumb = True):
        #  wide ...  # Big to small
        # h,w = frame.shape[0], frame.shape[1]
        # pixel distance of halfwidth

        # alpha = pixwid * radians_per_pixel2
        # dist = wide/math.tan( alpha)
        # I need to calculate 1m
        level = 0
        # print("XXXXX",wide)
        for iwide in wide:

            # multiply and round to one digit..before pixel calc
            for ix in range(4):
                if iwide*10**ix > 1:
                    iwide = round( iwide* 10**ix)/10**ix
                    break

            pixwid = math.atan(iwide / dist) / radians_per_pixel2
            # neverused alpha = pixwid * radians_per_pixel2

            # print(f" {radians_per_pixel}radpp {pixwid}   {wide}m <- {dist} ")
            step = 0
            mX, mY = int(w / 2), int(h / 2)
            if not (cross is None):
                mX += cross[0]
                mY += cross[1]
            # here I addd the red cross position

            mY = mY + level * step

            yA, yB = mY, mY

            xA = mX
            xB = mX + int(pixwid)

            yC = mY - int(pixwid) # up

            color = (0, 255, 0)  # BGR
            color = (55, 0, 255)  # BGR same as the red cross
            colos = (255, 0, 55)  # BGR same as the red cross
            if level == 0:
                # line - horiznotal
                cv2.line(
                    frame,
                    (int(xA), int(yA)),
                    (int(xB), int(yB)),
                    color,
                    1,
                )
                cv2.line( # left
                    frame,
                    (int(xA), int(yA)),
                    (int(2*xA-xB), int(yB)),
                    color,
                    1,
                )


                cv2.line( # probably central  mark
                    frame,
                    (int(xA), int(yA + 8)),
                    (int(xA), int(yA - 8)),
                    color,
                    1,
                )

            # vert bars on horiz axis
            cv2.line(  # ticks right
                frame,
                (int(xB), int(yB + 3)),
                (int(xB), int(yB - 3)),
                color,
                1,
            )
            cv2.line( # ticks left
                frame,
                (int(2*xA-xB), int(yB + 3)),
                (int(2*xA-xB), int(yB - 3)),
                color,
                1,
            )

            if yC>0:
                # horz bars on vertic axis
                cv2.line( # up
                    frame,
                    (int(xA), int(yA)),
                    (int(xA), int(yC)),
                    color,
                    1,
                )
                cv2.line(
                    frame,
                    (int(xA-3), int(yC )),
                    (int(xA+3), int(yC )),
                    color,
                    1,
                )

            unit = "m"
            # --- check the biggest to set the unit [0] is biggest
            if wide[0] <= 0.001:
                iwide = round(iwide * 1000 * 1000) / 1000
                unit = "mm"
            elif wide[0] <= 0.01:
                iwide = round(iwide * 100 * 1000) / 1000
                unit = "cm"
            elif wide[0] <= 0.1:
                iwide = round(iwide * 100 * 100) / 100
                unit = "cm"
            elif wide[0] < 1:
                iwide = round(iwide * 10 *100) / 100
                unit = "dm"
            else:
                iwide = round(iwide * 10) / 10

            # only properly round whatever unit
            if iwide <= 0.001:
                iwide = round(iwide * 10000) / 10000
            elif iwide <= 0.01:
                iwide = round(iwide * 1000) / 1000
            elif iwide <= 0.1:
                iwide = round(iwide * 100) / 100
            elif iwide < 1:
                iwide = round(iwide * 10) / 10
            else:
                iwide = round(iwide)


            if level > 0:
                unit = ""  # no unit during the scale
            unit2 = "m"

            if str(iwide)[:2] == "0.":
                iwide = str(iwide)[1:]

            if dispnumb:
                # width on scale - scale values
                cv2.putText(
                    frame,
                    f"{iwide}",
                    (int(xB - 10), int(mY - 7)),  # little rightx a bit up y
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    color,
                    1,
                )
                cv2.putText(
                    frame,
                    f"{iwide}",
                    (int(2*xA-xB - 10), int(mY - 7)),  # little rightx a bit up y
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    color,
                    1,
                )

                cv2.putText(  # up
                    frame,
                    f"{iwide}{unit}",
                    (int(xA + 10), int(yC)),  # little rightx a bit up y
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    color,
                    1,
                )



                if level==0 and unit!="":
                    cv2.putText(
                        frame,
                        f"  unit ... {unit}",
                        (
                            int(xA - 130),
                            int(mY - 5 -40),
                        ),  # little rightx a bit up y
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        color,
                        1,
                    )


            if level >= 0:
                # distance - only at first mark
                cv2.putText(
                    frame,
                    f"  at {dist} {unit2}",
                    (
                        int(xA - 130),
                        int(mY + 5 -40),
                    ),  # little rightx a bit up y
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    color,
                    1,
                )
                cv2.putText(
                    frame,
                    f"  FOV {measure_fov:.1f}deg",
                    (
                        int(xA - 130),
                        int(mY + 15 -40),
                    ),  # little rightx a bit up y
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    color,
                    1,
                )
                # I add velocity
                if (level == 0) and not (tracker1 is None):
                    cv2.putText(
                        frame,
                        f"speed {speed:6.2f}m/s",
                        (
                            int(xB - 50),
                            int(mY + 15),
                        ),  # little rightx a bit up y
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        color,
                        1,
                    )
            level += 1

    # main part of the ruler making---------------

    order,minorticks = get_order(dist=measure)
    # print(minorticks)



    # speed computation
    if not (tracker1 is None) and len(tracker_list) > 2:
        b = tracker_list[-1]
        try:
            v_from = -2
            a = tracker_list[v_from]
            while True:
                dt = (b[2] - a[2]).total_seconds()
                if dt > 1.0:
                    break
                else:
                    v_from -= 1
                if len(tracker_list) < abs(v_from):
                    break
                a = tracker_list[v_from]
        except:
            dt = 100000  # velocity 0
        c = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        v = c / dt * radians_per_pixel2
        v = round(100 * math.tan(v) * measure) / 100
        # print(f"i... speed = {v} m/s  {dt:.2}==dt " )
    else:
        v = 0
    # plot ruler
    one_mark(dist=measure, wide=minorticks, speed=v, dispnumb = False)
    one_mark(dist=measure, wide=order, speed=v)
    return frame
