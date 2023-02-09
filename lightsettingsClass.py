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


class lightsettingsClass:
    def __init__(self, debug=debugArray[12], RGB_value = [0,0,0], Brightness = 10):
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

    def lightsettings(self, debug=debugArray[13], RGB_value = [0,0,0], Brightness = 0.1):
                ## Settings of sliders
            ## Slider Red value
        self.w.SliderVal_but_text_red.setText(str(RGB_value[0]))

            ## Slider Green value
        self.w.SliderVal_but_text_green.setText(str(RGB_value[1]))   

            ## Slider Blue value
        self.w.SliderVal_but_text_blue.setText(str(RGB_value[2]))

            ## Slider Brightness 
        self.w.slider_intensity.setValue(Brightness)
        self.w.SliderVal_but_text_intensity.setText(str(Brightness)+"%")
