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
# 1     =   Exit program 1
# 2     =   ...
# 3     =   ...
# 4     =   ...
# 5     =   ...
# 6     =   ...
# 7     =   ...
# 999   =   System is booting
class errorMsgHandlerClass(QMessageBox):
    def __init__(self):
        super().__init__()

    def errorMsgHandler(self, errorMsgBit , cnt=0, debug = 0):
        if debug:
            print("Item is:", errorMsgBit, "Errorbit:", errorMsgBit, "Count:", cnt)

    # ERROR 1:  Program exit is pressend
        if errorMsgBit == 1:
            #dlg = QMessageBox.question(self,"Exit program?", "Are you sure to exit the current program?", QMessageBox.Yes | QMessageBox.No)
            txt = "program is exit"
            reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.print_on_GUI_terminal(text_to_print="Program is closed!",  color='default')
                sys.exit()
            return errorMsgBit, True

    # ERROR 2: Error while exporting to ZIP
        elif errorMsgBit == 2:
            dlg = QMessageBox()
            dlg.setWindowTitle("Error")
            dlg.setText("Error occured while extracting files to ZIP?")
            self.print_on_GUI_terminal(text_to_print="Error occured while extracting files to ZIP",  color='red')
            button = dlg.exec_()
            if button == QMessageBox.Ok:
                cnt = 0
                errorMsgBit = 0
            return errorMsgBit, True

    # ERROR @: Change admin rights
        elif errorMsgBit == 3:
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
            if ok:
                if text == "1466":
                    errorMsgBit = 0
                    self.print_on_GUI_terminal(text_to_print="Succesfull change of admin rights!",  color='green')
                    return errorMsgBit, True
                self.print_on_GUI_terminal(text_to_print="Wrong Password!",  color='red')
                return errorMsgBit, False

        else:
            print("No errors found")
            return errorMsgBit, True 