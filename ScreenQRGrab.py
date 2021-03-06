#!/usr/bin/python
# Author Dario Clavijo 2017
# GPLv3

import sys
import zbar
import Image
import time
import pyscreenshot as ImageGrab


fp = open(sys.argv[1],'rw+')


def scan_file(filename):
	pil = Image.open(filename).convert('L')
	return scan_image(pil)

def scan_image(pil):
	ret = []
	# create a reader
	scanner = zbar.ImageScanner()

	# configure the reader
	scanner.parse_config('enable')

  	width, height = pil.size

	#print width,height

        raw = pil.tobytes()

	#fp = open('/home/dclavijo/raw','w+')
	#fp.write(raw)
	#fp.close

        # wrap image data
        image = zbar.Image(width, height, 'Y800', raw)

	#print image

	# scan the image for barcodes
	scanner.scan(image)

	# extract results
	for symbol in image:
	    # do something useful with results
	    ret.append((symbol.type, symbol.data))
	    #print symbol

	# clean up
	del(image)
	return ret


def loadfile(fp):
	data = []
	for line in fp:
		data.append(line.rstrip().decode('hex'))
	return data

def screen_grab(col,fp):
	while True:
		time.sleep(0.5)
	    	#t = str(time.time()).replace('.','-')
	    	#tt = time.time(
		img=ImageGrab.grab().convert('L')
	    	#img = img.resize((800,600))
	    	#img.save(''.join(['img\\',t,'.png']))
	    	#print time.time() - tt
		ret = scan_image(img)
		if ret is not None and len(ret) > 0:
			for i in ret:

				if len(i) >1 and  i[1] not in col:
					print i[0],i[1]
					col.append(i[1])
					fp.write(i[1].encode('hex')+"\n")
		fp.flush()


data = loadfile(fp)
screen_grab(data,fp)
fp.close()
