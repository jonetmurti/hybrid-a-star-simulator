import math

class Node:
    def __init__(self, position, theta):
        self.dis_position = [math.floor(position[0]), math.floor(position[1])]
        self.con_position = [position[0], position[1]]
        self.theta = theta
    
    def __repr__(self):
        return (
            "Position    : " + str(self.con_position[0]) + "," + str(self.con_position[1]) +
            "\nOrientation : " + str(self.theta) +
            "\n"
        )
    
    def update(self, position, theta):
        self.dis_position = [math.floor(position[0]), math.floor(position[1])]
        self.con_position = [position[0], position[1]]
        self.theta = theta

object_size = 0.2
distance = 10
steering_angle = math.pi/6

movement = [[1, 0], [1, math.atan(math.pi/10)]]

def turning_angle(size, dist, alpha):
    return (dist/size)*math.tan(alpha)

node = Node([0, 0], math.pi/2)
print(node)
beta = turning_angle(object_size, movement[0][0], movement[0][1])
if abs(beta) < 0.001:
    R = movement[0][0]
    new_x = node.con_position[0] + R*math.sin(node.theta)
    new_y = node.con_position[1] + R*math.cos(node.theta)
else:
    R = movement[0][0]/beta
    cx = node.con_position[0] - R*math.cos(node.theta)
    cy = node.con_position[1] + R*math.sin(node.theta)
    new_x = cx + R*math.cos(node.theta + beta)
    new_y = cy - R*math.sin(node.theta +beta)

node.update([new_x, new_y], node.theta + beta)
print(node)

beta = turning_angle(object_size, movement[1][0], movement[1][1])
if abs(beta) < 0.001:
    R = movement[0][0]
    new_x = node.con_position[0] + R*math.sin(node.theta)
    new_y = node.con_position[1] + R*math.cos(node.theta)
else:
    R = movement[0][0]/beta
    cx = node.con_position[0] - R*math.cos(node.theta)
    cy = node.con_position[1] + R*math.sin(node.theta)
    new_x = cx + R*math.cos(node.theta + beta)
    new_y = cy - R*math.sin(node.theta +beta)

node.update([new_x, new_y], node.theta + beta)
print(node)