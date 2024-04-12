import grpc
import threading
from concurrent import futures
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc

class MapperImplementation(pb2_grpc.MasterMapperServicer):
    def MapPartition(self, request, context):
        print("Received request from master")
        print(request.points)
        num_mappers = request.numMappers
        print("Number of mappers:", num_mappers)

        threads = []
        for i in range(num_mappers):
            thread = threading.Thread(target=self.compute_task, args=(request, i,))
            thread.daemon = True
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def compute_task(self, request, i):
        start = request.points[i].start
        end = request.points[i].end

        points = []
        with open('points.txt', 'r') as file:
            lines = file.readlines()[start:end]
            for line in lines:
                x, y = map(float, line.strip().split(','))
                points.append((x, y))
        print(len(points), "points processed by mapper", i + 1)


def main():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

    mapper_impl = MapperImplementation()
    pb2_grpc.add_MasterMapperServicer_to_server(mapper_impl, server)

    print("Server started on port:", port)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
