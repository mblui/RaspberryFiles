##########################################################
##  Vision box - Raspberry File main code               ##   
##  Project:            201911                          ##
##  Authors:            Evi Weersink, Mart Bluiminck    ##
##  Version:            0.1                             ##
##  Last release:       XX-XX-XXXX, by XXXX             ## 
##########################################################

# Import system functionalities 
import sys, os, subprocess, zipfile, shutil
from functools import partial               # To pass multiple arguments in a function call
from showinfm import show_in_file_manager   # To open folder when button pressed

# Import PySide package
from PySide2.QtWidgets  import QApplication, QWidget, QMessageBox, QLabel, QMainWindow, QInputDialog, QGridLayout, QPushButton, QLineEdit, QDialog, QVBoxLayout, QDialogButtonBox, QTextEdit
from PySide2.QtCore     import * #QFile, QTimer, QSize
from PySide2.QtUiTools  import QUiLoader
from PySide2.QtGui      import QPixmap, QTouchEvent, QIcon, QColor
# Import common image packages
import cv2

# Import array sorting package
from natsort import natsorted 

# Import time related packages
import time
from datetime import datetime

# Import dependent scripts
from config             import *    #   Load configuration and initial values
from ErrorHandler       import *    #   Defines the error handling
from lightsettingsClass import *    #   Defines input/outputs    
from systemClass        import *    #   Defines general system fuctions
#from main               import *
from LED_strips         import *

