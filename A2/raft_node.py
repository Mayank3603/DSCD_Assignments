import grpc
from concurrent import futures
import client_pb2 as client
import client_pb2_grpc 
import node_pb2 as node
import node_pb2_grpc

class RaftNodeImplementation(node_grpc.RaftNodeServicer):
    def __init__(self):
        self.node = None

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node_service=RaftNodeImplementation()
    node_pb2_grpc.add_RaftNodeServicer_to_server(node_service, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Raft Node Server started on port 50051")
    server.wait_for_termination()

