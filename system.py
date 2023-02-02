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

from LinkSliders import *
from config import *
from system import *
from ErrorHandler import *

#   1)  Initialise
#   2)  Enable/Disable inputs based on User level
#   3)   



class systemSettings: #lightsettingsClass:
    ## Initialise 
    def __init__(self):
        print("...")
    
    def ExitProgram(self):
        self.MsgHandlerClass.errorMsgHandler(self, errorMsgBit=1, debug= False)
    

