import operator
import random
import copy
from helper import *
class Agent: 
    eye_sight = 2
    def __init__(self, name,init_x,init_y,x,y):#default constructor
        self.name = name #your given name
        self.l_heuristic = [] #each direction gets its own heuristic function
        self.r_heuristic = [] #each heuristic function is an matrix operation determined during the birth of the agent
        self.u_heuristic = [] #essentially the agent sees a matrix on its (left/right/up/down)
        self.d_heuristic = [] #and apply calculation based on the given heuristic
        self.value = {} #Legend of the map towards a specific agent
        self.lifespan =200 #when the lifespan goes to 0, the agent dies (could eventually introduce combat)
        self.score = 0 #score tracker
        self.x = init_x 
        self.y = init_y
        self.map_x = x
        self.map_y = y
    def build_value(self): #randomize how much the agent values the items they may see on the map, 
        self.value["X"]=random.randint(0,10) #walls
        self.value["."]=random.randint(0,10) #food/reward
        self.value[" "]=random.randint(0,10) #empty space
        self.value["M"]= 0 #Yourself/fellow agents
    def build_heuristic(self): #building heurisitc function with a random generator
        for direction in ["l","r","u","d"]:
            for i in range(0,2*self.eye_sight+1):
                temp = []
                for j in range(0,2*self.eye_sight+1):
                    temp.append(random.randint(0,10))
                if direction == "l":
                    self.l_heuristic.append(temp)
                if direction == "r":
                    self.r_heuristic.append(temp)
                if direction == "u":
                    self.u_heuristic.append(temp)
                if direction == "d":
                    self.d_heuristic.append(temp)
    def init_born(self): #constructing an agent
        self.build_heuristic()
        self.build_value()
        #print "Character setup finished"
    def brief_info(self):
        print ("Current score:",self.score)
    def info(self): #for debug sake, not called within the finished program
        print ("I am", self.name)
        print ("I am at",self.x,self.y)
        print ("My score:",self.score)
        #print "My Life:",self.lifespan
    def move(self,direction,world_map): #given direction, move towards the next step, move only when it's valid.
        if direction == "U":
            next_x = self.x-1
            next_y = self.y
        if direction == "D":
            next_x = self.x+1
            next_y = self.y
        if direction == "L":
            next_x = self.x
            next_y = self.y-1
        if direction == "R":
            next_x = self.x
            next_y = self.y+1
        valid = self.valid_move(next_x,next_y,world_map)
        if valid == True: #if move failed, agent lose a turn.
            if world_map[next_x][next_y] == ".":
                self.score = self.score+1
            world_map[next_x][next_y] = "M"
            world_map[self.x][self.y] = " "
            self.x = next_x
            self.y = next_y
            #print "successful move"
        self.lifespan= self.lifespan-1 #the purpose of losing a turn is to punish action like walking into the wall repeatedly
    def out_of_bound(self,x,y):
        if x<0 or x>=self.map_x or y < 0 or y>= self.map_y :
            return False #this means it's out of bound
        else:
            return True
    def valid_move(self,x,y,world_map):
        flag_1 = self.out_of_bound(x,y)
        if flag_1 == False:
            return False
        if world_map[x][y] == " " or world_map[x][y] == ".":
            flag_2 = True
        else:
            flag_2 = False
        return flag_2 and flag_1
    def observing(self,location,world):
        #location should be able to breakdown to loc_x loc_y by location[0] location[1]
        eye_sight = 2
        c_x = location[0]
        c_y = location[1]
        vision = []
        min_x = c_x - eye_sight
        max_x = c_x + eye_sight+1
        min_y = c_y - eye_sight
        max_y = c_y + eye_sight+1
        for i in range(min_x,max_x):
            temp = []
    
            for j in range(min_y,max_y):
                if (i,j) == location:
                    temp.append("M")
                elif self.out_of_bound(i,j) == False:
                    temp.append("X")
                else:
                    temp.append(world[i][j])
            vision.append(temp)
        return vision
    def whereIam(self): #helper function
        return self.x,self.y
    def think(self,world_map): #function called by the agent, performing matrix calculation to produce a heuristic value
        #returns a direction with the highest heuristic value
        eye_sight = self.eye_sight
        location = self.whereIam()
        loc = (location[0],location[1])
        saw = self.observing(loc,world_map)
        l_score = 0
        r_score = 0
        u_score = 0
        d_score = 0
        for i in range(0,eye_sight*2+1):
            for j in range(0,eye_sight*2+1):
                l_score += self.value[saw[i][j]]*self.l_heuristic[i][j]
                r_score += self.value[saw[i][j]]*self.r_heuristic[i][j]
                u_score += self.value[saw[i][j]]*self.u_heuristic[i][j]
                d_score += self.value[saw[i][j]]*self.d_heuristic[i][j]
        score_list = [l_score,r_score,u_score,d_score]
        score_list.sort(reverse=True)
        if l_score == score_list[0]:
            return "L"
        if r_score == score_list[0]:
            return "R"
        if d_score == score_list[0]:
            return "D"
        if u_score == score_list[0]:
            return "U"
    def lifeRemain(self): #helper function
        return self.lifespan
    def redeploy(self,init_x,init_y): #used after a round is completed, used to replenish unit's health and clean scoreboard
        self.x = init_x
        self.y = init_y
        self.score = 0
        self.lifespan= 200
    def mutate(self,gen): #key part of the program
        newname = self.name+str(gen) #give the descendant a name based on its ancester
        self.name = newname 
        for key,value in self.value.items():
            self.value[key] = random.uniform(-1,1)+self.value[key] #minor modification to its map legend
        for direction in ["l","r","u","d"]:
            for i in range(0,2*self.eye_sight+1):
                for j in range(0,2*self.eye_sight+1):
                    if direction == "l":
                        self.l_heuristic[i][j] += random.uniform(-1,1) #modification/mutation to the heuristic function
                    if direction == "r":
                        self.r_heuristic[i][j] += random.uniform(-1,1)
                    if direction == "u":
                        self.u_heuristic[i][j] += random.uniform(-1,1)
                    if direction == "d":
                        self.d_heuristic[i][j] += random.uniform(-1,1)

