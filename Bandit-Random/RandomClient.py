import random
import sys

from google.protobuf.internal import decoder
import Bandit_pb2 as Bandit
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

    # read bandit state
    state = dp.read(stream, Bandit.BanditState)
    print()
    print("state:")
    print(state)

    # send random arm selection
    action = Bandit.BanditAction()
    selected_arm = random.randint(0, state.banditCount - 1)
    print(f"Selecting arm {selected_arm}")
    action.arm = selected_arm
    dp.write(stream, action)
    stream.flush()

    # read result (but ignore it)
    dp.read(stream, Bandit.BanditResult)