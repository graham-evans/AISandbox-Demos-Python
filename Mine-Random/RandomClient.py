import random
import sys

from google.protobuf.internal import decoder
import Mine_pb2 as Mine
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

    # read mine state
    state = dp.read(stream, Mine.MineState)
    print()
    print("state:")
    print(state)

    # send random action
    action = Mine.MineAction()
    
    # select random coordinates within the board
    x = random.randint(0, state.width - 1)
    y = random.randint(0, state.height - 1)
    
    # randomly choose to dig or place flag
    if random.randint(0, 1) == 0:
        selected_action = Mine.FlagAction.DIG
        action_name = "DIG"
    else:
        selected_action = Mine.FlagAction.PLACE_FLAG
        action_name = "PLACE_FLAG"
    
    print(f"Action: {action_name} at position ({x}, {y})")
    action.x = x
    action.y = y
    action.action = selected_action
    
    dp.write(stream, action)
    stream.flush()

    # read result (but ignore it)
    dp.read(stream, Mine.MineResult)