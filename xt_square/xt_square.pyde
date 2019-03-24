
def setup():
    global blackPixels
    size(800, 800)
    colorMode(HSB)
    strokeWeight(3)
    blackPixels = getOutsiders(8)
    

def rainbowX(outside):
    """Makes a rainbow gradient X"""
    outside = int(outside)
    strokeWeight(3)
    noFill()
    colorMode(HSB)
    if outside <= width:
        coords = range(outside+1)
    else:
        coords = range(outside - width, width)
    for i in coords:
        h = (outside - i) * 256.0 / width
        stroke(h, 255, 255)
        line(width, height, i, 0)
        line(width, height, 0, i)

def fillFractal():
    for i in range(width+1):
        for j in range(height+1):
            if sq(i - width/2) + sq(j - height/2) > sq(height/2):
                strokeWeight(2)
                stroke(0)
                point(i, j)

# Square: x1, y1, x2, y2...
# In this way, a square is also a vector, representing its direction.
             
def nextSquares(square):
    x1, y1, x2, y2 = square
    
    xc = 0.5 * (x1 + x2)
    yc = 0.5 * (y1 + y2)
    
    xv = x2 - x1
    yv = y2 - y1
    
    a = (xc + 0.25*yv, yc - 0.25*xv, xc + 0.75*yv, yc - 0.75*xv)
    b = (xc + 0.25*xv, yc + 0.25*yv, xc + 0.75*xv, yc + 0.75*yv)
    c = (xc - 0.25*yv, yc + 0.25*xv, xc - 0.75*yv, yc + 0.75*xv)
    
    return [a, b, c]


def iterateSquares(square, square_list, order):
    square_list.append(square)
    if order > 0:
        for sq in nextSquares(square):
            iterateSquares(sq, square_list, order-1)

def getTsquareList(order):
    square = (0.25*width, 0.25*height, 0.75*width, 0.75*height)
    square1 = (0.375*width, 0.375*height, 0.125*width, 0.125*height)
    square_list = []
    iterateSquares(square, square_list, order)
    iterateSquares(square1, square_list, order-1)
    return square_list

def pointInSquare(pt, square):
    x1, x2 = sorted([square[0], square[2]])
    y1, y2 = sorted([square[1], square[3]])
    return x1 <= pt[0] <= x2 and y1 <= pt[1] <= y2


def getOutsiders(order):
    square_list = getTsquareList(order)
    outsiders = set([(i, j) for i in range(2*width) for j in range(2*height)])
    for square in square_list:
        x1, x2 = sorted([2*square[0], 2*square[2]])
        y1, y2 = sorted([2*square[1], 2*square[3]])
        for i in range(ceil(x1), floor(x2)+1):
            for j in range(ceil(y1), floor(y2)+1):
                if (i, j) in outsiders:
                    outsiders.remove((i, j))
    return [(0.5*x, 0.5*y) for (x, y) in outsiders]


def drawRainbowX(outside):
    pushMatrix()
    scale(0.5)
    for angle in [0, PI/2, PI, 3*PI/2]:
        pushMatrix()
        
        translate(width, height)
        rotate(angle)
        rainbowX(outside)
        popMatrix()
    popMatrix()

def draw():
    global blackPixels
    background(0)
    N = width/2
    COUNT = 250
    frame = frameCount-1
    #rainbowX(width)
    drawRainbowX((width-1) * (1 + sin(-PI/2 + TWO_PI*frame/COUNT)))
    
    stroke(0)
    strokeWeight(1)
    for i, j in blackPixels:
        point(i, j)

    if frameCount <= COUNT:
        print("Frame {} out of {}".format(frameCount, COUNT))
        saveFrame("frames//###.png")
