############################# /// script
############################# requires-python = ">=3.12"
############################# dependencies = [
#############################     "numpy",
#############################     "opencv-python",
#############################     "pyqt6",
#############################     "requests",
############################# ]
############################# ///
############################
a = """
* I keep this on legacy .venv ***    either --script install - or venv!
* from astropy.io import fits ***  some fits in threading done *** ... ds9.si.edu viewer DS9
* NOT NOW **** Or store as  hdf5 - files with metadata -  and  use HDFView ... one file
* view script to open napari inn uv ***** or napari (python)  uvx --with pyqt6
FITS and napari
 ...  if I save as fits.writeto('image.fits') and use napari:image_data=hdul[0].data viewer.add_image()
NEW - Fits saves nice, many CUBE , use like
  lbzip2 for compression
     ../Downloads/DS9/ds9 core6a_10.10.104.17_8000_20250514_104549.26.jpg.fits.bz2
    uv run explore_view_napari.py ~/DATA/core6a_10.10.104.44_8000_20250514_101055.37.jpg.fits.bz2
    napari plugins
   https://github.com/DKFZ-TMTRR/napari-nd-cropper
 use shapes.... to crop!!!!
uv run  --with=napari-crop  --with=napari-tabu ./explore_view_napari.py ~/DATA/core6a_video0_20250604_113217.25.fits
napari-tabu :((((
DS9 ...    ~/Downloads/DS9/ds9  core6a_video0_20250604_185439.68.fits                    just GRAY,
 wine /home/ojr/.wine/dosdevices/c:/Program Files (x86)/AvisFV30/AvisFV.exe     core6a_video0_20250604_185439.68.fits
#------------
NEW  1 2 3 4 and shift(save) are registers for rota,zoom,r_integrr,move,l_gamma (r_gain t?in future?)
CROSS, FG BG....

wget  http://a:a@localhost:8000/foreground -O foreground.jpg && sudo fbi -T 1 -a  foreground.jpg
___________
idea
*MAYBE* 1. \n \r for  terinal
*DONE* 2. iprint time frame  DONE
*Done local* 3. !! Integrate is remote (struggle with threshold)
*Done i think* 4. remote gain! expot and gammat!?
-----
*
"""
from PIL import ImageFont, ImageDraw, Image
import sys
import numpy as np
import cv2
import requests
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtCore import QSize


import socket
import datetime as dt
#import socket
#import cv2

import getpass
import os
import urllib
import base64
import getpass
import time


from pogucam.text_write import iprint, fonts_available, get_f_height, get_f_width, get_def_font, set_def_font
from pogucam import buffers

from console import fg, bg, fx

from astropy.io import fits
import threading
import json

import webbrowser
from collections import deque # acc

import click
import subprocess as sp
import re
import math

from astropy import wcs

#------------------------------------  subscibe
import struct
import paho.mqtt.client as mqtt
import numpy as np
import datetime as dt
import cv2
import threading

import glob # look for bg fg
import shutil

istrip = 0
UPDATE_INTERVAL = 1
#FITS_CUBE_N = 400
#FITS_INTERVAL_SECONDS = 60

# ---------- files:
FILE_USERPASS = "~/.config/flashcam/.flashcam_upw"  # will extend
FILE_REDCROSS0 = "~/.config/pogucam/crossred"  # will extend
FILE_REDCROSS = "~/.config/pogucam/crossred"  # will extend





# ================================================================================
#
# --------------------------------------------------------------------------------


# ================================================================================
#
# --------------------------------------------------------------------------------


# ================================================================================
#
# --------------------------------------------------------------------------------


# ================================================================================
#
# --------------------------------------------------------------------------------


# def parse_timestamp_in_saved_file(filename):
#     # Extract timestamp part YYmmdd_HHMMSS.ff from filename
#     parts = filename.split('_')
#     if len(parts) < 5:
#         return None
#     timestamp_str = parts[3] + '_' + parts[4]  # YYmmdd_HHMMSS.ff
#     try:
#         # Parse ignoring fractional seconds for sorting
#         dt = datetime.strptime(timestamp_str.split('.')[0], "%Y%m%d_%H%M%S")
#         return dt
#     except ValueError:
#         return None

def find_latest_bg_or_fg(new_name, foreground=False):
    #
    tag = "background"
    if foreground:
        tag = "foreground"
    base, ext = os.path.splitext(new_name) #
    parts = base.split('_')
    pattern = f"{parts[0]}_{parts[1]}_{parts[2]}_"
    copyfile = f"{pattern}{tag}{ext}"
    #if not base.endswith(tag):
    #    print("Filename must end with '_background' before extension")
    #    return
    #base_prefix = base[:-11]  # remove '_background'
    pattern2 = f"{pattern}20*{ext}" # 20ieth century
    files = glob.glob(pattern2)
    lastfile = None
    if not files:
        print("D... No matching files found for", pattern2)
    else:
        lastfile = sorted(files)[-1]
        print(f"D... {len(files)} possible files" , lastfile)
    if lastfile is None: print(f"{fg.red}X... no suitable saved file for {tag} ", fg.default)
    return lastfile,copyfile



# ================================================================================
# RA    "00 12 45.2"
# --------------------------------------------------------------------------------
def hms_to_deg(h, m=None, s=None):
    res = None
    if m is None and type(h) == str:
        h1, m1, s1 = h.strip().split(" ")
        res = ( float(h1) + float(m1)/60 + float(s1)/3600) * 15
    else:
        res = (h + m/60 + s/3600) * 15
    return res

# ================================================================================
# DEC  " "
# --------------------------------------------------------------------------------
def dms_to_deg(d, m=None, s=None):
    res = None
    if m is None and type(d) == str:
        d1, m1, s1 = d.strip().split(" ")
        sign = 1 if float(d1) >= 0 else -1
        res = float(d1) + sign * ( float(m1)/60 + float(s1)/3600)
    else:
        sign = 1 if d >= 0 else -1
        res = d + sign * (m/60 + s/3600)
    return  res

# ================================================================================
#
# --------------------------------------------------------------------------------

def get_v4l2_controls( device ):
    if device is not None:
        if not  os.path.exists(device):
            print(f"X... SORRY {device} doesn not exist")
            return None
    output = sp.check_output(['v4l2-ctl', '-d', device , '--list-ctrls'], text=True)
    controls = {}
    pattern = re.compile(r'^\s*(\w+)\s+0x[0-9a-f]+ \(.*\)\s+: min=(-?\d+) max=(-?\d+) step=(\d+) default=(-?\d+) value=(-?\d+)', re.MULTILINE)
    for match in pattern.finditer(output):
        name = match.group(1)
        controls[name] = {
            'min': int(match.group(2)),
            'max': int(match.group(3)),
            'step': int(match.group(4)),
            'default': int(match.group(5)),
            'value': int(match.group(6)),
        }
    return controls


def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n) # 0.0
        int_n = int(float_n) #0.0
    except ValueError:
        return False
    else:
        return float_n == int_n


def guess_url( inp ):
    """
    interpret url:   http: or /dev/
    - low integer== dev
    - int 80+ is local port; http+ is clear;
    - :1883/topic/var   or :1883
    """
    final = inp
    ip = ""
    port = ""
    path = ""
    if inp is None:
        print("X... no url")
        return None
    if inp[0] == ":":
        port = "".join(inp[1:])
        path = port.split("/")[1:]
        path = "/".join(path)
        port = port.split("/")[0]
        print("D... port is evidently given in ", inp[1:], "; port:", port, "path:" , path)
        if not is_int(port):
            print("X... port not integer")
            return None
        port = int(port)
        if port == 1883:
            final = f"mqtt://127.0.0.1/{path}"
            print("i... local mqtt ... ", final)
            return final
        else:
            final = f"http://127.0.0.1:{port}/{path}"
            print("i... local http ... ", final)
            return final
        #return inp
    if inp.find("/dev/video") == 0:
        print("D... no discussion, videodev:", inp)
        return inp
    if type(inp) is int:# dev # or port #
        if int(inp) < 80:
            print("D... maybe video device")
            videostr = f"/dev/video{inp}"
            if os.path.exists( videostr):
                print(f"i... {videostr} exists  ")
                return videostr
            else:
                return None
        else:
            print("i... maybe port...")
            if int(inp) > 79 and int(inp) < 64000:
                print("i... I put 127.0.0.1 address ")
                final = f"http://127.0.0.1:{inp}/video"
                return final
            print("X... IDK:")
            return None
    #  clearly mqtt
    if (inp.find("mqtt://") == 0):
        print("i... clearly mqtt:", inp)
        return final
    #  clearly http
    if (inp.find("http://") == 0) or (inp.find("https://") == 0):
        if (inp.find(":") >  0):
            return final
        else:
            print("X... a  problem, no port demanded")
            return None
    # something strange, less than any IP ... IDK
    elif len(inp) < 7:
        print("X... /ShoudntBeHere/ TOO short ip (can be 0 for video0):", inp)
        if is_int(inp):
            print("i... /ShoudntBeHere/ but this is one number, possibly port number", inp)
            if int(inp) > 79 and int(inp) < 64000 and int(inp) != 1883:
                print("i... /ShoudntBeHere/I put 127.0.0.1 address ")
                final = f"http://127.0.0.1:{inp}/video"
                return final
            elif int(inp) == 1883:
                print("i... mqtt is evidently required. Topic (too short inp)  is: ", path)
                # if inp.find("/") > 0:
                #     port = inp.split("/")[]
                # path = join("/").portplus.split("/")[1:]
                if path == "":
                    print("i... topic will be by default image/raw8000")
                    path = "image/raw8000"
                    ip = "127.0.0.1"
                    final = f"mqtt://{ip}/{path}"
                    print(final)
                    return final
            elif is_int(inp):
                print("D... /ShoudntBeHere/maybe video device")
                videostr = f"/dev/video{inp}"
                if os.path.exists( videostr):
                    print(f"i... /ShoudntBeHere/ {videostr} exists  ")
                    return videostr
                else:
                    print(f"i... /ShoudntBeHere/ {videostr} DOES NOT exist !!!!! ")
                    return videostr
            else:
                print("X... /ShoudntBeHere-maybe/ BAD input", inp)
                return None
    # address
    elif inp.find(".") < 0:
        print("X... no dots in the address ", inp)
        return None
    elif len(inp.split(".")) < 3:
        print("X... too few dots, not IP4  address ", inp)
        return None
    # ----------------------------------------------
    digit = inp.split(".")
    if is_int( digit[0]) and  is_int(digit[1]) and is_int(digit[2]): # 3 digits and d:port
        # DIGITS
        if is_int(digit[3]):
            print("i... a bit of problem, no port demanded at 3rd digit", digit, " giving 8000")
            ip = inp # back to 4 digits
            port = "8000"
            #return None
        elif digit[3].find(":") <= 0: # if not a digit, maybe path??
            print("X... /ShoudntBeHere-maybe/ a bit of problem, no port demanded, giving 8000")
            port = "8000"
            #return None
        else:# port ok-extract
            ip = inp.split(":")[0]
            portplus = inp.split(":")[1]
            # extract path
            if portplus.find("/") > 0:
                port = portplus.split("/")[0]
                pathlist = portplus.split("/")[1:]
                path = "/".join(pathlist)
            else:
                port = portplus
        # ---
        if not is_int(port):
            print("X... port is not a number:", port)
            return None
        # port is OK now----------------------------
        port = int(port)
        if port == 1883:
            print("i... mqtt is evidently required. Topic is: ", path)
            if path == "":
                print("i... topic will be by default image/raw8000")
                path = "image/raw8000"
            final = f"mqtt://{ip}:{port}/{path}"
            print(final)
            return final
        if path == "":
            print("i... a bit problem, no path obtained. Giving /video , but this should probably change in future")
            path = "video"

        final = f"http://{ip}:{port}/{path}"
        print(final)
        return final
    else:
        print("X... address is not digits, I am stopping")
        return None


# ___________________________________________________________________________
#            guessing url done
# ___________________________________________________________________________

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


def crosson( frame,  dix, diy, color = "g", box_small = True, box_large = False):
    """
    two types  g (just cross, r boxed cross)
    """
    #if color == 'r': crotype = 'line'
    #
    RADIUS=63
    y = int(frame.shape[0]/2)
    x = int(frame.shape[1]/2)

    ix = x+dix
    iy = y+diy

    if color=="g":
        lcolor=(0,255,55)
    elif (color=="r"):
        lcolor=(55,0,255) #BGR
    else:
        lcolor=(0,255,55)

    crscal = 4
    crnx,crny = int(64/crscal),int(48/crscal)
    #if crotype == "box":
    midskip = crnx
    midskipy = crny
    #else:
    #    midskip = 7
    #    midskipy = 7


    i2=cv2.circle( frame, (ix,iy), RADIUS, lcolor, 1)
    i2=cv2.line(i2, (ix-RADIUS+midskip,iy), (ix-midskip,iy), lcolor, thickness=1, lineType=8)
    i2=cv2.line(i2, (ix+RADIUS-midskip,iy), (ix+midskip,iy), lcolor, thickness=1, lineType=8)

    i2=cv2.line(i2, (ix,iy-RADIUS+midskipy), (ix,iy-midskipy), lcolor, thickness=1, lineType=8)
    i2=cv2.line(i2, (ix,iy+RADIUS-midskipy), (ix,iy+midskipy), lcolor, thickness=1, lineType=8)

    # mid
    i2=cv2.line(i2, (ix,iy), (ix,iy), lcolor, thickness=1, lineType=8)

    #if crotype == "box":
    if box_small:
        #corners  #  position 0.5deg from 11 deg. OK
        crscal = 4 # normal original box
        crscal = 3.2 # normal original box
        crnx,crny = int(64/crscal),int(48/crscal)

        i2=cv2.line(i2, (ix-crnx,iy-crny), (ix+crnx,iy-crny), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix+crnx,iy-crny), (ix+crnx,iy+crny), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix+crnx,iy+crny), (ix-crnx,iy+crny), lcolor, thickness=1, lineType=8)
        i2=cv2.line(i2, (ix-crnx,iy+crny), (ix-crnx,iy-crny), lcolor, thickness=1, lineType=8)

    if box_large:
        #corners  #  position 0.5deg from 11 deg. OK
        crscal = 1.4 # normal original box
        crnx,crny = int(64/crscal),int(48/crscal)

        i2=cv2.line(i2, (ix-crnx,iy-crny), (ix+crnx,iy-crny), lcolor, thickness=1 )
        i2=cv2.line(i2, (ix+crnx,iy-crny), (ix+crnx,iy+crny), lcolor, thickness=1 )
        i2=cv2.line(i2, (ix+crnx,iy+crny), (ix-crnx,iy+crny), lcolor, thickness=1 )
        i2=cv2.line(i2, (ix-crnx,iy+crny), (ix-crnx,iy-crny), lcolor, thickness=1 )

    return frame # CROSSON *********************************************************************




# ==========================================================================================
#  CLASS
# ------------------------------------------------------------------------------------------



