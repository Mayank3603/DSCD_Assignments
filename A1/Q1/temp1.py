import grpc
from concurrent import futures

import notification_server_pb2_grpc
import notification_server_pb2


channel = grpc.insecure_channel("localhost:50054")
stub = notification_server_pb2_grpc.NotificationServiceStub(channel)

                    
response = stub.ReceiveNotification(notification_server_pb2.Items(
    seller_address="localhost:50053",
    product_name="apple",
    category="fruit",
    quantity=10,
    description="fresh",
    price_per_unit=5
))    
print(response)