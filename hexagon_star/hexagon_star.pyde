
def setup():
    size(800, 800)
    colorMode(HSB)


class Hexagon:
    LIFE = 7
    LAYERS = 15
    RESET = 200
    PERIOD = 1.0 * RESET / LAYERS
    
    #BIRTH_FUN = lambda x: 
    
    @staticmethod
    def makeHexagon(a, c1=0, c2=7):
        hexagon = createShape()
        hexagon.beginShape()
        for angle in [i * PI / 3 for i in range(c1, c2)]:
            hexagon.vertex(a * cos(angle), a * sin(angle))
        hexagon.endShape()
        return hexagon
    
    def __init__(self, hue, birth_xy, life_xy, death_xy, birth_t, birth_dur, life_dur, death_dur, life_size, birth_fun=(lambda x: x), death_fun=(lambda x: x), corner_range=(0, 7)):
        self.hue = hue
        self.birth_xy = birth_xy
        self.life_xy = life_xy
        self.death_xy = death_xy
        self.birth_t = (birth_t * Hexagon.PERIOD) % Hexagon.RESET
        self.life_t = ((birth_t + birth_dur) * Hexagon.PERIOD) % Hexagon.RESET
        self.sick_t = ((birth_t + birth_dur + life_dur * Hexagon.LIFE) * Hexagon.PERIOD) % Hexagon.RESET
        self.death_t = ((birth_t + birth_dur + life_dur * Hexagon.LIFE + death_dur) * Hexagon.PERIOD) % Hexagon.RESET
        self.life_size = life_size
        self.birth_fun = birth_fun
        self.death_fun = death_fun
        self.corner_range = corner_range
    
    @staticmethod
    def interpolateValue(v1, v2, f):
        return v1 + f * (v2 - v1)
    
    @staticmethod
    def interpolatePoint(p1, p2, f):
        x = p1[0] + f * (p2[0] - p1[0])
        y = p1[1] + f * (p2[1] - p1[1])
        return (x, y)
    
    def getSaturation(self, t):
        t = t % Hexagon.RESET
        if not self.isBeingBorn(t):
            return 255
        else:
            return 255.0 * ((t - self.birth_t) % Hexagon.RESET) / ((self.life_t - self.birth_t) % Hexagon.RESET)
    
    def getAlpha(self, t):
        t = t % Hexagon.RESET
        if self.isBeingBorn(t):
            return 255
        if self.isAlive(t) or self.isDying(t):
            return 255.0 * (1 - ((t - self.life_t) % Hexagon.RESET) / ((self.death_t - self.life_t) % Hexagon.RESET))
        else:
            return 0
    
    def isDead(self, t):
        t = t % Hexagon.RESET
        if self.death_t < self.birth_t:
            return t >= self.death_t and t < self.birth_t
        return t < self.birth_t or t >= self.death_t
    
    def isBeingBorn(self, t):
        t = t % Hexagon.RESET
        if self.life_t < self.birth_t:
            return t >= self.birth_t or t < self.life_t
        return self.birth_t <= t < self.life_t
    
    def isAlive(self, t):
        t = t % Hexagon.RESET
        if self.sick_t < self.life_t:
            return t >= self.life_t or t < self.sick_t
        return self.life_t <= t < self.sick_t
    
    def isDying(self, t):
        t = t % Hexagon.RESET
        if self.death_t < self.sick_t:
            return t >= self.sick_t or t < self.death_t
        return self.sick_t <= t < self.death_t
    
    def drawHexagon(self, t):
        t = t % Hexagon.RESET
        if self.isDead(t):
            return
        fill(self.hue, self.getSaturation(t), 255, self.getAlpha(t))
        if self.isAlive(t):
            xy = self.life_xy
            size = self.life_size
        elif self.isBeingBorn(t):
            prop = 1.0*((t - self.birth_t) % Hexagon.RESET) / ((self.life_t - self.birth_t) % Hexagon.RESET)
            f1 = self.birth_fun(prop)
            f2 = self.birth_fun(prop)
            xy = Hexagon.interpolatePoint(self.birth_xy, self.life_xy, f1)
            size = Hexagon.interpolateValue(0, self.life_size, f2)
        else: # self.isDying
            f = self.death_fun(1.0*((t - self.sick_t) % Hexagon.RESET) / ((self.death_t - self.sick_t) % Hexagon.RESET))
            xy = Hexagon.interpolatePoint(self.life_xy, self.death_xy, f)
            size = Hexagon.interpolateValue(self.life_size, 0, f)
        h = Hexagon.makeHexagon(size, *self.corner_range)
        shape(h, *xy)


