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
from natsort import natsorted 
import zipfile, shutil
from datetime import datetime

# Set path to directory with images 1
dir_path = r'/home/dgslr/ProgramFiles/'
scp_path = dir_path + "SCP_images/"

# --- --- Define inputs ---
windowsize = [1920, 850, 0] # [width,heights, Fullsize = 1/0]
updatefps = 1

# ---- --- Define Global variables/ Initial values
cnt = int(1)
AvailableUserProfiles = ["Only-view",  "DGS admin"]
User = "default"            # [Default, DGS]
Password_admin = "1466"
maxImagesBits = 6           # Maxum number of images in the folder (in bits) -->  000000
globalImageUpdate = False
Brightness_value = int(50)
current_date_time = "01/01/2023 00:00:00"
errorMsgBit = int(0)
ExtendedPath = ""
RGB_val= [0,0,0]
img_count = 0           # number of images
img_to_display_cnt = 0  # number of displayed image     
img_files = 0           # sorted list of images
lightInputs = [ [0,0,0],        # Corresponding to GUI
                [0,0,0],
                [0,0,0]]
# ---- ---- ---- ---- ----

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
        lightsettingsClass.__init__(self)
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

    def ExitProgram(self):
        errorMsgHandlerClass.errorMsgHandler(self, errorMsgBit=1, debug= False)
        
    def openFolder(self):
        show_in_file_manager(scp_path)

    def on_export_files_zip(self):
        global img_count, current_date_time
        # Generate Name
        name = current_date_time.replace(" ", "_").replace("/", "_")
        name = "RecordedImages" + name + str(".zip")
        self.make_archiveZip(source=dir_path + "SCP_images", destination= dir_path + name)

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
            errorMsgHandlerClass.errorMsgHandler(self, errorMsgBit=2, debug= False)   
        
        # if backup is succesfull
        if img_backup_succesfull: 
            os.chdir(dir_path + "SCP_images")
            #[os.remove(f) for f in os.listdir()]        
            [print(f) for f in os.listdir()]       
            [os.remove(f) for f in os.listdir()]       
            #Pprint("Done")
        img_files, img_count = self.getAvailableImagesInFolder() 
        # TODO Add dialog to show that export is succesfull with name ... 

    def on_button_press(self):
        global globalImageUpdate
        if self.w.Start_pause_watching.isChecked():
            self.w.Start_pause_watching.setText(str("Start"))
            self.w.Start_pause_watching.setIcon(QIcon('play_icon.png'))
            globalImageUpdate = False
        else:
            self.w.Start_pause_watching.setText(str("Pause"))
            self.w.Start_pause_watching.setIcon(QIcon('pause_icon.png'))
            globalImageUpdate = True

    def on_lock_unlock_button(self):
        if self.w.lock_unlock_button.isChecked():
            self.w.text_current_user.setText(str(AvailableUserProfiles[1]))
            self.w.lock_unlock_button.setIcon(QIcon('lock_icon.png'))

        else:
            _,output = errorMsgHandlerClass.errorMsgHandler(self, errorMsgBit=3, debug= False)
            if str(output) == "1466":
                self.w.text_current_user.setText(str(AvailableUserProfiles[0]))
                self.w.lock_unlock_button.setIcon(QIcon('unlock_icon.png'))


    def on_next_previous_image(self,value):
        global img_to_display_cnt
        self.w.Start_pause_watching.setChecked(True)
        self.on_button_press()
        #print("editvalue1", img_to_display_cnt)
        if img_to_display_cnt >= 0 and  img_to_display_cnt < img_count:
            img_to_display_cnt = img_to_display_cnt + value

           
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

        lightsettingsClass.lightsettings(self, RGB_value=RGB_val, Brightness=Brightness_value)      ## Update lightvalues
        ## TODO place timerupdate on separate Qtimer --> now its randomly updating.
        current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.w.text_date_time.setText(str(current_date_time))

    def on_slider_change(self):
        global RGB_val, Brightness_value
        # Update RGBvalue
        Brightness_value = self.w.slider_intensity.value()
        RGB_val[0] = self.w.slider_red.value()
        RGB_val[1] = self.w.slider_green.value()
        RGB_val[2] = self.w.slider_blue.value()

    def getAvailableImagesInFolder(self):
        _,_,files = next(os.walk(scp_path))
        img_count = len(files)
        img_files = natsorted(files)
        print("img_count", img_count, "img_files", img_files)
        return img_files, img_count

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

if __name__ == "__main__":
    app = QApplication([])
    widget = visionbox()
    widget.show()
    sys.exit(app.exec_())
