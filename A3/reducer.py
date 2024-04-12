import grpc
import process_pb2 as pb2
import process_pb2_grpc as pb2_grpc

def receive_partitioned_data():
    pass

def shuffle_and_sort(partitioned_data):
    pass

def reduce_function(shuffled_data):
    pass

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.ReducerMapperStub(channel)

    partitioned_data = receive_partitioned_data()

    shuffled_data = shuffle_and_sort(partitioned_data)

    reduced_data = reduce_function(shuffled_data)

    pass

if __name__ == "__main__":
    main()
