class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.edges = set()
        self.faces = set()

    @property
    def p(self):
        return (self.x, self.y, self.z)

    @property
    def visibility(self):
        return self.z

    def transform(self, T):
        self.x, self.y, self.z = T(self.p)

    def draw(self, s, t, c=None):
        if self.visibility < 0.2:
            return
        x, y = self.x * s, self.y * s
        w = t / (1 + exp(15*(0.6 - self.visibility)))
        d = 3 * t
        i = t + 2
        c = c or color(1)
        pushStyle()
        if w < 0.5 * t:
            fill(c)
        stroke(hue(c), saturation(c), brightness(c), alpha(c) / 2)
        strokeWeight(w*.85 + 1)
        circle(x, y, w*2.3 + 1)
        stroke(c)
        strokeWeight(w*.85)
        circle(x, y, w*2.3)
        popStyle()


class Face:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

        self.edges = set()

        v1.faces.add(self)
        v2.faces.add(self)
        v3.faces.add(self)

    @property
    def visibility(self):
        (x1, y1, z1) = self.v1.p
        (x2, y2, z2) = self.v2.p
        (x3, y3, z3) = self.v3.p
        def determinant(m):
            ((a, b, c), (d, e, f), (g, h, i)) = m
            return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h
        
        c = determinant(((x1, y1, 1), (x2, y2, 1), (x3, y3, 1))) / determinant((self.v1.p, self.v2.p, self.v3.p))
        
        return c

    @property
    def p1(self):
        return self.v1.p

    @property
    def p2(self):
        return self.v2.p

    @property
    def p3(self):
        return self.v3.p


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        
        v1.edges.add(self)
        v2.edges.add(self)

        self.faces = v1.faces.intersection(v2.faces)
        for face in self.faces:
            face.edges.add(face)

    @property
    def p1(self):
        return self.v1.p

    @property
    def p2(self):
        return self.v2.p
    
    @property
    def visibility(self):
        return max(f.visibility for f in self.faces)
    
    def draw(self, s, t, c=None):
        if self.visibility < 0:
            return
        x1, y1, x2, y2 = self.v1.x * s, self.v1.y * s, self.v2.x * s, self.v2.y * s
        t = t * 1 #sqrt(self.visibility)
        c = c or color(1)
        pushStyle()
        magnitude = dist(x1, y1, x2, y2)
        if magnitude == 0:
            return
        f = 2 / magnitude
        stroke(hue(c), saturation(c), brightness(c), alpha(c) / 2)
        strokeWeight(t)
        line(x1 + f * (x2 - x1), y1 + f * (y2 - y1), x2 + f * (x1 - x2), y2 + f * (y1 - y2)) 
        stroke(c)
        strokeWeight(max(t - 2, 0))
        line(x1 + f * (x2 - x1), y1 + f * (y2 - y1), x2 + f * (x1 - x2), y2 + f * (y1 - y2)) 
        popStyle()


