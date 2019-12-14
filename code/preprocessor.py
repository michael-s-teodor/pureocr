
import cv2 #import the image processing 

class PreProcessor():

    def __init__(self,file):
    #import a sample image also 0 is for grey scale and store its properties
        self.file = file
        self.original_img = cv2.imread(file,0) 
        self.processed_img = cv2.imread(file,0) 
        self.img = cv2.imread(file,0) 

        self.height, self.width = self.img.shape[0], self.img.shape[1]
        self.threshold = -1

        self.charAnchors = [] # [x_min,y_min,x_max,y_max]
        self.charAnchorsRows = [] # [x_min,y_min,x_max,y_max]
        self.data = [] #contains copies of charachters row/char

    def processImage(self):
        self.threshold = getThreshold(self.height,self.width,self.img)
        self.charAnchors = findLetters(self.height,self.width,self.threshold,self.img)
        self.charAnchors = bubbleSort(self.charAnchors,1)
        self.charAnchorsRows = recogniseLines(self.charAnchors)
        self.charAnchorsRows = sortLettersInOrder(self.charAnchorsRows)
        self.charAnchorsRows = mergeNeighbours(self.charAnchorsRows)

    def previewImg(self):
        drawBoxesLines(self.charAnchorsRows,self.processed_img)
        while True:
            cv2.imshow("Preview (Press c to close)", self.processed_img)
            key = cv2.waitKey(0) & 0xFF
            # if the q key was pressed, break from the loop
            if key == ord("c"):
                break
            cv2.destroyAllWindows()

    def convertToBinary(self):
        if(self.threshold == -1):
            self.threshold = getThreshold(self.height,self.width,self.img)
        self.processed_img = convertToBinaryImg(self.height,self.width,self.threshold,self.processed_img)
        return self.processed_img

#===============================================================================================

def getThreshold(height,width,img):
    avg = 0
    for i in range(height):
        for j in range(width):
           avg += img[i][j]
    avg /= height*width
    return 0.75*avg        

def convertToBinaryImg(height,width,threshold,img):
    for i in range(height):
        for j in range(width):
            if( img[i][j] > threshold):
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img

def findLetters(height,width,threshold,img):
    anchors = []
    for i in range(height):
        for j in range(width):
            if( img[i][j] < threshold ):
                #map letter
                tempArr = [j,i,j,i]
                tempArr = mapLetter(j,i,tempArr,threshold,height,width,img)
                #store anchors
                anchors.append(tempArr)
    return anchors

def mapLetter(x,y,tempArr,threshold,height,width,img):
    if ( x < 0 or x >= width ) or ( y < 0 or y >= height ):
        return tempArr
        
    if( img[y][x] < threshold ):

        #delete so that we dont encounter it again
        img[y][x] = -1
        
        #find min x and y and max x and y
        if( x < tempArr[0] ):
            tempArr[0] = x 
        if( y < tempArr[1] ):
            tempArr[1] = y
        if( x > tempArr[2] ):
            tempArr[2] = x
        if( y > tempArr[3] ):
            tempArr[3] = y

        for n in range(-1,2):
            for m in range(-1,2):
                if not( n == 0 and m == 0 ):
                    tempArr = mapLetter(x+n,y+m,tempArr,threshold,height,width,img)
                
    return tempArr

def drawBoxesLines(anchorsRows,img):
    #draw boxes around letters in rows with the same colour and alternate
    for row in range(len(anchorsRows)):
        img = drawBoxes(anchorsRows[row], row%2*100,img)

def drawBoxes(arr,colour,img):
    for letter in range(len(arr)):
        minX = arr[letter][0]
        minY = arr[letter][1]
        maxX = arr[letter][2]
        maxY = arr[letter][3]
        for i in range(minX,maxX+1):
            img[minY][i] = colour
            img[maxY][i] = colour
        for j in range(minY,maxY+1):
            img[j][minX] = colour
            img[j][maxX] = colour
    return img

def recogniseLines(charAnchors):
    charAnchorsRows = []
    row = 0
    total = (charAnchors[0][1]+charAnchors[0][3])/2
    n = 1
    charAnchorsRows.append([])

    deviation = 20 #NOTE: needs to be adjusted so that its adaptive

    for i in range(len(charAnchors)):
        avg = total/n

        #calculate middle y
        y = (charAnchors[i][1] + charAnchors[i][3])/2

        if( y < avg + deviation and y > avg - deviation):
            total += y
            charAnchorsRows[row].append(charAnchors[i])
        else:
            row += 1
            n = 0
            total = y     
            charAnchorsRows.append([])
            charAnchorsRows[row].append(charAnchors[i])

        n+=1
    return charAnchorsRows

def bubbleSort(arr,by):
    length = len(arr)
    for i in range(length-1):
        for j in range(length-1):
            if( arr[j][by] > arr[j+1][by] ):
                temp = arr[j+1]
                arr[j+1] = arr[j]
                arr[j] = temp
    return arr

def sortLettersInOrder(charAnchorsRows):
    for row in range(len(charAnchorsRows)):
        #Sort by x
        charAnchorsRows[row] = bubbleSort(charAnchorsRows[row], 0)
    return charAnchorsRows

def mergeNeighbours(charAnchorsRows):

    for row in range(len(charAnchorsRows)):
        length = len(charAnchorsRows[row])-1
        for char in range(length):
            if(char + 1 < length ):
                c1 = charAnchorsRows[row][char]
                c2 = charAnchorsRows[row][char+1]
                #check if theyre on top of each other
                if( c1[1] >= c2[3] or c1[3] <= c2[1] ):
                    #check if their x's are intersecting
                    if( c2[0] <= c1[2] ):

                        charAnchorsRows[row][char][0] = min(c1[0],c2[0])
                        charAnchorsRows[row][char][1] = min(c1[1],c2[1])
                        charAnchorsRows[row][char][2] = max(c1[2],c2[2])
                        charAnchorsRows[row][char][3] = max(c1[3],c2[3])

                        charAnchorsRows[row].remove(c2)
                        length -=1

    return charAnchorsRows