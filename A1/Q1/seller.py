import grpc
import market_pb2 as proto
import market_pb2_grpc

import notification_server_pb2
import notification_server_pb2_grpc
from concurrent import futures

def register_seller(address, uuid):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_pb2_grpc.MarketServiceStub(channel)

    request = proto.SellerInfo(address=address, uuid=uuid)
    response = stub.RegisterSeller(request)

    if response.status == proto.SellerResponse.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def sell_item(seller_address, seller_uuid, product_name, category, quantity, description, price_per_unit):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_pb2_grpc.MarketServiceStub(channel)

    request = proto.ItemDetails(
        seller_address=seller_address,
        seller_uuid=seller_uuid,
        product_name=product_name,
        category=category,
        quantity=quantity,
        description=description,
        price_per_unit=price_per_unit
    )
    response = stub.SellItem(request)

    if response.status == proto.ItemResponse.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def update_item(seller_address, seller_uuid, item_id, quantity, price_per_unit):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_pb2_grpc.MarketServiceStub(channel)

    request = proto.UpdateItemRequest(
        item_id=item_id,
        new_price=price_per_unit,
        new_quantity=quantity,
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.UpdateItem(request)

    if response.status == proto.UpdateItemResponse.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def delete_item(seller_address, seller_uuid, item_id):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_pb2_grpc.MarketServiceStub(channel)

    request = proto.DeleteItemRequest(
        item_id=item_id,
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.DeleteItem(request)

    if response.status == proto.DeleteItemResponse.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")



def display_seller_items(seller_address, seller_uuid):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_pb2_grpc.MarketServiceStub(channel)

    request = proto.DisplayItemsRequest(
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )

    try:
        response = stub.DisplaySellerItems(request)

        for item in response.items:
            print(item)
            

    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        print(f"RPC Error: Status Code - {status_code}, Details - {details}")

class NotificationServiceServicer(notification_server_pb2_grpc.NotificationServiceServicer):
    def ReceiveNotification(self, response, context):
        print(response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_server_service = NotificationServiceServicer()
    notification_server_pb2_grpc.add_NotificationServiceServicer_to_server(notification_server_service, server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Seller server started. Listening on port 50055.")


if __name__ == "__main__":

    serve()
    seller_address = "localhost:50055"
    seller_uuid = "987a515c-a6e5-11ed-906b-76aef1e817c5"
    register_seller(seller_address, seller_uuid)

    while(True):
        print("1. Sell Item")
        print("2. Update Item")
        print("3. Delete Item")
        print("4. Display Seller Items")
        print("5. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            product_name = input("Enter product name: ")
            category = input("Enter category: ")
            quantity = int(input("Enter quantity: "))
            description = input("Enter description: ")
            price_per_unit = float(input("Enter price per unit: "))
            sell_item(seller_address, seller_uuid, product_name, category, quantity, description, price_per_unit)
        elif choice == 2:
            item_id = input("Enter item id: ")
            quantity = int(input("Enter quantity: "))
            price_per_unit = float(input("Enter price per unit: "))
            update_item(seller_address, seller_uuid, item_id, quantity, price_per_unit)
        elif choice == 3:
            item_id = input("Enter item id: ")
            delete_item(seller_address, seller_uuid, item_id)
        elif choice == 4:
            display_seller_items(seller_address, seller_uuid)
        elif choice == 5:
            break
        else:
            print("Invalid choice")
