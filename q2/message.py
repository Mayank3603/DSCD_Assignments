import time
import zmq
import threading
import json

context = zmq.Context()



group_info = {}

socket = context.socket(zmq.REP)
socket.bind("tcp://*:8888")

def func(message):
    
    socket = message[3]
    if message[0] == "group_register":
        name = message[1]
        port = message[2]
        if port not in  group_info.keys():
            group_info[port] = name
            print(f"JOIN REQUEST FROM {name}: {port}")
            time.sleep(1)
            socket.send_string("SUCCESS")
        else:
            print(f"JOIN REQUEST FROM {name}: {port}")
            time.sleep(1)
            socket.send_string("Failed")
            
    
    elif message[0] == "user":
        name = message[1]
        port = message[2]
        print(f"GROUP LIST REQUEST FROM {name}: {port}")
        time.sleep(1)
        data = json.dumps(group_info)
        socket.send_string(data)




while True:
    message = socket.recv_string()
    msg = json.loads(message)
    msg.append(socket)
    func(msg)
