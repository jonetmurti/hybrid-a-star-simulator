from file_parser import map_loader, solution_loader
import cv2 as cv
import numpy as np

track_id, start_pos, end_pos, track_identifier, track = map_loader("test/map1.txt")
a_star = solution_loader(track_id, "test/a-star.txt")
hybrid = solution_loader(track_id, "test/hybrid_a-star.txt")

def map_layout(track, track_size, screen_length, start_pos, end_pos):
    image = np.ones((screen_length,screen_length,3), np.uint8)*255
    area_width = screen_length//track_size
    for i in range(track_size - 1):
        cv.line(image, ((i + 1)*area_width, 0),
                ((i + 1)*area_width, screen_length), (0, 0, 0), thickness=2)
        cv.line(image, (0, (i + 1)*area_width),
                (screen_length, (i + 1)*area_width), (0, 0, 0), thickness=2)

    for i in range(track_size):
        for j in range(track_size):
            if track[i][j] != track_identifier:
                cv.rectangle(image, (j*area_width, i*area_width), 
                            ((j + 1)*area_width, (i + 1)*area_width), (0, 0, 0), -1)

    cv.circle(image, (start_pos[1]*area_width + area_width//2, start_pos[0]*area_width + area_width//2), area_width//5, (255, 0, 0), -1)
    cv.circle(image, (end_pos[1]*area_width + area_width//2, end_pos[0]*area_width + area_width//2), area_width//5, (0, 0, 255), -1)

    return image

def a_star_draw(image, solution, screen_length):
    area_width = screen_length//track_size
    half_area_width = area_width//2
    for i in range(len(solution) - 1):
        cv.line(image, (solution[i][1]*area_width + half_area_width, solution[i][0]*area_width + half_area_width),
                (solution[i + 1][1]*area_width + half_area_width, solution[i + 1][0]*area_width + half_area_width), (0, 255, 0), 2)

def hybrid_draw(image, solution, screen_length):
    area_width = screen_length//track_size
    half_area_width = area_width//2
    for i in range(len(solution) - 1):
        if (solution[i][0] == solution[i + 1][0] or solution[i][1] == solution[i + 1][1]):
            cv.line(image, (solution[i][1]*area_width + half_area_width, solution[i][0]*area_width + half_area_width),
                    (solution[i + 1][1]*area_width + half_area_width, solution[i + 1][0]*area_width + half_area_width), (0, 255, 0), 2)
        else:
            if solution[i][2] == 0 and solution[i + 1][2] == 3 or solution[i][2] == 1 and solution[i + 1][2] == 2:
                angle = 180
                x = max(solution[i][1], solution[i + 1][1])
                y = max(solution[i][0], solution[i + 1][0])
            elif solution[i][2] == 0 and solution[i + 1][2] == 1 or solution[i][2] == 3 and solution[i + 1][2] == 2:
                angle = 270
                x = min(solution[i][1], solution[i + 1][1])
                y = max(solution[i][0], solution[i + 1][0])
            elif solution[i][2] == 1 and solution[i + 1][2] == 0 or solution[i][2] == 2 and solution[i + 1][2] == 3:
                angle = 90
                x = max(solution[i][1], solution[i + 1][1])
                y = min(solution[i][0], solution[i + 1][0])
            else:
                angle = 0
                x = min(solution[i][1], solution[i + 1][1])
                y = min(solution[i][0], solution[i + 1][0])

            mid_x = x*area_width + half_area_width
            mid_y = y*area_width + half_area_width
            cv.ellipse(image, (mid_x, mid_y), (area_width, area_width), angle, 0, 90, (0, 255, 0), 2)

screen_length = 640
track_size = len(track)

a_star_map = map_layout(track, track_size, screen_length, start_pos, end_pos)
hybrid_map = map_layout(track, track_size, screen_length, start_pos, end_pos)

a_star_draw(a_star_map, a_star, screen_length)
hybrid_draw(hybrid_map, hybrid, screen_length)

cv.imshow("hybrid_a_star", hybrid_map)
cv.imshow("a_star", a_star_map)
cv.waitKey(0)