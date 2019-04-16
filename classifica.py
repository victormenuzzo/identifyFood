import csv
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
from sklearn.neighbors import KNeighborsClassifier
from skimage import color
from skimage import img_as_ubyte
import warnings
warnings.filterwarnings("ignore")

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

def extraiFeatures(image, labels, vetor):
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
                pixelVisitado.append(labels[i][j])

    resp = []
    for (i, segVal) in enumerate(np.unique(labels)):
            valorRGB = np.mean(image[segVal == labels], axis=0)
            resp.append(int(modelo.predict([[valorRGB[2], valorRGB[1], valorRGB[0], valorD[i]]])))
    		#resp.append(modelo.predict([[64.492252,	 35.600200,	 50.440185,	 0.135500]]))
    return resp

def slic_segmentation(img, ns):
    labels = slic(img, n_segments=ns, sigma=2, enforce_connectivity=True)
    #print(labels)
    vetor = []
    resp = extraiFeatures(img, labels, vetor)
    return resp

with open("baseDeDados.csv") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    dados=[]

    for r in reader:
    	dados.append(r)

tamanhoBD = len(dados)

features = np.zeros((tamanhoBD, 4),dtype=np.float64)
classificacao = []

for i in range(tamanhoBD):
	features[i][0] = float(dados[i][0])
	features[i][1] = float(dados[i][1])
	features[i][2] = float(dados[i][2])
	features[i][3] = float(dados[i][3])

for i in range(tamanhoBD):
	classificacao.append(float(dados[i][4]))

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(features, classificacao)

image = cv2.imread('teste3.jpg')
image = cv2.resize(image,(800,600))

retorno = slic_segmentation(image, 200)

retorno = set(retorno)

for r in retorno:
	if r==3:
		print('Alface')
	elif r==4:
		print('Cenoura')
	elif r==5:
		print('Beterraba')

