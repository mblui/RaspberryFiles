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

from config                 import *    #   Load configuration and initial values
from ErrorHandler           import *    #   Defines the error handling
from lightsettingsClass     import *    #   Defines input/outputs    
#from systemClass    import *    #   Defines general system fuctions
from main                   import *

class systemClass(QMessageBox):
    ## --- --- Exit Program  --- --- --- ---
    def ExitProgram(self):
        errorMsgHandlerClass.errorMsgHandler(self,errorMsgBit=1, debug= False) 

    ###############################################################################################
    ## Get available images in folder and sort
    ###############################################################################################
    def getAvailableImagesInFolder(self, debug = False):
        _,_,files = next(os.walk(scp_path))
        img_count = len(files)
        img_files = natsorted(files)
        if debug: print("img_count", img_count, "img_files", img_files)
        return img_files, img_count

    ###############################################################################################
    ## Make archive of images                          
    ###############################################################################################
    def on_export_files_zip(self, debug = False):
        if debug:   print("on_export_files_zippert")
        # Generate Name
        name = current_date_time.replace(" ", "_").replace("/", "_")
        name = "RecordedImages" + name + str(".zip")
        self.make_archiveZip(source=dir_path + "SCP_images", destination= dir_path + name)
        self.print_on_GUI_terminal(text_to_print="Export of ZIP succesfull!, name = " + str(name),  color='green') 

    def make_archiveZip(self, source, destination, debug = False):
        global img_files, img_count
        img_backup_succesfull = False
        try: 
            base = os.path.basename(destination)
            name = base.split('.')[0]
            format = base.split('.')[1]
            archive_from = os.path.dirname(source)
            archive_to = os.path.basename(source.strip(os.sep))
            #print(source, destination, archive_from, archive_to)
            shutil.make_archive(name, format, archive_from, archive_to)
            shutil.move('%s.%s'%(name,format), destination)
            img_backup_succesfull = True 
        except Exception as e:
            errorMsgHandlerClass.errorMsgHandler(self, errorMsgBit=2, debug= False)   
        
        # if backup is succesfull
        if img_backup_succesfull: 
            os.chdir(dir_path + "SCP_images")     
            if debug: [print(f) for f in os.listdir()]       
            [os.remove(f) for f in os.listdir()]       
        img_files, img_count = systemClass.getAvailableImagesInFolder(self) 
        