import grpc
from concurrent import futures
import client_pb2 as client
import client_pb2_grpc 
import node_pb2 as node
import node_pb2_grpc 

class ClientImplementation(client_grpc.ClientServicer):
    def __init__(self):
        self.node = None

    def SetNode(self, request, context):
        self.node = request
        return client.Empty()

    def GetNode(self, request, context):
        return self.node

    def GetNodeStream(self, request, context):
        yield self.node

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_service=ClientImplementation()
    client_pb2_grpc.add_ClientServicer_to_server(client_service, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Client Server started on port 50051")
    server.wait_for_termination()


