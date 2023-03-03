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
from main import *
from systemClass import *
from config import *


class lightsettingsClass:
    def __init__(self, Brightness, debug=debugArray[12], RGB_value = [0,0,0], ):
        ## Create groups
        RGB_white_Group1 = QButtonGroup(self.w)
        RGB_white_Group1.addButton(self.w.check_Top_RGB, 1)         # ID = 1
        RGB_white_Group1.addButton(self.w.check_Top_White,2)        # ID = 2 
        RGB_white_Group1.setExclusive(True)
        
        RGB_white_Group2 = QButtonGroup(self.w)
        RGB_white_Group2.addButton(self.w.check_Left_RGB, 1)        # ID = 1
        RGB_white_Group2.addButton(self.w.check_Left_White,2)       # ID = 2 
        RGB_white_Group2.setExclusive(True)

        RGB_white_Group3 = QButtonGroup(self.w)
        RGB_white_Group3.addButton(self.w.check_Right_RGB, 1)       # ID = 1
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
        self.w.slider_intensity.setMinimum(0)
        self.w.slider_intensity.setMaximum(100)
        self.w.slider_intensity.setValue(Brightness)
        self.w.SliderVal_but_text_intensity.setText(str(Brightness))

        ## Settings Checkboxes
            ## Enable/disable:
        self.w.check_Top_Enable.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug)) 
        self.w.check_Left_Enable.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
        self.w.check_Right_Enable.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
            
            ## RGB
        self.w.check_Top_RGB.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
        self.w.check_Left_RGB.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
        self.w.check_Right_RGB.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
            
            ## White:
        self.w.check_Top_White.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
        self.w.check_Left_White.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
        self.w.check_Right_White.toggled.connect(lambda: visionbox.onCheckboxChange(self, debug))
            
        ## Connecting sliders to actions
        self.w.slider_red.sliderMoved.connect(self.on_slider_change)
        self.w.slider_green.sliderMoved.connect(self.on_slider_change)
        self.w.slider_blue.sliderMoved.connect(self.on_slider_change)
        self.w.slider_intensity.sliderMoved.connect(self.on_slider_change)
        self.w.SliderVal_but_text_intensity.clicked.connect(partial(self.getItem,"intensity"))
        self.w.SliderVal_but_text_red.clicked.connect(partial(self.getItem,"red"))
        self.w.SliderVal_but_text_green.clicked.connect(partial(self.getItem,"green"))
        self.w.SliderVal_but_text_blue.clicked.connect(partial(self.getItem,"blue"))

    def lightsettings(self, debug=debugArray[13], RGB_value = [0,0,0], Brightness = 50):
                ## Settings of sliders
            ## Slider Red value
        self.w.SliderVal_but_text_red.setText(str(RGB_value[0]))

            ## Slider Green value
        self.w.SliderVal_but_text_green.setText(str(RGB_value[1]))   

            ## Slider Blue value
        self.w.SliderVal_but_text_blue.setText(str(RGB_value[2]))

            ## Slider Brightness 
        #self.w.slider_intensity.setValue(Brightness)
        self.w.SliderVal_but_text_intensity.setText(str(Brightness)+"%")
    
    def lightprofiles(self):
        profile= CustomDialog_LightProfiles()
        previous_key_val = profile.exec() 
        if previous_key_val:
            ## Write info from file into corresponding variables
            lines = open('/home/dgslr/ProgramFiles/LightProfiles_saved.txt', 'r').readlines()
            R_val = int(lines[int(profile.previous_key)+2][22:25])            
            G_val = int(lines[int(profile.previous_key)+2][26:29])
            B_val = int(lines[int(profile.previous_key)+2][30:33])            
            BB_val = int(lines[int(profile.previous_key)+2][50:53]) 
            lightInputs[0][0] = int(lines[int(profile.previous_key)+2][66])
            lightInputs[1][0] = int(lines[int(profile.previous_key)+2][68])
            lightInputs[2][0] = int(lines[int(profile.previous_key)+2][70])
            lightInputs[0][1] = int(lines[int(profile.previous_key)+2][72])
            lightInputs[1][1] = int(lines[int(profile.previous_key)+2][74])
            lightInputs[2][1] = int(lines[int(profile.previous_key)+2][76])
            lightInputs[0][2] = int(lines[int(profile.previous_key)+2][78])
            lightInputs[1][2] = int(lines[int(profile.previous_key)+2][80])
            lightInputs[2][2] = int(lines[int(profile.previous_key)+2][82])

            self.w.check_Top_Enable.setChecked(lightInputs[0][0])
            #lightInputs[1][0] = self.w.check_Left_Enable.isChecked()
            #lightInputs[2][0] = self.w.check_Right_Enable.isChecked()
            #lightInputs[0][1] = self.w.check_Top_RGB.isChecked()
            ##lightInputs[1][1] = self.w.check_Left_RGB.isChecked()
            #lightInputs[2][1] = self.w.check_Right_RGB.isChecked()
            #lightInputs[0][2] = self.w.check_Top_White.isChecked()
            #lightInputs[1][2] = self.w.check_Left_White.isChecked()
            #lightInputs[2][2] = self.w.check_Right_White.isChecked()

            #self.print_on_GUI_terminal(text_to_print= "LIGHTMATRIX " + str(lightInputs),  color='default')
           
            self.print_on_GUI_terminal(text_to_print="Light profile: " + str(profile.previous_key) + " is succesfully loaded!",  color='black')
            loaded_light_profile = profile.previous_key
            self.w.text_loaded_profile.setText(str(loaded_light_profile))
            self.w.slider_red.setValue(R_val)
            self.w.slider_green.setValue(G_val)
            self.w.slider_blue.setValue(B_val)
            self.w.slider_intensity.setValue(BB_val)
            visionbox.on_slider_change(self)

    def save_lightprofiles(self):
        areyousure = areYouSure()
        returnvalue = areyousure.exec()
        if returnvalue:
            # Write Setting to txt file
            R_val = str(self.w.slider_red.value()).zfill(3)
            G_val = str(self.w.slider_green.value()).zfill(3)
            B_val = str(self.w.slider_blue.value()).zfill(3)
            BB_val = str(self.w.slider_intensity.value()).zfill(3)
            text_to_print = str(self.w.text_loaded_profile.text()).zfill(2) + "; profile " +str(self.w.text_loaded_profile.text()).zfill(2)+ "; RGB; [" + R_val + "," + G_val + "," + B_val + "] ; BRIGHTNESS; [" + BB_val + "] ; MATRIX; [" +str(lightInputs[0][0])+","+str(lightInputs[1][0])+","+str(lightInputs[2][0])+";"+str(lightInputs[0][1])+","+str(lightInputs[1][1])+","+str(lightInputs[2][1])+";"+str(lightInputs[0][2])+","+str(lightInputs[1][2])+","+str(lightInputs[2][2])+ "] ; comment \n"
            lightsettingsClass.replace_line('/home/dgslr/ProgramFiles/LightProfiles_saved.txt', (int(self.w.text_loaded_profile.text()) + 2), text_to_print)  # Offset of 2 to start looking after initilisation of file
            self.print_on_GUI_terminal(text_to_print= "Profile " + str(self.w.text_loaded_profile.text()) + ". Settings stored in file!",  color='default')
            self.w.number_of_images.setText(str(img_count).zfill(3))

    def replace_line(file_name, line_num, text):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.write("\n")
        out.close()

        #if action == "save":
        #    self.print_on_GUI_terminal(text_to_print="HELLO TEST SAVE",  color='red')
        #elif action == "load":
        #    self.print_on_GUI_terminal(text_to_print="HELLO TEST LOAD",  color='red')
        #else:
        #    self.print_on_GUI_terminal(text_to_print="HELLO TEST NONE",  color='red')
        