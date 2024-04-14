import grpc
import time
import random
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc

NUM_MAPPERS = 1
NUM_REDUCERS = 3
NUM_CENTROIDS = 5
NUM_ITERATIONS = 1
INPUT_FILE = "points.txt"
mapper_ips = ["localhost:50051", "localhost:50052", "localhost:50053"]
centroids = []


class MasterImplementation(pb2_grpc.MasterMapperServicer):
    def __init__(self):
        centroids=[]
        points_per_mapper = 0
        num_points = 0

    def divide_input_data(self):
        with open(INPUT_FILE, "r") as f:
            data = f.readlines()
        self.num_points = len(data)
        self.points_per_mapper = self.num_points // NUM_MAPPERS
        
        for i in random.sample(data, NUM_CENTROIDS):
            x, y = map(float, i.strip().split(","))
            centroids.append([x, y])
        print(f"Initial Centroids: {centroids}")

        send_centroids = [pb2.Point(x=i[0], y=i[1]) for i in centroids]
        self.centroids = send_centroids
        
    def assign_map_tasks(self):
        for i in range(NUM_MAPPERS):
            start = i * self.points_per_mapper
            end = (i + 1) * self.points_per_mapper
            if i == NUM_MAPPERS - 1:
                end = self.num_points
            
            print(f"Mapper {i + 1} will process points {start + 1} to {end}")
            #try:
            channel = grpc.insecure_channel(mapper_ips[i])
            stub = pb2_grpc.MasterMapperStub(channel)

            request = pb2.MapPartitionRequest(start=start, end= end,numMappers=NUM_MAPPERS,centroids=self.centroids, numReducers=NUM_REDUCERS)
            response = stub.Map(request)
            if(response.status == "Success"):
                print(f"Points processed by mapper {i + 1}")
            else:
                print(f"Error in processing points by mapper {i + 1}")
            #except Exception as e:
                #print(f"Error in processing points by mapper {i + 1}")
    
    def assign_reduce_tasks(self):
        centroids = []
        for i in range(NUM_REDUCERS):
            print(f"Reducer {i + 1} will process partition {i + 1}")
            # try:
            channel = grpc.insecure_channel(f"localhost:5006{i+1}")
            stub = pb2_grpc.MasterMapperStub(channel)
            request = pb2.ReduceRequest(numReducers=NUM_REDUCERS,numMappers=NUM_MAPPERS)
            response = stub.GetReducerDetails(request)
            if(response.status == "Success"):
                print(f"Partition processed by reducer {i + 1}")
            else:
                print(f"Error in processing partition by reducer {i + 1}")
            # except Exception as e:
            #     print(f"Error in processing partition by reducer {i + 1}")
            with open(f"{response.reducer_file_path}", 'r') as file:
                lines = file.readlines()
            for line in lines:
                centroid_index, x, y = line.strip().split(" ")
                centroids.append([float(x), float(y)])
        
        print(f"Updated Centroids: {centroids}")
        

    def compile_centroids(self):    
     
def run_iteration():
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.MasterMapperStub(channel)
    master_impl = MasterImplementation()

    for iteration in range(NUM_ITERATIONS):
        print(f"Iteration {iteration + 1}/{NUM_ITERATIONS}")
        master_impl.divide_input_data()
        master_impl.assign_map_tasks()
        master_impl.assign_reduce_tasks()
        master_impl.compile_centroids()
        print("Centroids updated.")

if __name__ == "__main__":
    run_iteration()

