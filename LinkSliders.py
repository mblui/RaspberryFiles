# This Python file uses the following encoding: utf-8
import sys
import os
import cv2
import subprocess
from showinfm import show_in_file_manager

from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QMainWindow, QInputDialog
from PySide2.QtCore import QFile, QTimer, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QTouchEvent
from functools import partial
import time



class linksliders:
    def __init__(self):
        super().__init__()

    def linkslider(self):
        self.w.slider_red.setMinimum(0)
        self.w.slider_intensity.setValue(Brightness)
        self.w.slider_red.setMaximum(255)
        self.w.slider_green.setMinimum(0)
        self.w.slider_green.setMaximum(255)
        self.w.slider_blue.setMinimum(0)
        self.w.slider_blue.setMaximum(255)
        self.w.SliderVal_but_text_intensity.setText(str(Brightness))
        self.w.SliderVal_but_text_red.setText(str(RGB_val[0]))
        self.w.SliderVal_but_text_green.setText(str(RGB_val[1]))
        self.w.SliderVal_but_text_blue.setText(str(RGB_val[2]))

        self.w.pushButton.clicked.connect(self.on_button_press)
        self.w.slider_red.sliderMoved.connect(self.on_slider_change)
        self.w.slider_green.sliderMoved.connect(self.on_slider_change)
        self.w.slider_blue.sliderMoved.connect(self.on_slider_change)
        self.w.slider_intensity.sliderMoved.connect(self.on_slider_change)
        self.w.SliderVal_but_text_intensity.clicked.connect(partial(self.getItem,"intensity"))
        self.w.SliderVal_but_text_red.clicked.connect(partial(self.getItem,"red"))
        self.w.SliderVal_but_text_green.clicked.connect(partial(self.getItem,"green"))
        self.w.SliderVal_but_text_blue.clicked.connect(partial(self.getItem,"blue"))
        self.w.button_openImageFolder.clicked.connect(self.openFolder)
        self.w.button_ExitProgram.clicked.connect(self.ExitProgram) 
