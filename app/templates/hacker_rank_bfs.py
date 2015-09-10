import fileinput
import itertools
import Queue

class Node:
    edges = []
    is_visited = False
    distance = -1

def get_nodes_dict(edges):
    nodes = {}
    sorted_edges = sorted(edges)
    grouped_edges = itertools.groupby(sorted_edges)
    
    for key1, key_values in grouped_edges:
        nodes[key1[0]] = Node()
        
    for key1, key_values in grouped_edges:
        for key2, value in key_values:
            nodes[key2].edges.append(value)
            
    return nodes

def bfs(start_node, nodes):
    q = Queue.Queue()
    root = nodes[start_node]
    root.distance = 0
    q.put(root)
    distance_string = ""
    while not q.empty():
        node = q.get()
        if not node.is_visited:
            for neighbor_id in node.edges:
                neighbor = nodes[neighbor]
                neighbor.distance = node.distance + 6
                q.put(neighbor)
            node.is_visited = True
            if node != root:
                distance_string += "{} ".format(node.distance)
    return distance_string
    
def print_distances(start_node, edges):
    nodes = get_nodes_dict(edges)
    print bfs(start_node, nodes)
    
the_input = [
'1',
'4 2',
'1 2',
'1 3',
'1'
]

new_test = True
for line in the_input #fileinput.input():
    if line:
        if new_test:
            edges = []
            new_test = False
        else:
            if len(line.split()) < 2:
                start_node = int(line)
                print_distances(start_node, edges)
            else:
                edges.append(line.split)
          
    else:
        new_test = True