# if rotate == 180:
#     frame = cv2.rotate(frame, cv2.ROTATE_180)
#     # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
# elif rotate != 0:
#     frame = rotate_image( frame , rotate )

# ================================================================
#  Stream widget
# ----------------------------------------------------------------
class StreamWidget(QLabel):

    # ==================================================
    #  Called with parameters
    # --------------------------------------------------
    def __init__(self, url, resolution="1920x1080", fourcc="YUYV"):
        super().__init__()
        self.setWindowTitle( url)
        #self.setFixedSize(640, 480)
        self.setMinimumSize(640, 480)
        self.setMaximumSize(QSize(1920, 1080))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # --------------------------------------------- url 3 options handling, set default values
        self.device = None
        self.url = None
        self.post_addr = None
        self.internet_mqtt = False
        self.mqtt_topic = "image/raw8000" # default topic
        self.mqtt_subscribed = False
        self.mqtt_client = None
        self.mqtt_new_image = False # trafic light
        # url is mqtt://     of http://  or /dev/
        # ----- here only canonical address is present.....
        if url is None :
            print("X... I cannot find a relevant source kind, but program should not be here...")
            sys.exit(1)
        if (url is not None) and is_int(url) and int(url) < 10:
            print("X... should never get here - looks like videodev number")
            sys.exit(1)
        #--------------------- decide if device or internet http:// or mqtt ----
        if (url is not None) and url.find("/dev/video") >= 0:
            self.device = url
            self.url = url#"local"
            self.internet_not_device = False #
            self.post_addr = None# self.url.replace("/video", "/cross")
            if not os.path.exists( self.device):
                print(f"i... {self.device} DOES NOT exist - but may exist in the future...approved...  ")
                #sys.exit(1)
        elif (url is not None) and (url.find("http://") or url.find("http://")) >= 0:
            self.url = url
            self.internet_not_device = True #
            self.post_addr = self.url.replace("/video", "/cross")
        elif (url is not None) and url.find("mqtt://") >= 0:  # ******** MQTT HERE ***********
            self.url = url # I like full proto
            ipdeco = url.split("mqtt://")[-1] # remove protocol
            # postaddr with http:// HACK
            self.post_addr = "http://" + ipdeco.split("/")[0] # just IP address for mqtt
            temp = ipdeco.split("/")
            temp = [i for i in temp if len(i) > 0] # this solves "/" at the end without any path==topic...
            #print(temp)
            if len(temp) > 1: # topic is given...  >2?
                self.mqtt_topic = ipdeco.split("/")[1:] # IP address
                self.mqtt_topic = "/".join(self.mqtt_topic)
            else:
                pass
            print("i...  topic:", self.mqtt_topic)
            self.internet_not_device = True #
            self.internet_mqtt = True #
            #self.post_addr = None#self.url.replace("/video", "/cross")
        else:
            print(f"X... PROBLEM: {self.url}  x  {self.device} ... url x device")
            sys.exit(1)
        #---------------------------------------------------------------
        self.resolution = resolution
        self.fourcc = fourcc
        #self.internet_not_device = internet_not_device

        #
        #if (self.url is None):
        #    self.url = "local"
        #    self.internet_not_device = False # override
        #if not self.internet_not_device: # no internet...try local
        #    self.url = "local"   # LABEL IN IMAGES
        #else:

        # ----------------------------------------------
        self.width = 640
        self.height = 480

        self.img = np.zeros(( self.height, self.width, 3), dtype=np.uint8)

        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_and_update)
        self.timer.start(UPDATE_INTERVAL)  # update every 100 ms
        # ---------- operations
        self.stream = None # initially no stream
        self.bytex = b""  # stream
        # ----------------------------------- initial frame -------------- was always STRIPS, now NONE: helsp w VCR ----
        # with big colored strips
        self.frame = None # do COPY()  to img  # np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.which_error = "" # no error, can be url http...
        self.frames_to_fail_max = 5 # countdown to 0 and reset CAP
        self.frames_to_fail = self.frames_to_fail_max # countdown to 0 and reset CAP
        #strip_height = 64
        #for i in range(0, self.height, strip_height * 2):
        #    self.frame[i + istrip:i+strip_height+ istrip, :] = (185, 150, 150)       # bgr
        #    self.frame[i+strip_height+ istrip:i+ istrip+strip_height*2, :] = (5, 5, 5)  #
        #-----------------------------------------------------------------------------------
        # ----- this is length of one frame ad hoc
        self.stream_length_init = 1024 * 50  # i had 50k all the time from 1st working versn
        self.stream_length = self.stream_length_init  # i had 50k all the time from 1st working versn
        # --- timings
        self.t_posread = dt.datetime.now() # just before have read
        self.t_preread = dt.datetime.now() # just before have read
        self.t_oldread = dt.datetime.now()
        self.t_lasread = dt.datetime.now() # last have read
        self.frame_num = " " * 7
        self.frame_time = " " * 23
        # Local frame numbers ------------
        self.l_frame_num = 0
        self.l_frame_bia = 0 # see bias
        self.l_frame_offs = None # offset to remote
        self.l_frame_time = dt.datetime.now()
        # ------------------------- FLAGS
        self.saving_all = False  # every frame to jpg
        self.saving_fits_only = False  # but to fits
        self.saving_jpg = True
        self.FITS_INTERVAL_SECONDS = 60
        self.saving_once = False  # save one frame jpg
        self.saving_laps = -1  # save no laps
        self.saving_laps_last_save = dt.datetime.now()  # save no laps
        self.saving_transformed_image = True # idk - saving QT prepared image
        self.SAVED_NOW = False # for overtext info
        #
        self.xtended = False # 2x  local
        self.flag_print = False # terminal \n OR \r      "P"
        self.flag_print_over = True # overtext           "S-P"
        self.flag_redcross = False
        self.error = False
        self.zoomme = 1
        self.redcross = [0, 0]
        # ---------------------------- REMOTE ------------------------------
        self.r_integrate = 0
        # - - - - - - ----------
        self.r_gain = 0.5  # Remote; I keep info here
        self.r_expo = 0.5  # Remote; I keep info here
        self.r_gamma = 0.0 # Remote; I keep info here  remote is 0
        self.r_gaindef = False  # Remote; I keep info here
        self.r_expodef = False  # Remote; I keep info here
        self.r_gammadef = False # Remote; I keep info here
        self.r_xtend = "  " # nothing "  ";  LC RC  CU CD  ....
        #-------------
        self.l_gamma = 1 # i dont know, bnut probably ok for local
        self.l_rotate = 0
