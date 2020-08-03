from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room

adjacency_graph = {}
opposites = {"n": "s", "e": "w", "s": "n", "w": "e"}
dft_visited = []
while len(visited_rooms) < len(room_graph):

    # creating stack for dft
    s = Stack()
    s.push(player.current_room)
    # iterate over each room in a dft order

    while s.size():
        current_room = s.pop()
        exits = current_room.get_exits()
        print("current_room", current_room)
        if current_room not in visited_rooms:
            # checking if current room is in visited
            # adding current room to visited set if not
            # adding to adjacency_graph with "?" values if not
            visited_rooms.add(current_room)
            if current_room.id not in adjacency_graph:
                adjacency_graph[current_room.id] = {
                    e: "?" for e in exits}

        # if there are exits at the current room
        if len(exits) > 0:
            room_options = []
            # looping through current room exits
            # if unexplored then adding to room options list
            for e in exits:
                if adjacency_graph[current_room.id][e] == "?":
                    room_options.append((
                        e, current_room.get_room_in_direction(e)))
            # if there are rooms in room options
            # select a random room and add that to the stack
            # note: if no unexplored rooms are found
            # we will have found a dead end and the while loop will be complete
            if len(room_options) > 0:
                selection_tuple = random.choice(room_options)
                curr_room = selection_tuple[1]
                curr_direction = selection_tuple[0]
                # random room object is added to stack
                # and popped off (as current_room) in next iteration
                s.push(curr_room)
                # adding next direction room id to current room in adjacency graph
                adjacency_graph[current_room.id][curr_direction] = curr_room.id
                # checking if next room is in adjacency graph and adding it if not
                if curr_room.id not in adjacency_graph:
                    curr_room_exits = curr_room.get_exits()
                    adjacency_graph[curr_room.id] = {
                        e: "?" for e in curr_room_exits}
                # getting opposite direction
                # adding current room id to next room in adjacency graph
                opposite_direction = opposites[curr_direction]
                adjacency_graph[curr_room.id][opposite_direction] = current_room.id

                # direction from randomly selected room
                # is used to make player travel

                player.travel(curr_direction)
                traversal_path.append(curr_direction)

                # print("traversal_path after moving", traversal_path)
    # We've hit a dead end, so now we need to use bfs to turn around
    # and find the next room with an unexplored exit
    room_before_bfs = player.current_room
    qq = Queue()
    qq.enqueue([(player.current_room.id, player.current_room)])
    bfs_visited = set()
    found = False
    path = []
    while (qq.size() > 0) and (found == False) and (len(visited_rooms) < len(room_graph)):
        path = qq.dequeue()
        path_id = path[-1][0]
        path_room = path[-1][1]

        if path[-1] not in bfs_visited:
            # DO THE THING!!!
            if path_id not in adjacency_graph:
                found = True
                break
            else:
                exits = adjacency_graph[path_id]
                exit_tuples = exits.items()
                for tup in exit_tuples:
                    if tup[1] == "?":
                        found = True
                        break
            if found == True:
                break
            # DONE DOING THE THING!!!

            # mark as visited
            bfs_visited.add(path[-1])

            exits = path_room.get_exits()
            for direction in exits:
                next_room = path_room.get_room_in_direction(direction)

                new_path = list(path)
                new_path.append((next_room.id, next_room))
                qq.enqueue(new_path)
    path_back = path[1:]
    print("path_back after bfs loop", path_back)
    room_ids = [x[0] for x in path_back]
    print("player.current_room.id ||", player.current_room.id)
    print("room_ids after bfs loop", room_ids)

    directions_to_unexplored_room = []

    for room_id in room_ids:
        exit_directions = player.current_room.get_exits()
        for direction in exit_directions:
            next_room = player.current_room.get_room_in_direction(direction)
            if next_room.id == room_id:
                player.travel(direction)
                traversal_path.append(direction)


if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
