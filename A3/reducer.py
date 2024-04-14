import grpc
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc
from concurrent import futures

class ReducerImplementation(pb2_grpc.MasterMapperServicer):
    def __init__(self, reducer_id):
        self.reducer_id = reducer_id

    def Reduce(self, request, context):
        print("Received request")
        num_reducers = request.numReducers
        print("Number of reducers:", num_reducers)
        print("Reducer ID:", self.reducer_id)
        self.shuffle_and_sort(request)
        points = []
  
    def shuffle_and_sort(self, request):
        print("Shuffling and sorting data")
        partitions = {}
        for i in range(1, request.numMappers + 1):
            with open(f"Mappers/M{i}/partition_{self.reducer_id}.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    centroid_index,point_x,point_y = line.strip().split(" ")
                    print(centroid_index,point_x,point_y)

if __name__ == "__main__":
    reducer_id = int(input("Enter reducer id: "))
    reducer_ips = {1: "localhost:50061", 2: "localhost:50062", 3: "localhost:50063"}
    port = int(reducer_ips[reducer_id].split(":")[1])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reducer_impl = ReducerImplementation(reducer_id)
    pb2_grpc.add_MasterMapperServicer_to_server(reducer_impl, server)
    print("Server started on port:", port)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
