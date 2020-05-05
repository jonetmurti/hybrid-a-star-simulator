from file_parser import map_loader, solution_saver

track_id, start_pos, end_pos, track_identifier, track = map_loader("test/map1.txt")

movement = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0],
    [-1, 1],
    [1, 1],
    [-1, -1],
    [1, -1]
]

def euclidean_dist(start_pos, end_pos):
    return ((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5

class Node:
    def __init__(self, position, goal_position):
        self.position = [position[0], position[1]]
        self.parent = None
        self.h = euclidean_dist(self.position, goal_position)
        self.g = 0

def permitted(node, track_identifier):
    if (node.position[0] < len(track) and node.position[0] >= 0
        and node.position[1] < len(track) and node.position[1] >= 0):

        return track[node.position[0]][node.position[1]] == track_identifier

    return False

def path_reconstruction(expand_node):
    path = []
    current = expand_node

    while current.parent:
        path.append(current.position)
        current = current.parent

    path.append(current.position)

    return path[::-1]

def node_in_set(check_node, node_set):
    for node in node_set:
        if node.position[0] == check_node.position[0] and node.position[1] == check_node.position[1]:
            return node

    return None

def a_star(start_position, goal_position, track_identifier):
    parent_node = Node(start_position, goal_position)

    live_node = set()
    expanded_node = set()

    live_node.add(parent_node)

    while live_node:
        expand_node = min(live_node, key=lambda o:o.h + o.g)

        if expand_node.position[0] == goal_position[0] and expand_node.position[1] == goal_position[1]:
            return path_reconstruction(expand_node)

        live_node.remove(expand_node)
        expanded_node.add(expand_node)

        for move in movement:
            new_node = Node([move[0] + expand_node.position[0], move[1] + expand_node.position[1]], goal_position)
            if not node_in_set(new_node, expanded_node):
                if permitted(new_node, track_identifier):
                    new_node.g = expand_node.g + euclidean_dist(new_node.position, expand_node.position)
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

path = a_star(start_pos, end_pos, track_identifier)
print("rute yang dihasilkan A* : ")
print(path)
solution_saver(track_id, path, "test/a-star.txt")