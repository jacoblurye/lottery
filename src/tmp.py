from ttc import TTC

graph = {1:[3, 5],2:[1],3:[1,2,4],4:[3,5],5:[1,2,4],6:[1]}
print TTC._find_cycles(graph)