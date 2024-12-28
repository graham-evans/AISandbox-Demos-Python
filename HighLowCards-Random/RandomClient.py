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
    state = dp.read(stream,HighLowCards.HighLowCardsState)

    print("state:")
    print(state)

    # are we asked for an action?
    if state.signal == HighLowCards.Signal.PLAY:

        print("Sending action")

        action = HighLowCards.HighLowCardAction()
        action.action = HighLowCards.HighLowChoice.LOW

        dp.write(stream,action)
        stream.flush()

