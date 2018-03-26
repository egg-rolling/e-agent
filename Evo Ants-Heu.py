
# coding: utf-8

# In[1]:



# coding: utf-8

# In[1]:

import operator
import random
import copy
map_x = 300
map_y = 300
eye_sight = 2
def run_game(agent_list):
    for i in range(0,1000):
        for agent in agent_list:
            direction = agent.think()
            agent.move(direction)
def setup():
    map_t = []
    for i in range(0,map_x):
        temp = []
        for j in range(0,map_y):
            temp.append(" ")
        map_t.append(temp)
    food_count = 0
    Wall_count = 0
    while food_count < 20000:
        x = random.randint(0,map_x-1)
        y = random.randint(0,map_y-1)
        if map_t[x][y] == " ":
            map_t[x][y] = "."
            food_count = food_count+1
    while Wall_count < 10000:
        x = random.randint(0,map_x-1)
        y = random.randint(0,map_y-1)
        if map_t[x][y] == " ":
            map_t[x][y] = "X"
            Wall_count = food_count+1
    return map_t

def out_of_bound(x,y):
    if x<0 or x>=map_x or y < 0 or y>= map_y :
        return False #this means it's out of bound
    else:
        return True
def valid_move(x,y):
    flag_1 = out_of_bound(x,y)
    if flag_1 == False:
        return False
    if world_map[x][y] == " " or world_map[x][y] == ".":
        flag_2 = True
    else:
        flag_2 = False
    return flag_2 and flag_1
def observing(location,world):
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
            elif out_of_bound(i,j) == False:
                temp.append("X")
            else:
                temp.append(world[i][j])
        vision.append(temp)

    return vision
def output_map(map_t,filename):
    thefile = open(filename, 'w')
    for item in map_t:
        #thefile.write("%s\n" % item)
        thefile.write("".join(item))
        thefile.write("\n")
def evaluate(agent_list):
    collect = []
    for agent in agent_list:
        collect.append((agent.score,agent.name))
    sorted_data = sorted(collect, key=lambda tup: tup[0],reverse=True)
    winner_name = []
    for i in range(0,10):
        winner_name.append(sorted_data[i])
    winner = []
    for agent in agent_list:
        name = agent.name
        for elem in winner_name:
            if name== elem[1]:
                winner.append(agent)
    return winner
def new_evaluate(agent_list):
    winner = []
    sorted_data =  sorted(agent_list, key=operator.attrgetter('score'),reverse = True)
    for i in range(0,10):
        winner.append(sorted_data[i])
    return winner

# In[2]:


class Agent: 
    eye_sight = 2
    def __init__(self, name,init_x,init_y):#default constructor
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
    def info(self): #for debug sake, not called within the finished program
        print ("I am", self.name)
        print ("I am at",self.x,self.y)
        print ("My score:",self.score)
        #print "My Life:",self.lifespan
    def move(self,direction): #given direction, move towards the next step, move only when it's valid.
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
        valid = valid_move(next_x,next_y)
        if valid == True: #if move failed, agent lose a turn.
            if world_map[next_x][next_y] == ".":
                self.score = self.score+1
            world_map[next_x][next_y] = "M"
            world_map[self.x][self.y] = " "
            self.x = next_x
            self.y = next_y
            #print "successful move"
        self.lifespan= self.lifespan-1 #the purpose of losing a turn is to punish action like walking into the wall repeatedly
    def whereIam(self): #helper function
        return self.x,self.y
    def think(self): #function called by the agent, performing matrix calculation to produce a heuristic value
        #returns a direction with the highest heuristic value
        location = self.whereIam()
        loc = (location[0],location[1])
        saw = observing(loc,world_map)
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


# In[3]:

#main
world_map = setup() 
agent_list = []
f=open("agent names.txt",'r')
for line in f:
    init_x = random.randint(0,map_x-1)
    init_y = random.randint(0,map_y-1)
    while world_map[init_x][init_y] != " ":
        init_x = random.randint(0,map_x-1)
        init_y = random.randint(0,map_y-1)
    new_agent = Agent(line.strip(),init_x,init_y)
    new_agent.init_born()
    #new_agent.info()
    loc = new_agent.whereIam()
    world_map[loc[0]][loc[1]] = "M"
    agent_list.append(new_agent)
output_map(world_map,"init_map.txt")
run_game(agent_list)
survivor = new_evaluate(agent_list)

new_batch = []
for agent in survivor:
    new_batch.append(agent)
    for i in range(0,5):
        new_kid = copy.deepcopy(agent)
        new_kid.mutate(i)
        new_batch.append(new_kid)

world_map = setup()
for agent in new_batch:
    init_x = random.randint(0,map_x-1)
    init_y = random.randint(0,map_y-1)
    while world_map[init_x][init_y] != " ":
        init_x = random.randint(0,map_x-1)
        init_y = random.randint(0,map_y-1)
    agent.redeploy(init_x,init_y)


gen_count = 0
history = []

while gen_count < 255:
    gen_count = gen_count+1
    print (gen_count)
    run_game(new_batch)
    survivor = new_evaluate(new_batch)
    survivor[0].info()
    history = survivor[0].score
    with open("Parents included2.txt", "a") as myfile:
        myfile.write(str(survivor[0].score)+",")
    new_batch = []
    for agent in survivor:
        new_batch.append(agent)
        for i in range(1,6):
            new_kid = copy.deepcopy(agent)
            new_kid.mutate(i)
            new_batch.append(new_kid)
    world_map = setup()
    print ("Current population:",len(new_batch))
    for agent in new_batch:
        #print agent.name
        init_x = random.randint(0,map_x-1)
        init_y = random.randint(0,map_y-1)
        while world_map[init_x][init_y] != " ":
            init_x = random.randint(0,map_x-1)
            init_y = random.randint(0,map_y-1)
        agent.redeploy(init_x,init_y)

