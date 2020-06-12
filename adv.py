from room import Room
from player import Player
from world import World

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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def my_direction(current_room, visited_rooms):
    exits = []

    for exit in current_room.get_exits():
        if room_graph[current_room.id][1][exit] not in visited_rooms:
            exits.append(exit)
    return exits

def seek_room():
    visited_rooms = set()
    visited_rooms.add(player.current_room.id)
    path = []

    
    while len(visited_rooms) < len(room_graph.keys()):
        current_room = player.current_room.id
        exits = my_direction(player.current_room, visited_rooms)

        if len(exits) == 0: 
            exit_path = path.pop()
            player.travel(exit_path) 
            traversal_path.append(exit_path) 
            continue 

        for exit_path in exits:
            visited_rooms.add(room_graph[current_room][1][exit_path]) 
            traversal_path.append(exit_path)  

            if exit_path == "n":
                path.append("s")
            elif exit_path == "s":
                path.append("n")
            elif exit_path == "w":
                path.append("e")
            else:
                path.append("w")
            player.travel(exit_path)
            break

seek_room()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
