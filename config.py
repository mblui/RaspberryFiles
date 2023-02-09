from PySide2.QtGui      import QColor
import time
import board
import neopixel
import numpy as np
## ------------------------------ Inputs ------------------------------
# Set Path directories 
dir_path =  r'/home/dgslr/ProgramFiles/'
scp_path =  dir_path + "SCP_images/"

## Set main window size
windowsize = np.array([1920, 900, 0])     # [width,heights, Fullsize = 1/0]
default_font_size = 18
default_font_size_buttons = 14

## Set update FPS
updatefps = 3

## Define user/Admin settings
AvailableUserProfiles = ["DGS admin", "View only"]
Password_admin  = "1466"
color_green     = QColor(0,153,0)
color_red       = QColor(255,0,0)
color_black     = QColor(0,0,0)
color_default   = QColor(0,0,0)

# Led light related variables
RGB_val= np.array([0,0,0])                      # Default RGB value             range: [0-255]
Brightness_value = 50                           # Default brightness value      range: [0-50]%
pixel_pin = board.D18
ORDER = neopixel.GRBW
num_pixels = 60
max_brightness = 255;                           # Range [0-1]

pos_led_top     = np.array([20,  25])           
pos_led_left    = np.array([30,  35])
pos_led_right   = np.array([40,  45])
max_pixels_manual = 60


# Define maximum allowed number of images
maxImagesBits = 6                           # Maxum number of images in the folder (in bits) -->  000000

debugArray = [      0,      # Debug 0:  update image
                    0,      # Debug 1:  on_export_files_zip
                    0,      # Debug 2:  errorhandler     
                    0,      # Debug 3:  enable_disable_inputs
                    0,      # Debug 4:  onCheckboxChange  
                    0,      # Debug 5:  openFolder
                    0,      # Debug 6:  on_button_press  
                    0,      # Debug 7:  on_lock_unlock_button
                    0,      # Debug 8:  on_next_previous_image
                    0,      # Debug 9:  on_slider_change
                    0,      # Debug 10: getItem
                    0,      # Debug 11: getAvailableImagesInFolder
                    0,      # Debug 12: lightsettingsClass.__init__
                    0,      # Debug 13: lightsettingsClass.lightsettings
                    0,      # Debug 14: print_on_GUI_terminal  
                    0,      # Debug 15: apply_signal_to_leds
                    0,      # Debug 16:   
                    0,      # Debug 17:   
                    0,      # Debug 18:   
                    0,      # Debug 19:   
                    0,      # Debug 20:   
            ]


## ------------------------------ Initilisation ------------------------------
# Error handling
errorMsgBit = int(999)                        # Initial errorbit value, see ErrorHandler for details

# Date and time initilisatoin
current_date_time = "01/01/2023 00:00:00"
ExtendedPath = ""

# The number of images in scp_path
img_count = 0                               # number of images
img_to_display_cnt = 0                      # number of displayed image     
img_files = 0                               # sorted list of images

# Automaticly start to show most recent image in scp folder on startup
globalImageUpdate = False                   # (Afterwards managable via start/pause/previous/next buttons)

# Object to pass to LED (range [0-1])                      Top:    Left:   Right:
lightInputs =np.array([ [0,     0,      0],         # Enable:       X       X       X                   
                        [0,     0,      0],         # RGB:          X       X       X
                        [0,     0,      0]])        # White:        X       X       X    