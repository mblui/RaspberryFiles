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


def errorMsg(errorMsgBit, cnt):
    if errorMsgBit:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error! counter bigger than setpoint!")
        dlg.setText("Counter bigger than setpoint! Do you want to reset the counter?")
        button = dlg.exec_()
        if button == QMessageBox.Ok:
            cnt = 0
            errorMsgBit = 0
        return errorMsgBit
