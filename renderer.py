from bs4 import BeautifulSoup
import sys, pygame, GameObject
#========================================== Pygae Stuff
pygame.init()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

size = width, height = 1280, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Example code for the draw module")
done = False
clock = pygame.time.Clock()
handimage = pygame.image.load('hand.png').convert_alpha()
hand = GameObject.GameObject(handimage, 10, 5, size)

#========================================== BeautifulSoup Stuff
f = file("ex.svg", "r")
html_doc = f.read();
f.close()
svg = BeautifulSoup(html_doc, 'html.parser')

#========================================== Global Stuff
lines = [] #Lines that will be rendered every frame

#========================================== Main Functions
def save_line(pos1, pos2):
    #pygame.draw.aaline(screen, WHITE, pos1, pos2, 5)
    hand.add_point(pos1)
    hand.add_point(pos2)
    lines.append([pos1,pos2]) #[[x0,y0],[x1,y1]]
    
    
def make_polyline(poly):
    points = poly['points'].replace("\n\t","").split(" ")
    pointlist = []
    for p in points[0:-1]:
        p = p.split(",")
        pointlist.append([int(float(p[0])), int(float(p[1]))])
    prevp = pointlist[0]
    for p in pointlist[1:]:
        save_line(prevp, p)
        prevp = p

def make_path(path,steps):
    curves = path['d'].replace("c","cp,")\
                    .replace("C","cP,")\
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
        if(c[0] == "p"):
            x1 = m0 + float(c[1])
            y1 = m1 + float(c[2])
            x2 = m0 + float(c[3])
            y2 = m1 + float(c[4])
            x3 = m0 + float(c[5])
            y3 = m1 + float(c[6])
        elif(c[0] =="P"):
            x1 = float(c[1])
            y1 = float(c[2])
            x2 = float(c[3])
            y2 = float(c[4])
            x3 = float(c[5])
            y3 = float(c[6])
            
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
            save_line(prevp, [x, y])
            prevp = [x, y]
            

def renderSVG(soup):
    for tag in soup.find_all():
        n = tag.name
        if(n == "polyline"):
            #print "Poly"
            make_polyline(tag)
        if(n == "line"):
            #print "Line"
            pass
        elif(n =="path"):
            #print "Path"
            make_path(tag, 20)
        elif(n =="rect"):
            #print "Rect"
            pass

def render_lines(lines):
    for line in lines:
        pygame.draw.aaline(screen, WHITE, line[0], line[1], 5)

renderSVG(svg)
hand.add_lines(lines)
    
while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    screen.fill(BLACK)
    render_lines(lines)
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
