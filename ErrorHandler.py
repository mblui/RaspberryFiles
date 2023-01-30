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


# Error message bits
# 0     =   no error
# 1     =   Exit program
# 2     =   ...
# 3     =   ...
# 4     =   ...
# 5     =   ...
# 6     =   ...
# 7     =   ...

class errorMsgHandlerClass(QMessageBox):
    def __init__(self):
        super().__init__()

    def errorMsgHandler(self, errorMsgBit , cnt=0, debug = 0):
        if debug:
            print("Item is:", errorMsgBit, "Errorbit:", errorMsgBit, "Count:", cnt)

    # ERROR 1:  Program exit is pressend
        if errorMsgBit == 1:
            dlg = QMessageBox.question(self,"Exit program?", "Are you sure to exit the current program?", QMessageBox.Yes | QMessageBox.No)
            if dlg.Yes:
                sys.exit()    
            return True, errorMsgBit

    # ERROR 2: ....
        elif errorMsgBit == 2:
            dlg = QMessageBox()
            dlg.setWindowTitle("Program exit?")
            dlg.setText("Are you sure to exit current program?")
            button = dlg.exec_()
            if button == QMessageBox.Ok:
                cnt = 0
                errorMsgBit = 0
            return errorMsgBit, True

    # ERROR @: ....
        elif errorMsgBit == 2:  
            print("...")

        else:
            print("No errors found")
            return False, errorMsgBit 