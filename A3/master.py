import grpc
import time
import random
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc

NUM_MAPPERS = 3
NUM_REDUCERS = 3
NUM_CENTROIDS = 5
NUM_ITERATIONS = 1
INPUT_FILE = "points.txt"
mapper_ips = ["localhost:50051", "localhost:50052", "localhost:50053"]
centroids = []

def divide_input_data():
    with open(INPUT_FILE, "r") as f:
        data = f.readlines()
    num_points = len(data)
    points_per_mapper = num_points // NUM_MAPPERS
    
    for i in random.sample(data, NUM_CENTROIDS):
        x, y = map(float, i.strip().split(","))
        centroids.append([x, y])
    print(f"Initial Centroids: {centroids}")

    send_centroids = [pb2.Point(x=i[0], y=i[1]) for i in centroids]
    print(send_centroids)
    

    for i in range(NUM_MAPPERS):
        start = i * points_per_mapper
        end = (i + 1) * points_per_mapper
        if i == NUM_MAPPERS - 1:
            end = num_points
        
        print(f"Mapper {i + 1} will process points {start + 1} to {end}")
        #try:
        channel = grpc.insecure_channel(mapper_ips[i])
        stub = pb2_grpc.MasterMapperStub(channel)

        request = pb2.MapPartitionRequest(start=start, end= end,numMappers=NUM_MAPPERS,centroids=send_centroids, numReducers=NUM_REDUCERS)
        response = stub.Map(request)
        print(response)
        #except Exception as e:
            #print(f"Error in processing points by mapper {i + 1}")
        


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

