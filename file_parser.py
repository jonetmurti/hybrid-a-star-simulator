# Map Structure :
# Map id
# Map size
# Start Position
# Goal Position
# track and obstacle identifier
# The Map

def map_loader(filename):
    f = open(filename, "r")

    track_id = int(f.readline())
    track_size = int(f.readline())
    start_pos = [int(x) for x in f.readline().split(" ")]
    end_pos = [int(x) for x in f.readline().split(" ")]
    track_identifier = int(f.readline())

    track = []
    for i in range(track_size):
        row = [int(x) for x in f.readline().split(" ")]
        track.append(row)

    f.close()
    return track_id, start_pos, end_pos, track_identifier, track

def solution_saver(track_id, solution_list, filename):
    f = open(filename, "w")
    text = []
    text.append(str(track_id) + "\n")

    text.append(str(len(solution_list)) + "\n")
    for path in solution_list:
        line = ""
        for elmt in path :
            line += (str(elmt) + " ")
        new_line = line[:len(line) - 1] + "\n"
        text.append(new_line)

    f.writelines(text)

    f.close()

def solution_loader(track_id, filename):
    f = open(filename, "r")

    solution_id = int(f.readline())
    if solution_id != track_id:
        f.close()
        raise Exception("Invalid solution file")

    solution_len = int(f.readline())

    solution = []
    for i in range(solution_len):
        solution.append([int(x) for x in f.readline().split(" ")])

    f.close()

    return solution