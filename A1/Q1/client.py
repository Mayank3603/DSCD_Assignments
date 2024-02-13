# Import the generated protobuf code
import market_buyer_pb2 as proto

# Create a gRPC client for the BuyerService
import grpc
from market_buyer_pb2_grpc import BuyerServiceStub

# Create a gRPC channel (assuming the server is running at localhost:50051)
channel = grpc.insecure_channel('localhost:50051')

# Create a stub (client)
buyer_service_stub = BuyerServiceStub(channel)

def search_item(item_name="", item_category=proto.ItemCategory.ANY):
    # Create a SearchRequest
    search_request = proto.SearchRequest1(item_name=item_name, item_category=item_category)

    # Call the SearchItem RPC
    search_response = buyer_service_stub.SearchItem(search_request)

    # Print the search results
    for item in search_response.items:
        print(f"Item ID: {item.item_id}, Price: ${item.price}, Name: {item.product_name}, Category: {item.category}")
        print(f"Description: {item.description}")
        print(f"Quantity Remaining: {item.quantity}")
        print(f"Rating: {item.rating} / 5  |  Seller: {item.seller_address}\n")

def buy_item(item_id, quantity, buyer_address):
    # Create a BuyRequest
    buy_request = proto.BuyRequest1(item_id=item_id, quantity=quantity, buyer_address=buyer_address)

    # Call the BuyItem RPC
    buy_response = buyer_service_stub.BuyItem(buy_request)

    # Print the result
    print(f"Buy request {quantity} of item {item_id}, from {buyer_address}: {buy_response.status}")

def add_to_wishlist(item_id, buyer_address):
    # Create an AddToWishListRequest
    wishlist_request = proto.AddToWishListRequest1(item_id=item_id, buyer_address=buyer_address)

    # Call the AddToWishList RPC
    wishlist_response = buyer_service_stub.AddToWishList(wishlist_request)

    # Print the result
    print(f"Wishlist request of item {item_id}, from {buyer_address}: {wishlist_response.status}")

def rate_item(item_id, buyer_address, rating):
    # Create a RateItemRequest
    rate_request = proto.RateItemRequest1(item_id=item_id, buyer_address=buyer_address, rating=rating)

    # Call the RateItem RPC
    rate_response = buyer_service_stub.RateItem(rate_request)

    # Print the result
    print(f"{buyer_address} rated item {item_id} with {rating} stars: {rate_response.status}")

# Example usage
search_item(item_name="", item_category=proto.ItemCategory.ANY)
buy_item(item_id="1", quantity=2, buyer_address="120.13.188.178:50051")
add_to_wishlist(item_id="3", buyer_address="120.13.188.178:50051")
rate_item(item_id="3", buyer_address="120.13.188.178:50051", rating=4)
