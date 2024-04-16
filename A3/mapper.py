import grpc
import threading
from concurrent import futures
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc

class MapperImplementation(pb2_grpc.MasterMapperServicer):

    def __init__(self, mapper_id): 
        mapper_id = mapper_id

    def Map(self, request, context):
        print("Received request from master")
        num_mappers = request.numMappers
        num_reducers = request.numReducers
        print("Number of mappers:", num_mappers)
        print("Start:", request.start, "End:", request.end)

        start = request.start
        end = request.end

        points = []
        with open(r'Input/points.txt', 'r') as file:
            lines = file.readlines()[start:end]
            for line in lines:
                x, y = map(float, line.strip().split(','))
                points.append(pb2.Point(x=round(x, 1), y=round(y, 1)))      
        print(len(points), "points processed by mapper")
        to_partition = [] 
        for point in points:
            min_distance = float('inf')
            closest_centroid_index = None
            for centroid_index, centroid in enumerate(request.centroids):
                distance = (point.x - centroid.x) ** 2 + (point.y - centroid.y) ** 2
                if distance < min_distance:
                    min_distance = distance
                    closest_centroid_index = centroid_index
            print(f"Point {point} is closest to centroid {closest_centroid_index}")
            to_partition.append((closest_centroid_index, (round(point.x, 1), round(point.y, 1))))  

        print("Points to partition:", to_partition)
        self.Partition(to_partition,num_reducers)
        return pb2.MapPartitionResponse(status="Success")

    def Partition(self, to_partition, num_reducers):
        num_mappers = len(to_partition)
        num_partitions_per_mapper = num_reducers

        partitions = {}

        for index, (centroid_index, point) in enumerate(to_partition):
            if centroid_index not in partitions:
                partitions[centroid_index] = []
            partitions[centroid_index].append(point)
        partitions = dict(sorted(partitions.items(), key=lambda x: x[0]))
        print("Partitions created by mapper", partitions) 

        for centroid_index, points in partitions.items():
            reducer_id = (centroid_index % num_reducers) + 1
            print("Sending partition to reducer", reducer_id)
            with open(f"Mappers/M{mapper_id}/partition_{reducer_id}.txt", 'a') as file:
                for point in points:
                    file.write(f"{centroid_index} {point[0]} {point[1]}\n")

    def GetInputfromMapper(self, request, context):
        print("Received request from reducer")
        reducer_id = request.reducer_id
        print("Reducer ID:", reducer_id)
        partition_file = f"Mappers/M{mapper_id}/partition_{reducer_id}.txt"
        data=""
        for line in open(partition_file, 'r'):
            data += line
        response = pb2.GetInputResponse(data=data)
        return response


if __name__ == "__main__":
    
    mapper_id = int(input("Enter mapper id: "))
    mapper_ips = {1: "localhost:50051", 2: "localhost:50052", 3: "localhost:50053"}
    port = int(mapper_ips[mapper_id].split(":")[1])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mapper_impl = MapperImplementation(mapper_id)
    pb2_grpc.add_MasterMapperServicer_to_server(mapper_impl, server)
    print("Server started on port:", port)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


