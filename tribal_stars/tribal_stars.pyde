

class Star:
    def __init__(self, points, inner, outer, angle, phase, hue):
        self.n = points
        self.a = angle
        self.ph = phase % TWO_PI
        self.r1 = outer - (outer - inner) / PI * abs(self.ph - PI)
        self.r2 = inner + (outer - inner) / PI * abs(self.ph - PI)
        self.h = hue
    
    def points(self):
        points = []
        for i in range(self.n):
            points.append((cos(self.a + TWO_PI * i / self.n) * self.r2, sin(self.a + TWO_PI * i / self.n) * self.r2))
            points.append((cos(self.a + TWO_PI * (i + 0.5) / self.n) * self.r1, sin(self.a + TWO_PI * (i + 0.5) / self.n) * self.r1))
        return points
    
    def draw(self, value=1):
        fill(self.h, 1, value)
        stroke(1, 0, 1)
        star = createShape()
        star.beginShape()
        for p in self.points():
            star.vertex(*p)
        star.endShape(CLOSE)
        shape(star, 0, 0)
    


def setup():
    size(800, 800)
    colorMode(HSB, 1)

def draw():
    FRAMES = 250
    FACT = PI * frameCount / FRAMES
    background(0, 0, 0)
    translate(400, 400)
    rotate(-PI/2)
    
    for i, n in enumerate(range(10, 2, -1)):
        Star(n, 20*n, 40*n, FACT, FACT, (2.08 * i / 7) % 1).draw()
    fill(0, 0, 0)
    ellipse(0, 0, 100, 100)
    
    if frameCount < FRAMES:
        saveFrame("frames//###.png")
        
