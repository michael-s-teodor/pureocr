#### Libraries
# Own libraries
from essentials import Essentials
# Third-party libraries
import cv2

#### Class
class Preprocessor():

    def __init__(self, file):

        # Import a sample image also 0 is for grey scale and store its properties
        self.file = file
        self.original_img = cv2.imread(file, 0) 
        self.processed_img = cv2.imread(file, 0) 
        self.img = cv2.imread(file, 0) 

        self.height, self.width = self.img.shape[0], self.img.shape[1]
        self.threshold = -1

        self.char_anchors = []      # [x_min, y_min, x_max, y_max]
        self.char_anchors_rows = [] # [x_min, y_min, x_max, y_max]
        self.data = []              # Contains copies of charachters row/char

    def process_image(self):
        self.threshold = get_threshold(self.height, self.width, self.img)
        self.char_anchors = find_letters(self.height, self.width, self.threshold, self.img)
        Essentials().wham_sort_by(len(self.char_anchors), self.char_anchors, 1)
        self.char_anchors_rows = recognise_lines(self.char_anchors)
        self.char_anchors_rows = sort_letters_in_order(self.char_anchors_rows)
        self.char_anchors_rows = merge_neighbours(self.char_anchors_rows)

    def preview_image(self):
        draw_boxes_lines(self.char_anchors_rows, self.processed_img)
        while True:
            cv2.imshow("Preview (Press q to close)", self.processed_img)
            key = cv2.waitKey(0) & 0xFF

            # If the q key was pressed, break from the loop
            if key == ord("q"):
                break
            cv2.destroyAllWindows()

    def convert_to_binary(self):
        if (self.threshold == -1):
            self.threshold = get_threshold(self.height, self.width, self.img)
        self.processed_img = convert_to_binary_img(self.height, self.width, self.threshold, self.processed_img)
        return self.processed_img

#### Functions
def get_threshold(height, width, img):
    avg = 0
    for i in range(height):
        for j in range(width):
           avg += img[i][j]
    avg /= height*width
    return 0.75*avg        

def convert_to_binary_img(height, width, threshold, img):
    for i in range(height):
        for j in range(width):
            if( img[i][j] > threshold):
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img

def find_letters(height, width, threshold, img):
    anchors = []
    for i in range(height):
        for j in range(width):
            if (img[i][j] < threshold):

                # Map letter
                temp_arr = [j, i, j, i]
                temp_arr = map_letter(j, i, temp_arr, threshold, height, width, img)

                # Store anchors
                anchors.append(temp_arr)
    return anchors

def map_letter(x, y, temp_arr, threshold, height, width, img):
    if (x < 0 or x >= width or y < 0 or y >= height):
        return temp_arr

    if (img[y][x] < threshold):

        # Delete so that we dont encounter it again
        img[y][x] = -1

        # Find min x and y and max x and y
        if (x < temp_arr[0]):
            temp_arr[0] = x 
        if (y < temp_arr[1]):
            temp_arr[1] = y
        if (x > temp_arr[2]):
            temp_arr[2] = x
        if (y > temp_arr[3]):
            temp_arr[3] = y

        for n in range(-1,2):
            for m in range(-1,2):
                if not (n == 0 and m == 0):
                    temp_arr = map_letter(x+n, y+m, temp_arr, threshold, height, width, img)
                
    return temp_arr

def draw_boxes_lines(anchors_rows, img):

    # Draw boxes around letters in rows with the same colour and alternate
    for row in range(len(anchors_rows)):
        img = draw_boxes(anchors_rows[row], row%2*100,img)

def draw_boxes(arr, colour, img):
    for letter in range(len(arr)):
        min_x = arr[letter][0]
        min_y = arr[letter][1]
        max_x = arr[letter][2]
        max_y = arr[letter][3]
        for i in range(min_x, max_x+1):
            img[min_y][i] = colour
            img[max_y][i] = colour
        for j in range(min_y, max_y+1):
            img[j][min_x] = colour
            img[j][max_x] = colour
    return img

def recognise_lines(char_anchors):
    char_anchors_rows = []
    row = 0
    total = (char_anchors[0][1] + char_anchors[0][3])/2
    n = 1
    char_anchors_rows.append([])

    deviation = 20 # NOTE: needs to be adjusted so that its adaptive

    for i in range(len(char_anchors)):
        avg = total/n

        # Calculate middle y
        y = (char_anchors[i][1] + char_anchors[i][3])/2

        if (y < avg + deviation and y > avg - deviation):
            total += y
            char_anchors_rows[row].append(char_anchors[i])
        else:
            row += 1
            n = 0
            total = y     
            char_anchors_rows.append([])
            char_anchors_rows[row].append(char_anchors[i])
        n+=1
    return char_anchors_rows

def sort_letters_in_order(char_anchors_rows):
    for row in range(len(char_anchors_rows)):

        # Sort by x
        Essentials().wham_sort_by(len(char_anchors_rows[row]), char_anchors_rows[row], 0)
    return char_anchors_rows

def merge_neighbours(char_anchors_rows):
    for row in range(len(char_anchors_rows)):
        length = len(char_anchors_rows[row])-1
        for char in range(length):
            if (char+1 < length):
                c1 = char_anchors_rows[row][char]
                c2 = char_anchors_rows[row][char+1]

                # Check if theyre on top of each other
                if (c1[1] >= c2[3] or c1[3] <= c2[1]):

                    # Check if their x's intersect
                    if( c2[0] <= c1[2] ):
                        char_anchors_rows[row][char][0] = min(c1[0],c2[0])
                        char_anchors_rows[row][char][1] = min(c1[1],c2[1])
                        char_anchors_rows[row][char][2] = max(c1[2],c2[2])
                        char_anchors_rows[row][char][3] = max(c1[3],c2[3])
                        char_anchors_rows[row].remove(c2)
                        length -=1            
    return char_anchors_rows