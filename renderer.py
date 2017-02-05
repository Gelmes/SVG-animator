from bs4 import BeautifulSoup
import sys, pygame
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

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Example code for the draw module")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

f = file("example.svg", "r")
html_doc = f.read();
svg = BeautifulSoup(html_doc, 'html.parser')
def renderPolyline(poly):
    points = poly['points'].replace("\n\t","").split(" ")
    pointlist = []
    for p in points[0:-1]:
        p = p.split(",")
        pointlist.append([int(float(p[0])), int(float(p[1]))])

    prevp = pointlist[0]

    for p in pointlist[1:]:
        pygame.draw.line(screen, GREEN, prevp, p, 5)
        prevp = p

def renderSVG(soup):
    for tag in soup.find_all():
        n = tag.name
        if(n == "polyline"):
            print "Poly"
            renderPolyline(tag)
        elif(n =="path"):
            print "Path"
        elif(n =="rect"):
            print "Rect"
            print int(tag['x']) + int(tag['y'])


while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
    screen.fill(BLACK)
    renderSVG(svg)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    pygame.display.flip()
    #break

pygame.display.quit()
sys.exit()
