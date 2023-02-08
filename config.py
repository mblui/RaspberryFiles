
## ------------------------------ Inputs ------------------------------
# Set Path directories 
dir_path =  r'/home/dgslr/ProgramFiles/'
scp_path =  dir_path + "SCP_images/"

## Set main window size
windowsize = [1920, 850, 1]     # [width,heights, Fullsize = 1/0]

## Set update FPSdf
updatefps = 1

## Define user/Admin settings
AvailableUserProfiles = ["DGS admin", "View only"]
Password_admin = "1466"

# Led light related variables
RGB_val= [0,0,0]                            # Default RGB value             range: [0-255]
Brightness_value = int(50)                  # Default brightness value      range: [0-100]

# Define maximum allowed number of images
maxImagesBits = 6                           # Maxum number of images in the folder (in bits) -->  000000

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
lightInputs = [ [0,     0,      0],         # Enable:       X       X       X                   
                [0,     0,      0],         # RGB:          X       X       X
                [0,     0,      0]]         # White:        X       X       X    