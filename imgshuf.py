from PIL import Image
from PIL import ImageDraw
import random
import io
import os
from sys import argv

#TODO
# Make function to stitch the independant channels into a continuous bytes object representing the final image.
# stitchChannels should return a bytes object.

def stitchChannels(imgsize, r, g, b):
	finalImage = bytearray()
	print(len(r))
	print(len(g))
	print(len(b))
	for pixel in (range(0, (imgsize * imgsize))):
		finalImage.append(r[pixel])
		finalImage.append(g[pixel])
		finalImage.append(b[pixel])
	return bytes(finalImage)
	print(len(finalImage))


def rip_channel(n, byteobj):
	channel = bytearray()
	#print(byteobj)
	print ( "Lenght of byteobj in rip_channel: " + str(len(byteobj)) + " It should be a multiple of three")
	if (n == 1):
		for i in range(1, len(byteobj), 3):
			channel.append(byteobj[i])
	elif (n == 2):
		for i in range(2, len(byteobj), 3):
			channel.append(byteobj[i])
	elif (n == 3):
		for i in range(3, len(byteobj), 3):
			channel.append(byteobj[i])	
	return bytes(channel)


def get_channels(imgsize, args):
	#files = []
	chandata = []
	#print("getting channels")
	for i in args:
		print(i)
		with Image.open(i) as imgFile:
			print(type(imgFile))
			myImage = imgFile.resize((imgsize,imgsize))
			filex = io.BytesIO()
			myImage.save(filex, format='BMP')
			filex = filex.getvalue()
			chandata.append([rip_channel(1, filex), rip_channel(2, filex), rip_channel(3, filex)])
	#print(chandata)
	return chandata


def mixed_img(imgsize, *args):
	#print(args)
	chandata = get_channels(imgsize, args)
	data = []
	#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	#for image in args:
	#	with Image.open(image) as imgFile:
	#		print(type(imgFile))
	#		myImage = imgFile.resize((imgsize,imgsize))
	#		chandata.append([ bytes(imgFile.getdata(0)), bytes(imgFile.getdata(1)), bytes(imgFile.getdata(2)) ])
	#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	#for i in range(0, len(args)-1)
	data.append(stitchChannels(imgsize, chandata[0][0], chandata[1][1], chandata[2][2]))
	data.append(stitchChannels(imgsize, chandata[1][2], chandata[1][0], chandata[2][1]))
	data.append(stitchChannels(imgsize, chandata[1][1], chandata[1][2], chandata[2][0]))
	return data

def check_if_file(*args):
	for path in args:
		if ( not os.path.exists(path) ):
			raise ValueError("O caminho especificado " + str(path) + " , não existe.")
	return True

def getData(imgsize, img1, img2, img3):

	if ( len(argv) != 5):
		raise Exception("É necessário ao menos 4 argumentos. Você mandou " + str(len(argv) -1) + " argumentos.")
	
	if (check_if_file(img1, img2, img3)):
		#with PIL.Image.open(img1) as file:
		#	img1Data = file.read()
		#with PIL.Image.open(img2) as file:
		#	img2Data = file.read()
		#with PIL.Image.open(img3) as file:
		#	img3Data = file.read()
		imgData = mixed_img(imgsize, img1, img2, img3)
		#print(imgData[0][0])
		return imgData

	else:
		raise Exception("Caminhos/Arquivos inválidos ou inacessíveis. ")

def buildImages(imgsize, imgdata):
	#print(imgdata)
	for data in imgdata:
		image = Image.frombytes('RGB', (imgsize, imgsize), data)
		image.save(str(random.randrange(0,10000000)) + ".png")
	#image01D.bitmap((0,0), imgdata[0][0])
	#print(imgdata[0])
	#print(len(imgdata[0]))
	#image01.save('img01.bmp')

	

if __name__ == "__main__":
	buildImages(int(argv[1]) , getData(int(argv[1]) ,argv[2], argv[3], argv[4]))