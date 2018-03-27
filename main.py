import operator
import random
import copy
from helper import *
from agent_class import *
import sys
import numpy
import matplotlib.pyplot as plt


def main(map_size,eye_sight,output_file):
    max_gen = 250
    map_x = int(map_size)
    map_y = int(map_size)
    output_txt = str(output_file)+".txt"
    output_png = str(output_file)+".png"
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
    x=[]

    while gen_count < max_gen:
        gen_count = gen_count+1
        x.append(gen_count)
        print (gen_count)
        run_game(new_batch,world_map)
        survivor = new_evaluate(new_batch)
        survivor[0].brief_info()
        history.append(survivor[0].score)
        with open(output_txt, "a") as myfile:
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
    plt.plot(x,history)
    y_mean = [numpy.mean(history)]*len(x)
    z = numpy.polyfit(x,history,1)
    p = numpy.poly1d(z)
    plt.plot(x,p(x),label="Trend Line")
    plt.plot(x,y_mean,linestyle='--',label='Avg:'+str(numpy.mean(history)))
    plt.legend()
    plt.savefig(output_png)
    plt.gcf().clear()
    plt.close()
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print (len(sys.argv))
        print ("please input arguments in the following fashion: ")
        print ("map_size, how far can the units see, filename of the output file")
    else:
        main(sys.argv[1],sys.argv[2],sys.argv[3])