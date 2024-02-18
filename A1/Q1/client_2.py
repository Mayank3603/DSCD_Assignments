import grpc
import market_pb2 as proto
import market_pb2_grpc 
import notification_server_pb2
import notification_server_pb2_grpc
from concurrent import futures
import sys
market_ip = "localhost"
market_port = 50053

notification_ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
notification_port = int(sys.argv[2]) if len(sys.argv) > 2 else 50055



channel = grpc.insecure_channel(market_ip + ':' + str(market_port) )
stub = market_pb2_grpc.MarketServiceStub(channel)



def search_item(item_name,item_category):
    request = proto.SearchItemRequest(item_name=item_name, item_category=item_category)
    response = stub.SearchItem(request)
    for item in response.items:
        print(f"Item Id: {item.item_id}")
        print(f"Item Name: {item.product_name}")
        print(f"Item Category: {item.category}")
        print(f"Item Quantity: {item.quantity}")
        print(f"Item Description: {item.description}")
        print(f"Item Price Per Unit: {item.price_per_unit}")
        print(f"Seller Address: {item.seller_address}")
        print(f"Rating: {item.rating}")
        print("----------------------------------------------------")
    

def buy_item(item_id, quantity, buyer_address):
    request = proto.BuyRequest(
            buyer_address=buyer_address,
            item_id=item_id,
            quantity=quantity
    )

    response = stub.BuyItem(request)

    print(response)

    if response.status == proto.BuyResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")


def add_to_wishlist(item_id, buyer_address):
    request = proto.AddToWishListRequest(item_id=item_id, buyer_address=buyer_address)
    response = stub.AddToWishList(request)
    if response.status == proto.AddToWishListResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")

def rate_item(item_id, buyer_address, rating):
    request = proto.RateItemRequest(item_id=item_id, buyer_address=buyer_address, rating=rating)
    response = stub.RateItem(request)

    if response.status == proto.RateItemResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")

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
    server.add_insecure_port('localhost:'+str(notification_port) )
    server.start()
    print("Client server started. Listening on port " + str(notification_port))

    while(True):
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add to Wishlist")
        print("4. Rate Item")
        print("5. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            item_name = input("Enter item name: ")
            item_category = input("Enter item category: ")
            search_item(item_name, item_category)
        elif choice == 2:
            item_id = input("Enter item id: ")
            quantity = int(input("Enter quantity: "))
            buyer_address = notification_ip + ':' + str(notification_port)

            buy_item(item_id, quantity, buyer_address)
 
        elif choice == 3:
            item_id = input("Enter item id: ")
            buyer_address = notification_ip + ':' + str(notification_port)
            add_to_wishlist(item_id, buyer_address)
        elif choice == 4:
            item_id = input("Enter item id: ")
            buyer_address = notification_ip + ':' + str(notification_port)
            rating = int(input("Enter rating: "))
            rate_item(item_id, buyer_address, rating)
        elif choice == 5:
            break
        else:
            print("Invalid choice")
