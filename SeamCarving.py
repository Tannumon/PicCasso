# CS3100 - Fall 2023 - Programming Assignment 4
#################################
# Collaboration Policy: You may discuss the problem and the overall
# strategy with up to 4 other students, but you MUST list those people
# in your submission under collaborators.  You may NOT share code,
# look at others' code, or help others debug their code.  Please read
# the syllabus carefully around coding.  Do not seek published or online
# solutions for any assignments. If you use any published or online resources
# (which may not include solutions) when completing this assignment, be sure to
# cite them. Do not submit a solution that you are unable to explain orally to a
# member of the course staff.
#################################
# Your Computing ID: ebh2cd
# Collaborators: 
# Sources: Introduction to Algorithms, Cormen
#################################


class SeamCarving:
    def __init__(self):
        self.seam = []
        return

    # This method is the one you should implement.  It will be called to perform
    # the seam carving.  You may create any additional data structures as fields
    # in this class or write any additional methods you need.
    # 
    # @return the seam's weight 
    def compute(self, image):
        rows, cols = len(image), len(image[0])
        weightmatrix = [([(-1)] * (cols)) for i in range(rows)]
                
        for pxl in range(cols):
            weightmatrix[rows-1][pxl] = self.energyValue(image, pxl, (rows-1))
                        
        for r in range(rows-2, -1, -1):
            for c in range(cols):
                weightmatrix[r][c] = self.energyValue(image, c, r)    
                if c == 0:
                    weightmatrix[r][c] += min(weightmatrix[r + 1][c], weightmatrix[r + 1][c + 1])
                elif c == (cols-1):
                    weightmatrix[r][c] += min(weightmatrix[r + 1][c - 1], weightmatrix[r + 1][c])
                else:
                    weightmatrix[r][c] += min(weightmatrix[r + 1][c - 1], weightmatrix[r + 1][c], weightmatrix[r + 1][c + 1])      
        
        
        toprowmincol = weightmatrix[0].index(min(weightmatrix[0]))

        self.seam.append(toprowmincol)
        for ro in range(1, rows):
            arr = []
            for idx in range(-1, 2):
                if (0 <= idx + toprowmincol < cols):
                    arr.append(weightmatrix[ro][idx + toprowmincol])
            if len(arr) == arr.count(0):
                self.seam.append(toprowmincol)
            else:   
                toprowmincol += (arr.index(min(arr)) - 1)
                self.seam.append(toprowmincol)
                
        return min(weightmatrix[0])

    # Get the seam, in order from top to bottom, where the top-left corner of the
    # image is denoted (0,0).
    # 
    # Since the y-coordinate (row) is determined by the order, only return the x-coordinate
    # 
    # @return the ordered list of x-coordinates (column number) of each pixel in the seam
    # as an array

    def getSeam(self):
        return self.seam
    
    def euclidDistance(self, image, col, row, col2, row2):
        return (((image[row2][col2][0] - image[row][col][0]) ** 2) + ((image[row2][col2][1] - image[row][col][1]) ** 2) + ((image[row2][col2][2] - image[row][col][2]) ** 2)) ** 0.5

    def energyValue(self, img, col, row):
        totalenergy = 0
        adj = 0
        for j in range(-1, 2):
            for i in range(-1, 2):
                if (0 <= row + j < len(img)) and (0 <= col + i < len(img[0])):
                    totalenergy += self.euclidDistance(img, col, row, (col + i), (row + j))
                    adj += 1
        return (totalenergy/(adj - 1))