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
from PySide2.QtGui import QPixmap, QTouchEvent, QFont
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
        exit = ExitDialog()
        returnvalue = exit.exec() 
        if returnvalue:
                self.print_on_GUI_terminal(text_to_print="--> Program is closed!",  color='default')
                LED_strips.__init__(self)
                sys.exit()

    ###############################################################################################
    ## Get available images in folder and sort
    ###############################################################################################
    def getAvailableImagesInFolder(self, debug=debugArray[11]):
        _,_,files = next(os.walk(scp_path))
        img_count = len(files)
        img_files = natsorted(files)
        if debug: print("img_count", img_count, "img_files", img_files)
        return img_files, img_count

    ###############################################################################################
    ## Make archive of images                          
    ###############################################################################################
    def on_export_files_zip(self, time, debug=debugArray[1]):
        # Generate Name
        name = time.replace(" ", "_").replace("/", "_")
        name = "Export_files_zip_" + name + str(".zip")
        if debug:   print("Exportfilename: ", name)
        source = source=dir_path + "SCP_images"
        destination= dir_path + name
        img_backup_succesfull = False
        try: 
            base = os.path.basename(destination)
            name = base.split('.')[0]
            format = base.split('.')[1]
            archive_from = os.path.dirname(source)
            archive_to = os.path.basename(source.strip(os.sep))
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
        print("Export of ZIP succesfull!, name = " + str(name))
        self.print_on_GUI_terminal(text_to_print="Export of ZIP succesfull!, name = " + str(name),  color='green') 



###############################################################################################
## Dialog for Make archive of images                          
###############################################################################################

class ExitDialog(QDialog):
    def __init__(self):
        global insertedText
        super().__init__()

        self.setWindowTitle("Quit")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setFont(QFont('Times', default_font_size_buttons))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to quit?")
        message.setFont(QFont('Times', default_font_size))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)