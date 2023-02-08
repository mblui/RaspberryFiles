# This Python file uses the following encoding: utf-8
import sys
import os
import cv2
import subprocess
# Import array sorting package
from natsort import natsorted 
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

class systemClass(QMessageBox):
    def __init__(self):
        print("...")

    def ExitProgram(self):
        errorMsgHandlerClass.errorMsgHandler(self,errorMsgBit=1, debug= False) 

    def getAvailableImagesInFolder(self, debug = False):
        _,_,files = next(os.walk(scp_path))
        img_count = len(files)
        img_files = natsorted(files)
        if debug: print("img_count", img_count, "img_files", img_files)
        return img_files, img_count