def drawHexagon(a, x, y):
    h = makeHexagon(a)
    shape(h, x, y)

def layerCoordinates(a, layer):
    if layer <= 0:
        return [(0, 0)]
    coords = []
    radius = layer * sqrt(3) * a
    for angle in [PI/6 + i * PI / 3 for i in range(7)]:
        coords.append((radius * cos(angle), radius * sin(angle)))
    return coords


def draw():
    background(0)
    noStroke()
    a = 13
    b = 16
    
    translate(width/2, height/2)
    
    frame = frameCount-1# + Hexagon.RESET / 2 - 8
    
    birth_fun = lambda x: (x + 1) / 2.0
    birth_fun = lambda x: (x + 0.6) / 1.6
    death_fun = lambda x: 0 if x < 0.2 else (x - 0.2) / 0.8
    # birth_fun = lambda x: x
    death_fun = lambda x: x
    # death_fun = lambda x: 0 if x < 0.5 else 2 * (x - 0.5)
    hexagons = []
    hexagons.append(Hexagon(255, (0, 0), (0, 0), (0, 0), 0, 1, 1, 1, a, birth_fun, death_fun))
    HEX = hexagons[0]
    coords = [[(0, 0)] * 6] * 2 + [layerCoordinates(b, i) for i in range(1, Hexagon.LAYERS)] + [layerCoordinates(b, Hexagon.LAYERS-1)]
    
    for i in range(1, Hexagon.LAYERS):
        for j in range(6):
            hexagons.append(Hexagon(i * 255.0 / Hexagon.LAYERS, coords[i][j], coords[i+1][j], coords[i+1][j], i, 1, 1, 1, a, birth_fun, death_fun))
    
    middles = []
    for i in range(3, Hexagon.LAYERS+1):
        for j in range(6):
            for h in range((i-1)/2):
                if i % 2 and h == (i-3)/2:
                    cr1 = (j+4, j+8)
                    cr2 = (j+1, j+5)
                else:
                    cr1 = cr2 = (0, 7)
                frac = 1.0 / (i - 1)
                p1 = Hexagon.interpolatePoint(coords[i][j], coords[i][j+1], h * frac)
                p2 = Hexagon.interpolatePoint(coords[i][j], coords[i][j+1], (h + 1) * frac)
                hexagons.append(Hexagon((i - 1) * 255.0 / Hexagon.LAYERS, p1, p2, p2, i + h, 1, 1, 1, a, birth_fun, death_fun, corner_range=cr1))
                p3 = Hexagon.interpolatePoint(coords[i][j+1], coords[i][j], h * frac)
                p4 = Hexagon.interpolatePoint(coords[i][j+1], coords[i][j], (h + 1) * frac)
                hexagons.append(Hexagon((i - 1) * 255.0 / Hexagon.LAYERS, p3, p4, p4, i + h, 1, 1, 1, a, birth_fun, death_fun, corner_range=cr2))
    
    for hexagon in hexagons:
        if not hexagon.isAlive(frame):
            hexagon.drawHexagon(frame)
    for hexagon in hexagons:
        if hexagon.isAlive(frame):
            hexagon.drawHexagon(frame)
    
    if frameCount <= Hexagon.RESET:
        saveFrame("frames//###.png")
