import operator
import random
import copy

def run_game(agent_list,world_map):
    for i in range(0,1000):
        for agent in agent_list:
            direction = agent.think(world_map)
            agent.move(direction,world_map)
def setup(map_x,map_y):
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

