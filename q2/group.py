import zmq
from datetime import datetime
import threading
import json 

class group:
    def __init__(self, name, ip,port):
        self.context = zmq.Context()
       
        self.name = name
        self.ip = ip
        self.port = port
        self.ip_port = ip+":"+port
        self.users = {}
        self.messages = {}
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://{self.ip_port}")
        
    def handle_user_request(self, request):  
        if request[0] == "joinGroup":
            user_uuid = request[1]
            if user_uuid in self.users.keys():
                return "User Exists"
            self.users[user_uuid] = 1
            print(f"JOIN REQUEST FROM {user_uuid}")
            out = "SUCCESS"
            return out
        
        elif request[0] == "leaveGroup":
            user_uuid = request[1]
            del self.users[user_uuid]
            print(f"LEAVE REQUEST FROM {user_uuid}")
            out = "SUCCESS"
            return out
        
        elif request[0] ==  "getMessages":
            user_uuid = request[1]
            timestamp = request[2]
            print(f"MESSAGE REQUEST FROM {user_uuid}")
            if user_uuid in self.users:
                send_message = []
                if timestamp:
                 
                    timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    for i in self.messages.keys():
                        a = i
                        i = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
                     
                        if i >= timestamp_dt:
                            for j in self.messages[a]:
                                send_message.append(j)
                else:
                    for i in self.messages.keys():
                        for j in self.messages[i]:
                            send_message.append(j)  
            else:
                send_message = "FAILED"      

            return send_message
        
        elif request[0] == "sendMessage":
            user_uuid = request[1]
            message = request[2]
            timestamp = datetime.now()
            formatted_datetime = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(formatted_datetime)
            ret = "FAILED"
            print(f"MESSAGE SEND FROM {user_uuid}")
            if user_uuid in self.users:
                ret = "SUCCESS"
                if formatted_datetime in self.messages.keys():
                    self.messages[formatted_datetime].append(message)
                   
                    
                    return ret
                else:
                  
                    self.messages[formatted_datetime] = [message]
                    return ret
            else:
                return ret
            
            
            
    def serve_requests(self):
        while True:
            request = self.socket.recv_string()
            req = json.loads(request)
            response = self.handle_user_request(req)
            if isinstance(response, list):
                response = json.dumps(response)
            self.socket.send_string(response)



context1 = zmq.Context()
socket1 = context1.socket(zmq.REQ)
socket1.connect("tcp://127.0.0.1:8888")
    
while True:
    n =1
    ans = input("Want To register in message_server yes/no: ")
    if ans == "yes":
        name = input("Enter Name of the Group: ")
        port = input(f"Enter The port Number of {name}: ")
        group_data = ["group_register",name,port]
        msg = json.dumps(group_data)
        socket1.send_string(msg)
        recv_msg = socket1.recv_string()
        if recv_msg == "SUCCESS":
            print(recv_msg)
            ip = "127.0.0.1"
            groupp = group(name,ip,port)
            
            group_thread = threading.Thread(target=groupp.serve_requests).start()
            # group_thread.join()