class Polyhedron:
    def __init__(self, vertices, faces):
        self.verts = [Vertex(*vertex) for vertex in vertices]
        self.faces = [Face(*[self.verts[f] for f in face]) for face in faces]

        edges = set()
        for (a, b, c) in faces:
            edges.add(tuple(sorted([a, b])))
            edges.add(tuple(sorted([a, c])))
            edges.add(tuple(sorted([b, c])))
        edges = sorted(list(edges))
        self.edges = [Edge(*[self.verts[e] for e in edge]) for edge in edges]
        self.verts = set(self.verts)
        self.faces = set(self.faces)
        self.edges = set(self.edges)

    @property
    def V(self):
        return len(self.verts)
    
    @property
    def F(self):
        return len(self.faces)
    
    @property
    def E(self):
        return len(self.edges)

    def transform(self, T):
        for v in self.verts:
            v.transform(T)
    
    def rotate_about(self, vector, angle):
        u, v, w = vector
        # Normalize the vector
        magnitude = sqrt(u*u + v*v + w*w)
        u, v, w = u / magnitude, v / magnitude, w / magnitude

        a = angle

        cosa = cos(a)
        sina = sin(a)

        def f(p):
            x, y, z = p

            c = (u*x + v*y + w*z) * (1 - cosa)
            
            x1 = u*c + x*cosa + (-w*y + v*z)*sina
            y1 = v*c + y*cosa + (w*x - u*z)*sina
            z1 = w*c + z*cosa + (-v*x + u*y)*sina

            return x1, y1, z1
        
        self.transform(f)

    def get_visible_edges(self):
        visibility = {e: max(f.visibility for f in e.faces) for e in self.edges}
        return {k: v for k, v in visibility.items() if v >= 0}
    
    def get_visible_vertices(self):
        visibility = {v: v.z for v in self.verts}
        return {k: v for k, v in visibility.items() if v >= 0}

    def draw(self, cx, cy, s, t, c=None):
        c = c or color(1)
        push()
        translate(cx, cy)
        pushStyle()
        circle(0, 0, 2*s + 60)
        rect(0, 0, 500, -500)
        popStyle()
        for edge in self.edges:
            edge.draw(s, t, c)
        for vert in self.verts:
            vert.draw(s, t, c)
        pop()


C0 = sqrt(5 * (5 - 2 * sqrt(5))) / 5
C1 = sqrt(10 * (5 - sqrt(5))) / 10
C2 = (6 * sqrt(5) + sqrt(2 * (85 - sqrt(5))) - 16) / 19
C3 = sqrt(10 * (5 + sqrt(5))) / 10
C4 = (7 - 5 * sqrt(5) + sqrt(2 * (125 + 41 * sqrt(5)))) / 19
C5 = sqrt(10 * (5 - sqrt(5))) / 5

V = [
        (0.0, 0.0,  C5),
        (0.0, 0.0, -C5),
        ( C5, 0.0, 0.0),
        (-C5, 0.0, 0.0),
        (0.0,  C5, 0.0),
        (0.0, -C5, 0.0),
        ( C2, 0.0,  C4),
        ( C2, 0.0, -C4),
        (-C2, 0.0,  C4),
        (-C2, 0.0, -C4),
        ( C4,  C2, 0.0),
        ( C4, -C2, 0.0),
        (-C4,  C2, 0.0),
        (-C4, -C2, 0.0),
        (0.0,  C4,  C2),
        (0.0,  C4, -C2),
        (0.0, -C4,  C2),
        (0.0, -C4, -C2),
        ( C0,  C1,  C3),
        ( C0,  C1, -C3),
        ( C0, -C1,  C3),
        ( C0, -C1, -C3),
        (-C0,  C1,  C3),
        (-C0,  C1, -C3),
        (-C0, -C1,  C3),
        (-C0, -C1, -C3),
        ( C3,  C0,  C1),
        ( C3,  C0, -C1),
        ( C3, -C0,  C1),
        ( C3, -C0, -C1),
        (-C3,  C0,  C1),
        (-C3,  C0, -C1),
        (-C3, -C0,  C1),
        (-C3, -C0, -C1),
        ( C1,  C3,  C0),
        ( C1,  C3, -C0),
        ( C1, -C3,  C0),
        ( C1, -C3, -C0),
        (-C1,  C3,  C0),
        (-C1,  C3, -C0),
        (-C1, -C3,  C0),
        (-C1, -C3, -C0)
]


