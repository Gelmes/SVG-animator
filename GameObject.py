import Queue, math
class GameObject:
    def __init__(self, image, height, speed, end):
        self.speed = float(speed) * 5
        self.speed_slow = float(speed)
        self.speed_fast = float(speed) * 10
        self.image = image
        self.pos = image.get_rect().move(0, height)
        self.path = Queue.Queue()
        self.goal = [0,height]
        self.end_pos = end
        self.lines_len = 0
        self.lines = []
        self.render_lines = []
        self.counter = 0
    def move(self):
        """
        Moves hand based on a list of points provided by the used

        Future implementation should use a list of lines instead
        and modify them so that they are drawn accordingly
        Returns true if the hand is succesfully moved
        """
        result = 1
        #if (not self.path.empty()):
        if (self.counter < self.lines_len):
            if(abs(self.pos[0] - self.goal[0]) < (self.speed) and \
               abs(self.pos[1] - self.goal[1]) < (self.speed)):
                #print self.goal, self.counter/2, self.counter%2
                self.goal =  self.lines[self.counter/2][self.counter%2]
                if(self.counter%2==1):
                    self.render_lines.append(self.lines[self.counter/2])
                    self.speed = self.speed_slow
                self.counter = self.counter + 1
            
        else:
            self.goal = self.end_pos
            self.speed = self.speed_fast
            if(abs(self.pos[0] - self.goal[0]) < (self.speed) and \
               abs(self.pos[1] - self.goal[1]) < (self.speed)):
                result = 0
            #print "Done Drawing"
        if(self.goal[0] - self.pos[0] != 0):
            angle = math.atan((float(self.goal[1]) - float(self.pos[1])) /\
                                (float(self.goal[0]) - float(self.pos[0])))
        else:
            angle = math.pi / 2.0
        angle = abs(angle) # + math.pi/2
        if((self.goal[1] - self.pos[1]) < 0):
            angle = angle * -1        
        if((self.goal[0] - self.pos[0]) < 0):
            angle =  math.pi - angle
        x = self.speed * math.cos(angle)
        y = self.speed * math.sin(angle)
        #print self.goal, self.pos, math.degrees(ogangle), math.degrees(angle), x, y
        self.pos = self.pos.move(x, y)
        return result
        
    def move_lines(self):
        pass
        
    def add_point(self, point):
        self.path.put(point)
        
    def add_lines(self, lines):
        self.lines_len = len(lines) * 2
        self.lines = lines




        

