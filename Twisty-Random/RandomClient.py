import random
import sys

from google.protobuf.internal import decoder
import Twisty_pb2 as Twisty
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

    # read twisty state
    state = dp.read(stream, Twisty.TwistyState)
    print()
    print("state:")
    print(state)

    # send random move selection
    action = Twisty.TwistyAction()
    
    # select random move from valid moves
    if state.validMoves:
        selected_move = random.choice(state.validMoves)
        print(f"Selected move: {selected_move}")
        action.move = selected_move
    else:
        # fallback if no valid moves (shouldn't happen in normal gameplay)
        print("No valid moves available")
        action.move = "RESET"
    
    dp.write(stream, action)
    stream.flush()

    # read result (but ignore it)
    dp.read(stream, Twisty.TwistyResult)