

def makeSpiral(r, a, o, m=100):
    spiral = createShape()
    spiral.beginShape()
    
    M = m * abs(a) / TWO_PI
    for i in range(int(M) + 1):
        t = i * a / M
        spiral.vertex(
            cos(t + o) * t * r / a,
            sin(t + o) * t * r / a
        )
    
    spiral.endShape()
    return spiral


def spiralSections(L, P, m=100):
    
    def addSection(sect, t1, t2, r, o):
        for i in range(m + 1):
            t = t1 + (t2 - t1) * i / m
            sect.vertex(
                r * t * cos(t + o) / (L * PI / P),
                r * t * sin(t + o) / (L * PI / P)
            )
    
    def getSection(l, p):
        def makeSection(r, o=0):
            sect = createShape()
            sect.beginShape()
            addSection(sect, PI / P * l, PI / P * (l + 1), r, TWO_PI / P * p + o)
            addSection(sect, -PI / P * (l + 1), -PI / P * l, r, TWO_PI / P * (p + l - 4) + o)
            if l > 0:
                addSection(sect, PI / P * l, PI / P * (l - 1), r, TWO_PI / P * (p + 1) + o)
                addSection(sect, -PI / P * (l - 1), -PI / P * l, r, TWO_PI / P * (p + l - 5) + o)
            sect.endShape()
            return sect
        return makeSection
    
    return [[getSection(l, p) for p in range(P)] for l in range(L)]


def spiralRings(L, P, m=100):
    
    M = 2 * P * m
    
    def addSection(ring, t1, t2, r, o):
        for i in range(m + 1):
            t = t1 + (t2 - t1) * i / m
            ring.vertex(
                r * t * cos(t + o) / (L * PI / P),
                r * t * sin(t + o) / (L * PI / P)
            )
    
    def getRing(l):
        def makeRing(r, o=0):
            ring = createShape()
            ring.beginShape()
            for p in range(P):
                addSection(ring, PI / P * l, PI / P * (l + 1), r, TWO_PI / P * p + o)
                addSection(ring, -PI / P * (l + 1), -PI / P * l, r, TWO_PI / P * (p + l - 4) + o)
            ring.endShape()
            return ring
        return makeRing
    
    return [getRing(l) for l in range(L)]
    

def setup():
    size(800, 800)
    global sections, rings, R, COUNT, L, P

    L = 14
    P = 5 # 10 is the one that works "correctly"
    R = width/2
    o = 0
    COUNT = 250
    sections = spiralSections(L, P)
    rings = spiralRings(L, P)
    
    colorMode(HSB)


def draw():
    global sections, rings, R, COUNT, L, P
    #noStroke()
    background(0)
    translate(width/2, height/2)
    
    frame = frameCount - 1 + COUNT / 2
    #rotate(frameCount * PI * 3 / (2 * P * COUNT))
    for (i, ring) in enumerate(rings):
        #rotateate(frameCount * PI / 300)
        fill(255 * i / len(rings), 255, 255)
        shape(rings[-1-i](R * L / (L+1) * 2*(.5 + (i+1) / (len(rings)+1) - .5 * (i+1) / (len(rings)+1) * cos(frame * TWO_PI / COUNT)), frame * TWO_PI / (P * COUNT) * (i+1)), 0, 0)
        #shape(rings[-1-i](R * L / (L+1) * 2*(.5 + (i+1) / (len(rings)+1) - .5 * (i+1) / (len(rings)+1) * cos(frame * TWO_PI / COUNT)), PI / P * (i+1)), 0, 0)
  
    if frameCount <= COUNT:
            saveFrame("frames{:02d}//###.png".format(P))

        