F = [
        ( 6,  0, 20),
        ( 6, 20, 28),
        ( 6, 28, 26),
        ( 6, 26, 18),
        ( 6, 18,  0),
        ( 7,  1, 19),
        ( 7, 19, 27),
        ( 7, 27, 29),
        ( 7, 29, 21),
        ( 7, 21,  1),
        ( 8,  0, 22),
        ( 8, 22, 30),
        ( 8, 30, 32),
        ( 8, 32, 24),
        ( 8, 24,  0),
        ( 9,  1, 25),
        ( 9, 25, 33),
        ( 9, 33, 31),
        ( 9, 31, 23),
        ( 9, 23,  1),
        (10,  2, 27),
        (10, 27, 35),
        (10, 35, 34),
        (10, 34, 26),
        (10, 26,  2),
        (11,  2, 28),
        (11, 28, 36),
        (11, 36, 37),
        (11, 37, 29),
        (11, 29,  2),
        (12,  3, 30),
        (12, 30, 38),
        (12, 38, 39),
        (12, 39, 31),
        (12, 31,  3),
        (13,  3, 33),
        (13, 33, 41),
        (13, 41, 40),
        (13, 40, 32),
        (13, 32,  3),
        (14,  4, 38),
        (14, 38, 22),
        (14, 22, 18),
        (14, 18, 34),
        (14, 34,  4),
        (15,  4, 35),
        (15, 35, 19),
        (15, 19, 23),
        (15, 23, 39),
        (15, 39,  4),
        (16,  5, 36),
        (16, 36, 20),
        (16, 20, 24),
        (16, 24, 40),
        (16, 40,  5),
        (17,  5, 41),
        (17, 41, 25),
        (17, 25, 21),
        (17, 21, 37),
        (17, 37,  5),
        ( 0, 18, 22),
        ( 0, 24, 20),
        ( 1, 21, 25),
        ( 1, 23, 19),
        ( 2, 26, 28),
        ( 2, 29, 27),
        ( 3, 31, 33),
        ( 3, 32, 30),
        ( 4, 34, 35),
        ( 4, 39, 38),
        ( 5, 37, 36),
        ( 5, 40, 41),
        (18, 26, 34),
        (19, 35, 27),
        (20, 36, 28),
        (21, 29, 37),
        (22, 38, 30),
        (23, 31, 39),
        (24, 32, 40),
        (25, 41, 33)
]


pentakis = Polyhedron(V, F)


def drawBackground(c=None):
    c = c or color(0)
    clear()
    fill(c)
    rect(0, 0, width, height)

def drawBorder(x, y, w, h, t, c=None):
    c = c or color(1)
    pushStyle()
    noFill()
    stroke(hue(c), saturation(c), brightness(c), alpha(c) / 2)
    strokeWeight(t)
    rect(x + t / 2, y + t / 2, w - t + 2, h - t + 2)
    stroke(c)
    strokeWeight(t - 2)
    rect(x + t / 2, y + t / 2, w - t + 2, h - t + 2)
    popStyle()

def drawWord(word, x, y, c=None):
    global IMAGES
    image(IMAGES[word], x, y)

def drawWords(x, y, c=color(1)):
    drawWord('data', x + 8, y + 5 * sin(2*PI*frameCount/60), c)
    drawWord('science', x - 10 * cos(2*PI*frameCount/70), y + 115, c)
    drawWord('group', x+1 + 7 * sin(2*PI*frameCount/80), y + 231 - 12 * cos(2*PI*frameCount/50))


IMAGES = {}

def setup():
    global IMAGES
    IMAGES = {tag: loadImage('/home/justin/sandbox/gimp/{}.png'.format(tag)) for tag in ['data', 'science', 'group']}
    size(1000, 1000)
    colorMode(HSB, 1)
    noStroke()
    noFill()
    pentakis.rotate_about((0, 0, 1), 0.8)
    
def draw():
    pentakis.rotate_about((-0.3, 0.9, 0), 0.01)
    drawBackground(color(0.67, 1, 1, 1))
    translate(0, 100)
    drawBorder(27, 27, 719, 719, 15)
    drawWords(89, 365)
    s = 200 + 50 * sin(2 * PI * frameCount / 200)
    pentakis.draw(600, 200, s, 12)
