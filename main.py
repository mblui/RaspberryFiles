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
from ErrorHandler import *
from LinkSliders import *

# Set path to directory with images 1
dir_path = r'/home/dgslr/ProgramFiles/'
scp_path = dir_path + "SCP_images/"

# --- --- Define inputs ---
windowsize = [800, 600] # [width,heights]
updatefps = 1

# ---- --- Define Global variables
cnt = int(1)
Brightness_value = int(50)
errorMsgBit = int(0)
ExtendedPath = ""
RGB_val= [0,0,0]
file_count = 0
lightInputs = [ [0,0,0],        # Corresponding to GUI
                [0,0,0],
                [0,0,0]]
# ---- ---- ---- ---- ----


class visionbox(QMainWindow):

    def __init__(self, parent: QWidget = None):
        global file_count
        super().__init__(parent)
        self.setWindowTitle("Vision Box")
        self.setFixedSize(QSize(windowsize[0], windowsize[1]))

        self.__acquisition_timer = QTimer()
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.w = loader.load(ui_file, self) #self
        self.w.show()
        ui_file.close()

        # Link sliders and initialize
        lightsettingsClass.lightsettings(self, RGB_value=RGB_val, Brightness=Brightness_value)

        # Initial count number of images
        _,_,files = next(os.walk(scp_path))
        file_count = len(files)
        print(file_count)

        self.w.pushButton.clicked.connect(self.on_button_press)
        self.w.button_openImageFolder.clicked.connect(self.openFolder)
        self.w.button_ExitProgram.clicked.connect(self.ExitProgram) 
        

        timer = QTimer(self)
        timer.timeout.connect(self.update_image)
        timer.start((1/updatefps)*1000)
        self.update_image()

    def onCheckboxChange(self):
        lightInputs[0,0] = self.w.check_Top_Enable.toggled.isChecked()
        lightInputs[0,1] = self.w.check_Left_Enable.toggled.isChecked()
        lightInputs[0,2] = self.w.check_Right_Enable.toggled.isChecked()
        lightInputs[1,0] = self.w.check_Top_RGB.toggled.isChecked()
        lightInputs[1,1] = self.w.check_Left_RGB.toggled.isChecked()
        lightInputs[1,2] = self.w.check_Right_RGB.toggled.isChecked()
        lightInputs[2,0] = self.w.check_Top_White.toggled.isChecked()
        lightInputs[2,1] = self.w.check_Left_White.toggled.isChecked()
        lightInputs[2,2] = self.w.check_Right_White.toggled.isChecked()
        print(lightInputs)
        print("UpdateDone")

    def ExitProgram(self):
        errorMsgHandlerClass.errorMsgHandler(self, errorMsgBit=1, debug= False)
        
    def openFolder(self):
        #subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')
        show_in_file_manager('/home/dgslr/ProgramFiles/SCP_images')
    def on_button_press(self):
        global cnt, errorMsgBit, ExtendedPath, file_count
        cnt += 1
        _,_,files = next(os.walk(scp_path))
        file_count = len(files)
        self.w.num_img.setText(str(file_count))
        if False: #nt > file_count:
            errorMsgBit = 1

    def update_image(self):
        global cnt, file_count, Brightness_value, RGB_val
        _,_,files = next(os.walk(scp_path))
        file_count = len(files)

        cnt = file_count
        self.w.num_img.setText(str(file_count))
        ExtendedPath = scp_path + "img" + str(cnt) + ".jpg"
        print(ExtendedPath)
        label = self.w.imglabel
        pixmap =QPixmap(ExtendedPath)
        label.setPixmap(pixmap)
        label.show()
        self.w.SliderVal_but_text_intensity.setText(str(Brightness_value))
        self.w.SliderVal_but_text_red.setText(str(RGB_val[0]))
        self.w.SliderVal_but_text_green.setText(str(RGB_val[1]))
        self.w.SliderVal_but_text_blue.setText(str(RGB_val[2]))

    def on_slider_change(self):
        global RGB_val, Brightness_value
        # Update RGBvaluea
        Brightness_value = self.w.slider_intensity.value()
        RGB_val[0] = self.w.slider_red.value()
        RGB_val[1] = self.w.slider_green.value()
        RGB_val[2] = self.w.slider_blue.value()

    def getItem(self, slidertype):  # slidertype := [intensity', 'red', 'green', 'blue']
        global Brightness,RGB_val
        items_1 = ("0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100")
        items_2 = ("0", "25", "51", "77", "102", "128", "153", "178", "204", "229", "255")
        items = items_1 if slidertype == "intensity" else items_2
        #item, ok = QInputDialog.getInt(self, "select input", "enter a number", self.w.slider_intensity.value())
        item, ok = QInputDialog.getItem(self, "select input", "enter a number", items, 0, False)
        if ok:
            if (slidertype == "intensity"):
                Brightness = int(item)
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

# test
if __name__ == "__main__":
    app = QApplication([])
    widget = visionbox()
    widget.show()
    sys.exit(app.exec_())
