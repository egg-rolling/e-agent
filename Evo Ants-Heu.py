import operator
import random
import copy
from helper import *
from agent_class import *
map_x = 300
map_y = 300
eye_sight = 2

# In[3]:

#main
world_map = setup(map_x,map_y) 
agent_list = []
f=open("agent names.txt",'r')
for line in f:
    init_x = random.randint(0,map_x-1)
    init_y = random.randint(0,map_y-1)
    while world_map[init_x][init_y] != " ":
        init_x = random.randint(0,map_x-1)
        init_y = random.randint(0,map_y-1)
    new_agent = Agent(line.strip(),init_x,init_y,map_x,map_y)
    new_agent.init_born()
    #new_agent.info()
    loc = new_agent.whereIam()
    world_map[loc[0]][loc[1]] = "M"
    agent_list.append(new_agent)
output_map(world_map,"init_map.txt")
run_game(agent_list,world_map)
survivor = new_evaluate(agent_list)

new_batch = []
for agent in survivor:
    new_batch.append(agent)
    for i in range(0,5):
        new_kid = copy.deepcopy(agent)
        new_kid.mutate(i)
        new_batch.append(new_kid)

world_map = setup(map_x,map_y)
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
    run_game(new_batch,world_map)
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
    world_map = setup(map_x,map_y)
    print ("Current population:",len(new_batch))
    for agent in new_batch:
        #print agent.name
        init_x = random.randint(0,map_x-1)
        init_y = random.randint(0,map_y-1)
        while world_map[init_x][init_y] != " ":
            init_x = random.randint(0,map_x-1)
            init_y = random.randint(0,map_y-1)
        agent.redeploy(init_x,init_y)

