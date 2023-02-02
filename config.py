# This Python file uses the following encoding: utf-8
import sys
import os
import cv2
import subprocess
import numpy as np
from showinfm import show_in_file_manager

from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QMainWindow, QInputDialog, QButtonGroup
from PySide2.QtCore import QFile, QTimer, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QTouchEvent
from functools import partial
import time
from natsort import natsorted 

# Set path to directory with images 1
dir_path = r'/home/dgslr/ProgramFiles/'
scp_path = dir_path + "SCP_images/"

# --- --- Define inputs ---
windowsize = [1920, 850, 0] # [width,heights, Fullsize = 1/0]
updatefps = 1

# ---- --- Define Global variables/ Initial values
cnt = int(1)
AvailableUserProfiles = ["DGS admin", "View only"]
Password_admin = "1466"
maxImagesBits = 6           # Maxum number of images in the folder (in bits) -->  000000
globalImageUpdate = False
Brightness_value = int(50)
current_date_time = "01/01/2023 00:00:00"
errorMsgBit = int(0)
ExtendedPath = ""
RGB_val= [0,0,0]
img_count = 0           # number of images
img_to_display_cnt = 0  # number of displayed image     
img_files = 0           # sorted list of images
lightInputs = [ [0,0,0],        # Corresponding to GUI
                [0,0,0],
                [0,0,0]]
