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
        self.on_a_line = 0 #Flag inicating if hand is on a line
        self.starting_line_pos = [0,0] #Position of first point on current line
        self.ending_line_pos = [0,0]
    def move(self):
        """
        Moves hand based on a list of points provided by the used
        These points are then updated at every call to this function
        and new list is generated that contains the lines drawn up
        to the point where the hand has moved.
        
        Returns true if the hand is succesfully moved
        """
        result = 1

        ###################################################################
        #Empty list and collision detection
        if (self.counter < self.lines_len):
            while(abs(self.pos[0] - self.goal[0]) < (self.speed) and \
               abs(self.pos[1] - self.goal[1]) < (self.speed)):
                #Render Line only after second point is reached
                self.counter = self.counter + 1
                if(self.counter >= self.lines_len):
                    #self.counter = self.counter - 1
                    self.handle_collision()                    
                    self.counter = self.counter + 1
                    break
                self.handle_collision()
                          
        else:
            self.goal = self.end_pos
            self.speed = self.speed_fast
            if(abs(self.pos[0] - self.goal[0]) < (self.speed) and \
               abs(self.pos[1] - self.goal[1]) < (self.speed)):
                result = 0

        ###################################################################
        #Get angle to move hand towards
        if(self.goal[0] - self.pos[0] != 0):
            angle = math.atan((float(self.goal[1]) - float(self.pos[1])) /\
                                (float(self.goal[0]) - float(self.pos[0])))
        #Handle division by zero exception
        else:
            angle = math.pi / 2.0
        angle = abs(angle)

        ###################################################################
        #If Y is negative inverse the angle
        if((self.goal[1] - self.pos[1]) < 0):
            angle = angle * -1
        #If X is negative get vertical mirror of angle
        if((self.goal[0] - self.pos[0]) < 0):
            angle =  math.pi - angle
        x = self.speed * math.cos(angle)
        y = self.speed * math.sin(angle)
        #print self.goal, self.pos, math.degrees(ogangle), math.degrees(angle), x, y
        self.pos = self.pos.move(x, y)

        ###################################################################
        #dynamic line rendering of current line is done here        
        try:
            if(self.on_a_line):
                self.starting_line_pos = self.render_lines.pop()[0]
                self.render_lines.append([self.starting_line_pos, \
                                         [self.pos[0],self.pos[1]]])
        except(IndexError):
            pass
        
            
        return result
    def handle_collision(self):
        if(self.counter%2==1):
            line = self.lines[self.counter/2]
            self.render_lines.append(line)
            self.starting_line_pos = line[0]
            self.ending_line_pos = line[1]
            self.speed = self.speed_slow
            self.on_a_line = 1
        else:
            try:
                self.render_lines.pop()
                self.render_lines.append([self.starting_line_pos,\
                                          self.ending_line_pos])
            except(IndexError):
                pass
            
            self.on_a_line = 0
        #Set next goal point
        if(self.counter != self.lines_len):
            self.goal =  self.lines[self.counter/2][self.counter%2]  
        
    def move_lines(self):
        pass
        
    def add_point(self, point):
        self.path.put(point)
        
    def add_lines(self, lines):
        #length is doubled to account for starting and ending points
        self.lines_len = len(lines) * 2
        self.lines = lines
        self.goal = self.lines[0][0]

    def get_lines(self):
        return self.render_lines




        

