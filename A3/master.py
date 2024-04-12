import grpc
import time
import random
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc

# Define constants
NUM_MAPPERS = 6
NUM_REDUCERS = 3
NUM_CENTROIDS = 3
NUM_ITERATIONS = 1
INPUT_FILE = "points.txt"

def divide_input_data():
    with open(INPUT_FILE, "r") as f:
        data = f.readlines()
    num_points = len(data)
    points_per_mapper = num_points // NUM_MAPPERS
    mapper_ranges = []

    for i in range(NUM_MAPPERS):
        start = i * points_per_mapper
        end = (i + 1) * points_per_mapper
        if i == NUM_MAPPERS - 1:
            end = num_points
        
        mapper_ranges.append(pb2.PointRange(start=start, end=end))
        print(f"Mapper {i + 1} will process points {start + 1} to {end}")

    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.MasterMapperStub(channel)

    request = pb2.MapPartitionRequest(points=mapper_ranges,numMappers=NUM_MAPPERS)
    response = stub.MapPartition(request)
    print(f"Point {i + 1}/{len(points)} processed by mapper")
     


def run_iteration():
    # Connect to gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.MasterMapperStub(channel)

    for iteration in range(NUM_ITERATIONS):
        print(f"Iteration {iteration + 1}/{NUM_ITERATIONS}")
        divide_input_data()
        #assign_map_tasks()
        #assign_reduce_tasks()
        #compile_centroids()
        print("Centroids updated.")

if __name__ == "__main__":
    run_iteration()

