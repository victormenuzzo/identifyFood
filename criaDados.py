# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage import segmentation as seg
from skimage.feature import greycomatrix, greycoprops
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
import mahotas as mt
from skimage import color
from skimage import img_as_ubyte

def texture(image, labels, fundo, prato, alimento, matriz):
    gray = color.rgb2gray(image)

    gray = img_as_ubyte(gray)
    pixelVisitado=[]
    novaImg = np.zeros((80, 80), dtype=np.uint8)
    valorD = []
    valorC = []
    for i in range(600):
        for j in range(800):
            if(labels[i][j] not in pixelVisitado):
                for k in range(4):
                    for l in range(4):
                        if(i+k < 600 and j+l<800):
                            novaImg[k][l] = gray[i+k][j+l]
                        elif(i-k>0 and j+l<800):
                            novaImg[k][l] = gray[i-k][j+l]
                        elif(i+k>800 and j-l>0):
                            novaImg[k][l] = gray[i+k][j-l]
                        else:
                            novaImg[k][l] = gray[i-k][j-l]
                glcm = greycomatrix(novaImg, [5], [0], 256, symmetric=True, normed=True)
                valorD.append(greycoprops(glcm, 'dissimilarity')[0, 0])
                valorC.append(greycoprops(glcm, 'correlation')[0, 0])
                pixelVisitado.append(labels[i][j])

    for (i, segVal) in enumerate(np.unique(labels)):
        if segVal in fundo:
            #print("fundo")
            matriz[i][3] = valorD[i]
        elif segVal in prato:
            matriz[i][3] = valorD[i]
        else:
            matriz[i][3] = valorD[i]

def mean_color(image, labels, fundo, prato, alimento, matriz):
    for (i, segVal) in enumerate(np.unique(labels)):
        if segVal in fundo:
            #print("fundo")
            valorRGB = np.mean(image[segVal == labels], axis=0)
            matriz[i][0] = valorRGB[2]
            matriz[i][1] = valorRGB[1]
            matriz[i][2] = valorRGB[0]
            matriz[i][4] = 1
        elif segVal in prato:
            #print("prato")
            valorRGB = np.mean(image[segVal == labels], axis=0)
            matriz[i][0] = valorRGB[2]
            matriz[i][1] = valorRGB[1]
            matriz[i][2] = valorRGB[0]
            matriz[i][4] = 2
        elif segVal in alimento:
            #print("Alimento")
            valorRGB = np.mean(image[segVal == labels], axis=0)
            matriz[i][0] = valorRGB[2]
            matriz[i][1] = valorRGB[1]
            matriz[i][2] = valorRGB[0]
            matriz[i][4] = 6#lembrar de trocar essa linha pelo valor do alimento
        else:
         	print('ERRO NO TESTE %d DA BASE DE DADOS' % (segVal))
    return matriz

def slic_segmentation(img, ns, fundo, prato, alimento):
    labels = slic(img, n_segments=ns)
    #print(labels)
    matriz = np.zeros((len(np.unique(labels)), 5), dtype=np.float64)
    mean_color(img, labels, fundo, prato, alimento, matriz)
    texture(img, labels, fundo, prato, alimento, matriz)
    return matriz

# load the image and apply SLIC and extract (approximately)
# the supplied number of segments
image = cv2.imread('alimentos1.jpg')
image = cv2.resize(image,(800,600))

#alface 1
fundo = [0, 1, 2, 3, 4, 7, 10, 15, 16, 19, 21, 23, 25, 27, 28]
prato = [5, 6, 8, 9, 11, 12, 13, 18, 20, 22, 24, 26]
alimento = [14, 17]
retorno = slic_segmentation(image, 40, fundo, prato, alimento)
#a = np.round(retorno, 4)
#print(a)

for i in range(len(retorno)):
		print("[%f, %f, %f, %f, %d]" % (retorno[i][0], retorno[i][1], retorno[i][2], retorno[i][3], int(retorno[i][4])))
	#		(round(retorno[i][0],4),round(retorno[i][1],4),round(retorno[i][2],4),round(retorno[i][3],4),round(retorno[i][4],4))

