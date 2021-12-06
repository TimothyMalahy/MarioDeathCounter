import cv2 as cv
import numpy as np
from pathlib import Path
import pyautogui
from time import sleep

'''
The intent behind this file is to use image recognition to automatically count up when an event occurs
'''

def countup():
    game = 'MarioIsMissing' # This will help to make a specific file for a specific game to promote abstraction in the code

    myfile = Path( game + '.txt') # assigns the variable myfile to gamefilename.txt


    myfile.touch(exist_ok=True) # If it already exists, don't do anything, else create it.
    f = open(myfile, 'r') # Open the file for reading purposes.

    try:
        filevalue = f.readlines()[0] # Reads the first line's value. The file should only have 1 value in it anyway.
    except IndexError:
        filevalue = 0 # If the file is empty, which it would be if it was just created

    f.close() # close the file

    try:
        oldvalue = int(filevalue)
    except ValueError as e:
        print('there is not a number on the file')
        exit()

    newvalue = oldvalue + 1

    f = open(myfile, 'w')
    f.write(str(newvalue))
    f.close()

    sleep(10) # Wait 10 seconds because the game cannot re-gameover in the next 10 seconds.
    return
    



def Scan():
    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #         'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    while True:
        SCREEN_SIZE = (1275, 1348)
        snes = pyautogui.screenshot(region=(1277, 55, 1275, 1348))
        frame = np.array(snes)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #cv.imshow("frame_gray", frame_gray)
        gameover_img = cv.imread("gameover.jpg", cv.IMREAD_UNCHANGED)
        gameover_img_gray = cv.cvtColor(gameover_img, cv.COLOR_BGR2GRAY)
        cv.imshow('gameover_gray', gameover_img_gray)
        w = gameover_img_gray.shape[1]
        h = gameover_img_gray.shape[0]
        
        result = cv.matchTemplate(gameover_img_gray, frame_gray, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        threshold = .90
        
        if max_val >= threshold:
            countup()
        
        
        yloc, xloc = np.where(result >= threshold)
        for (x, y) in zip(xloc, yloc):
            cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,255), 2)
        
        
        if cv.waitKey(1) == ord("q"):
            break
        
        
    



    # if amount_found != 0:
    #     for (x, y, width, height) in found:
    #         cv.rectangle(img_rgb, (x, y),
    #         (x + height, y+width),
    #         (0, 255, 0), 5)

    # plt.subplot(1, 1, 1)
    # plt.imshow(img_rgb)
    # plt.show()

Scan()

cv.destroyAllWindows()