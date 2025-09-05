import random
import sys

from google.protobuf.internal import decoder
import Maze_pb2 as Maze
import delimited_protobuf as dp
import socket

# connect to the server using localhost and 9000 as defaults

host = "localhost"
port = 9000

if len(sys.argv) == 2:
    port = int(sys.argv[1])
elif len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))

# create input and output streams
stream = connection.makefile(mode='rwb')

while True:

    # read maze state
    state = dp.read(stream, Maze.MazeState)
    print()
    print("state:")
    print(state)

    # send random direction
    action = Maze.MazeAction()
    directions = [Maze.Direction.NORTH, Maze.Direction.SOUTH, Maze.Direction.EAST, Maze.Direction.WEST]
    selected_direction = random.choice(directions)
    direction_names = {Maze.Direction.NORTH: "NORTH", Maze.Direction.SOUTH: "SOUTH", 
                      Maze.Direction.EAST: "EAST", Maze.Direction.WEST: "WEST"}
    print(f"Moving {direction_names[selected_direction]}")
    action.direction = selected_direction
    dp.write(stream, action)
    stream.flush()

    # read result (but ignore it)
    dp.read(stream, Maze.MazeResult)