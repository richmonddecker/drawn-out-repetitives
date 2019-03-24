def setup():
    size(800, 800)
    colorMode(HSB)

def drawSine(frame, FRAMES):
    pushMatrix()
    rotate(TWO_PI * frame / FRAMES - 0.666 * cos(frame * TWO_PI / FRAMES))
    sine = createShape()
    sine.beginShape()

    for x in range(0, width/2):
        sine.vertex(x, cos(2 * TWO_PI * frame / FRAMES) * 0.2 * x * sin(TWO_PI * x / (width/8)) - 0.1 * x * (1 + sin(frame * TWO_PI / FRAMES)))
    sine.endShape()
    shape(sine, 0, 0)
    popMatrix()

def draw():
    background(0)
    translate(width/2, height/2)
    strokeWeight(2)
    FRAMES = 125
    COUNT = 25
    SPACE = 2.5
    frame = frameCount - 1
    noFill()
    
    pushMatrix()
    rotate(TWO_PI * frame / (2 * FRAMES))
    
    for i in range(0, COUNT):
        frame = frameCount - 1 - SPACE * i
        stroke(i * 255.0 / COUNT, 255, 255)
        drawSine(frame, FRAMES)
    
    stroke(255)
    drawSine(frameCount - 1 - COUNT * SPACE, FRAMES)
    drawSine(frameCount - 1 + SPACE, FRAMES)
    
    popMatrix()
    
    ellipse(0, 0, width-2, height-2)
    
    stroke(0)
    strokeWeight(12)
    ellipse(0, 0, width+12, height+12)
    
    if frameCount <= 2 * FRAMES:
       saveFrame("frames//###.png")