from functools import partial
class visionbox(QMainWindow):
    def __init__(self, parent: QWidget = None):
        # global img_files, img_count, globalImageUpdate
        global current_date_time
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
        self.print_on_GUI_terminal(text_to_print="--> Program is started!",  color='default')
        

        # Initial count number of images
        img_files, img_count = systemClass.getAvailableImagesInFolder(self) 

        # Link buttons
        self.on_lock_unlock_button()
        self.w.button_openImageFolder.clicked.connect(self.openFolder)
        self.w.button_ExitProgram.clicked.connect(lambda: systemClass.ExitProgram(self))
        self.w.Start_pause_watching.clicked.connect(self.on_button_press)
        self.w.Start_pause_watching.setCheckable(True)
        self.w.button_ExportFilesZIP.clicked.connect(lambda: systemClass.on_export_files_zip(self, time=current_date_time))
        self.w.button_previous_img.clicked.connect(partial(self.on_next_previous_image,-1))
        self.w.button_next_img.clicked.connect(partial(self.on_next_previous_image, 1))
        self.w.lock_unlock_button.clicked.connect(self.on_lock_unlock_button)
        self.w.lock_unlock_button.setCheckable(True)

        # Initialise 
        lightsettingsClass.__init__(self)       #   Link buttons and sliders to functions
        LED_strips.__init__(self)               #   Send initial command to LED strips
        self.on_button_press()                  #   Initialse start/pause button
        
        ## Set update timer
        self.__acquisition_timer = QTimer()
        timer = QTimer(self)
        timer.timeout.connect(partial(self.update_GUI))     
        timer.start((1/updatefps)*1000)
        self.update_GUI()
        self.print_on_GUI_terminal(text_to_print="Init done!",  color='default')

    def print_on_GUI_terminal(self, text_to_print, debug=debugArray[14], color = 'default'):
        global current_date_time
        self.w.textBrowser.setReadOnly(True)
        current_date_time = str(datetime.now().strftime("%d/%m/%Y   %H:%M:%S"))
        message = current_date_time + "  " + str(text_to_print)
        # Set colors      
        if      color == 'r' or color =='red':      self.w.textBrowser.setTextColor(color_red)
        elif    color == 'g' or color =='green':    self.w.textBrowser.setTextColor(color_green)
        else:                                       self.w.textBrowser.setTextColor(color_default)
        self.w.textBrowser.append(message)
        ## Also write Gui_terminal to txt file

        with open("/home/dgslr/ProgramFiles/log_file.txt","a") as file:
            file.write("\n")
            file.write(message)
        

    def enable_disable_inputs(self, value, debug=debugArray[3]):
        self.w.button_openImageFolder.setEnabled(value)
        #self.w.button_ExitProgram.setEnabled(False)
        #self.w.lock_unlock_button.setEnabled(False)
        #self.w.Start_pause_watching.setEnabled(value)
        self.w.button_ExportFilesZIP.setEnabled(value)
        #self.w.button_previous_img.setEnabled(value)
        #self.w.button_next_img.setEnabled(value)
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

    def onCheckboxChange(self, debug=debugArray[4]):
        lightInputs[0][0] = self.w.check_Top_Enable.isChecked()
        lightInputs[1][0] = self.w.check_Left_Enable.isChecked()
        lightInputs[2][0] = self.w.check_Right_Enable.isChecked()
        lightInputs[0][1] = self.w.check_Top_RGB.isChecked()
        lightInputs[1][1] = self.w.check_Left_RGB.isChecked()
        lightInputs[2][1] = self.w.check_Right_RGB.isChecked()
        lightInputs[0][2] = self.w.check_Top_White.isChecked()
        lightInputs[1][2] = self.w.check_Left_White.isChecked()
        lightInputs[2][2] = self.w.check_Right_White.isChecked()
        if debug: print(lightInputs)
        LED_strips.apply_signal_to_leds(self, lightInputs)
        
    def openFolder(self, debug=debugArray[5]):
        show_in_file_manager(scp_path)

    def on_button_press(self, debug=debugArray[6]):
        global globalImageUpdate
        if self.w.Start_pause_watching.isChecked():
            self.w.Start_pause_watching.setText(str("Start"))
            self.w.Start_pause_watching.setIcon(QIcon('play_icon.png'))
            globalImageUpdate = False
        else:
            self.w.Start_pause_watching.setText(str("Pause"))
            self.w.Start_pause_watching.setIcon(QIcon('pause_icon.png'))
            globalImageUpdate = True
        


    def on_lock_unlock_button(self,debug=debugArray[7]):
        if self.w.lock_unlock_button.isChecked():
            unlock = CustomDialog()
            unlock.exec()
            print("OUPUT:", unlock)
            #if output:
            #   self.enable_disable_inputs(value=1) #True
            #    self.w.text_current_user.setText(str(AvailableUserProfiles[0]))
            #    self.w.lock_unlock_button.setIcon(QIcon('unlock_icon.png'))
        else:
            self.enable_disable_inputs(value=0) #False
            self.w.text_current_user.setText(str(AvailableUserProfiles[1]))
            self.w.lock_unlock_button.setIcon(QIcon('lock_icon.png'))

    def on_next_previous_image(self,value, debug=debugArray[8]):
        global img_to_display_cnt
        self.w.Start_pause_watching.setChecked(True)
        self.on_button_press()
        if img_to_display_cnt >= 0 and  img_to_display_cnt < img_count:
            img_to_display_cnt = img_to_display_cnt + value
           
    def update_GUI(self, debug=debugArray[0]):
        global cnt, img_count, Brightness_value, RGB_val, globalImageUpdate, current_date_time, img_to_display, img_to_display_cnt
        if debug: print(globalImageUpdate)
        img_files, img_count = systemClass.getAvailableImagesInFolder(self) 
        
        self.w.number_of_images.setText(str(img_count).zfill(maxImagesBits))
        if len(img_files)<1:
            self.w.num_img.setText("No files in folder to display")
        else:
            if globalImageUpdate:
                img_to_display_cnt = img_count-1 ## show latest image
            img_to_display = img_files[img_to_display_cnt]
            self.w.num_img.setText(img_to_display)
            ExtendedPath = scp_path + str(img_to_display)
            label = self.w.imglabel
            pixmap =QPixmap(ExtendedPath)
            label.setPixmap(pixmap)
            label.show()

        lightsettingsClass.lightsettings(self, RGB_value=RGB_val, Brightness=Brightness_value)      ## Update lightvalues
        ## TODO place timerupdate on separate Qtimer --> now its randomly updating.
        current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.w.text_date_time.setText(str(current_date_time))

    def on_slider_change(self, debug=debugArray[9]):
        global RGB_val, Brightness_value
        # Update RGBvalue
        Brightness_value = self.w.slider_intensity.value()
        RGB_val[0] = self.w.slider_red.value()
        RGB_val[1] = self.w.slider_green.value()
        RGB_val[2] = self.w.slider_blue.value()
        LED_strips.apply_signal_to_leds(self, lightInputs)

    def getItem(self, slidertype, debug=debugArray[10]):  # slidertype := [intensity', 'red', 'green', 'blue']
        global Brightness_value,RGB_val
        items_1 = ("0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100")
        items_2 = ("0", "25", "51", "77", "102", "128", "153", "178", "204", "229", "255")
        items = items_1 if slidertype == "intensity" else items_2
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

if __name__ == "__main__":
    app = QApplication([])
    widget = visionbox()
    widget.show()
    sys.exit(app.exec_())

class CustomDialog(QDialog):
    def __init__(self):
        global insertedText
        super().__init__()
        insertedText = ""

        self.setWindowTitle("Virtual Keyboard")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.keyinputDisplay = QLineEdit()
        self.keyinputDisplay.setReadOnly(True)
        self.layout.addWidget(self.keyinputDisplay)
        self.layout.addWidget(message)
        #############################################
        WINDOW_SIZE = 235
        DISPLAY_HEIGHT = 35
        BUTTON_SIZE = 40
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["", "0", ""],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
                self.buttonMap[key].clicked.connect(partial(self.showww, key))
        self.layout.addLayout(buttonsLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    def showww(self, key):
        global insertedText
        insertedText = insertedText + str(key)
        self.keyinputDisplay.setText(insertedText)
        print(insertedText)


##############    # ERROR @: Change admin rights
        # elif errorMsgBit == 3:
        #     text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        #     if ok:
        #         if text == "1466":
        #             errorMsgBit = 0
        #             self.print_on_GUI_terminal(text_to_print="Succesfull change of admin rights!",  color='green')
        #             return errorMsgBit, True
        #         self.print_on_GUI_terminal(text_to_print="Wrong Password!",  color='red')
        #         return errorMsgBit, False
