def rainbowCircle(radius, outside):
    """Makes a rainbow gradient circle that expands out."""
    outside = int(outside % (2 * radius))
    strokeWeight(2)
    noFill()
    colorMode(HSB)
    if outside <= radius:
        radii = range(1, outside)
    else:
        radii = range(outside - radius, radius)
    for i in radii:
        h = (outside - i) * 255.0 / radius
        stroke(h, 255, 255)
        ellipse(0, 0, 2*i, 2*i)

def innerKochPoints(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    pa = (2*x1 + x2) / 3.0, (2*y1 + y2) / 3.0
    pc = (x1 + 2*x2) / 3.0, (y1 + 2*y2) / 3.0
    pb = (x1 + x2) / 2.0 - (y2 - y1) / (2 * sqrt(3)), (y1 + y2) / 2.0 + (x2 - x1) / (2 * sqrt(3))
    
    return [pa, pb, pc]

def kochCurve(order):
    
    def iterateCurve(curve, order):
        if order == 0:
            return curve
        new = []
        for i in range(len(curve)-1):
            new.append(curve[i])
            new.extend(innerKochPoints(curve[i], curve[i+1]))
        new.append(curve[-1])
        return iterateCurve(new, order-1)
    
    points = [(-0.5, 0), (0.5, 0)]
    return iterateCurve(points, order)


def kochShape(order):
    points = kochCurve(order)
    shp = createShape()
    shp.beginShape()
    for p in points:
        shp.vertex(*p)
    
    shp.vertex(10, -10)
    shp.vertex(-10, -10)
    shp.vertex(-0.5, 0)

    shp.endShape()
    return shp


def sierpinski(order):
    triangles = [[1]] + [[1] + [0] * (i - 1) + [1] for i in range(1, 2**order)]
    for i in range(1, 2**order):
        for j in range(1, i):
            if triangles[i-1][j-1] != triangles[i-1][j]:
                triangles[i][j] = 1
    return triangles

def fillSierpinski(order):
    triangles = sierpinski(order)
    for i in range(2**order):
        for j in range(i+1):
            if triangles[i][j]:
                pushMatrix()
                scale(2**-order)
                #print(1 - 1.0 / 2**order - 1.5 * i / 2**order)
                translate(sqrt(3) * j - sqrt(3)/2 * i, -2**order + 1.0 + 1.5 * i)
                triangle(0, -1, -sqrt(3)/2, 0.5, sqrt(3)/2, 0.5)
                popMatrix()
        

def triangleCenter(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x = (x1 + x2) / 2.0 - (y2 - y1) / (6 * sqrt(3))
    y = (y1 + y2) / 2.0 + (x2 - x1) / (6 * sqrt(3))
    return (x, y)

def triangleSize(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    d = sqrt(sq(x2-x1) + sq(y2-y1))
    return d / (3 * sqrt(3))

def triangleAngle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return atan2(y2-y1, x2-x1)

def fillSierpinskiFromLine(order, p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    r = triangleSize(p1, p2)
    angle = triangleAngle(p1, p2)
    x0, y0 = triangleCenter(p1, p2)
    pushMatrix()
    translate(x0, y0)
    rotate(angle + PI)
    scale(r)
    fillSierpinski(order)
    popMatrix()
    if order > 0:
        points = [p1] + innerKochPoints(p1, p2) + [p2]
        for i in range(len(points)-1):
            fillSierpinskiFromLine(order-1, points[i], points[i+1])

def setup():
    size(800, 800)
    
def draw():
    background(0)
    translate(width/2, height/2)
    R = width/2
    COUNT = 250
    frame = frameCount - 1
    rainbowCircle(R, frame * 2.0 * R / COUNT)
    noStroke()
    scale(R)
    fill(0)

    shp = kochShape(8)
    
    # Fill the outside border
    for i in range(6):
        angle = -PI/2 + i * PI/3
        pushMatrix()
        rotate(angle)
        translate(0, -sqrt(3)/2)
        shape(shp, 0, 0)
        popMatrix()

    p1 = (0, -1)
    p2 = (-sqrt(3)/2, 0.5)
    p3 = (sqrt(3)/2, 0.5)

    # Draw center sierpinski
    fillSierpinski(9)
    
    # Iterate the outer sierpinskis
    fillSierpinskiFromLine(7, p1, p2)
    fillSierpinskiFromLine(7, p2, p3)
    fillSierpinskiFromLine(7, p3, p1)
    
    if frameCount <= COUNT:
        print("Frame {} out of {}".format(frameCount, COUNT))
        saveFrame("frames//###.png")
