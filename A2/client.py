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

    def recovery(self, node_id):
        request = node_pb2.RecoverRequest(NodeId=node_id)
        response = self.stub.Recovery(request)
        return response

def main():
    client = RaftClient('localhost:50051')
    serve_request = node_pb2.GetRequest(key="a")
    response = client.serve_get(serve_request)
    print("Get Response:", response)

    serve_request = node_pb2.SetRequest(key="b", value="1")
    response = client.serve_set(serve_request)
    print("Set Response:", response)
    

if __name__ == "__main__":
    main()
