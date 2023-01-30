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
# 1     =   exit program
# 2     =   ...
# 3     =   ...
# 4     =   ...
# 5     =   ...
# 6     =   ...
# 7     =   ...

def errorMsg(errorMsgBit, cnt):
    # Program exit is pressend
    if errorMsgBit == 1:
        dlg = QMessageBox(self)
        dlg.question(self,'', "Are you sure to reset all the values?", qm.Yes | qm.No)
        if qm.Yes:
            sys.exit(app.exec_())    
        return errorMsgBit, True

    ## error bit ...
    if errorMsgBit == 2:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Program exit?")
        dlg.setText("Are you sure to exit current program?")
        button = dlg.exec_()
        if button == QMessageBox.Ok:
            cnt = 0
            errorMsgBit = 0
        return errorMsgBit, True

