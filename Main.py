import sys
from PIL import Image
import numpy as np
import math

fp = Image.open("ducks.jpg").convert('RGBA')
pixels = fp.load()
w, h = fp.size
image_data = [[[0 for k in range(3)] for j in range(w)] for i in range(h)]
for i in range(w):
    for j in range(h):  
        image_data[j][i][0] = pixels[i, j][0]
        image_data[j][i][1] = pixels[i, j][1]
        image_data[j][i][2] = pixels[i, j][2]   


# Functions to compute the seam
def compute(image):
    global seam
    seam = [] 
    rows, cols = len(image), len(image[0])
    weightmatrix = [([(-1)] * (cols)) for i in range(rows)]
            
    for pxl in range(cols):
        weightmatrix[rows-1][pxl] = energyValue(image, pxl, (rows-1))
                    
    for r in range(rows-2, -1, -1):
        for c in range(cols):
            weightmatrix[r][c] = energyValue(image, c, r)    
            if c == 0:
                weightmatrix[r][c] += min(weightmatrix[r + 1][c], weightmatrix[r + 1][c + 1])
            elif c == (cols-1):
                weightmatrix[r][c] += min(weightmatrix[r + 1][c - 1], weightmatrix[r + 1][c])
            else:
                weightmatrix[r][c] += min(weightmatrix[r + 1][c - 1], weightmatrix[r + 1][c], weightmatrix[r + 1][c + 1])      
    
    
    toprowmincol = weightmatrix[0].index(min(weightmatrix[0]))

    seam.append(toprowmincol)
    for ro in range(1, rows):
        arr = []
        for idx in range(-1, 2):
            if (0 <= idx + toprowmincol < cols):
                arr.append(weightmatrix[ro][idx + toprowmincol])
        if len(arr) == arr.count(0):
            seam.append(toprowmincol)
        else:   
            toprowmincol += (arr.index(min(arr)) - 1)
            seam.append(toprowmincol)


def euclidDistance(image, col, row, col2, row2):
    return (((image[row2][col2][0] - image[row][col][0]) ** 2) + ((image[row2][col2][1] - image[row][col][1]) ** 2) + ((image[row2][col2][2] - image[row][col][2]) ** 2)) ** 0.5

def energyValue(img, col, row):
    totalenergy = 0
    adj = 0
    for j in range(-1, 2):
        for i in range(-1, 2):
            if (0 <= row + j < len(img)) and (0 <= col + i < len(img[0])):
                totalenergy += euclidDistance(img, col, row, (col + i), (row + j))
                adj += 1
    return (totalenergy/(adj - 1))

perc = 101
while ((perc > 100) or (perc <= 0)):
    perc = int(input("enter the percent of image you want to remove"))

perc = math.floor((perc / 100) * w)


def deleting(times):
    for x in range(times):
        compute(image_data)
        for l in range(len(image_data)):
            del image_data[l][seam[l]]
        npImage = np.array(image_data)
        npImage = npImage.astype(np.uint8)
    
    return npImage


finalImage = deleting(perc)
img_edit = Image.fromarray(finalImage)
img_edit.show()
