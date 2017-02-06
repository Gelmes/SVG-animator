import Queue, math
class GameObject:
    def __init__(self, image, height, speed):
        self.speed = float(speed)
        self.image = image
        self.pos = image.get_rect().move(0, height)
        self.path = Queue.Queue()
        self.goal = [0,height]
    def move(self):
        if(abs(self.pos[0] - self.goal[0]) < (self.speed + 1) and \
           abs(self.pos[1] - self.goal[1]) < (self.speed + 1)):
            self.goal = self.path.get()

        if(self.goal[1] - self.pos[1] != 0):
            angle = math.atan((float(self.goal[1]) - float(self.pos[1])) /\
                                (float(self.goal[0]) - float(self.pos[0])))
        else:
            angle = math.pi / 2.0
        ogangle = angle
        angle = abs(angle) # + math.pi/2
        if((self.goal[1] - self.pos[1]) < 0):
            angle = angle * -1        
        if((self.goal[0] - self.pos[0]) < 0):
            angle =  math.pi - angle
        
        x = self.speed * math.cos(angle)
        y = self.speed * math.sin(angle)

        #print self.goal, self.pos, math.degrees(ogangle), math.degrees(angle), x, y
        self.pos = self.pos.move(x, y)
        #if self.pos.right > 1280:
        #    self.pos.left = 0
    def addPoint(self, point):
        self.path.put(point)


        """
        if(int(self.goal[1]) - int(self.pos[1]) != 0):
            angle = math.atan(float(int(self.goal[0]) - int(self.pos[0])) /\
                                float(int(self.goal[1]) - int(self.pos[1])))
                                """
