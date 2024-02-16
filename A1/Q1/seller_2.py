import grpc
import market_pb2 as proto
import market_pb2_grpc

import notification_server_pb2
import notification_server_pb2_grpc
from concurrent import futures
import uuid
import sys

market_ip = "localhost"
market_port = 50053

notification_ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
notification_port = int(sys.argv[2]) if len(sys.argv) > 2 else 50054

seller_uuid = str(uuid.uuid1())



channel = grpc.insecure_channel(market_ip + ':' + str(market_port) )
stub = market_pb2_grpc.MarketServiceStub(channel)


def register_seller(address, uuid):

    request = proto.SellerInfo(address=address, uuid=uuid)
    response = stub.RegisterSeller(request)
    print(uuid)

    if response.status == proto.SellerResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")
    


def sell_item(seller_address, seller_uuid, product_name, category, quantity, description, price_per_unit):
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
        print(f"SUCCESS")
    else:
        print(f"FAIL")

def update_item(seller_address, seller_uuid, item_id, quantity, price_per_unit):

    request = proto.UpdateItemRequest(
        item_id=item_id,
        new_price=price_per_unit,
        new_quantity=quantity,
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.UpdateItem(request)

    if response.status == proto.UpdateItemResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")

def delete_item(seller_address, seller_uuid, item_id):

    request = proto.DeleteItemRequest(
        item_id=item_id,
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.DeleteItem(request)

    if response.status == proto.DeleteItemResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")



def display_seller_items(seller_address, seller_uuid):
    # channel = grpc.insecure_channel('localhost:50053')
    # stub = market_pb2_grpc.MarketServiceStub(channel)

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
        print("Item Id:"+response.item_id+", Price:"+str(response.price_per_unit)+", Name:"+response.product_name+", Category:"+response.category+", Description:"+response.description+", Quantity Remaining:"+str(response.quantity)+", Seller:"+response.seller_address+", Rating:"+str(response.rating))
        # print("Item Id:"+response.item_id+" is sold")
        # print("Item Name:"+response.product_name+" is sold")
        # print("Item Category:"+response.category+" is sold")
        # print("Item Quantity:"+str(response.quantity)+" is sold")
        # print("Item Description:"+response.description+" is sold")
        # print("Item Price Per Unit:"+str(response.price_per_unit)+" is sold")
        # print("Seller Address:"+response.seller_address+" is sold")
        # print("Rating:"+str(response.rating)+" is sold")
        # return notification_server_pb2.ItemsResponse(status=notification_server_pb2.NotificationResponse.Status.SUCCESS)
        return notification_server_pb2.ItemsResponse(message="SUCCESS")



if __name__ == "__main__":

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_server_service = NotificationServiceServicer()
    notification_server_pb2_grpc.add_NotificationServiceServicer_to_server(notification_server_service, server)
    server.add_insecure_port('localhost:'+str(notification_port))
    server.start()
    print("Seller server started. Listening on port"+ str(notification_port))
    
    while(True):

        print("1. Register Seller")
        print("2. Sell Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Display Seller Items")
        print("6. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            seller_address = notification_ip + ':' + str(notification_port)
            register_seller(seller_address, seller_uuid)
        elif choice == 2:

            seller_address = notification_ip + ':' + str(notification_port)
            product_name = input("Enter product name: ")
            category = input("Enter category: ")
            quantity = int(input("Enter quantity: "))
            description = input("Enter description: ")
            price_per_unit = int(input("Enter price per unit: "))
            sell_item(seller_address, seller_uuid, product_name, category, quantity, description, price_per_unit)
        elif choice == 3:

            seller_address = notification_ip + ':' + str(notification_port)
            item_id = input("Enter item id: ")
            quantity = int(input("Enter quantity: "))
            price_per_unit = int(input("Enter price per unit: "))
            update_item(seller_address, seller_uuid, item_id, quantity, price_per_unit)
        elif choice == 4:

            seller_address = notification_ip + ':' + str(notification_port)
            item_id = input("Enter item id: ")
            delete_item(seller_address, seller_uuid, item_id)
        elif choice == 5:

            seller_address = notification_ip + ':' + str(notification_port)
            display_seller_items(seller_address, seller_uuid)
        elif choice == 6:
            break
        else:
            print("Invalid choice")