import grpc
import market_pb2 as proto
import market_pb2_grpc 

channel = grpc.insecure_channel('localhost:50053')
stub = market_pb2_grpc.MarketServiceStub(channel)


def search_item(item_name,item_category):
    request = proto.SearchItemRequest(item_name=item_name, item_category=item_category)
    response = stub.SearchItem(request)
    print(response)
    

def buy_item(item_id, quantity, buyer_address):
    request = market_pb2.BuyItemRequest(
            buyer_address=buyer_address,
            item_id=item_id,
            quantity=quantity
    )

    response = stub.BuyItem(request)
    print(response.message)

    if response.status == proto.BuyItemResponse.Status.SUCCESS:
        print(f"SUCCESS")
    else:
        print(f"FAIL")

def add_to_wishlist(item_id="", buyer_address=""):
    request = proto.AddToWishlistRequest(item_id=item_id, buyer_address=buyer_address)
    response = stub.AddToWishlist(request)
    if response.status == proto.AddToWishlistResponse.Status.SUCCESS:
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

if __name__ == "__main__":
    # search_item("Laptop", "ELECTRONICS")
    # buy_item(item_id="1", quantity=2, buyer_address="120.13.188.178:50051")
    # add_to_wishlist(item_id="3", buyer_address="120.13.188.178:50051")
    rate_item(item_id="1", buyer_address="120.13.188.178:50051", rating=4)

