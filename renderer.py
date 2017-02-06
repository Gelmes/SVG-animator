from bs4 import BeautifulSoup
import sys, pygame, GameObject
pygame.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

size = width, heignt = 1280, 800
speed = [2, 2]
black = 0, 0, 0
movement_path = []

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Example code for the draw module")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
handimage = pygame.image.load('hand.png').convert_alpha()
hand = GameObject.GameObject(handimage, 10, 5)
f = file("ex.svg", "r")
html_doc = f.read();
f.close()
svg = BeautifulSoup(html_doc, 'html.parser')
def drawLine(pos1, pos2):
    pygame.draw.line(screen, WHITE, pos1, pos2, 5)
    hand.addPoint(pos1)
    hand.addPoint(pos2)
    
def renderPolyline(poly):
    points = poly['points'].replace("\n\t","").split(" ")
    pointlist = []
    for p in points[0:-1]:
        p = p.split(",")
        pointlist.append([int(float(p[0])), int(float(p[1]))])

    prevp = pointlist[0]

    for p in pointlist[1:]:
        drawLine(prevp, p)
        prevp = p

def renderPath(path,steps):
    curves = path['d'].replace("c","cp,")\
                    .replace("M","")\
                    .replace("-",",-")\
                    .split("c")
    m = curves[0].split(",")
    m0 = int(float(m[0]))
    m1 = int(float(m[1]))
    for curve in curves[1:]:
        curve = curve.replace(",,",",")
        c = curve.split(",")
        prevp = [m0, m1]
        x0 = m0
        y0 = m1
        x1 = m0 + float(c[1])
        y1 = m1 + float(c[2])
        x2 = m0 + float(c[3])
        y2 = m1 + float(c[4])
        x3 = m0 + float(c[5])
        y3 = m1 + float(c[6])
        step_size = 1.0/steps
        t = 0
        for s in range(steps):
            t = t + step_size
            x = ((1-t)*(1-t)*(1-t)*x0) +\
                (3*(1-t)*(1-t)*t*x1) +\
                (3*(1-t)*t*t*x2) +\
                (t*t*t*x3)         
            y = ((1-t)*(1-t)*(1-t)*y0) +\
                (3*(1-t)*(1-t)*t*y1) +\
                (3*(1-t)*t*t*y2) +\
                (t*t*t*y3)
            drawLine(prevp, [x, y])
            prevp = [x, y]
            

def renderSVG(soup):
    for tag in soup.find_all():
        n = tag.name
        if(n == "polyline"):
            #print "Poly"
            renderPolyline(tag)
        if(n == "line"):
            #print "Line"
            pass
        elif(n =="path"):
            #print "Path"
            renderPath(tag, 20)
        elif(n =="rect"):
            #print "Rect"
            pass


while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    screen.fill(BLACK)
    renderSVG(svg)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    hand.move()
    screen.blit(hand.image, hand.pos)
    pygame.display.flip()
    pygame.time.delay(10)
    #break

pygame.display.quit()
sys.exit()
