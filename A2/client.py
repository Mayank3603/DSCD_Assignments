import grpc
import node_pb2
import node_pb2_grpc

class RaftClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = node_pb2_grpc.RaftServiceStub(self.channel)

    def serve_get(self, request):
        response = self.stub.ServeGet(request)
        return response

    def serve_set(self, request):
        response = self.stub.ServeSet(request)
        return response



def main():
    ips=['localhost:50051','localhost:50052','localhost:50053']
    leaderip=ips[0]
    client = RaftClient(leaderip)

    key=input("Enter key:")
    value=input("Enter value:")

    serve_request = node_pb2.SetRequest(key=key, value=value)
    response = client.serve_set(serve_request)
    print("Set Response:", response)
    # serve_request = node_pb2.GetRequest(key="b")
    # response = client.serve_get(serve_request)
    # print("Get Response:", response)
    

if __name__ == "__main__":
    main()
