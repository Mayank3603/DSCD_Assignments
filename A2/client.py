import grpc
import node_pb2
import node_pb2_grpc

class RaftClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = node_pb2_grpc.RaftServiceStub(self.channel)
        self.currLeaderAddr=server_address

    def serve_get(self, request):
        response = self.stub.ServeGet(request)
        return response

    def serve_set(self, request):
        response = self.stub.ServeSet(request)
        return response



def main():
    node_ips = {1:'localhost:50051', 2:'localhost:50052', 3:'localhost:50053'}
    leaderip=node_ips[1]
    client = RaftClient(leaderip)
    while True:
        op=input("Operation:")
        if(op=="set"):
            key=input("Enter key:")
            value=input("Enter value:")
            try:
                serve_request = node_pb2.SetRequest(key=key, value=value)
                response = client.serve_set(serve_request)
                if(response.Success=="False"):
                    if(response.LeaderID==-1):
                        print("No leader found")
                        continue
                    client.currLeaderAddr=ips[response.LeaderID]
                    print("Leader changed to:",client.currLeaderAddr)

                print("Set Response:", response)
            except:
                print("No current active node found")
        else:
            try:
                key=input("Enter key:")
                serve_request = node_pb2.GetRequest(key=key)
                response = client.serve_get(serve_request)
                print("Get Response:", response.value)
                if(response.success=="False"):
                    if(response.LeaderID==-1):
                        print("No leader found")
                        continue
                    client.currLeaderAddr=ips[response.LeaderID]
                    print("Leader changed to:",client.currLeaderAddr)
            except:
                print("No current active node found")
        

if __name__ == "__main__":
    main()
