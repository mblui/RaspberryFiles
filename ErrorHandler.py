# This Python file uses the following encoding: utf-8
import sys
import os
import cv2
import subprocess
from showinfm import show_in_file_manager

from PySide2.QtWidgets  import QApplication, QWidget, QMessageBox, QLabel, QMainWindow, QInputDialog, QGridLayout, QPushButton, QLineEdit, QDialog, QVBoxLayout, QDialogButtonBox, QTextEdit
from PySide2.QtCore     import * #QFile, QTimer, QSize
from PySide2.QtUiTools  import QUiLoader
from PySide2.QtGui      import QPixmap, QTouchEvent, QIcon, QColor, QFont
from functools import partial

from config import *
from LED_strips import *
# Error message bits
# 0     =   no error
# 1     =   
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

    def errorMsgHandler(self, errorMsgBit , debug=debugArray[2], cnt=0):
        if debug:print("Item is:", errorMsgBit, "Errorbit:", errorMsgBit, "Count:", cnt)

    # ERROR 1:  Program exit is pressend


    # ERROR 2: Error while exporting to ZIP
        elif errorMsgBit == 2:
            dlg = QMessageBox()
            #dlg.setFont(QFont('Times', default_font_size_buttons))
            dlg.setWindowTitle("Error")
            dlg.setText("Error occured while extracting files to ZIP?")
            self.print_on_GUI_terminal(text_to_print="Error occured while extracting files to ZIP",  color='red')
            button = dlg.exec_()
            if button == QMessageBox.Ok:
                cnt = 0
                errorMsgBit = 0
            return errorMsgBit, True

        else:
            print("No errors found")
            return errorMsgBit, True 