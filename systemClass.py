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

from config         import *    #   Load configuration and initial values
from ErrorHandler   import *    #   Defines the error handling
from LinkSliders    import *    #   Defines input/outputs    
#from systemClass    import *    #   Defines general system fuctions
from main import *

class systemClass:
    def __init__(self, RGB_value = [0,0,0], Brightness = 10):
        print("...")

    def ExitProgram():
        print("In Exit program")
        print(visionbox)
        #errorMsgHandlerClass.errorMsgHandler(self,errorMsgBit=1, debug= False) 

