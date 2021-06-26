'''
buff_reader.py

Author: Ian Harvey

Date: 06/26/2021

Description:
	Reads smeeta charm buffs from Warframe while in mission and keeps track of multiple charm buffs stacking at once.

	Bounding area of the buffs was manually calculated to my screen. Warframe hud is not straight so I crop, rotate,
	and then crop again to get the line of buff numbers if they exist and then split up that image into seperate
	potential numbers to detect with pytesseract which is a wrapper to a Google cv api. If I get a plausible
	affinity buff number back I added it to the list of buffs and keep tabs on it.

Usage:
	Configured for a 1920 x 1080 resolution with default Warframe hud settings.

	You need to pip install the modules below.

	Ran on python 3.7.
'''

import os
import cv2
import time
import numpy as np
from PIL import ImageGrab, ImageOps
import pytesseract

last_buff_time = 0.0
buff_recognition_cooldown = 20
l_bound = 134
u_bound = 156
buffs = []

while(True):

	# get screengrab and convert to np array
	screenshot_time = time.time()
	img = ImageGrab.grab(bbox=(990,57,1730,117))
	img = np.array(img.getdata(),dtype='uint8').reshape((img.size[1],img.size[0],3))

	# rotate image
	dim = ((1730-990),(117-57))
	center = ((1730-990)/2,(117-57)/2)
	mat = cv2.getRotationMatrix2D(center, -3.09405806, 1.0)
	rot_img = cv2.warpAffine(img, mat, dim)

	# crop rotated image
	crop_img = rot_img[20:40,35:740]

	# switch color back to correct
	crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)

	# sharpen image with filter
	_filter = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
	crop_img = cv2.filter2D(crop_img,-1,_filter)

	# crop into seperate potential buff images
	images = []
	for i in range(15):
		prev = i
		cur = i+1
		tmp = crop_img[0:20,prev*47:cur*47]
		images.append(tmp)

	# pass sharpened image to google to see if they can read numbers
	pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
	for image in images:
		crop_send_time = time.time()
		text = pytesseract.image_to_string(image)

		# they return a list of chars... thanks turn to string
		tmp = ''
		for i in text:
			tmp += i
		
		# we have a string that represents lines now... 
		tmp2 = tmp.split('\n')
		tmp2 = [x.strip() for x in tmp2]

		# finally back to sanity
		text = tmp2

		# go thru text looking for biiiig number aka smeeta buff timer
		for line in text:
			try:
				num = float(line.strip())

				# check if buff could be new
				if(num > l_bound and num <= u_bound and (screenshot_time - last_buff_time) > buff_recognition_cooldown):
					# record expiry time
					last_buff_time = screenshot_time
					buffs.append(screenshot_time + num - (crop_send_time - screenshot_time))
			except Exception as e:
				continue

	# done processing print out updated buff status list
	os.system('cls')
	print('Affinity buff tracker:')
	buff_count = 0
	for buff in list(buffs):
		if(buff < time.time()):
			buffs.remove(buff)
			continue

		buff_count += 1
		print('\tBuff %i: %.1f' % (buff_count, buff - time.time()))

