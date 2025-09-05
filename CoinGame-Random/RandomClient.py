import random
import sys

from google.protobuf.internal import decoder
import CoinGame_pb2 as CoinGame
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

    # read coin game state
    state = dp.read(stream, CoinGame.CoinGameState)
    print()
    print("state:")
    print(state)

    # send random move selection
    action = CoinGame.CoinGameAction()
    
    # find rows that have coins
    available_rows = [i for i, coins in enumerate(state.coinCount) if coins > 0]
    
    if available_rows:
        # select a random row with coins
        selected_row = random.choice(available_rows)
        # select random number of coins to remove (1 to min(maxPick, coins in row))
        max_remove = min(state.maxPick, state.coinCount[selected_row])
        remove_count = random.randint(1, max_remove)
        
        print(f"Selecting row {selected_row}, removing {remove_count} coins")
        action.selectedRow = selected_row
        action.removeCount = remove_count
    else:
        # fallback if no coins available (shouldn't happen in normal gameplay)
        action.selectedRow = 0
        action.removeCount = 1
    
    dp.write(stream, action)
    stream.flush()

    # read result (but ignore it)
    dp.read(stream, CoinGame.CoinGameResult)