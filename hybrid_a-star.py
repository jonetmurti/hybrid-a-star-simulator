from file_parser import map_loader, solution_saver

track_id, start_pos, end_pos, track_identifier, track = map_loader("test/map1.txt")

import math

movement = [[1, 0], [1, -1], [1, 1]]
# (Front, Front-Right, Front-Left)


def euclidean_dist(start_pos, end_pos):
    return ((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5

class Node:
    def __init__(self, position, theta,  goal_position):
        self.dis_position = [math.floor(position[0]), 
                            math.floor(position[1])]
        self.con_position = [position[0], position[1]]
        # To simplify, I only use discrete orientation (0, 1, 2, 3)
        self.theta = theta
        self.parent = None
        self.h = euclidean_dist(self.dis_position, goal_position)
        self.g = 0

def permitted(node, track_identifier):
    if (node.dis_position[0] < len(track) and node.dis_position[0] >= 0
        and node.dis_position[1] < len(track) and node.dis_position[1] >= 0):

        return track[node.dis_position[0]][node.dis_position[1]] == track_identifier

    return False

def path_reconstruction(expand_node):
    path = []
    current = expand_node

    while current.parent:
        elmt = [current.dis_position[0], current.dis_position[1], current.theta]
        path.append(elmt)
        current = current.parent

    elmt = [current.dis_position[0], current.dis_position[1], current.theta]
    path.append(elmt)

    return path[::-1]

def node_in_set(check_node, node_set):
    for node in node_set:
        if node.dis_position[0] == check_node.dis_position[0] and node.dis_position[1] == check_node.dis_position[1]:
            return node

    return None

# def turning_angle(size, dist, alpha):
#     return (dist/size)*math.tan(alpha)

# TODO : CHANGE THIS
def hybrid_a_star(start_position, goal_position, initial_orientation, track_identifier):
    parent_node = Node(start_position, initial_orientation, goal_position)

    live_node = set()
    expanded_node = set()

    live_node.add(parent_node)
    while live_node:
        expand_node = min(live_node, key=lambda o:o.h + o.g)

        if expand_node.dis_position[0] == goal_position[0] and expand_node.dis_position[1] == goal_position[1]:
            return path_reconstruction(expand_node)

        live_node.remove(expand_node)
        expanded_node.add(expand_node)

        for move in movement:
            # current orientation
            beta = (expand_node.theta + 1)*math.pi/2
            if beta >= 2*math.pi:
                beta = 0

            # Assume that R = 1
            new_x = expand_node.con_position[1] + move[0]*int(math.cos(beta))
            new_y = expand_node.con_position[0] - move[0]*int(math.sin(beta))

            if (move[1] != 0):
                beta = beta + move[1]*math.pi/2
                if beta >= 2*math.pi:
                    beta = 0
                elif beta < 0:
                    beta += 2*math.pi
                new_x += move[0]*int(math.cos(beta))
                new_y -= move[0]*int(math.sin(beta))

            new_orientation = int(beta/(math.pi/2)) - 1
            if new_orientation < 0:
                new_orientation = 3

            new_node = Node([new_y, new_x], new_orientation, goal_position)
            #print([new_y, new_x], new_orientation)
            ##############################################
            if not node_in_set(new_node, expanded_node):
                if permitted(new_node, 0):
                    new_node.g = expand_node.g + euclidean_dist(new_node.dis_position, expand_node.dis_position)
                    new_node.parent = expand_node
                    temp_node = node_in_set(new_node, live_node)
                    if temp_node:
                        if new_node.g < temp_node.g:
                            live_node.remove(temp_node)
                            live_node.add(new_node)
                    else:
                        live_node.add(new_node)
                else:
                    expanded_node.add(new_node)
                                    
    return []

path = hybrid_a_star(start_pos, end_pos, 3, track_identifier)
new_path = [[elmt[0], elmt[1]] for elmt in path]
print("rute yang dihasilkan Hybrid A* : ")
print(new_path)
solution_saver(track_id, path, "test/hybrid_a-star.txt")