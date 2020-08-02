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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
while len(visited_rooms) < len(room_graph):

    # creating stack for dft
    s = Stack()
    s.push(player.current_room)
    # iterate over each room in a dft order

    while s.size():
        current_room = s.pop()
        exits = current_room.get_exits()
        # print("current_room", current_room)
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
    # q = Queue()
    # bfs_visited = set()
    # path = [player.current_room]
    # q.enqueue(path)
    unexplored_exit_count = 0
    back_pedal_count = -1
    back_pedal_path = []
    while (unexplored_exit_count == 0) and (len(visited_rooms) < len(room_graph)):

        # current_path = q.dequeue()

        # current_room = current_path[-1]

        current_exits = player.current_room.get_exits()

        # print("current_exits", current_exits)
        for exit in current_exits:
            if adjacency_graph[player.current_room.id][exit] == "?":
                unexplored_exit_count += 1

        if unexplored_exit_count == 0:
            # print("traversal_path", traversal_path)
            # print("traversal_path[back_pedal_count]",
            #   traversal_path[back_pedal_count])
            next_direction = traversal_path[back_pedal_count]
            # print("BEFORE player.current_room.id", player.current_room.id)
            opposite_direction = opposites[next_direction]
            # print(f"moving {opposite_direction} from {player.current_room.id}")
            player.travel(opposite_direction)
            back_pedal_path.append(opposite_direction)
            # print("AFTER player.current_room.id", player.current_room.id)
            back_pedal_count -= 1

            #     if current_room not in bfs_visited:
            #         bfs_visited.add(current_room.id)

            #     for exit in current_exits:
            #         exit_path = current_path.copy()
            #         exit_path.append(exit)
            #         new_room = current_room.get_room_in_direction(exit)
            # for move in traversal_path:
            #     player.travel(move)
            #     visited_rooms.add(player.current_room)
    traversal_path.extend(back_pedal_path)

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
