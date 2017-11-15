import time
import numpy as np
import imageio
from itertools import *
np.set_printoptions(threshold=np.inf)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)	

imMap = imageio.imread('assets/240RGB.png') #imMap = np.int_(imMap)
imDraw = imageio.imread('assets/transparent_colors.png')

maMap = np.ma.masked_where(imMap > 240, imMap, False)#Mask the Map and the Draw Canvas
maDraw = np.ma.masked_where(np.ma.getmask(maMap), imDraw, False)#False to not return a copy but work in place

maMapDraw = np.ma.concatenate((maMap[:,:,[0]], maDraw), axis=2)#remove any additional g & b information but keep dimensionality

compMapDraw = maMapDraw.compressed()#remove masked values
iterCMP = grouper(4, compMapDraw, 0)#turn into iterable chunks
for data in iterCMP:
	print "id: {0} r: {1} g: {2} b: {3}".format(data[0], data[1], data[2], data[3])

