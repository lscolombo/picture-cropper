from PIL import Image
from datetime import datetime
import glob
import os
import sys
from colorama import Fore, Back, Style,init

init()

def log_start_end(s):
    log_string = s
    print(Fore.GREEN+Style.BRIGHT+log_string+Style.RESET_ALL)
    log(log_string)


def log_info(cur_index,filename,s):
    log_string = "["+str(cur_index)+" - " + filename+"]: "
    print(Fore.CYAN + Style.DIM + log_string + Style.BRIGHT + s + Style.RESET_ALL)
    log(log_string+s)

def log_error(cur_index,filename,s):
    log_string = "["+str(cur_index)+" - " + filename + "]: ERROR - "
    print(Fore.RED + Style.DIM + log_string +Style.BRIGHT + s + Style.RESET_ALL)
    log(log_string+s)

def log_timer(cur_index,filename,s):
    log_string =  "[" + str(cur_index)+" - " + filename + "]: " 
    print(Fore.YELLOW + Style.DIM +log_string+Style.BRIGHT + s+Style.RESET_ALL)
    log(log_string+s)
    
def save_picture(pic,filename_i):
    saved_filename = 'foto-'+str(filename_i).zfill(4)+'.png'
    pic.save(DIRECTORY_OUTPUT+saved_filename)
    return(saved_filename)

def log(s):
    with open("log.txt", "a") as log_file:
        log_file.write(s)
        log_file.write("\n")

def check_if_directories_exist():
    if not os.path.exists(DIRECTORY_INPUT.replace("*.png",'')):
        log_error("-","-","Input directory does not exist: " + DIRECTORY_INPUT.replace("*.png",''))
        sys.exit(0)
    if not os.path.exists(DIRECTORY_OUTPUT):
        log_error("-","-","Output directory does not exist: " + DIRECTORY_OUTPUT)
        sys.exit(0)


try:
    last_filename_index = int(input(Fore.BLUE + Style.BRIGHT + "Enter last filename index (i.e. 0001): " + Style.RESET_ALL))
    last_filename_index+=1
except ValueError:
    log_error('-','-',"You must enter a number")
    sys.exit(0)

start_filename_index = last_filename_index

startTime = datetime.now()

Image.MAX_IMAGE_PIXELS = None

COEFFICIENT_X_HQ = 0.548175
COEFFICIENT_Y_HQ = 0.513569

PICTURE_WIDTH = 2330
PICTURE_HEIGHT = 3430

HQ_RESOLUTION = (10192, 14039)
LIGHTWEIGHT_RESOLUTION = (5096,7019)

DIRECTORY_INPUT='/home/luciana/Documentos/luciana/utn/picture-splitter/fotos-cropper/todas/*.png'
DIRECTORY_OUTPUT='/home/luciana/Documentos/luciana/utn/picture-splitter/fotos-cropper/test/'

check_if_directories_exist()


i=0
log_start_end("Begins process for directory "+ DIRECTORY_INPUT)
files = glob.glob(DIRECTORY_INPUT)
dir_length = len(files)

for image_file in files:
    counter=1

    try:
        loop_time = datetime.now()

        i+=1
        scanned_image = Image.open(image_file)
        filename = os.path.splitext(os.path.basename(image_file))
        filename_w_extension = filename[0]+filename[1]
        filename_without_extension = filename[0]
        
        log_info(i,filename_w_extension,"Processing %d from %s files" % (i,dir_length))
        log_info(i,filename_w_extension, "Begins process for file: " + filename_w_extension)

        if scanned_image.size == HQ_RESOLUTION:
            log_info(i,filename_w_extension,"Image has HQ resolution: " + str(scanned_image.size))
            log_info(i,filename_w_extension, "Resizing image to resolution " + str(LIGHTWEIGHT_RESOLUTION[0]) +"X"+str(LIGHTWEIGHT_RESOLUTION[1]))
            scanned_image = scanned_image.resize(LIGHTWEIGHT_RESOLUTION)
            log_info(i,filename_w_extension,"Image is resized. Current size: "+str(scanned_image.size))

        elif scanned_image.size == LIGHTWEIGHT_RESOLUTION:
            log_info(i,filename_w_extension,"Image has lightweight resolution: " + str(scanned_image.size))
        else:
            log_error(i,filename_w_extension,"IMAGEN CON RESOLUCION DESCONOCIDA")
            continue

        #The crop rectangle, as a (left, upper, right, lower)-tuple.
        pic_1 = scanned_image.crop((0,0,PICTURE_WIDTH,PICTURE_HEIGHT))
        
        saved_as = save_picture(pic_1, last_filename_index)
        log_info(i,filename_w_extension, str(counter) + ": Cropped image saved as " + saved_as)
        last_filename_index+=1
        counter+=1

        pic_2 = scanned_image.crop((0,LIGHTWEIGHT_RESOLUTION[1]-PICTURE_HEIGHT,PICTURE_WIDTH,LIGHTWEIGHT_RESOLUTION[1]))
        
        saved_as = save_picture(pic_2, last_filename_index)
        log_info(i,filename_w_extension, str(counter) + ": Cropped image saved as " + saved_as)
        last_filename_index+=1
        counter+=1

        pic_3 = scanned_image.crop((LIGHTWEIGHT_RESOLUTION[0]-PICTURE_WIDTH,0,LIGHTWEIGHT_RESOLUTION[0],PICTURE_HEIGHT))
                                
        saved_as = save_picture(pic_3, last_filename_index)
        log_info(i,filename_w_extension, str(counter) + ": Cropped image saved as " + saved_as)
        last_filename_index+=1
        counter+=1

        pic_4 = scanned_image.crop((LIGHTWEIGHT_RESOLUTION[0]-PICTURE_WIDTH,LIGHTWEIGHT_RESOLUTION[1]-PICTURE_HEIGHT,LIGHTWEIGHT_RESOLUTION[0],LIGHTWEIGHT_RESOLUTION[1]))

        saved_as = save_picture(pic_4, last_filename_index)
        log_info(i,filename_w_extension, str(counter) + ": Cropped image saved as " + saved_as)
        last_filename_index+=1
         
        log_timer(i, filename_w_extension,"Process time : " + str(datetime.now() - loop_time))
        log_timer(i,filename_w_extension,"Total time: " + str(datetime.now()-startTime))
    except Exception as e:
        log_error(i,filename_w_extension,str(e))

log_start_end("End of process: " + str(last_filename_index-start_filename_index) + " pictures were created in output directory: " + DIRECTORY_OUTPUT )
log_start_end("Total time: "+str(datetime.now() - startTime))
log_start_end("*********** LAST FILENAME INDEX: " + str(last_filename_index) + " ***********")
