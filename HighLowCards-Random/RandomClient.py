import random
import sys

from google.protobuf.internal import decoder
import HighLowCards_pb2 as HighLowCards
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

    # read play state
    state = dp.read(stream, HighLowCards.HighLowCardsState)
    print()
    print("state:")
    print(state)

    # send random response
    action = HighLowCards.HighLowCardsAction()
    if (random.randint(0, 1) == 0):
        print("Sending prediction 'lower'")
        action.action = HighLowCards.HighLowChoice.LOW
    else:
        print("Sending prediction 'higher'")
        action.action = HighLowCards.HighLowChoice.HIGH
    dp.write(stream, action)
    stream.flush()

    # read result
    dp.read(stream,HighLowCards.HighLowCardsReward)