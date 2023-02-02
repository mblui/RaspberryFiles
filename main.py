# This Python file uses the following encoding: utf-8
import sys
import os
import cv2
import subprocess
from showinfm import show_in_file_manager

from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QMainWindow, QInputDialog
from PySide2.QtCore import QFile, QTimer, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QTouchEvent, QIcon
from functools import partial
import time
from ErrorHandler import *
from LinkSliders import *
from system import *
from natsort import natsorted 
import zipfile, shutil
from datetime import datetime



# Load default parameters
from config import *

class visionbox(QMainWindow):
    def __init__(self, parent: QWidget = None):
        global img_files, img_count, globalImageUpdate
        super().__init__(parent)
        self.setWindowTitle("Vision Box")
        self.showMaximized() if windowsize[2] else self.setFixedSize(QSize(windowsize[0], windowsize[1]))
        # Load GUI
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.w = loader.load(ui_file, self)
        self.w.show()
        ui_file.close()

        # Link sliders and initialize
        GUIsettingsClass.__init__(self)
        #self.on_button_press()      ## initialse start/pause button
        
        # Initial count number of images
        img_files, img_count = self.getAvailableImagesInFolder()

        # Link buttons
        self.on_lock_unlock_button()
        self.w.button_openImageFolder.clicked.connect(self.openFolder)
        self.w.button_ExitProgram.clicked.connect(self.ExitProgram) 
        self.w.Start_pause_watching.clicked.connect(self.on_button_press)
        self.w.Start_pause_watching.setCheckable(True)
        self.w.button_ExportFilesZIP.clicked.connect(self.on_export_files_zip)
        self.w.button_previous_img.clicked.connect(partial(self.on_next_previous_image,-1))
        self.w.button_next_img.clicked.connect(partial(self.on_next_previous_image, 1))
        self.w.lock_unlock_button.clicked.connect(self.on_lock_unlock_button)
        self.w.lock_unlock_button.setCheckable(True)

        ## Set update timer
        self.__acquisition_timer = QTimer()
        timer = QTimer(self)
        timer.timeout.connect(partial(self.update_image, debugval=False))     
        timer.start((1/updatefps)*1000)
        self.update_image(debugval=False)

    def onCheckboxChange(self):
        lightInputs[0][0] = self.w.check_Top_Enable.isChecked()
        lightInputs[1][0] = self.w.check_Left_Enable.isChecked()
        lightInputs[2][0] = self.w.check_Right_Enable.isChecked()
        lightInputs[0][1] = self.w.check_Top_RGB.isChecked()
        lightInputs[1][1] = self.w.check_Left_RGB.isChecked()
        lightInputs[2][1] = self.w.check_Right_RGB.isChecked()
        lightInputs[0][2] = self.w.check_Top_White.isChecked()
        lightInputs[1][2] = self.w.check_Left_White.isChecked()
        lightInputs[2][2] = self.w.check_Right_White.isChecked()
        print(lightInputs)
           
    def update_image(self, debugval):
        global cnt, img_count, Brightness_value, RGB_val, globalImageUpdate, current_date_time, img_to_display, img_to_display_cnt
        if debugval: print(globalImageUpdate)
        img_files, img_count = self.getAvailableImagesInFolder() 
        self.w.number_of_images.setText(str(img_count).zfill(maxImagesBits))
        if len(img_files)<1:
            self.w.num_img.setText("No files in folder to display")
        else:
            if globalImageUpdate:
                img_to_display_cnt = img_count-1 ## show latest image
            #print("editvalue", img_to_display_cnt)
            img_to_display = img_files[img_to_display_cnt]
            self.w.num_img.setText(img_to_display)
            ExtendedPath = scp_path + str(img_to_display)
            label = self.w.imglabel
            pixmap =QPixmap(ExtendedPath)
            label.setPixmap(pixmap)
            label.show()

        GUIsettingsClass.lightsettings(self, RGB_value=RGB_val, Brightness=Brightness_value)      ## Update lightvalues
        ## TODO place timerupdate on separate Qtimer --> now its randomly updating.
        current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.w.text_date_time.setText(str(current_date_time))



if __name__ == "__main__":
    app = QApplication([])
    widget = visionbox()
    widget.show()
    sys.exit(app.exec_())
