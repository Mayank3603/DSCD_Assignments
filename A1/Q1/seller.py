import grpc
import market_seller_pb2 as proto
import market_seller_pb2_grpc

def register_seller(address, uuid):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_seller_pb2_grpc.MarketServiceStub(channel)

    request = proto.SellerInfo(address=address, uuid=uuid)
    response = stub.RegisterSeller(request)

    if response.status == proto.Response.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def sell_item(seller_address, seller_uuid, product_name, category, quantity, description, price_per_unit):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_seller_pb2_grpc.MarketServiceStub(channel)

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

    if response.status == proto.Response.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def update_item(seller_address, seller_uuid, item_id, quantity, price_per_unit):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_seller_pb2_grpc.MarketServiceStub(channel)

    request = proto.UpdateItemRequest(
        item_id=item_id,
        new_price=price_per_unit,
        new_quantity=quantity,
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.UpdateItem(request)

    if response.status == proto.Response.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def delete_item(seller_address, seller_uuid, item_id):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_seller_pb2_grpc.MarketServiceStub(channel)

    request = proto.DeleteItemRequest(
        item_id=item_id,
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.DeleteItem(request)

    if response.status == proto.Response.Status.SUCCESS:
        print(f"Seller prints: SUCCESS")
    else:
        print(f"Seller prints: FAIL")

def display_seller_items(seller_address, seller_uuid):
    channel = grpc.insecure_channel('localhost:50053')
    stub = market_seller_pb2_grpc.MarketServiceStub(channel)

    request = proto.DisplayItemsRequest(
        seller_address=seller_address,
        seller_uuid=seller_uuid
    )
    response = stub.DisplaySellerItems(request)

    for item in response.items:
        print(f"Item ID: {item.item_id}, Price: ${item.price_per_unit}, Name: {item.product_name}, Category: {item.category}")
        print(f"Description: {item.description}")
        print(f"Quantity Remaining: {item.quantity}\n")

if __name__ == '__main__':
    seller_address = "192.13.188.178:50053"
    seller_uuid = "987a515c-a6e5-11ed-906b-76aef1e817c5"

    register_seller(seller_address, seller_uuid)
    sell_item(seller_address, seller_uuid, "Laptop", 1, 10, "High-performance laptop", 1200.00)
    update_item(seller_address, seller_uuid, "1", 8, 1300.00)
    # delete_item(seller_address, seller_uuid, "Laptop987a515c-a6e5-11ed-906b-76aef1e817c5")
    display_seller_items(seller_address, seller_uuid)
#     seller1()
#     print("Seller prints: SUCCESS")
#     print("Seller prints: FAIL")
#     print("yyyyyyyyyyy")
