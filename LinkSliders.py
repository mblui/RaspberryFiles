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

#   1)  Initialise
#   2)  Enable/Disable inputs based on User level
#   3)   



class GUIsettingsClass: #lightsettingsClass:
    ## Initialise 
    def __init__(self, RGB_value = [0,0,0], Brightness = 10):
        ## Create groups
        RGB_white_Group1 = QButtonGroup(self.w)
        RGB_white_Group1.addButton(self.w.check_Top_RGB, 1)      # ID = 1
        RGB_white_Group1.addButton(self.w.check_Top_White,2)      # ID = 2 
        RGB_white_Group1.setExclusive(True)
        
        RGB_white_Group2 = QButtonGroup(self.w)
        RGB_white_Group2.addButton(self.w.check_Left_RGB, 1)      # ID = 1
        RGB_white_Group2.addButton(self.w.check_Left_White,2)      # ID = 2 
        RGB_white_Group2.setExclusive(True)

        RGB_white_Group3 = QButtonGroup(self.w)
        RGB_white_Group3.addButton(self.w.check_Right_RGB, 1)      # ID = 1
        RGB_white_Group3.addButton(self.w.check_Right_White,2)      # ID = 2 
        RGB_white_Group3.setExclusive(True)

        # Default white checkbox
        self.w.check_Top_White.setChecked(True)
        self.w.check_Left_White.setChecked(True)
        self.w.check_Right_White.setChecked(True)
        
        ## Settings of sliders
            ## Slider Red value
        self.w.slider_red.setMinimum(0)
        self.w.slider_red.setMaximum(255)
        self.w.SliderVal_but_text_red.setText(str(RGB_value[0]))

            ## Slider Green value
        self.w.slider_green.setMinimum(0)
        self.w.slider_green.setMaximum(255)
        self.w.SliderVal_but_text_green.setText(str(RGB_value[1]))   

            ## Slider Blue value
        self.w.slider_blue.setMinimum(0)
        self.w.slider_blue.setMaximum(255)
        self.w.SliderVal_but_text_blue.setText(str(RGB_value[2]))

            ## Slider Brightness 
        self.w.slider_intensity.setValue(Brightness)
        self.w.SliderVal_but_text_intensity.setText(str(Brightness))

        ## Settings Checkboxes
            ## Enable/disable:
        self.w.check_Top_Enable.toggled.connect(self.onCheckboxChange)
        self.w.check_Left_Enable.toggled.connect(self.onCheckboxChange)
        self.w.check_Right_Enable.toggled.connect(self.onCheckboxChange)
            
            ## RGB
        self.w.check_Top_RGB.toggled.connect(self.onCheckboxChange)
        self.w.check_Left_RGB.toggled.connect(self.onCheckboxChange)
        self.w.check_Right_RGB.toggled.connect(self.onCheckboxChange)
            
            ## White:
        self.w.check_Top_White.toggled.connect(self.onCheckboxChange)
        self.w.check_Left_White.toggled.connect(self.onCheckboxChange)
        self.w.check_Right_White.toggled.connect(self.onCheckboxChange)
            
        ## Connecting sliders to actions
        self.w.slider_red.sliderMoved.connect(self.on_slider_change)
        self.w.slider_green.sliderMoved.connect(self.on_slider_change)
        self.w.slider_blue.sliderMoved.connect(self.on_slider_change)
        self.w.slider_intensity.sliderMoved.connect(self.on_slider_change)
        self.w.SliderVal_but_text_intensity.clicked.connect(partial(self.getItem,"intensity"))
        self.w.SliderVal_but_text_red.clicked.connect(partial(self.getItem,"red"))
        self.w.SliderVal_but_text_green.clicked.connect(partial(self.getItem,"green"))
        self.w.SliderVal_but_text_blue.clicked.connect(partial(self.getItem,"blue"))

    ## Enable/disable based on user level 
    def on_lock_unlock_button(self):
        if self.w.lock_unlock_button.isChecked():
            _,output = self.MsgHandlerClass.errorMsgHandler(self, errorMsgBit=3, debug= False)
            if output:
                self.enable_disable_inputs(value=1) #True
                self.w.text_current_user.setText(str(self.AvailableUserProfiles[0]))
                self.w.lock_unlock_button.setIcon(self.QIcon('unlock_icon.png'))
        else:
            self.enable_disable_inputs(value=0) #False
            self.w.text_current_user.setText(str(self.AvailableUserProfiles[1]))
            self.w.lock_unlock_button.setIcon(self.QIcon('lock_icon.png'))

    def enable_disable_inputs(self, value):
        self.w.button_openImageFolder.setEnabled(value)
        self.w.button_ExportFilesZIP.setEnabled(value)
        self.w.check_Top_Enable.setEnabled(value)
        self.w.check_Left_Enable.setEnabled(value)
        self.w.check_Right_Enable.setEnabled(value)
        self.w.check_Top_RGB.setEnabled(value)
        self.w.check_Left_RGB.setEnabled(value)
        self.w.check_Right_RGB.setEnabled(value)
        self.w.check_Top_White.setEnabled(value)
        self.w.check_Left_White.setEnabled(value)
        self.w.check_Right_White.setEnabled(value)
        self.w.slider_red.setEnabled(value)
        self.w.slider_green.setEnabled(value)
        self.w.slider_blue.setEnabled(value)
        self.w.slider_intensity.setEnabled(value)
        self.w.SliderVal_but_text_intensity.setEnabled(value)
        self.w.SliderVal_but_text_red.setEnabled(value)
        self.w.SliderVal_but_text_green.setEnabled(value)
        self.w.SliderVal_but_text_blue.setEnabled(value)
        self.w.text_right.setEnabled(value)
        self.w.text_left.setEnabled(value)
        self.w.text_top.setEnabled(value)
        self.w.text_enable.setEnabled(value)
        self.w.text_rgb.setEnabled(value)
        self.w.text_white.setEnabled(value)
        self.w.text_brightness.setEnabled(value)
        self.w.text_red.setEnabled(value)
        self.w.text_green.setEnabled(value)
        self.w.text_blue.setEnabled(value)

    ## Open folder with received images from Jetson Nano
    def openFolder(self):
        show_in_file_manager(self.scp_path)

    ## Export received files to ZIP and empty folder
    def on_export_files_zip(self):
        global img_count, current_date_time
        # Generate Name
        name = current_date_time.replace(" ", "_").replace("/", "_")
        name = "RecordedImages" + name + str(".zip")
        self.make_archiveZip(source=self.dir_path + "SCP_images", destination= self.dir_path + name)

    def make_archiveZip(self, source, destination):
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
            MsgHandlerClass.errorMsgHandler(self, errorMsgBit=2, debug= False)   
        
        # if backup is succesfull
        if img_backup_succesfull: 
            os.chdir(dir_path + "SCP_images")
            #[os.remove(f) for f in os.listdir()]        
            [print(f) for f in os.listdir()]       
            [os.remove(f) for f in os.listdir()]       
            #Pprint("Done")
        img_files, img_count = self.getAvailableImagesInFolder() 
        # TODO Add dialog to show that export is succesfull with name ... 
    
    ## Viewed image manual
    def on_next_previous_image(self,value):
        global img_to_display_cnt
        self.w.Start_pause_watching.setChecked(True)
        self.on_button_press()
        #print("editvalue1", img_to_display_cnt)
        if img_to_display_cnt >= 0 and  img_to_display_cnt < img_count:
            img_to_display_cnt = img_to_display_cnt + value



    ## Slider change
    def on_slider_change(self):
        global RGB_val, Brightness_value
        # Update RGBvalue
        Brightness_value = self.w.slider_intensity.value()
        RGB_val[0] = self.w.slider_red.value()
        RGB_val[1] = self.w.slider_green.value()
        RGB_val[2] = self.w.slider_blue.value()


    ## Get available images in folder
    
    def getAvailableImagesInFolder(self):
        _,_,files = next(os.walk(self.scp_path))
        img_count = len(files)
        img_files = natsorted(files)
        print("img_count", img_count, "img_files", img_files)
        return img_files, img_count


    ## Get Lightsettingsitems
    def getItem(self, slidertype):  # slidertype := [intensity', 'red', 'green', 'blue']
        global Brightness_value,RGB_val
        items_1 = ("0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100")
        items_2 = ("0", "25", "51", "77", "102", "128", "153", "178", "204", "229", "255")
        items = items_1 if slidertype == "intensity" else items_2
        #item, ok = QInputDialog.getInt(self, "select input", "enter a number", self.w.slider_intensity.value())
        item, ok = QInputDialog.getItem(self, "select input", "Enter a number", items, 0, False)
        if ok:
            if (slidertype == "intensity"):
                Brightness_value = int(item)
                self.w.slider_intensity.setValue(int(item))
            elif (slidertype == "red"):
                RGB_val[0] = int(item)
                self.w.slider_red.setValue(int(item))
            elif (slidertype == "green"):
                RGB_val[1] = int(item)
                self.w.slider_green.setValue(int(item))
            elif(slidertype == "blue"):
                RGB_val[2] = int(item)
                self.w.slider_blue.setValue(int(item))
            else:
                errorMsgBit = 1

    def lightsettings(self, RGB_value = [0,0,0], Brightness = 10):
                ## Settings of sliders
            ## Slider Red value
        self.w.SliderVal_but_text_red.setText(str(RGB_value[0]))

            ## Slider Green value
        self.w.SliderVal_but_text_green.setText(str(RGB_value[1]))   

            ## Slider Blue value
        self.w.SliderVal_but_text_blue.setText(str(RGB_value[2]))

            ## Slider Brightness 
        self.w.slider_intensity.setValue(Brightness)
        self.w.SliderVal_but_text_intensity.setText(str(Brightness))