# -------------------------  stack
        self.my_img_list = [] # keeps images
        self.my_tim_list = [] # keeps times of images (local)
        self.rgb_image = None # for save
        # ************
        self.setup_dict = {}
        self.setup(action="r", number=1)
        self.setup(action="r", number=2)
        self.setup(action="r", number=3)
        self.setup(action="r", number=4)
        # ------------------------  capture
        self.cap = None
        # ------------------------- FastBuffer
        self.FABuffer = buffers.FastAccumBuffer(1) # shape is default
        #self.accum_n = 1           #
        #self.accum_buffer = None   #
        #self.accum_image = None    #
        self.l_show_accum = False  # THIS MUST BE KEPT
        self.l_show_accum_avg = False
        # ---- np stak-------------------------------------
        #self.accum_buffer_size = 0 #
        #self.accum_count = 0       # actual number of img in buff
        # -------------------------------------------------
        #self.level2_buffer = None
        #self.level2_buffer_max_size = 10
        #---------------------------------------------
        self.filename_background = None
        self.filename_foreground = None
        self.image_background = None
        self.image_foreground = None
        self.l_timelaps = False
        self.l_timelaps_seconds = 16 # initial 2^4
        self.l_timelaps_last = dt.datetime.now() #
        # --------------------------------- I put it at the end so that it knows all attributes
        self.update_image( self.rgb_image )



 ###########################################################
 #   mmm  m    m mmmm           mmmm  mmmmmm mm   m mmmm   #
 # m"   " ##  ## #   "m        #"   " #      #"m  # #   "m #
 # #      # ## # #    #        "#mmm  #mmmmm # #m # #    # #
 # #      # "" # #    #            "# #      #  # # #    # #
 #  "mmm" #    # #mmm"         "mmm#" #mmmmm #   ## #mmm"  #
 ###########################################################

    # ================================================================================
    # REQUEST COMMAND SEND  ---  hybrid for sending to flashcam or doing locally
    # --------------------------------------------------------------------------------
    def send_command(self, data =None):
        """
        1. sends commands via HTTP to remote
        2. for device, tries to act for some commands
        """
        #print(self.internet_not_device, self.internet_not_device)
        # -------------------------------------------------------------- ACCUM -----------------
        if self.internet_not_device:
            #### every internet call do here
            ####  but skip anyting with ACCUM ACCUMTXT !!!!!!!!
            if ('accumtxt' in data) and int(data['accumtxt']) == 1:   # skip Loop 1
                print("D... LOOP 1 skipped for remote send command - for some reason I send out 0 only,not 1")
                pass
            elif ('accumtxt' in data): # NO ACCUM REMOTE !!!!!!!!!!! ??? test
                val = int(data['accumtxt']) # SIZE OF THE BUFFER
                if val == 0: val = 1 # trying to fix
                if len(self.FABuffer) != val and val > 0:
                    self.FABuffer.set_max_frames(val)
            else:#### HERE REALLY ######--------------------------------------------------
                # HACK TO COMMUNICATE WITOUT FULL MQTT!!!!
                print(self.post_addr, data)
                if self.post_addr.find("http://") == 0:
                    print(self.post_addr, data)
                    post_response = requests.post(url=self.post_addr, data=data )
                elif self.post_addr.find("mqtt://") == 0:
                    #else:# mqtt://
                    hacked_post = self.url.split("mqtt://")[-1]
                    hacked_port = 8000
                    if self.mqtt_topic.find("image/raw") > 0:
                        hacked_port = self.mqtt_topic.split("image/raw")[-1]
                    hacked_post = f"http://{hacked_post.strip(" / ")}:{hacked_port}/cross"
                    print(  f"mqtt hack ... {hacked_post} "  , data)
                    try:
                        post_response = requests.post(url=hacked_post, data=data )
                    except:
                        print(f"{fg.red}X...  request failed {hacked_post} --- {data} {fg.default}")
                        pass
        else:
            # ---------------------------------------------------------  JUST LOCAL DEVICE ----------------
            #print("X... no remote IP defined - nothing sent", data)
            #--------------------------- ------------------------------------ACUUMULATE LOCALY
            if ('accumtxt' in data):
                val = int(data['accumtxt']) # SIZE OF THE BUFFER
                # how to solve 0? the forgotten problem with 1 allowed here and not 0
                if val == 0: val = 1 # trying to fix
                if len(self.FABuffer) != val and val > 0:
                    self.FABuffer.set_max_frames(val)
                #if val != self.accum_n:
                #    self.accum_n = val
                #    #if val == 0: self.accum_n = val # This looks obsolete!; commenting out
                #    #
                #    ###self.accum_buffer = deque(maxlen=self.accum_n)
                #    self.define_accum_buffer( self.accum_n )


            #-----------------------------------------------------------------SWITCHRES LOCALY
            if ('switch_res_on' in data) and (self.r_xtend != "  ") and self.device.find("/dev/video") >= 0:
                self.resolution="1920x1080"  # possible when 1920 on start
                self.fourcc="MJPG"
                width, height  = self.parse_resolution(self.resolution)
                fourcc = self.fourcc #
                print(f"----- {width}  {height}  {fourcc} ")
                self.cap.release()
                time.sleep(1)
                self.controls_dict = get_v4l2_controls(self.device)
                if self.controls_dict is None: self.which_error = "Device not found"

                self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
                fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
                self.cap.set(cv2.CAP_PROP_FOURCC, fourcc_code)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

                self.zoome = 1
                self.FABuffer.set_max_frames(1)
                #self.define_accum_buffer(0 ) # RESET BUFFER

            #----------------------------------------------------------

            if ('switch_res_off' in data) and (self.r_xtend == "  ") and self.device.find("/dev/video") >= 0:
                self.resolution="640x480"
                self.fourcc="YUYV"
                width, height  = self.parse_resolution(self.resolution)
                fourcc = self.fourcc #
                print(f"----- {width}  {height}  {fourcc}")
                self.cap.release()
                time.sleep(1)
                self.controls_dict = get_v4l2_controls(self.device)
                if self.controls_dict is None: self.which_error = "Device not found"

                self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
                fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
                self.cap.set(cv2.CAP_PROP_FOURCC, fourcc_code)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

                #self.define_accum_buffer(0 ) # RESET BUFFER
                self.FABuffer.set_max_frames(1)
                self.zoome = 1

            #----------------------------------------------------------
            if  ('expotxt' in data) and self.device.find("/dev/video") >= 0:
                if not 'exposure_time_absolute' in self.controls_dict.keys():
                    pass
                else:
                    target = data['expotxt']
                    contr = self.controls_dict["exposure_time_absolute"]
                    min_, max_ = contr['min'], contr['max']
                    if target < 0:
                        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)  # manual
                    else:
                        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual
                        rng_ = max_ - min_
                        exp_target = target ** 2#(math.exp(target) - 1) / (math.e - 1)
                        target = int(rng_ * exp_target + min_)
                        print(" EXPO minmax  ", min_, max_, target, cv2.CAP_PROP_EXPOSURE)
                        self.cap.set(cv2.CAP_PROP_EXPOSURE, target)

            if  ('gaintxt' in data) and self.device.find("/dev/video") >= 0:
                if not 'gain' in self.controls_dict.keys():
                    pass
                else:
                    target = data['gaintxt']
                    contr = self.controls_dict["gain"]
                    min_, max_ = contr['min'], contr['max']
                    if target < 0:
                        target = contr["default"]
                    else:
                        min_, max_ = contr['min'], contr['max']
                        rng_ = max_ - min_
                        exp_target = target ** 2#(math.exp(target) - 1) / (math.e - 1)
                        target = int(rng_ * exp_target + min_)
                    print(" GAIN minmax  ",min_, max_, target, cv2.CAP_PROP_GAIN)
                    self.cap.set(cv2.CAP_PROP_GAIN, target)

            if  ('gammatxt' in data) and self.device.find("/dev/video") >= 0:
                if not 'gamma' in self.controls_dict.keys():
                    pass
                else:
                     target = data['gammatxt']
                     contr = self.controls_dict["gamma"]
                     min_, max_ = contr['min'], contr['max']
                     if target < 0:
                         target = contr["default"]
                     else:
                         min_, max_ = contr['min'], contr['max']
                         rng_ = max_ - min_
                         exp_target = target ** 2#(math.exp(target) - 1) / (math.e - 1)
                         target = int(rng_ * exp_target + min_)
                     print(" GAMMA minmax  ",min_, max_, target, cv2.CAP_PROP_GAMMA)
                     self.cap.set(cv2.CAP_PROP_GAMMA, target)

 # __________________________________  hybrid request ended ________________________________

 #############################################
 #  mmmm  mmmmmm mmmmmmmmmmmmm m    m mmmmm  #
 # #"   " #      #        #    #    # #   "# #
 # "#mmm  #mmmmm #mmmmm   #    #    # #mmm#" #
 #     "# #      #        #    #    # #      #
 # "mmm#" #mmmmm #mmmmm   #    "mmmm" #      #
 #############################################

    # ================================================================================
    # SETUP            SETUP     SETUP
    # --------------------------------------------------------------------------------

    def setup(self, action="i", number=1):
        """
        remember zoom, center, integr locgamma loc rotate
        before creating anything, be sure to load previous
        """
        FILENAME = os.path.expanduser(f'~/.flashcam_ng_uni_dict_{number}.json') # keys 1 2 3 4
        self.post_addr = None
        if self.internet_not_device:
            # ???? HACK MQTT here???to http??
            self.post_addr = self.url.replace("/video", "/cross")

        if self.url in self.setup_dict:
            pass
        else:
            if len(self.setup_dict) == 0:
                if os.path.exists(FILENAME):
                    with open( FILENAME, 'r') as f:
                        self.setup_dict = json.load(f)

            self.setup_dict[self.url] = {}

        # now i have it for each url
        if action == "q": # quit
            self.zoomme = 1
            self.redcross = [0, 0]
            self.l_gamma = 1 # local is 1
            self.l_rotate = 0

            self.r_integrate = 0
            self.r_gain = 0.5 # self.setup_dict["gain"]
            self.r_expo = 0.5 # self.setup_dict["gain"]
            self.r_gamma = 0.5 # self.setup_dict["gain"]

            self.r_gaindef = True # self.setup_dict["gain"]
            self.r_expodef =  True # self.setup_dict["gain"]
            self.r_gammadef = True # self.setup_dict["gain"]
            self.r_xtend = "  " # no remote extense

            self.send_command( data={"switch_res_off": "SWITCH_RES_OFF"})
            self.r_xtend = "  "
            time.sleep(1.5)
            self.send_command( data= {"accum": "ACCUM", "accumtxt": 0})
            time.sleep(0.5)
            self.send_command( data= {"expot": "EXPOT", "expotxt": -1})
            time.sleep(0.5)
            self.send_command( data= {"gaint": "GAINT", "gaintxt": -1})
            time.sleep(0.5)
            self.send_command( data= {"gammat": "GAMMAT", "gammatxt": -1})


        if action == "i" or len(self.setup_dict[self.url]) == 0: # init
            self.setup_dict[self.url]["zoomme"] = self.zoomme
            self.setup_dict[self.url]["redcross"] = self.redcross
            self.setup_dict[self.url]["l_gamma"] = self.l_gamma
            self.setup_dict[self.url]["l_rotate"] = self.l_rotate
            self.setup_dict[self.url]["r_integrate"] = self.r_integrate

            self.setup_dict[self.url]["r_gain"] = round(self.r_gain, 3)
            self.setup_dict[self.url]["r_expo"] = round(self.r_expo, 3)
            self.setup_dict[self.url]["r_gamma"] = round(self.r_gamma, 3)

            self.setup_dict[self.url]["r_gaindef"] = self.r_gaindef
            self.setup_dict[self.url]["r_expodef"] = self.r_expodef
            self.setup_dict[self.url]["r_gammadef"] =self.r_gammadef

            self.setup_dict[self.url]["r_xtend"] =self.r_xtend

        if action == "a": # apply
            if self.url in self.setup_dict:
                self.zoomme = self.setup_dict[self.url]["zoomme"]
                self.redcross = self.setup_dict[self.url]["redcross"]
                self.l_gamma = self.setup_dict[self.url]["l_gamma"]
                self.l_rotate = self.setup_dict[self.url]["l_rotate"]
                self.r_integrate = self.setup_dict[self.url]["r_integrate"]

                self.r_gain = self.setup_dict[self.url]["r_gain"]
                self.r_expo = self.setup_dict[self.url]["r_expo"]
                self.r_gamma = self.setup_dict[self.url]["r_gamma"]

                self.r_gaindef = self.setup_dict[self.url]["r_gaindef"]
                self.r_expodef = self.setup_dict[self.url]["r_expodef"]
                self.r_gammadef = self.setup_dict[self.url]["r_gammadef"]

                print("D... xtend OLD:", self.r_xtend )
                old_r_xtend = self.r_xtend
                self.r_xtend = self.setup_dict[self.url]["r_xtend"]

                # ------------------------------------------------------------ EXTENDING FIRST --------------------
                print("D... xtend NEW", self.r_xtend )
                #if (self.r_xtend == "  "):
                #    print("D... no xtending, pass")
                #    pass
                #else:
                if old_r_xtend == self.r_xtend:  # same stuff...
                    print("D... old == new, i digress")
                    pass
                elif self.r_xtend == "  ":  # easy part - switch  off ------------------------------------
                    print("D...  xtending to '  ' (unzoom) ")
                    self.send_command( data={"switch_res_off": "SWITCH_RES_OFF"})
                    time.sleep(1.5)
                elif self.r_xtend != "  ":  # complicated - for sure there will be high resolution ---------
                    print("D...  target xtend is no '  '" )
                    if old_r_xtend != "  ": # already at high resolution
                        if old_r_xtend[0] != self.r_xtend[0]: # LR
                            pass
                        elif old_r_xtend[1] != self.r_xtend[1]: #UD
                            pass
                    else:#  not  yet at high resolution
                        print("D... Starting High Res to 'CC'...i think ")
                        print("D...  xtending to 'CC' (zoom) ")
                        self.send_command(  data={"switch_res_on": "SWITCH_RES_ON"})
                        old_r_xtend = "CC" # Pretend this !!
                        print("D... old_r_xtend  redefined", old_r_xtend)
                        time.sleep(1.9)
                # ------------------------------- hi res should be ok here ---- but not the quadrant ---------

                if (self.r_xtend[0] == "L" and old_r_xtend[0] == "C") or (self.r_xtend[0] == "C" and old_r_xtend[0] == "R"):
                    print("D...  xtending to L-   ")
                    self.send_command(  data={"left": "LEFT"})
                    time.sleep(0.7)
                if (self.r_xtend[0] == "C" and old_r_xtend[0] == "L") or (self.r_xtend[0] == "R" and old_r_xtend[0] == "C"):
                    print("D...  xtending to R-   ")
                    self.send_command( data={"right": "RIGHT"})
                    time.sleep(0.7)
                if (self.r_xtend[1] == "C" and old_r_xtend[1] == "D") or (self.r_xtend[1] == "U" and old_r_xtend[1] == "C"):
                    print("D...  xtending to -U   ")
                    self.send_command( data={"up": "UP"})
                    time.sleep(0.7)
                if (self.r_xtend[1] == "C" and old_r_xtend[1] == "U") or (self.r_xtend[1] == "D" and old_r_xtend[1] == "C"):
                    print("D...  xtending to -D   ")
                    self.send_command( data={"down": "DOWN"})
                    time.sleep(0.7)
                else:
                    print("D...  xtending -  other situation, not extending")

                # ------------------------------------------------------------ Accum second --------------------


                print("D...  accum ...  ")
                self.send_command( data= {"accum": "ACCUM", "accumtxt": int(self.r_integrate)})
                time.sleep(0.5)

                print("D...  expot ...  ")
                if self.r_expodef:
                    self.send_command( data= {"expot": "EXPOT", "expotxt": -1})
                else:
                    self.send_command( data= {"expot": "EXPOT", "expotxt": round(self.r_expo, 3)})
                time.sleep(0.7)
                print("D...  gain ...  ")
                if self.r_gaindef:
                    self.send_command( data= {"gaint": "GAINT", "gaintxt": -1})
                else:
                    self.send_command( data= {"gaint": "GAINT", "gaintxt": round(self.r_gain, 3)})
                time.sleep(0.7)
                print("D...  gamma ...  ")
                if self.r_gammadef:
                    self.send_command( data= {"gammat": "GAMMAT", "gammatxt": -1})
                else:
                    self.send_command( data= {"gammat": "GAMMAT", "gammatxt": round(self.r_gamma, 3)})
                #-----------------

                # ------------------------------------------------------------ Timelaps now...------------------
                #  !!!!!!!!!!!!!!! udelat timelaps, that would do the same good for local video

        #----------------------- end of apply----

        elif action == "w": # write
            print(f"i... writing {FILENAME}")
            with open(FILENAME, 'w') as f:
                json.dump(self.setup_dict, f)

        elif action == "r":
            if os.path.exists(FILENAME):
                with open( FILENAME, 'r') as f:
                    self.setup_dict = json.load(f)



 ###########################################################
 #                               m                    m    #
 #  mmm   m   m   mmm    m mm  mm#mm   mmm   m   m  mm#mm  #
 # #" "#  "m m"  #"  #   #"  "   #    #"  #   #m#     #    #
 # #   #   #m#   #""""   #       #    #""""   m#m     #    #
 # "#m#"    #    "#mm"   #       "mm  "#mm"  m" "m    "mm  #
 ###########################################################


    # ================================================================================
    #                               OVERTEXT
    # --------------------------------------------------------------------------------

    def overtext(self, blackbar=False, image=None):
        """
        great font for small numbers
        """
        #
        #
        #
        selfimg = image
        if selfimg is None:
            selfimg = self.img
        # ---------------------------
        if selfimg is None:
            return

        #print(f"D...  overtext {self.img.shape}   ")
        RXT = f"XT:{self.r_xtend}" #  CC LU ... for remote ok
        ZOO = f"ZOO:{self.zoomme:3.1f}"
        ROO = f"ROT:{self.l_rotate:3.1f}"
        LGA = f"LGAM:{self.l_gamma:3.1f}"
        SAV = f"      "
        if self.saving_all: # not used anymore
            SAV = f"SAVING"
        LAPS = f"LAPS:{self.saving_laps:3d}"
        if self.l_timelaps:
            LAPS = f"LLAP:{self.l_timelaps_seconds:3d}"
        #
        FIT = f"        "
        if self.saving_fits_only:
            FIT = f"FITS {self.FITS_INTERVAL_SECONDS:3d}"

        # ---------------------- ACCUM
        total_size = sys.getsizeof(self.FABuffer)
        cur_size = len(self.FABuffer)
        max_size = self.FABuffer.get_max_frames()
        total_size = sys.getsizeof(selfimg) * cur_size

        #if self.accum_buffer is not None:
        #    total_size = sys.getsizeof(self.accum_buffer) + sum(sys.getsizeof(arr) for arr in self.accum_buffer)
        #BUF = f"BUF={self.accum_count:3d}/{self.accum_n:3d} {total_size/1024/1024:5.0f} MB"
        bufshow = "(   )"
        if self.l_show_accum:
            if self.l_show_accum_avg:
                bufshow = "(AVG)"
            else:
                bufshow = "(SUM)"
        else:
            bufshow = "(   )"
        bgfg1 = "  "
        bgfg2 = "  "
        if self.image_foreground is not None: bgfg1 = "FG"
        if self.image_background is not None: bgfg2 = "BG"

        BUF = f"BUF{bufshow}={cur_size:3d}/{max_size:3d} {total_size/1024/1024:5.0f} MB"
        #
        #*********************************** HERE I CONTRUCT THE BOTTOM LINE ***********************
        #
        #overtext = f"{self.frame_time} # {self.frame_num} # {self.l_frame_num:6d} #  {RXT} . {ZOO} . {ROO} . {LGA} . {SAV} {FIT} . {BUF}. {LAPS}"
        # SAVING is already red
        #overtext = f"{self.frame_time} # {self.frame_num} # {self.l_frame_num:6d} #  {RXT} . {ZOO} . {ROO} . {LGA} . {FIT} . {BUF}. {LAPS}"
        # ROTATE IS LOCAL
        #overtext = f"{self.frame_time} # {self.frame_num} # {self.l_frame_num:6d} #  {RXT} . {ZOO} .  {LGA} . {FIT} . {BUF}. {LAPS}"
        # I add BG-FG
        overtext = f"{self.frame_time} # {self.frame_num} # {self.l_frame_num:6d} #  {RXT} . {ZOO} .  {LGA} . {FIT} . {bgfg1}{bgfg2} . {BUF}. {LAPS}"
        #
        position = ( 0, selfimg.shape[0]-1 ) # 480 on x-axis
        #

        if blackbar:
            overlay = selfimg.copy()
            if self.resolution == "1920x1080":
                shade_height = 20
            else:
                shade_height = 10
            height, width = selfimg.shape[:2]
            cv2.rectangle(overlay, (0, height - shade_height), (width, height), (0, 0, 0), -1)
            alpha = 0.5
            #alpha = 0.
            #cv2.addWeighted(overlay, alpha, self.frame, 1 - alpha, 0, self.frame)
            cv2.addWeighted(overlay, alpha, selfimg, 1 - alpha, 0, selfimg)
        #
        font = "di"
        if self.resolution == "1920x1080":
            font = "di2"
        selfimg = iprint(selfimg, str(overtext), font=font, position=position,color_rgb=(0,255,0) )
        if self.SAVED_NOW:
            position = (  selfimg.shape[1] - 20, selfimg.shape[0]-1 ) # 480 on x-axis
            selfimg = iprint(selfimg, f"SAVE", font=font, position=position,color_rgb=(0,0,255) ) # bgr
        self.img = selfimg




    # ======================================================================
    #  make folder give the correct timetag - original if possible
    #
    #                  SAVING
    #
    # ----------------------------------------------------------------------

    def prepare_save(self, png=False, time_tag=None):
        #   .....   self.saving_fits_only is not necessary, handled elsewhere
        dir2create = os.path.expanduser("~/DATA/")
        if not os.path.isdir(os.path.expanduser(dir2create)):
            print(f"D... trying to create directory {dir2create} for saving")
            # result = False
            os.mkdir(os.path.expanduser(dir2create))
        now = time_tag
        if time_tag is None:
            now = dt.datetime.now().strftime( '%Y%m%d_%H%M%S.%f')[:-4]  # dot fraction - should be conform with other parts
        else:
            if len(time_tag) < 12:
                # http         variant       # 20:23:46.12
                now = dt.datetime.now().strftime( '%Y%m%d_')+now.replace(":", "")
            else:
                # full variant from mqtt
                now1 = dt.datetime.strptime(now, '%Y-%m-%d %H:%M:%S.%f')
                #print("1", now1, type(now1))
                now1 = now1.strftime('%Y%m%d_%H%M%S.%f')
                #print("2", now1, type(now1))
                now = str(now1)[:-4]
                #print("3", now)
        ext = "jpg"
        if png:ext = "png"
        #if self.saving_fits_only:ext = "fits" # not necessary here...
        host = socket.gethostname()
        murl = ""
        #print("POOP", self.url)
        if self.url.find("http://") >= 0:
            murl = self.url.split("http://")[-1]
            murl = murl.split("/")[0]
            murl = murl.replace(":", "_")
        elif self.url.find("mqtt://") >= 0:
            murl = self.url.split("mqtt://")[-1]
            #print("10", murl)
            murl = murl.split("/")[0]
            murl = murl.replace(":", "_")
            #print("11", murl) # pure IP
            extmurl = self.mqtt_topic.split("/")[-1]
            murl = f"{murl}_{extmurl}"
            #print("12", murl) # pure IP
        elif self.url.find("/dev/video") >= 0:
            murl = self.url.split("/dev/")[-1]
        else:# also  code doesnt go  here
            murl = murl.split("/")[0]
            murl = murl.replace(":", "_")
        sfilenamea = os.path.expanduser(f"~/DATA/{host}_{murl}_{now}.{ext}"  )
        return sfilenamea

    # ======================================================================
    #
    # ----------------------------------------------------------------------

    def save_fits_in_background(self, data_cube, fname, numero=None):
        """
        numero means slice in the cube - cube is no more though. but fits are one-by-one
        """
        newname = ""
        if numero is None:
            newfname = fname.replace(".jpg", "")
            newfname = f"{newfname}.fits"
        else:
            newfname = fname.replace(".jpg", f"_{numero:05d}")
            newfname = f"{newfname}.fits"
        #print(data_cube.shape )#q, 10, 480, 640, 3)  # it sees 3 640 8
        print(f" ... {newfname} ... ")
        lencube = data_cube.shape[0] # is 3 colors   (3, 480, 640)
        #print(lencube, data_cube.shape )
        width = data_cube.shape[2]
        height = data_cube.shape[1]
        def save():

            # J2000 for KSTARS
            RA = "05 41 42.57"
            DEC = "-01 51 22.6"
            ra_deg = hms_to_deg(RA)
            dec_deg = dms_to_deg(DEC)
            #print("RA  J2000 in degrees:", ra_deg)
            #print("DEC J2000 in degrees:", dec_deg)
            SCALE = 10 # size of the field
            w = wcs.WCS(naxis=2)
            w.wcs.crpix = [ int(width / 2), int(height / 2) ]
            #w.wcs.cdelt = np.array([-SCALE/3600, SCALE/3600]) # Originally but kstars reverted ///// it is always reverted 180
            w.wcs.cdelt = np.array([-SCALE/3600, -SCALE/3600]) # Perfect with the sky in kstars => but image is reverted 180 !!!
            w.wcs.crval = [ra_deg, dec_deg]
            w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
            header = w.to_header()

            #data_cuber = np.array([np.rot90(image, k=-1) for image in data_cube])
            #data_cuber = np.array([np.flipud(np.transpose(image)) for image in data_cube])
            hdu = fits.PrimaryHDU(data_cube, header=header)
            # a bit different - like in crfits
            hdul = fits.HDUList([hdu])
            hdr = hdul[0].header

            #hdr['SIMPLE'] = True  # -bit floating point
            #hdr['BITPIX'] = 8 # 480#8  # -bit floating point
            #hdr['NAXIS'] = 4      # Number of axes
            #hdr['EXTEND'] = True      # Number of axes
            #hdr['NAXIS1'] = data_cube.shape[2]  # Size of the first axis (width)
            #hdr['NAXIS2'] = data_cube.shape[1]  # Size of the second axis (height)
            #hdr['NAXIS3'] = data_cube.shape[3]  # Size of the third axis (number of images)
            #hdr['NAXIS4'] = lencube #3  # Size of the third axis (number of images)
            hdr['FOCALLEN'] = (300.0, 'Focal length in mm (works)')
            hdr['OBJECT'] = (' TestObj NGC2024', "Target Description")
            #hdr['DATA-TYP'] = ('OBJECT  ', " Characteristics of this data")
            hdr['OBJCTRA'] = (RA, 'Right Ascension in hms (wrks siril)')
            hdr['OBJCTDEC'] = (DEC, 'Declination in dms (wrks siril)')
            #hdr['RA'] = (RA, 'Right Ascension in hms')
            #hdr['DEC'] = (DEC, 'Declination in dms')
            # ----- this and probably SCALE make arcsec / pixel in Siril
            #   --------- BUT ALSO FORCES TO SHOW arcsec for FWHM /
            #   ------------- if commented: FWHM in pixels is shown
            hdr["XPIXSZ"] = (2.9, "IMX291 pixel size in microns ( wrks)")
            hdr["YPIXSZ"] = (2.9, "IMX291 pixel size in microns ( wrks)")
            hdr["IMAGEW"] = (width, "Image width, in pixels.")
            hdr["IMAGEH"] = (height, "Image height, in pixels.")
            # Add current time to header
            current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            hdu.header['DATE'] = current_time
            hdu.header['DATEEXA'] = current_time
            hdr['HOST'] = (socket.gethostname(), 'host computer')
            hdr['SENSOR'] = ('imx291', 'sensor used')
            #hdu.header['CREATOR'] = 'Your Name'
            #hdu.header['DATE'] = '2025-05-12'

            hdul.writeto(newfname, overwrite=True) # .gz is too expensive too
        # -------------------------------------------------
        thread = threading.Thread(target=save)
        thread.start()


    ########################################################## #
    #                                      "                   #
    #  mmm    mmm   m   m   mmm          mmm    mmmmm   mmmm   #
    # #   "  "   #  "m m"  #"  #           #    # # #  #" "#   #
    #  """m  m"""#   #m#   #""""           #    # # #  #   #   #
    # "mmm"  "mm"#    #    "#mm"         mm#mm  # # #  "#m"#   #
    #                                                   m  #   #
    #                            """"""                  ""    #
    ########################################################## #

    # ===========================================================
    #
    # -----------------------------------------------------------
    def save_img(self, fname=None, time_tag=None, silent=True,  dumpbuffer=False, use_fits=False, use_buffer=None):
        """
        saving self.img

        FITS:    save all buffer members / save one as FITS (like no compression...metadata...)
        dumpbuffer:
        use_buffer is None OR THE BUFFER TO USE (level2)
        """
        fname1 = fname
        if fname is None:
            fname1 = self.prepare_save( time_tag=time_tag)
        if not silent: print(fname1)
        #---------- FITS *****
        if use_fits: # --------- FITS CASE --- more complex -------------------------------
            if dumpbuffer and (not self.l_show_accum): # ------ Do Just evry frame in the buffer
                print("           xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                  ")
                #mylst = []
                n = 1
                for i, info in self.FABuffer:#self.order_accum_buffer_frames(): # ITER WORKS BUT NO GREEN LABELS
                    i = np.moveaxis( i, [0, 1, 2], [1, 2, 0])
                    i = np.rot90(i, 2)
                    #mylst.append(i)
                    #data_cube3 = np.stack(mylst, axis=0)
                    self.save_fits_in_background(i, fname1, numero=n)
                    n += 1
            elif dumpbuffer and (self.l_show_accum) and (use_buffer is not None):   # I WILL NOT USE THIS ***********
                print("           xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                  ")
                #print("D... some way to save only one AVG image per Nbuf: TO DO!")   # TODO
                #mylst = []
                n = 1
                for i in use_buffer:#
                    i = np.moveaxis( i, [0, 1, 2], [1, 2, 0]) # 210=480 640 3;  120== 640 480 3 otoc
                    i = np.rot90(i, 2)
                    #i = i[..., [2, 1, 0]]
                    #mylst.append(i)
                    #data_cube3 = np.stack(mylst, axis=0)
                    self.save_fits_in_background(i, fname1, numero=n)
                    n += 1
            elif (not dumpbuffer) and  (not self.l_show_accum):
                print("... just one foto in FITS, why not") # trivial   ------- NOBUFFER
                mylast = self.FABuffer.get_last_img()#self.accum_buffer[self.accum_index]
                i = np.moveaxis( mylast, [0, 1, 2], [1, 2, 0])
                i = np.rot90(i, 2)
                self.save_fits_in_background(i, fname1)
            elif (not dumpbuffer) and  (self.l_show_accum):
                print(" ... provide average, 1 image in FITS") # trivial ------- NOBUFFER
                mymean = self.FABuffer.get_sum_frames()#get_mean_accum_buffer()
                i = np.moveaxis( mymean, [0, 1, 2], [1, 2, 0])
                i = np.rot90(i, 2)
                self.save_fits_in_background(i, fname1)
        # -------  JPG ****   ****  **** **** *** *** * * * *
        else:#                                              --------NOT FITS
            if (dumpbuffer) and (not self.l_show_accum):
                # dump buffer - straight
                mycnt = 0
                #for i in self.order_accum_buffer_frames(): # ITER WORKS BUT NO GREEN LABELS
                for i, info in self.FABuffer:
                    mycnt += 1
                    fff = fname1.replace(".jpg", f"_{mycnt:03d}.jpg")
                    print(fff)
                    # ----------------------- Overtext shoud be IMPROVED FOR DUMPED BUFFER
                    if self.flag_print_over:
                        self.overtext(blackbar=True, image=i) # ---- after ACCUM ------------------  img should be tagged
                        i = self.img
                    print(fg.magenta, "D... simple save - overtext solved ", fg.default, end="\n")
                    if self.saving_jpg:
                        cv2.imwrite(fff, i, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                    else:
                        cv2.imwrite(fff.replace("jpg", "png"), i )
                pass
            # -----------------------------------------------
            elif (not dumpbuffer) and (not self.l_show_accum):
                print(fg.magenta, "D... simple save overtext is there", fg.default)
                # This is a simple save
                if self.saving_jpg:
                    cv2.imwrite(fname1, self.img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                else:
                    cv2.imwrite(fname1.replace("jpg", "png"), self.img )
            elif (dumpbuffer) and (self.l_show_accum):
                # -....
                print(fg.magenta, "D... the trickies - save every Nth-every new buffer - IDK ", fg.default)
            elif (len(self.FABuffer) < 2) and (not dumpbuffer):# and (self.l_show_accum):
                # ....
                print(fg.magenta, f"D... buffer <1; cannot dump; save SUM {not self.l_show_accum_avg}  or AVG {self.l_show_accum_avg}", fg.default)
                mymean = None
                if self.l_show_accum_avg: # not sum
                    mymean = self.FABuffer.get_avg_frames()
                else:#                    # yes sum
                    mymean = self.FABuffer.get_sum_frames()
                # NO OVERTEXT !  ! ! !  !  !  SOLVED
                if self.flag_print_over:
                    self.overtext(blackbar=True, image=mymean)
                    mymean = self.img
                if self.saving_jpg:
                    cv2.imwrite(fname1, mymean, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                else:
                    cv2.imwrite(fname1.replace("jpg", "png"), mymean )
            elif (len(self.FABuffer) > 1) and (not dumpbuffer):# and (self.l_show_accum):
                # ....
                print(fg.magenta, "D... buffer >1; do not dump; save SUM or AVG", fg.default)
                mymean = None
                if self.l_show_accum_avg: # not sum
                    mymean = self.FABuffer.get_avg_frames()
                else:#                    # yes sum
                    mymean = self.FABuffer.get_sum_frames()
                # NO OVERTEXT !  ! ! !  !  !  SOLVED
                if self.flag_print_over:
                    self.overtext(blackbar=True, image=mymean)
                    mymean = self.img
                if self.saving_jpg:
                    cv2.imwrite(fname1, mymean, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                else:
                    cv2.imwrite(fname1.replace("jpg", "png"), mymean )


    # ======================================================================
    #
    # ----------------------------------------------------------------------

    def get_passfile(self, videodev ):
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


    # ==================================================
    #
    # --------------------------------------------------



    # ================================================================================
    #   FINAL TRANSFORM
    # --------------------------------------------------------------------------------

    def final_transformations(self, myimage ): # self.rgb_image or self.img
        """
        all independent on self.
        """
        if self.l_rotate != 0:
            myimage = rotate_image(myimage, self.l_rotate)

        if self.l_gamma != 1:
            myimage = adjust_gamma(myimage, self.l_gamma)

        if self.zoomme > 1:
            if len(myimage.shape)==3:
                height, width, channels = myimage.shape
            else:
                height, width = myimage.shape
            #prepare the crop
            centerX = int(height/2)
            centerY = int(width/2)

            if (self.redcross[0]!=0) or (self.redcross[1]!=0):
                dwidth = -self.redcross[0]    #negative up
                dheight = -self.redcross[1]   # positive down
                T = np.float32([[1, 0, dwidth], [0, 1, dheight]])
                myimage = cv2.warpAffine(myimage, T, (myimage.shape[1], myimage.shape[0]))

            radiusX,radiusY= int(height/2/self.zoomme),int(width/2/self.zoomme)
            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY
            cropped = myimage[minX:maxX, minY:maxY]
            myimage = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_NEAREST)
        return myimage



 ################################################################################
 #                   #           m                    "                         #
 # m   m  mmmm    mmm#   mmm   mm#mm   mmm          mmm    mmmmm   mmm    mmmm  #
 # #   #  #" "#  #" "#  "   #    #    #"  #           #    # # #  "   #  #" "#  #
 # #   #  #   #  #   #  m"""#    #    #""""           #    # # #  m"""#  #   #  #
 # "mm"#  ##m#"  "#m##  "mm"#    "mm  "#mm"         mm#mm  # # #  "mm"#  "#m"#  #
 #        #                                                               m  #  #
 #        "                                 """"""                         ""   #
 ################################################################################


    # ==================================================
    #  UPDATE IMAGE   ****************************************************  KEY ACTION TO QT display
    # --------------------------------------------------

    def update_image(self, rgb_image):
        """
        QT6 -  Stream Widget!!!!!  self==stream  technically takes img and put pixmap
        """

        if rgb_image is None:return # 1st contact may no exist


        #self.rgb_image.shape

        h, w, ch = rgb_image.shape

        maxw = 1280
        if w > maxw:#1280:#640:
            rati = w / maxw
            w = maxw
            h = int(h / rati)
            rgb_image = cv2.resize(rgb_image, (w, h ), interpolation=cv2.INTER_NEAREST)

        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data,  w,  h, bytes_per_line, QImage.Format.Format_RGB888)

        # --  I can extrend the display window
        if self.xtended:
            qt_image = qt_image.scaled(2 * w, 2 * h)
            self.resize(2 * w, 2 * h)
        else:
            self.resize( w,  h)
        self.setPixmap(QPixmap.fromImage(qt_image))


    # ==================================================
    #
    # --------------------------------------------------

    def get_stream(self, videodev):
        """
        I start with password and continue with REQ
        """
        u, p = getpass.getuser(), "a"
        passfile = self.get_passfile( videodev )
        passfile = f"{FILE_USERPASS}_{passfile}"
        nopass = True
        try:
            with open(os.path.expanduser(passfile)) as f:
                #print("i...  PASSWORD FILE  ", passfile)
                w1 = f.readlines()
                u = w1[0].strip()
                p = w1[1].strip()
                nopass = False
        except:
            print("X... NO PASSWORD FILE (gs) ", os.path.expanduser(passfile))
            nopass = True
        if nopass:
            print("X....   user pass not found ...... can be a bit problem .... ")
            #sys.exit(1)


        # ----------------------------------------------------------
        request = urllib.request.Request(videodev)
        #print("D... USER/PASS", u, p)
        base64string = base64.b64encode(bytes("%s:%s" % (u, p), "ascii"))
        #print("D... stream ok1", base64string)
        request.add_header("Authorization", "Basic %s" % base64string.decode("utf-8"))
        print("D...  @urlopen: ", end=" ==>> ")
        #
        ok = False
        stream = None
        self.error = False
        self.which_error = ""
        try:
            stream = urllib.request.urlopen(
                request, timeout=4
            )  # timeout to 7 from 5 sec.
            ok = True
            print(" stream ok ", end="")
        except urllib.error.HTTPError as e:
            print(f"Srv Offline {e} {videodev} ", end="\n")
            self.which_error = "http error"
            self.error = True
            # do stuff here
        except urllib.error.URLError as e:
            print(f"Srv Offline {e} {videodev} ", end="\n")
            self.which_error = "url  error"
            # do stuff here
            self.error = True
        except:
            self.error = True
            self.which_error = "timeout error"
            print("X.... Timeouted on URLOPEN", end="\n")
        if nopass:
            self.which_error = f"{self.which_error} / NOPASS" # no password file
        if not ok and self.which_error ==  "timeout error":
            time.sleep(1) # extra sleep
        print( f"{str(dt.datetime.now() )[:-4]}....", end="\r")

        return stream




    # ==================================================
    #  NOT USED
    # --------------------------------------------------

    def trim_bytex(self, max_size):
        if len(self.bytex) > max_size:
            self.bytex = self.bytex[-max_size:]



    # ==================================================
    #  COPY frame to img
    # --------------------------------------------------
    # ===============================================================================
    #             VCR SCR
    # ===============================================================================
    def vcr_pal_style(self, messages, eximg=None):
        w, h = 640, 480
        img = eximg
        if eximg is None:
            img = np.zeros((h, w, 3), dtype=np.uint8)
            img[:] = (255, 0, 0)  # Blue background

        color = (0, 255, 255)  # Yellow text
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.0
        thickness = 2

        lines = messages#.split(',')
        n = len(lines)
        line_height = h // (n + 1)

        for i, line in enumerate(lines, 1):
            (text_w, text_h), _ = cv2.getTextSize(line, font, scale, thickness)
            org = ((w - text_w) // 2, line_height * i + text_h // 2)
            cv2.putText(img, line, org, font, scale, color, thickness, cv2.LINE_AA)

        self.img = img
        #cv2.imshow('VCR PAL Style', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


    # ================================================================================
    #     COPY FRAME TO IMG .................
    # --------------------------------------------------------------------------------

    def use_frame(self, stripes=False):
        """
        put frame on tom of img .... ONLY HERE  ..... also failed strips....
        """
        def vcr_write( eximg=None):
            addi = ""
            if self.internet_mqtt:
                addi = f"proto mqtt:// ; topic: {self.mqtt_topic}"
            elif self.internet_not_device:
                addi = "proto http://"
            else:
                addi = "no device found"
            self.vcr_pal_style(["GOT NO FRAME", "", f"URL:{self.url}", f"{addi}"], eximg=eximg)

        if self.frame is None:
            # NEVER ACTIVE.................... 1st frame is STRIPES!
            print("X... no image", end="")
            time.sleep(0.2)
            #if stripes: # THIN
            #    for y in range(0, self.img.shape[0], 16):
            #        self.img[y:y + 1, :, :] = np.zeros((1, self.img.shape[1], 3), dtype=np.uint8) + 120
            if self.which_error == "": #
                vcr_write()
            else:# when connection refused...
                self.vcr_pal_style([ self.which_error, "", "URL:", f"{self.url}"])
            return False
        #--------------------- ^^^  never started. Frame was always None ______________----
        # ___________________ vvv  started, make gray strips _____________________________
        ret_val = False
        if True:# self.img.shape == self.frame.shape:
            self.img = self.frame.copy()
            if not self.image_background is None:
                #self.img = self.img - self.image_background
                self.img = cv2.subtract(self.img , self.image_background )
            if not self.image_foreground is None:
                #self.img = self.img + self.image_foreground
                self.img = 0.5*self.img + 0.5*self.image_foreground
            if stripes: # These are thin gray
                self.img = np.clip(self.img * 0.5, 0, 255).astype(np.uint8)
                vcr_write(eximg=self.img)
                #self.vcr_pal_style(["NO SIGNAL"], eximg=self.img) # vcr over image
                for y in range(0, self.img.shape[0], 16):
                    self.img[y:y + 1, :, :] = np.zeros((1, self.img.shape[1], 3), dtype=np.uint8) + 120
            ret_val = True
        #
        return ret_val

    # ================================================================================
    # CLICK TRICK to recover resolution in CLI
    # --------------------------------------------------------------------------------

    #def parse_resolution(self, ctx, param, value):
    def parse_resolution(self,  value):
        try:
            w, h = map(int, value.lower().split('x'))
            return w, h
        except Exception:
            raise click.BadParameter("Resolution must be in WIDTHxHEIGHT format, e.g. 1920x1080")



 ####################################################
 #                        m                         #
 #  mmm    mmm   mmmm   mm#mm  m   m   m mm   mmm   #
 # #"  "  "   #  #" "#    #    #   #   #"  " #"  #  #
 # #      m"""#  #   #    #    #   #   #     #""""  #
 # "#mm"  "mm"#  ##m#"    "mm  "mm"#   #     "#mm"  #
 #               #                                  #
 #               "                                  #
 ####################################################


    # ================================================================================
    #   CAPTURE
    # --------------------------------------------------------------------------------

    def capture_only(self, resolution="640x480", fourcc="YUYV"):
        width, height  = self.parse_resolution(resolution)
        ### print(f"D... cap == {self.cap}  ")
        if self.cap is None:
            fourcc = self.fourcc #
            print("i... connecting device ", self.device )
            self.controls_dict = get_v4l2_controls(self.device)
            if self.controls_dict is None: self.which_error = "Device not found"

            self.cap = cv2.VideoCapture(  int(self.device[-1])  , cv2.CAP_V4L2)
            fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
            self.cap.set(cv2.CAP_PROP_FOURCC, fourcc_code)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        else:
            ret, self.frame = self.cap.read()
            #### print(f"D...  ret = {ret} ")
            if ret is False:
                self.frames_to_fail -=1
            if ret is False and (self.frames_to_fail <= 0): # cap is set but ret is False, no video case (wierd)
                print(f"D... reseting cap"  )
                self.cap = None
                time.sleep(2)
                self.frames_to_fail = self.frames_to_fail_max

            #self.frame_time = dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-4]
            self.l_frame_time = dt.datetime.now()
            self.frame_time = self.l_frame_time.strftime("%H:%M:%S.%f")[:-4]
            if not ret:
                return False
            print(f" ... {self.frame_time} ; resolution /{self.frame.shape}/  .... ", end="")
            # ADD ONE FRAME !!!!!!!!
            self.l_frame_num += 1
            #avg = self.frame # once per Nx it is AVG
            #self.img = avg # normally frame. but sometimes avg == really averaged img!
            self.img = self.frame.copy()
        return True




    # ==================================================
    #  FETCHING THE IMAGE FROM internet VIDEODEV  ------------  ALSO INITI
    # --------------------------------------------------

    def fetch_only(self):
        """
        called from from fetch_and_update()  / returns BOOL
        """
        ret_val = False
        if self.stream is None:     #   INITIALIZE THE STREAM -----------------
            #self.make_strips()
            self.stream = self.get_stream(videodev=self.url)
            if self.stream is not None:
                print("\ni....  stream acquired")
            else:
                time.sleep(1) # dont be too offensive
                return False
        if self.stream is not None:
        #else:# I have the stream -----------------------------------------
            ret_val = False
            # --------- try to grab stream ------------
            try:
                print(f"i... acq {self.stream_length/1024:.1f} kB ", end="")
                delta_wait = 0
                self.t_oldread = self.t_preread
                self.t_preread = dt.datetime.now()
                delta_loop = (self.t_preread - self.t_oldread).total_seconds() # FULL LOOP
                # ------------------------ ******
                self.bytex += self.stream.read(self.stream_length)
                # ------------------------ *******
                self.t_posread = dt.datetime.now()
                delta_read = (self.t_posread-self.t_preread).total_seconds() # wait
                if delta_read < 0.01:
                    time.sleep(0.03)
                    self.t_posread = dt.datetime.now()
                    delta_read = (self.t_posread-self.t_preread).total_seconds() # wait

                self.t_lasread = self.l_frame_time
                self.l_frame_time =  dt.datetime.now()
                delta_frame = (self.l_frame_time - self.t_lasread).total_seconds() # TOTAL
                self.l_frame_num += 1 # INCREMENT LOCAL FRAME NUMBER
                #
                print(f" ; {self.stream_length/delta_frame/1024/1024*8:4.2f} Mbs .. buffer tot= {len(self.bytex)/1024:4.1f} kB;  Reading:{delta_read:4.2f} s.;  TOT {str(delta_frame)[:4]} s.;  Duty {int((delta_frame-delta_read)/delta_frame*100):3.0f} % ", end="")
                #
            except:
                self.bytex = b""
                #print()
                self.stream = None
            a = self.bytex.find(b"\xff\xd8")  # frame starting
            b = self.bytex.find(b"\xff\xd9")  # frame ending
            ttag = self.bytex.find( "#FRAME_ACQUISITION_TIME".encode("utf8") )  # frame ending
            webframen = " " * 7
            webframetime = " " * 23
            if ttag != -1:
                # print(f"i... FRACQT: /{ttag}/ \
                    # /{bytex[ttag:ttag+32]}/----------------")
                webframen = self.bytex[ttag: ttag + 32 + 23].decode("utf8")
                self.frame_num, self.frame_time = " " * 7, " " * 23
                if "#" in webframen:
                    webframen = webframen.split("#")
                    # print(len(webframen), webframen)
                    if len(webframen) > 3:
                        self.frame_num, self.frame_time = webframen[2], webframen[3]


            if a != -1 and b != -1: # jpg detected
                #io_none = 0
                # HERE THE TIME AND FRAME NUMBER ARE CURRENT
                print(f"#{self.frame_num} {self.frame_time} | {self.l_frame_num:7d} | {self.l_frame_time.strftime('%H:%M:%S.%f')[:-4]} ", end="")
                print(f"| LOS:{self.l_frame_bia:5d} ", end="")

                jpg = self.bytex[a: b + 2]
                if ttag != -1:
                    # this is with framen
                    self.bytex = self.bytex[b + 2 :]
                    self.stream_length = int((b + 2 - a) ) + 24 +  30 + 29# expected length 24 TEXT;30 FRAMNEMS; 29
                else:
                    self.bytex = self.bytex[b + 2 :]
                    self.stream_length = int((b + 2 - a) )  # expected length

                if self.stream_length < 1000: # if a -b == 0 reset
                    self.stream_length = self.stream_length_init
                # ****************  FINISH PRINT HERE **************
                #*****************print()
                #print(len(jpg))
                #print(f"...  jpg {len(jpg)} ")


                if len(jpg) > 1000:  # was crash here
                    # *******************************
                    self.frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    ret_val = self.use_frame() # COPY TO IMG and RETURN VALUE!
                    #
                    # --- tune the size of next JPG
                    #self.stream_length = int((b + 2 - a) / 2)  # expected length divided by 2
                else:
                    ret_val = False # small jpg is no good
            else:# no jpg detected
                ret_val = False # no change
            return ret_val



    # ==================================================
    #  FETCHING THE IMAGE FROM  ------------  MQTT
    # --------------------------------------------------



    def decode_payload(self, data):
        """
        MUST BE SAME AS SENDER
        """
        header_size = struct.calcsize('!HHQddIfff')  # SAME CODE  2x
        width, height, framenumber, timestamp_ts, recording_started_ts, _, exposition, gain, gamma = struct.unpack('!HHQddIfff', data[:header_size])
        image = np.frombuffer(data[header_size:], dtype=np.uint8).reshape((height, width, 3))
        timestamp = dt.datetime.fromtimestamp(timestamp_ts)
        recording_started = dt.datetime.fromtimestamp(recording_started_ts)
        return {
            'width': width,
            'height': height,
            'framenumber': framenumber,
            'timestamp': timestamp,
            'recording_started': recording_started,
            'exposition': exposition,
            'gain': gain,
            'gamma': gamma,
            'image': image
        }


    def on_message(self, client, userdata, msg):  # ___________ this seems to be MQTT callback _________
        """
        just copy content to frame and set flag
        """
        data = msg.payload
        #width, height = struct.unpack('!HH', data[:4])
        #image = np.frombuffer(data[4:], dtype=np.uint8).reshape((height, width, 3))
        #####image = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))
        data_block = self.decode_payload(data)  #   RECEIVE PAYLOAD !!!!!!!!!!
        self.frame_num = data_block['framenumber']
        self.frame_time = str(data_block['timestamp'])[:-4]
        self.frame = data_block['image'].copy()
        print(f"i... mqtt: shape={self.frame.shape} time={str(dt.datetime.now())[:-4]} frame#={self.frame_num} {data_block['exposition']:.3f}/{data_block['gain']:.3f}/{data_block['gamma']:.3f}", end="\r" )
        self.mqtt_new_image = True
        #print( flush=True)
        #cv2.imshow("Received Image", image)
        #cv2.waitKey(10)  # Needed to refresh window

    def subscribe_only(self):  # ___________________________________________ this seems to be MQTT subscribe function _____
        """
        called from from fetch_and_update()  / returns BOOL / I want to read image via mqtt 1883
        """
        if not self.mqtt_subscribed:
            #self.mqtt_broker = "10.10.104.17"
            #self.mqtt_topic = "image/raw"

            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) # mqtt.CallbackAPIVersion.VERSION1
            self.mqtt_client.on_message = self.on_message # __________HA-callback referred here__________
            remote_ip = self.url.split("mqtt://")[-1]
            print(f"D...   {remote_ip}")
            remote_ip = remote_ip.split("/")[0]
            print(f"D...   {remote_ip}")
            self.mqtt_client.connect( remote_ip, 1883, 60) #  no mqtt://  !!   ;60 seconds?
            self.mqtt_client.subscribe(self.mqtt_topic)
            print("i...  ... looping inside thread... on_message active")
            self.mqtt_subscribed = True
            # Start loop in a separate thread to handle network traffic
            thread = threading.Thread(target=self.mqtt_client.loop_start)
            thread.daemon = True
            thread.start()
            #self.mqtt_client.loop_forever()

        else:# ==================== it is subscribed =========================
            # just loop-wait for a new image
            waitmq = 0
            waitmq_t = 0.05
            waitmq_mx = int(2.0/ waitmq_t)  # x second timeout
            while True:
                waitmq += 1
                if waitmq > waitmq_mx:
                    return False#break
                #print(self.mqtt_new_image)
                if self.mqtt_new_image: # ALL ACTION HERE - use_frame; franum++ ....
                    self.mqtt_new_image = False
                    self.use_frame() # i copy grame
                    self.l_frame_num += 1
                    self.error = False
                    return True
                    #break
                else:
                    time.sleep(0.05) # 20fps max?
            #else:
            #    time.sleep(0.1)
            #    return False
                #break
                #time.sleep(0.1)
        return True



    # ==================================================
    #  FETCHING THE IMAGE FROM VIDEODEV AND ALL LOCAL-ACTIONS  ------------  ALSO INITIATING THE STREAM ------------
    #
    #  I think the main function here is fetch_and_update #
    #  - when IP,  it does fetch,  when not, it grabs image.
    #  -
    #
    # --------------------------------------------------

    def fetch_and_update(self):  # * * *  ** *  * * * *  * * * * * * * * *  * * * * * * * *  * * * *
        """
        main operation with image::  fetch_and_update + update_only
        """
        ret = None
        #print(f"....  fau : {self.internet_not_device} ")
        if self.internet_not_device:
            if self.internet_mqtt:
                ret = self.subscribe_only()   # MQTT -
            else:
                ret = self.fetch_only() # just normaly fetch
        else:
            #resol = "640x480"
            #resol = "1920x1080"
            ret = self.capture_only(self.resolution)
        self.update_only(ret)


 ##################################################################
 #                   #           m            mmmm  mm   m m      #
 # m   m  mmmm    mmm#   mmm   mm#mm   mmm   m"  "m #"m  # #      #
 # #   #  #" "#  #" "#  "   #    #    #"  #  #    # # #m # #      #
 # #   #  #   #  #   #  m"""#    #    #""""  #    # #  # # #      #
 # "mm"#  ##m#"  "#m##  "mm"#    "mm  "#mm"   #mm#  #   ## #mmmmm #
 #        #                                                       #
 #        "                                                       #
 ##################################################################



    # ================================================================================
    #         All the traNSFORMS and saves are here          CRUTIAL FOR PREPARING THE IMAGE
    # --------------------------------------------------------------------------------

    def update_only(self, ret_val):
        """
        called from fetch_and_update() ;  FINAL OPERATIONS ON FRAME IMG (incl SAVE) ; BEFORE QT
        """
        #        print() NOT FINAL \n
        # ___________________________________ whatever, RET VAL ------------RET VAL ------------RET VAL ------------
        # ___________________________  after this point - NO REFERENCE TO FRAME ***** only img *********************
        # ___________________________________ whatever, RET VAL ------------RET VAL ------------RET VAL ------------
        if ret_val and not self.error: # OK
            # IMG SHOULD BE HERE READY!!!!!!!!!!!!

            #self.l_frame_num += 1 # NOT GOOD!!!!!!!!!!!!!!!
            #print("D...  ...  franum", self.l_frame_num)

            # -------------------------  calculate bias to see lost frames count ----------------------
            # no change to frame
            if self.l_frame_offs is None or (self.l_frame_bia < 0):
                try:
                    self.l_frame_offs =  int(self.frame_num.lstrip('0')) - self.l_frame_num
                except:
                    pass
            self.l_frame_bia = 0
            if self.l_frame_offs is not None:
                try:
                    self.l_frame_bia = int(self.frame_num.lstrip('0')) - self.l_frame_num -  self.l_frame_offs
                except:
                    pass

            # CROSS
            if self.flag_redcross:
                self.img = crosson(self.img, self.redcross[0], self.redcross[1], color="r", box_large=True)



            # Final transformations before SAVE, you save zoomed------------------TRANNS OR NOT TRANS
            #    TRANS Before save
            if self.saving_transformed_image:
                self.img = self.final_transformations( self.img )
                    #self.SAVED_NOW = False  # this is for overtext RED save # maybe I dont need it

            #                  SAVING  organization    HERE
            #                  SAVING  organization    HERE
            #                  SAVING  organization    HERE
            #                  SAVING  organization    HERE
            #                  SAVING  organization    HERE
            #                  SAVING  organization    HERE

            #if self.level2_buffer is None:
            #    self.level2_buffer = buffers.AccumBuffer(self.img)
            #    self.level2_buffer.define_accum_buffer(  self.level2_buffer_max_size  ) # ???


            # DEFINE BUFFER, if not yet /  if overtext is before,  i have blurred timemarks
            # ---------------------------- if overtext is after  , i do not have greentext on image
            self.FABuffer.add( self.img, {'name':'test', 'time': dt.datetime.now()} )
            #if self.define_accum_buffer( self.accum_n ): # does  nothing if already exists
            #    self.add_to_accum_buffer( self.img) # No idea why fits has wrong colors

            # showing or NOT the average image   ************* SHO@WING *********** SHOWING **********
            if self.l_show_accum and (len(self.FABuffer) > 1):# and (len(self.accum_buffer) > 1):
                rimg = None
                if self.FABuffer.new_sum_available():
                    if self.l_show_accum_avg:
                        rimg = self.FABuffer.get_avg_frames()#_mean_accum_buffer()
                    else:
                        rimg = self.FABuffer.get_sum_frames()#_mean_accum_buffer()
                        #print("\n    new", type(rimg))
                        print(f"SATURATED: {self.FABuffer.get_saturated_pixel_count()}", end="") # only for SUM
                else:
                    rimg = self.FABuffer.get_previous_sum_frames()#_mean_accum_buffer()
                    #print("\n----pre", type(rimg))
                if rimg is not None:
                    self.img = rimg
                    #### self.overtext(blackbar=True) # applies on img

            if self.saving_all: #
                self.SAVED_NOW = True
            if self.flag_print_over:
                self.overtext(blackbar=True) # ---- after ACCUM ------------------  img should be tagged


            # # -- LAPS 1s 10s 60s  but also   accumulated local frames
            # if self.saving_laps == 0:
            #     pass
            # elif (self.saving_laps == 1) and self.accum_n > 2:
            #     #  this is not set to internet!!! and also it feels accum
            #     now = dt.datetime.now()
            #     if (now - self.saving_laps_last_save).total_seconds() > self.saving_laps: # at least 1s
            #         if len(self.accum_buffer) ==  1: # the trick to save only when accum image is available
            #             fitag = "X "
            #             if self.saving_fits_only:
            #                 fitag = f"{fitag}f"
            #             print(fg.red, f"L{self.saving_laps}{fitag}", fg.default, end="")
            #             self.saving_laps_last_save = now
            #             # IT IS  saving self.img.....
            #             # self.img = self.accum_image  # Would do just frame without real other actions...zoom...
            #             self.save_img( time_tag=self.frame_time + f"A{self.accum_n}", savingjpg=False, save_accum=True) #

            # elif self.saving_laps > 0:
            #     now = dt.datetime.now()
            #     if (now - self.saving_laps_last_save).total_seconds() > self.saving_laps:
            #         fitag = "! "
            #         if self.saving_fits_only:
            #             fitag = f"{fitag}f"
            #         print(fg.red, f"L{self.saving_laps}{fitag}", fg.default, end="")
            #         self.saving_laps_last_save = now
            #         self.save_img( time_tag=self.frame_time  , savingjpg=False) #
            DO_TIMELAPS = False
            if self.l_timelaps:
                if dt.datetime.now() > self.l_timelaps_last + dt.timedelta(seconds=self.l_timelaps_seconds):
                    print(f"\ni... {fg.cyan} TIMELAPS saving now {fg.default} ... every {fg.orange} {self.l_timelaps_seconds} s. {fg.default}")
                    self.l_timelaps_last = dt.datetime.now()
                    DO_TIMELAPS = True
            # ---- just save once -------------------- ************  "s" ***********
            if self.saving_once or DO_TIMELAPS:
                DO_TIMELAPS = False
                # jpg and NO AVG --------- No difference show_accum_not_showaccum if frabuffer ==1
                if (len(self.FABuffer) < 2)    and (not self.l_show_accum) and (not self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    print(f"\ni... {fg.red}SAVING ONE 1  B1 NOshac{fg.default}")
                    self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=False ) # one simple image
                    #print(fg.magenta, "\ns1 b1 shac", fg.default, end="\n")
                    self.saving_once = False
                elif (len(self.FABuffer) < 2)    and (self.l_show_accum) and (not self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    print()
                    print(f"i... {fg.red}SAVING ONE 2  B1   shac{fg.default}")
                    self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=False ) # one simple image
                    #print(fg.red, "\ns1", fg.default, end="\n")
                    self.saving_once = False
                # jpg and NO AVG
                elif (len(self.FABuffer) >= 2) and (not self.l_show_accum) and (not self.saving_fits_only):
                    print()
                    print(fg.red, "SAVING ONE 3  B2+  NOshac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False ) #  save one simple image only
                    self.saving_once = False
                # jpg and  AVG
                elif (len(self.FABuffer) < 2)  and (self.l_show_accum) and (not self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    print()
                    print(fg.red, "SAVING ONE 4  B1  shac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False ) # just one simple image /lshow inside
                    #print(fg.red, "F1", fg.default, end="")
                    self.saving_once = False
                    pass
                # jpg and AVG
                elif (len(self.FABuffer) >= 2) and (self.l_show_accum) and (not self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    #if self.accum_index >= len(self.FABuffer) - 1:
                    print()
                    print(fg.red, "SAVING ONE 5  B2+  shac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False ) # should be 1 AVG IMG
                    #print(fg.red, "F1", fg.default, end="")
                    self.saving_once = False
                # FITS and NO AVG ---------------------------------------------------------------------------- FITS
                elif (len(self.FABuffer) < 2)  and (not self.l_show_accum) and (self.saving_fits_only):
                    # no bufffer no loopshow YES fits
                    print()
                    print(fg.red, "SAVING ONE 6  B1  NOshac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=True ) # 1 img
                    #print(fg.red, "F1", fg.default, end="")
                    self.saving_once = False
                    pass
                # FITS and NO AVG
                elif (len(self.FABuffer) >= 2) and (not self.l_show_accum) and (self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    print(fg.red, "SAVING ONE 7  B2  NOshac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time , dumpbuffer=True, use_fits=True ) # dump buffer once
                    #print(fg.red, "F1", fg.default, end="")
                    self.saving_once = False
                    pass
                # FITS and avg
                elif (len(self.FABuffer) < 2)  and (self.l_show_accum) and (self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    print()
                    print(fg.red, "SAVING ONE 8  B1   shac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=True ) # one AVG
                    #print(fg.red, "F1", fg.default, end="")
                    self.saving_once = False
                    pass
                # FITS and avg  there are more
                elif (len(self.FABuffer) >= 2) and (self.l_show_accum) and (self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    #if self.accum_index >= len(self.FABuffer) - 1:
                    print()
                    print(fg.red, "SAVING ONE 9  B2+  shac ", fg.default, end="\n")
                    self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=True ) # many AVG IDK
                    #print(fg.red, "F1", fg.default, end="")
                    self.saving_once = False


            # ----  save ALL  -----------------  -------------------------------------------- ************  "shift-s" ***********
            #
            # ----  save ALL  -----------------  -------------------------------------------- ************  "shift-s" ***********
            if self.saving_all: # ---------------  Shift-S-------    ALWAYS PUT RED

                # jpg and NO AVG  when no frbuffer, showaccum makes no sense
                if (len(self.FABuffer) < 2)   and (not self.l_show_accum) and (not self.saving_fits_only):
                    print()
                    print(fg.red, "D... SALL 1 B1 NOshaccum NOdump", fg.default, f"{bg.red}{fg.white}!!ALL-1!!{bg.default}{fg.default}", end="\n")
                    self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False) # every frame, BURSTING JPGS!
                elif (len(self.FABuffer) < 2)   and (self.l_show_accum) and (not self.saving_fits_only):
                    print()
                    print(fg.red, "D... SALL 2 B1   shaccum NOdump", fg.default, f"{bg.red}{fg.white}!!ALL-2!!{bg.default}{fg.default}", end="\n")
                    self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False) # every frame, BURSTING JPGS!
                # jpg and NO AVG
                elif (len(self.FABuffer) >= 2) and (not self.l_show_accum) and (not self.saving_fits_only):
                    print()
                    print(fg.red, "D... SALL 3  B2+  NOshac DUMP", fg.default, end="\n") # ONE DUMP
                    self.save_img( time_tag=self.frame_time, dumpbuffer=True, use_fits=False ) #  Dump Full Buffer and stop
                    self.saving_all = False
                # jpg and  AVG
                elif (len(self.FABuffer) < 2)  and (self.l_show_accum) and (not self.saving_fits_only):
                    # no bufffer no loopshow no fits
                    #self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False ) # just one simple image /lshow inside
                    print()
                    print(fg.red, "D... SALL 4 B1 shaccum / switching OFF saving all but not saving", fg.default, end="\n") # ???
                    self.saving_all = False
                    pass
                # jpg and AVG
                elif (len(self.FABuffer) >= 2) and (self.l_show_accum) and (not self.saving_fits_only): # ??? newSUM x newAVG
                    #
                    #if self.l_show_accum_avg:
                    #    rimg = self.FABuffer.get_avg_frames()#_mean_accum_buffer()
                    #
                    # no bufffer no loopshow no fits
                    #self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False ) # should be AVG
                    #if self.accum_index >= len(self.FABuffer) - 1:
                    if self.FABuffer.new_sum_available():
                        print()
                        if self.l_show_accum_avg:
                            print(fg.red, "D... SALL 5a shac Save AVG evry Nth ", fg.default, end="\n")
                        else:
                            print(fg.red, "D... SALL 5b Save SUM evry Nth ", fg.default, end="\n")
                        self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=False ) #  Dump Full Buffer and stop
                # FITS and NO AVG ---------------------------------------------------------------------------- FITS
                # FITS and NO AVG ---------------------------------------------------------------------------- FITS
                elif (len(self.FABuffer) < 2)  and (not self.l_show_accum) and (self.saving_fits_only):
                    print(fg.red, "D... SALL 6 fits for every image ... ", fg.default, end="\n")
                    #print("          here fits for  every image ....   too low buffer --- so   MAYBE        ")
                    # no bufffer no loopshow YES fits
                    self.save_img( time_tag=self.frame_time, dumpbuffer=False, use_fits=True) # every frame, BURSTING FITS !?!?!
                    #print(fg.red, "every N frames to FITS-IDK", fg.default, f"{bg.red}{fg.white}???{bg.default}{fg.default}", end="\n")
                    pass
                # FITS and NO AVG
                elif (len(self.FABuffer) >= 2) and (not self.l_show_accum) and (self.saving_fits_only):
                    print(fg.red,"          here fits for ALL BUFFER NONONO   no save        ", fg.default, end="")
                    ## no bufffer no loopshow no fits
                    #if self.accum_index >= len(self.FABuffer) - 1:
                    #    self.save_img( time_tag=self.frame_time , dumpbuffer=True, use_fits=True ) # dump buffer every time
                    #    print(fg.red, "F-FuB", fg.default , f"{bg.red}{fg.white}!!!!!!!!!!!!{bg.default}{fg.default}", end="\n")
                    pass
                # FITS and avg
                elif (len(self.FABuffer) < 2)  and (self.l_show_accum) and (self.saving_fits_only):
                    print(fg.red,  "          here -  too low buffer+ ACCUM =>   no save        ", fg.default, end="")
                    # no bufffer no loopshow no fits
                    #self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=True ) # one AVG (lshow handled inside)
                    #print(fg.red, "xxxx FITS -IDK", fg.default, end="")
                    self.saving_all = False
                    pass
                # FITS and avg
                elif (len(self.FABuffer) >= 2) and (self.l_show_accum) and (self.saving_fits_only):
                    # TOO COMPLEX --------------   I CHANGE TO FITS EVERY TIME NEW BUFFER IS OK -----------
                    # no bufffer no loopshow no fits
                    #self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=True ) # many AVG IDK
                    if self.FABuffer.new_sum_available():
                    #if self.accum_index >= len(self.FABuffer) - 1: # ONLY THE ACCUM FRAME!
                        print(fg.red, "F-Every Nth-AVG to FITS -IDK", fg.default, end="")
                        self.save_img( time_tag=self.frame_time , dumpbuffer=False, use_fits=True ) # SIMPLIFIED
                        ###########################################################################################################################################
                        # if self.level2_buffer.get_frame_shape() != self.img.shape:                                                                              #
                        #     print(self.level2_buffer.get_frame_shape,  self.img.shape) # CLEAR WHEN RES_CHANGE                                                  #
                        #     self.level2_buffer.clear_buffer(self.img) # repaired resoltution switch-crash                                                       #
                        # #                                                                                                                                       #
                        # self.level2_buffer.add_to_accum_buffer( self.img) # ACCUMULATE                                                                          #
                        # print(" level2 frames*: ", self.level2_buffer.get_current_size(), end=" ")                                                              #
                        # if (self.level2_buffer.is_accum_index_at_end) and ( self.level2_buffer.get_current_size() == self.level2_buffer.get_max_buffer_size()): #
                        #     # BUFFER OF BUFFERS !! TODO                                                                                                         #
                        #     level2buff_ord = self.level2_buffer.order_accum_buffer_frames()                                                                     #
                        ###########################################################################################################################################
                            #self.save_img( time_tag=self.frame_time , dumpbuffer=True, use_fits=True, use_buffer=level2buff_ord) # many AVG IDK
                            #############################################
                            # self.level2_buffer.clear_buffer(self.img) #
                            #############################################
                            # print(fg.red, "F-Every Nth-AVG to FITS -IDK", fg.default, end="")
                    pass


            if self.flag_print_over:
                ####self.overtext(blackbar=True)
                self.SAVED_NOW = False  # this is for overtext RED save


            # ------------------------------------- --------------------   TRANNS OR NOT TRANS
            if not self.saving_transformed_image:
                self.img = self.final_transformations( self.img )
                if self.flag_print_over:
                    self.overtext(blackbar=True)
                    #self.SAVED_NOW = False  # this is for overtext RED save

        # -------------------------------------------------------------------------------------
        #            *********************   NO IMAGE     ********************************
        # -------------------------------------------------------------------------------------
        else:# --- NO IMAGE CREATED ------------------------------- ... make the image gray ...
            print(f"x... ret_val={ret_val} ... self.error={self.error} ")
            #print("D... 3")
            # Extra override with some frame
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR) #I want to keep 3 channels
            self.use_frame(stripes=True)# img = self.frame



        #=============================== --------------------- ===================  UPDATE/SHOW
        #=============================== --------------------- ===================  UPDATE/SHOW
        #=============================== --------------------- ===================  UPDATE/SHOW
        if self.flag_print:
            print("     ", end="\n") # FINQAL \n
        else:
            print("     ", end="\r") # FINQAL \n

        #  -------------    # rgb_image MUST EXIST ! ! ! ! !
        self.rgb_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB) #I need for QT
        self.update_image(  self.rgb_image ) # need self.rgb_image




 ###########################################################
 # #                    mmmmm                              #
 # #   m   mmm   m   m  #   "#  m mm   mmm    mmm    mmm   #
 # # m"   #"  #  "m m"  #mmm#"  #"  " #"  #  #   "  #   "  #
 # #"#    #""""   #m#   #       #     #""""   """m   """m  #
 # #  "m  "#mm"   "#    #       #     "#mm"  "mmm"  "mmm"  #
 #                m"                                       #
 #               ""                                        #
 ###########################################################

    # ==================================================
    #
    # --------------------------------------------------

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        parts = []

        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            parts.append("Shift")
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            parts.append("Ctrl")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            parts.append("Alt")

        #parts.append(f"Key: {key}") # only modifiers
        parts_set = set(parts)
        if key < 256:
            self.post_addr = None
            if self.internet_not_device:
                print(self.url, self.internet_not_device)
                self.post_addr = self.url.replace("/video", "/cross")
            #post_addr = self.url.replace("/video", "/cross") # FOR REMOTE COMMANDS

            #print(" + ".join(parts), f"  /{chr(key)}/ ....   {parts_set}")


            # -----------------------------------------------------------------   s   savings - LOCAL ONLY !
            if (key == Qt.Key.Key_S):
                self.SAVED_NOW = True # red blink
                if ( len(parts_set) == 0) :
                    self.saving_once = True
                    self.saving_all = False
                    #self.saving_fits_only = False
                    #self.saving_jpg = True
                    #print(f"i... {fg.red}SAVING_ONCE IMAGE {fg.default}")
                #---------------- SHIFT-S:  1) IbufferON=> save every nth image; 2)  ---
                elif (parts_set == {'Shift'}):
                    self.saving_all = not self.saving_all
                    #self.saving_fits_only = False
                    print(f"i... {fg.orange}'SAVING_all' SET TO {self.saving_all}  !!!!!FITS=={self.saving_fits_only}!!!!!  {fg.default}")
                    if self.saving_all:
                        print('ffmpeg -framerate 5 -pattern_type glob -i "*.jpg" -c:v libx264 -pix_fmt yuv420p output.mkv')
                        print('ffmpeg -hide_banner -y -framerate 5 -pattern_type glob -i "*.jpg" -c:v libx264 -pix_fmt yuv420p output.mkv')
                        print('flatpak run  org.siril.Siril ; seuqence create')
                        print('kstars  (but press revert)')
                        print()
                elif (parts_set == {'Ctrl'}) :
                    pass

                elif (parts_set == {'Ctrl', 'Shift'}) :
                    # --------------
                    self.saving_jpg = not self.saving_jpg
                    self.saving_all = False
                    if self.saving_jpg:
                        print(f"i...  {fg.green}SAVING_JPG set to {self.saving_jpg}{fg.default} (interval is {self.FITS_INTERVAL_SECONDS}) ;  but 'SAVING_all' SET TO ", self.saving_all)
                    else:
                        print(f"i...  {fg.orange}PNG!{fg.default} SAVING_JPG set to {fg.cyan}{self.saving_jpg}{fg.default} (interval is {self.FITS_INTERVAL_SECONDS}) ;  but 'SAVING_all' SET TO ", self.saving_all)
                elif (parts_set == {'Alt'}) :
                    #   FITS / JPEG saving !!!
                    self.saving_fits_only = not self.saving_fits_only
                    self.saving_all = False
                    if self.saving_fits_only:
                        print(f"i...  {fg.orange}FITS_ONLY set to {self.saving_fits_only}{fg.default} (interval is {self.FITS_INTERVAL_SECONDS}) ;  but 'SAVING_all' SET TO ", self.saving_all)
                    else:
                        print(f"i...  FITS_ONLY set to {fg.cyan}{self.saving_fits_only}{fg.default} (interval is {self.FITS_INTERVAL_SECONDS}) ;  but 'SAVING_all' SET TO ", self.saving_all)



            # ------------------------------   xtend x2 ot switchres resolution---   x  XRES SWITCH - REMOTE - **SEND_COMMAND**
            if (key == Qt.Key.Key_X):
                if ( len(parts_set) == 0):
                    self.xtended = not self.xtended
                    print("i... xtending IMAGE locally 2x ", self.xtended)

                elif (parts_set == {'Shift'}):
                    self.r_xtend = "CC"
                    self.send_command( data={"switch_res_on": "SWITCH_RES_ON"})
                    print("D....    r_xtend == CC <<========= ", self.r_xtend)



                elif (parts_set == {'Ctrl'}) :
                    self.r_xtend = "  "
                    self.send_command( data={"switch_res_off": "SWITCH_RES_OFF"})
                    print("D....    r_xtend == '  ' <<======== ", self.r_xtend)

            # -----------------------------------------------------------------   p    printout - LOCAL ONLY
            if (key == Qt.Key.Key_P):
                if ( len(parts_set) == 0):
                    self.flag_print = not self.flag_print
                    print(f"i... termtext: {self.flag_print}")
                    #print("i... flasg print ", self.flag_print)
                elif (parts_set == {'Shift'}):
                    self.flag_print_over = not self.flag_print_over
                    print(f"i... overtext: {self.flag_print_over}")
                elif (parts_set == {'Ctrl'}) :
                    pass
            # -----------------------------------------------------------------   e    expo - REMOTE ONLY ! **SEND_COMMAND**
            if (key == Qt.Key.Key_E):
                if ( len(parts_set) == 0):
                    if self.r_expo < 1.0: self.r_expo += 0.02
                    if self.r_expo > 1: self.r_expo = 1
                    self.r_expodef = False
                    self.send_command( data= {"expot": "EXPOT", "expotxt":self.r_expo} )
                elif (parts_set == {'Shift'}) :
                    if self.r_expo > 0.0: self.r_expo -= 0.05
                    if self.r_expo < 0: self.r_expo = 0
                    self.r_expodef = False
                    self.send_command( data= {"expot": "EXPOT", "expotxt":self.r_expo} )
                elif (parts_set == {'Ctrl'}) :
                    self.send_command( data= {"expot": "EXPOT", "expotxt": -1.0} )
                    self.r_expodef = True

            # -----------------------------------------------------------------   g   gain  - REMOTE ONLY ! **SEND_COMMAND**
            if (key == Qt.Key.Key_G):
                if ( len(parts_set) == 0):
                    if self.r_gain < 1.0: self.r_gain += 0.1
                    if self.r_gain > 1: self.r_gain = 1
                    self.send_command( data= {"gaint": "GAINT", "gaintxt":self.r_gain} )
                    self.r_gaindef = False
                elif (parts_set == {'Shift'}) :
                    if self.r_gain > 0.0: self.r_gain -= 0.1
                    if self.r_gain < 0: self.r_gain = 0
                    self.send_command( data= {"gaint": "GAINT", "gaintxt":self.r_gain} )
                    self.r_gaindef = False
                elif (parts_set == {'Ctrl'}) :
                    self.send_command( data= {"gaint": "GAINT", "gaintxt": -1.0} )
                    self.r_gaindef = True
                #    self.send_command( data= {"gain2": "GAIN2"} )
                #elif (parts_set == {'Shift'}) :
                #    self.send_command( data= {"gain05": "GAIN05"})
                #elif (parts_set == {'Ctrl'}) :
                #    self.send_command( data= {"gain": "GAIN"} )
            # -----------------------------------------------------------------   y  gamma - REMOTE ONLY ! **SEND_COMMAND**
            if (key == Qt.Key.Key_Y):
                if ( len(parts_set) == 0):
                    if self.r_gamma < 1.0: self.r_gamma += 0.1
                    if self.r_gamma > 1: self.r_gamma = 1
                    self.r_gammadef = False
                    self.send_command( data= {"gammat": "GAMMAT", "gammatxt":self.r_gamma} )
                elif (parts_set == {'Shift'}) :
                    if self.r_gamma > 0.0: self.r_gamma -= 0.1
                    if self.r_gamma < 0: self.r_gamma = 0
                    self.r_gammadef = False
                    self.send_command( data= {"gammat": "GAMMAT", "gammatxt":self.r_gamma} )
                elif (parts_set == {'Ctrl'}) :
                    self.send_command( data= {"gammat": "GAMMAT", "gammatxt": -1.0} )
                    self.r_gammadef = True

                #    self.send_command( data= {"gamma2": "GAMMA2"} )
                #elif (parts_set == {'Shift'}) :
                #    self.send_command( data= {"gamma05": "GAMMA05"})
                #elif (parts_set == {'Ctrl'}) :
                #    self.send_command( data= {"gamma": "GAMMA"} )
            # -----------------------------------------------------------------   d     local gamma - LOCAL ONLY
            if (key == Qt.Key.Key_D):
                if ( len(parts_set) == 0):
                    self.l_gamma = self.l_gamma * 1.4
                elif (parts_set == {'Shift'}) :
                    self.l_gamma = self.l_gamma / 1.4
                elif (parts_set == {'Ctrl'}) :
                    self.l_gamma = 1

            # -----------------------------------------------------------------   w - Web Browser - LOCAL ONLY
            if (key == Qt.Key.Key_W):
                if ( len(parts_set) == 0):
                    webbrowser.open(self.url.replace("/video", ""))  # BRUTAL
                elif (parts_set == {'Shift'}) :
                    pass
                elif (parts_set == {'Ctrl'}) :
                    pass
            # -----------------------------------------------------------------   z - ZOOM - LOCAL ONLY !
            if (key == Qt.Key.Key_Z):
                if ( len(parts_set) == 0):
                    self.zoomme *= 1.5
                    if self.zoomme > 5:
                        self.zoomme = 5
                elif (parts_set == {'Shift'}) :
                    if self.zoomme > 1:
                        self.zoomme /= 1.5
                    if self.zoomme < 1: self.zoome= 1
                elif (parts_set == {'Ctrl'}) :
                    self.zoomme = 1
            # -----------------------------------------------------------------   hjkl - H - **SEND_COMMAND** c-s-*
            # self.send_command( data={"right": "RIGHT"})
            if (key == Qt.Key.Key_H):
                if ( len(parts_set) == 0):
                    self.redcross[0] -= 4
                elif (parts_set == {'Shift'}) :
                    self.redcross[0] -= 17
                elif (parts_set == {'Ctrl'}) :
                    self.redcross[0] -= 65
                elif (parts_set == {'Ctrl', 'Shift'}) :
                    self.send_command( data={"left": "LEFT"})
                    if self.r_xtend[0] == "R": self.r_xtend = "C" + self.r_xtend[1:]
                    elif self.r_xtend[0] == "C": self.r_xtend = "L" + self.r_xtend[1:]
                    elif self.r_xtend[0] == " ": self.r_xtend = "L" + self.r_xtend[1:]
            # -----------------------------------------------------------------   hjkl - J **SEND_COMMAND** c-s-*
            if (key == Qt.Key.Key_J):
                if ( len(parts_set) == 0):
                    self.redcross[1] += 4 # DOWN
                elif (parts_set == {'Shift'}) :
                    self.redcross[1] += 17
                elif (parts_set == {'Ctrl'}) :
                    self.redcross[1] += 65
                elif (parts_set == {'Ctrl', 'Shift'}) :
                    self.send_command( data={"down": "DOWN"})
                    if self.r_xtend[1] == "U": self.r_xtend =  self.r_xtend[:1] + "C"
                    elif self.r_xtend[1] == "C": self.r_xtend =  self.r_xtend[:1] + "D"
                    elif self.r_xtend[1] == " ": self.r_xtend =  self.r_xtend[:1] + "D"
            # -----------------------------------------------------------------   hjkl - K **SEND_COMMAND** c-s-*
            if (key == Qt.Key.Key_K):
                if ( len(parts_set) == 0):
                    self.redcross[1] -= 4 # UP
                elif (parts_set == {'Shift'}) :
                    self.redcross[1] -= 17 # UP
                elif (parts_set == {'Ctrl'}) :
                    self.redcross[1] -= 65
                elif (parts_set == {'Ctrl', 'Shift'}) :
                    self.send_command( data={"up": "UP"})
                    if self.r_xtend[1] == "D": self.r_xtend =  self.r_xtend[:1] + "C"
                    elif self.r_xtend[1] == "C": self.r_xtend =  self.r_xtend[:1] + "U"
                    elif self.r_xtend[1] == " ": self.r_xtend =  self.r_xtend[:1] + "U"
            # -----------------------------------------------------------------   hjkl - L **SEND_COMMAND** c-s-*
            if (key == Qt.Key.Key_L):
                if ( len(parts_set) == 0):
                    self.redcross[0] += 4
                elif (parts_set == {'Shift'}) :
                    self.redcross[0] += 17
                elif (parts_set == {'Ctrl'}) :
                    self.redcross[0] += 65
                elif (parts_set == {'Ctrl', 'Shift'}) :
                    self.send_command( data={"right": "RIGHT"})
                    if self.r_xtend[0] == "L": self.r_xtend = "C" + self.r_xtend[1:]
                    elif self.r_xtend[0] == "C": self.r_xtend = "R" + self.r_xtend[1:]
                    elif self.r_xtend[0] == " ": self.r_xtend = "R" + self.r_xtend[1:]
            # -----------------------------------------------------------------   v      GREEN CROSS - REMOTE **SEND_COMMAND**
            if (key == Qt.Key.Key_V):
                if ( len(parts_set) == 0):
                    self.send_command( data= {"crosson": "CROSSON"} )
                elif (parts_set == {'Shift'}) :
                    #self.send_command( data= {"expo05": "EXPO05"})
                    pass
                elif (parts_set == {'Ctrl'}) :
                    self.send_command( data= {"crossoff": "CROSSOFF"} )
            # -----------------------------------------------------------------   c     RED      CROSS - LOCAL ONLY
            if (key == Qt.Key.Key_C):
                if ( len(parts_set) == 0):
                    self.flag_redcross = True# not self.flag_redcross
                    print( "i... showinf red cross", self.flag_redcross)
                elif (parts_set == {'Shift'}) :
                    self.flag_redcross = False# not self.flag_redcross
                    pass
                elif (parts_set == {'Ctrl'}) :
                    print( "i... reset position red cross")
                    self.redcross = [0, 0]
            # -----------------------------------------------------------------   i   integrate accumulate - LOCAL ONLY !  tricky**SEND_COMMAND**
            if (key == Qt.Key.Key_I):    #    i:inc   shift-i:dec   Ctrl-i:reset    Ctrl-Shift-i:watch     Alt-i: SUM vs. AVG
                #   4.6GB / 1000 640x480
                if ( len(parts_set) == 0):
                    if self.r_integrate < 8:
                        if self.r_integrate < 1:
                            self.r_integrate = 1
                        self.r_integrate = self.r_integrate * 2
                    elif self.r_integrate < 40:
                        self.r_integrate = self.r_integrate + 4
                    elif self.r_integrate < 100:
                        self.r_integrate = self.r_integrate + 8
                    else:
                        self.r_integrate = self.r_integrate + 16

                    print("i... integrate to ", self.r_integrate)
                    self.send_command( data= {"accum": "ACCUM", "accumtxt": int(self.r_integrate)})
                elif (parts_set == {'Shift'}) :
                    if self.r_integrate >= 4: # I am not allowed to send 1 but I dont remember why
                        self.r_integrate = int(self.r_integrate / 2)
                        print("i... integrate to ", self.r_integrate)
                        self.send_command( data= {"accum": "ACCUM", "accumtxt": int(self.r_integrate)})
                    else:#as crtl
                        self.r_integrate = 1
                        print("i... integrate to 0 (not 1)")
                        self.send_command( data= {"accum": "ACCUM", "accumtxt": 0})
                elif (parts_set == {'Ctrl'}) :
                    self.r_integrate = 1
                    self.send_command( data= {"accum": "ACCUM", "accumtxt": 0})
                    self.l_show_accum = False
                    # 0 would be a problem (locally???);    but 1 is not sent!!! ; SENDING 0, checking@send_command
                elif (parts_set == {'Ctrl', 'Shift'}) :
                    # REMOVE SHOW ACCUM .... ok but I remove it also when reseting buffer
                    self.l_show_accum = not self.l_show_accum
                    print(f"i...  BUFFER ACCUMULATED SHOW IS {self.l_show_accum} ;  MODE AVG={self.l_show_accum_avg} MODE SUM = {not self.l_show_accum_avg}")
                elif (parts_set == {'Alt'}) :
                    self.l_show_accum_avg = not self.l_show_accum_avg
                    print(f"i... ACCUMULATION DISPLAY MODE SWITCHED:   AVG (nonSUM) IS {self.l_show_accum_avg}")

            # -----------------------------------------------------------------   b BACKGROUND - REMOTE **SEND_COMMAND**
            if (key == Qt.Key.Key_B):
                if ( len(parts_set) == 0):
                    #self.send_command( data= {"subbg": "SUBBG"})
                    fname1 = self.prepare_save( time_tag=None)
                    #print(fg.green, f"D... looking for like {fname1}", fg.default)
                    bgfilename, copyname= find_latest_bg_or_fg(fname1, foreground=False)
                    self.filename_background = copyname
                    if os.path.exists(self.filename_background):
                        print(f"{fg.green}D... BG= {self.filename_background}", fg.default)
                        self.image_background = cv2.imread(self.filename_background)
                    pass
                elif (parts_set == {'Shift'}) :
                    fname1 = self.prepare_save( time_tag=None)
                    #print(fg.green, f"D... looking for like {fname1}", fg.default)
                    bgfilename, copyname= find_latest_bg_or_fg(fname1, foreground=False)
                    if not bgfilename is None:
                        print(f"{fg.green}D... copying:", bgfilename, copyname, fg.default)
                        shutil.copy(bgfilename, copyname)
                    #self.send_command( data= {"savebg": "SAVEBG"})
                    pass
                elif (parts_set == {'Ctrl'}) :
                    self.filename_background = None
                    self.image_background = None
                    pass
            # -----------------------------------------------------------------   f FOREGROUND - LOCAL ONLY !
            if (key == Qt.Key.Key_F):
                if ( len(parts_set) == 0):
                    #self.send_command( data= {"mixfg": "MIXFG"})
                    fname1 = self.prepare_save( time_tag=None)
                    bgfilename, copyname= find_latest_bg_or_fg(fname1, foreground=True)
                    self.filename_foreground = copyname
                    if os.path.exists(self.filename_foreground):
                        print(f"{fg.green}D... FG= {self.filename_foreground}", fg.default)
                        self.image_foreground = cv2.imread(self.filename_foreground)
                elif (parts_set == {'Shift'}) :
                    #self.send_command( data= {"savefg": "SAVEFG"})
                    fname1 = self.prepare_save( time_tag=None)
                    #print(fg.green, f"D... looking for like {fname1}", fg.default)
                    bgfilename, copyname= find_latest_bg_or_fg(fname1, foreground=True)
                    if not bgfilename is None:
                        print(f"{fg.green}D... copying:", bgfilename, copyname, fg.default)
                        shutil.copy(bgfilename, copyname)
                elif (parts_set == {'Ctrl'}) :
                    self.filename_foreground = None
                    self.image_foreground = None
                    pass

            # -----------------------------------------------------------------   r ROTATE - LOCAL ONLY !
            if (key == Qt.Key.Key_R):
                if ( len(parts_set) == 0):
                    self.l_rotate += 1
                elif (parts_set == {'Shift'}) :
                    self.l_rotate -= 1
                elif (parts_set == {'Ctrl'}) :
                    self.l_rotate = 0
            # -----------------------------------------------------------------  1 config
            if (key == Qt.Key.Key_1) or (key == ord("!") ):
                if ( len(parts_set) == 0):
                    print("i... config 1 - recall")
                    self.setup("r", 1)
                    self.setup("a", 1)
                elif (parts_set == {'Shift'}) :
                    print("i... config! 1 - save")
                    print("D... r_xtend == ", self.r_xtend)
                    self.setup("i", 1)
                    print("D... r_xtend == ", self.r_xtend)
                    print("D....   action write ..........  ")
                    self.setup("w", 1)
                    print("D... r_xtend == ", self.r_xtend)
                elif (parts_set == {'Ctrl'}) :
                    self.setup("q")
            # -----------------------------------------------------------------  2 config
            if (key == Qt.Key.Key_2) or (key == ord("@") ):
                if ( len(parts_set) == 0):
                    print("i... config 2 - recall")
                    self.setup("r", 2)
                    self.setup("a", 2)
                elif (parts_set == {'Shift'}) :
                    print("i... config! 2 - save")
                    self.setup("i", 2)
                    self.setup("w", 2)
                elif (parts_set == {'Ctrl'}) :
                    self.setup("q")
            # -----------------------------------------------------------------  3 config
            if (key == Qt.Key.Key_3) or (key == ord("#") ):
                if ( len(parts_set) == 0):
                    print("i... config 3 - recall")
                    self.setup("r", 3)
                    self.setup("a", 3)
                elif (parts_set == {'Shift'}) :
                    print("i... config! 3 - save")
                    self.setup("i", 3)
                    self.setup("w", 3)
                elif (parts_set == {'Ctrl'}) :
                    self.setup("q")
            # -----------------------------------------------------------------  4  config
            if (key == Qt.Key.Key_4) or (key == ord("$") ):
                if ( len(parts_set) == 0):
                    print("i... config 4 - recall")
                    self.setup("r", 4)
                    self.setup("a", 4)
                elif (parts_set == {'Shift'}) :
                    print("i... config! 4 - save")
                    self.setup("i", 4)
                    self.setup("w", 4)
                elif (parts_set == {'Ctrl'}) :
                    self.setup("q") # quit-resetall


            # -----------------------------------------------------------------   [ ]   tests whatever
            if (key == Qt.Key.Key_T):
                if ( len(parts_set) == 0):
                    #self.send_command( data= {"gaint": "GAINT", "gaintxt": float(0.123)})
                    #self.send_command( data= {"expot": "EXPOT", "expotxt": float(0.1)})
                    pass
                elif (parts_set == {'Shift'}) :
                    #self.send_command( data= {"gaint": "GAINT", "gaintxt": float(0.723)})
                    #self.send_command( data= {"expot": "EXPOT", "expotxt": float(0.7)})
                    pass
                elif (parts_set == {'Ctrl'}) :
                    #self.send_command( data= {"expot": "EXPOT", "expotxt": float(-1.0)})
                    pass

            # -----------------------------------------------------------------   [ ]   tests whatever      A  timelaps LOCAL
            if (key == Qt.Key.Key_A):
                if ( len(parts_set) == 0):
                    self.l_timelaps = True
                    if self.l_timelaps_seconds == 0:
                        self.l_timelaps_seconds = 1
                    else:
                        self.l_timelaps_seconds = self.l_timelaps_seconds * 2
                    self.l_timelaps_last = dt.datetime.now()- dt.timedelta(seconds=self.l_timelaps_seconds)
                    pass
                elif (parts_set == {'Shift'}) :
                    if self.l_timelaps_seconds > 1:
                        self.l_timelaps_seconds = int(self.l_timelaps_seconds / 2)
                    else:
                        self.l_timelaps_seconds = 1
                    self.l_timelaps_last = dt.datetime.now()- dt.timedelta(seconds=self.l_timelaps_seconds)
                    pass
                elif (parts_set == {'Ctrl'}) :
                    self.l_timelaps = False
                    print(f"{fg.cyan}i... NO TIMELAPS from now {fg.default}")
                    pass
                elif (parts_set == {'Alt'}) :
                    pass
            # -----------------------------------------------------------------   t   tests whatever REMOTE !   **SEND_COMMAND**
            if (key == Qt.Key.Key_T):
                if ( len(parts_set) == 0):
                    # THIS IS in reallity SKIPPED IN send_command ....
                    # also -1 means in remote -  every image
                    self.send_command( data= {"timelaps": "TIMELAPS" ,"timelaps_input": "1" })
                    self.saving_laps = 1
                    print(f"i...  TimeLapse  {fg.orange}  1 second or ACCUM {fg.default} ")
                    pass
                elif (parts_set == {'Shift'}) :
                    self.send_command( data= {"timelaps": "TIMELAPS" ,"timelaps_input": "10" })
                    self.saving_laps = 10
                    print(f"i...  TimeLapse  {fg.orange}  10 seconds {fg.default} ")
                    pass
                elif (parts_set == {'Ctrl', 'Shift'}) :
                    self.send_command( data= {"timelaps": "TIMELAPS" ,"timelaps_input": "60" })
                    self.saving_laps = 60
                    print(f"i...  TimeLapse  {fg.orange}  60 seconds {fg.default} ")
                    pass
                elif (parts_set == {'Ctrl'}) :
                    self.send_command( data= {"timelaps": "TIMELAPS" ,"timelaps_input": "0" })
                    self.saving_laps = 0
                    print(f"i...  TimeLapse  {fg.orange}  OFF {fg.default} ")
                    pass



        # ##################################################################### konec ##
        else:
            #  shift alt ctrl
            pass #print("b + ".join(parts))

        if key == Qt.Key.Key_Escape or (key == Qt.Key.Key_Q):
            #print(chr(key))
            QApplication.quit()



@click.command()
@click.argument('url', default="127.0.0.1")
@click.option('-r', '--resolution', default="640x480", required=False, help='Resolution value')
@click.option('-f', '--fourcc', default="YUYV", required=False, help='YUYV or MJPG')
def handle_cli(url, resolution, fourcc):
    """
    commandline is solved here; guess url
    """
    #app = QApplication() #
    app = QApplication(sys.argv) # NOT clear why argv here
    url = guess_url(url)
    widget = None

    widget = StreamWidget(url,  resolution=resolution, fourcc=fourcc)
    widget.show()
    sys.exit(app.exec())


# =====================================================================
# MAIN ENTRY
# ---------------------------------------------------------------------
if __name__ == "__main__":
    handle_cli()
