
import zmq
import json
context = zmq.Context()

import uuid
import time

unique_id = str(uuid.uuid1())
while True:
    
    print("1. Access The Group List")
    print("2. Join Group")
    print("3. Leave Group")
    print("4. GetMessage")
    print("5. SendMessage")
    num = int(input("Enter the operation you want to do: "))
    if num == 1:
      
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:8888")
        print("Connecting to Message  server…")
        print("Sending request for getting group  list …")
        data  = ["user","user1",unique_id] 
        user_data = json.dumps(data)
        socket.send_string(user_data)
            
        message = socket.recv_string()
        group_data = json.loads(message)
        
        k = 1
        for i in group_data:
            print(f"Server Name {k} - {group_data[i]} : {i}")
            k += 1
        socket.close()
    
    elif num == 2:
        name = input("name of the group_server: ")
        port = input(f"port number of the group {name}: ")
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://127.0.0.1:{port}")
        data = ["joinGroup",unique_id]
        print("Connecting to Group  server…")
        print(f"Sending request to Group server for joining Group {name} …")
        msg = json.dumps(data)
        socket.send_string(msg)
        recv = socket.recv_string()
        print(recv)
        socket.close()
        time.sleep(1)
        
    elif num == 3:
        name = input("name of the group_server: ")
        port = input(f"port number of the group {name}: ")
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://127.0.0.1:{port}")
        data = ["leaveGroup",unique_id]
        print("Connecting to Group  server…")
        print(f"Sending request to Group server for leaving Group {name} …")
        msg = json.dumps(data)
        socket.send_string(msg)
        recv = socket.recv_string()
        print(recv)
        socket.close()
        time.sleep(1)
        
    elif num == 4:
        name = input("name of the group_server: ")
        port = input(f"port number of the group {name}: ")
        message = input("Timestamp: ")
        socket1 = context.socket(zmq.REQ)
        socket1.connect(f"tcp://127.0.0.1:{port}")
        data = ["getMessages",unique_id,message]
        print("Connecting to Group  server…")
        print(f"Sending request to Group server {name} for getting message  …")
        msg = json.dumps(data)
        socket1.send_string(msg)
        recv = socket1.recv_string()
        print(recv)
        socket1.close()
        time.sleep(1)
        
    elif num == 5:
        name = input("name of the group_server: ")
        port = input(f"port number of the group {name}: ")
        message = input("Message to send: ")
        socket2= context.socket(zmq.REQ)
        socket2.connect(f"tcp://127.0.0.1:{port}")
        data = ["sendMessage",unique_id,message]
        print("Connecting to Group  server…")
        print(f"Sending message to Group server  {name} …")
        msg = json.dumps(data)
        socket2.send_string(msg)
        recv = socket2.recv_string()
        print(recv)
        socket2.close()
        time.sleep(1)
        