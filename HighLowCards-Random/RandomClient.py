import random

from google.protobuf.internal import decoder
import HighLowCards_pb2 as HighLowCards
import delimited_protobuf as dp
import socket

# connect to the server running on locahost, port 9000

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("localhost", 9000))

# create input and output streams
stream = connection.makefile(mode='rwb')

while True:

    # read play state
    state = dp.read(stream, HighLowCards.HighLowCardsState)

    print("state:")
    print(state)

    # send random response
    action = HighLowCards.HighLowCardAction()
    if (random.randint(0, 1) == 0):
        action.action = HighLowCards.HighLowChoice.LOW
    else:
        action.action = HighLowCards.HighLowChoice.HIGH

    print("Sending action")
    dp.write(stream, action)
    stream.flush()

    # read result
    dp.read(stream,HighLowCards.HighLowCardsResult)