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
                next_room = selection_tuple[1]
                next_direction = selection_tuple[0]
                # random room object is added to stack
                # and popped off (as current_room) in next iteration
                s.push(next_room)
                # adding next direction room id to current room in adjacency graph
                adjacency_graph[current_room.id][next_direction] = next_room.id
                # checking if next room is in adjacency graph and adding it if not
                if next_room.id not in adjacency_graph:
                    next_room_exits = next_room.get_exits()
                    adjacency_graph[next_room.id] = {
                        e: "?" for e in next_room_exits}
                # getting opposite direction
                # adding current room id to next room in adjacency graph
                opposite_direction = opposites[next_direction]
                adjacency_graph[next_room.id][opposite_direction] = current_room.id

                # direction from randomly selected room
                # is used to make player travel
                player.travel(next_direction)
                traversal_path.append(next_direction)
    # We've hit a dead end, so now we need to use bfs to turn around
    # and find the next room with an unexplored exit
    q = Queue()
    # get all exits in the current room
    exits = player.current_room.get_exits()
    # add all exits to the queue
    # note we add a tuple containing the room object as well
    # as the direction that the room is in
    for e in exits:
        next_room = player.current_room.get_room_in_direction(e)
        q.enqueue((e, next_room))
    # loop through queue and break if
    # the queue is empty or if we've found an unexplored exit
    while q.size() and ("?" not in exits):
        curr_tuple = q.dequeue()
        # destructure the room object and the room direction from
        # dequeued tuple
        curr_room = curr_tuple[1]
        curr_direction = curr_tuple[0]

        # travel to the dequeued direction
        # and this direction to our travel path list
        player.travel(curr_direction)
        traversal_path.append(curr_direction)

        # get the exits for the dequeued room object
        # (this is the reason that we included our room obj in the tuple)
        exits = curr_room.get_exits()
        # iterate over the exit list and get the room objects for each
        # enqueue a tuple of each room object and direction for the next iteration
        for e in exits:
            next_room = curr_room.get_room_in_direction(e)
            q.enqueue((e, next_room))


# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)


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
