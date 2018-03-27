
# e-agent v1.0
So this is a little side project of mine. 
The idea would be to have the agent evolving its heuristic function on its on through hundreds of iteration. 

The problem is proposed as this: 
There's a finite size grid map with finite size, there are obstacles, food scattered on the map.
An agent is thrown into a random location on the map. He can see within a few blocks away from itself, how does the agent collect enough food within limited round?

The approach I took towards this hypothetical problem is to have them going through generations of trial and error. The program deploys a set of agents with randomized heuristic function. For each turn, each agent is allowed to look around, run calculation through its heuristic function, then make a step towwards either left, right, down, or up. After 200 turns, the system tally the score and harvest the best scorer. These best agents are able to multiply and make descendents. Their score will be cleared but they keep their heuristic function (like their brain). 

However random minor mutation were applied to all the descendents. After mutation, all descendents and ancestors are entered into the map again. 

Through a few hundred simulations, we can observe significant growth. 

execute the program by running

python main.py (size of the map) (How Far can the agents see) (output file name without .txt/png)

The program produces a PNG file graphing the highest score of every round. I also provided a txt version of the data if you want to graph your own version. 

