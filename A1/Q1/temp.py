import grpc
import notification_server_pb2
import notification_server_pb2_grpc
from concurrent import futures

class NotificationServiceServicer(notification_server_pb2_grpc.NotificationServiceServicer):
    def ReceiveNotification(self, request, context):
        print(request)
        return notification_server_pb2.ItemsResponse(message="SUCCESS")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_server_service = NotificationServiceServicer()
    notification_server_pb2_grpc.add_NotificationServiceServicer_to_server(notification_server_service, server)
    server.add_insecure_port('localhost:50054')
    server.start()
    print("Listening on port"+ "localhost:50054" )
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    