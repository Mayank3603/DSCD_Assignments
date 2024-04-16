import grpc
import time
import random
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc
import threading



class MasterImplementation(pb2_grpc.MasterMapperServicer):
    def __init__(self,num_mappers,num_reducers,num_centroids,num_iterations,input_file,mapper_ips):
        self.centroids=[]
        self.send_centroids=[]
        self.points_per_mapper = 0
        self.num_points = 0
        self.num_mappers=num_mappers
        self.num_reducers=num_reducers
        self.num_centroids=num_centroids
        self.num_iterations=num_iterations
        self.input_file=input_file
        self.mapper_ips=mapper_ips

    def divide_input_data(self):
        with open(self.input_file, "r") as f:
            data = f.readlines()
        self.num_points = len(data)
        self.points_per_mapper = self.num_points // self.num_mappers
        
        for i in random.sample(data, self.num_centroids):
            x, y = map(float, i.strip().split(","))
            self.centroids.append([x, y])
        print(f"Initial Centroids: {self.centroids}")

        
        self.centroids = [(i[0], i[1]) for i in self.centroids]
        
    def assign_map_tasks(self):
            def map_task(i):
                start = i * self.points_per_mapper
                end = (i + 1) * self.points_per_mapper
                if i == self.num_mappers - 1:
                    end = self.num_points
                    
                print(f"Mapper {i + 1} will process points {start + 1} to {end}")
                self.send_centroids = [pb2.Point(x=i[0], y=i[1]) for i in self.centroids]
                try:
                    channel = grpc.insecure_channel(self.mapper_ips[i])
                    stub = pb2_grpc.MasterMapperStub(channel)
                    request = pb2.MapPartitionRequest(start=start, end=end, numMappers=self.num_mappers, centroids=self.send_centroids, numReducers=self.num_reducers)
                    response = stub.Map(request,timeout=0.6)
                    if response.status == "Success":
                        print(f"Points processed by mapper {i + 1}")
                    else:
                        print(f"Error in processing points by mapper {i + 1}")
                except grpc._channel._InactiveRpcError:
                    print(f"Error in processing points by mapper {i + 1}")


                except Exception as e:
                    print(f"Error in processing points by mapper {i + 1}")
                
                
            threads = []
            for i in range(self.num_mappers):
                thread = threading.Thread(target=map_task, args=(i,))
                threads.append(thread)
                thread.start()
                
            for thread in threads:
                thread.join()

    def assign_reduce_tasks(self):
        def reduce_task(i):
            print(f"Reducer {i + 1} will process partition {i + 1}")
            # try:
            channel = grpc.insecure_channel(f"localhost:5006{i + 1}")
            stub = pb2_grpc.MasterMapperStub(channel)
            request = pb2.ReduceRequest(numReducers=self.num_reducers, numMappers=self.num_mappers)
            response = stub.GetReducerDetails(request)
            if response.status == "Success":
                print(f"Partition processed by reducer {i + 1}")
            else:
                print(f"Error in processing partition by reducer {i + 1}")
            
            lines=response.data.split("\n")
            lines=lines[:-1]
            for line in lines:
                if line == "":
                    continue
                centroid_index, x, y = line.strip().split(" ")
                centroids[int(centroid_index)] = (float(x), float(y))
            # except Exception as e:
            #     print(f"Error in processing partition by reducer {i + 1}")
                
        centroids = {}
        threads = []
        for i in range(self.num_reducers):
            thread = threading.Thread(target=reduce_task, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

        updated_centroids = [(0, 0) for _ in range(self.num_centroids)]
        print(centroids)
        for centroid_index, points in centroids.items():
            updated_centroids[centroid_index] = points
        
        print(f"Updated Centroids: {updated_centroids}")
        return updated_centroids

   
     
def run_iteration():
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.MasterMapperStub(channel)
    NUM_MAPPERS = int(input("Enter number of mappers: "))
    NUM_REDUCERS = int(input("Enter number of reducers: "))
    NUM_CENTROIDS = int(input("Enter number of centroids: "))
    NUM_ITERATIONS = int(input("Enter number of iterations: "))
    INPUT_FILE = r'Input/points2.txt'
    mapper_ips = ["localhost:50051", "localhost:50052","localhost:50053"]


    master_impl = MasterImplementation(NUM_MAPPERS, NUM_REDUCERS, NUM_CENTROIDS, NUM_ITERATIONS, INPUT_FILE, mapper_ips)

    master_impl.divide_input_data()
    for iteration in range(master_impl.num_iterations):
        print(f"Iteration {iteration + 1}/{master_impl.num_iterations}")
        master_impl.assign_map_tasks()
        master_impl.centroids=master_impl.assign_reduce_tasks()
        print("Centroids updated.")

    with open ("centroids.txt", "w") as f:
        for i in master_impl.centroids:
            f.write(f"{i[0]} {i[1]}\n")

if __name__ == "__main__":
    run_iteration()