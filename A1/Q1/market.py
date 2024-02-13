import grpc
from concurrent import futures
import market_seller_pb2 as seller_proto
import market_seller_pb2_grpc
# import market_buyer_pb2 as buyer_proto
# import market_buyer_pb2_grpc

class Item:
    def __init__(self, id, product_name, category, quantity, description, seller_address, price_per_unit, seller_uuid, rating):
        self.id = id
        self.product_name = product_name
        self.category = category
        self.quantity = quantity
        self.description = description
        self.seller_address = seller_address
        self.price_per_unit = price_per_unit
        self.seller_uuid = seller_uuid
        self.rating = rating

class Seller:
    def __init__(self, address, uuid):
        self.address = address
        self.uuid = uuid
        self.product_list = {}

    def add_product(self, product):
        self.product_list[product.id] = product

    def remove_product(self, product_id):
        self.product_list.pop(product_id)

    def update_product(self, product_id, product):
        self.product_list[product_id] = product

    def get_product(self, product_id):
        return self.product_list[product_id]

class MarketServiceImplementation(market_seller_pb2_grpc.MarketServiceServicer):
    def __init__(self):
        self.sellers = {}
        self.items = []

    def RegisterSeller(self, request, context):
        address = request.address
        uuid = request.uuid
        if address in self.sellers:
            print(f"Seller join request from {address}[ip:port], uuid = {uuid}: FAILED")
            return seller_proto.Response(status=seller_proto.Response.Status.FAILED)
        resp=seller_proto.Response(status=seller_proto.Response.Status.SUCCESS)

        self.sellers[address] = uuid
        print(f"Seller join request from {address}[ip:port], uuid = {uuid}")

        return resp

    def SellItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            print(f"Sell Item request from {seller_address}[ip:port]: FAILED (Invalid Seller)")
            return seller_proto.ItemResponse(status=seller_proto.Response.Status.FAILED)

        item_id = str(len(self.items) + 1)

        self.items.append(Item(item_id, request.product_name, request.category, request.quantity, request.description, seller_address, request.price_per_unit, seller_uuid, request.rating))

        print(f"Sell Item request from {seller_address}[ip:port]")


        return seller_proto.ItemResponse(status=seller_proto.Response.Status.SUCCESS, item_id=item_id)

    def UpdateItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            print(f"Update Item request from {seller_address}[ip:port]: FAILED")
            return seller_proto.UpdateItemResponse(status=seller_proto.UpdateItemResponse.Status.FAILED)

        for item in self.items:
            if item.id== request.item_id:
                item.price_per_unit = request.new_price
                item.quantity = request.new_quantity

                print(f"Update Item request from {seller_address}[ip:port]")
 
                return seller_proto.UpdateItemResponse(status=seller_proto.UpdateItemResponse.Status.SUCCESS)

        return seller_proto.UpdateItemResponse(status=seller_proto.UpdateItemResponse.Status.FAILED)

    def DeleteItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            return seller_proto.Response(status=seller_proto.Response.Status.FAILED)

        for item in self.items:
            if item['item_id'] == request.item_id:
                self.items.remove(item)
                print(f"Delete Item request from {seller_address}[ip:port]")
                # print(f"Seller prints: {seller_proto.Response.Status.SUCCESS}")
                return seller_proto.Response(status=seller_proto.Response.Status.SUCCESS)

        return seller_proto.Response(status=seller_proto.Response.Status.FAILED)

    def DisplaySellerItems(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            print(f"Display Seller Items request from {seller_address}[ip:port]: FAILED (Invalid Seller)")
            return seller_proto.ItemsResponse(status=seller_proto.Response.Status.FAILED)

        for item in self.items:

            if item.seller_address == seller_address:
                print("2")
                response = seller_proto.ItemDetails(
                    product_name=item.product_name,
                    category=item.category,
                    quantity=item.quantity,
                    description=item.description,
                    seller_address=item.seller_address,
                    price_per_unit=item.price_per_unit,
                    seller_uuid=item.seller_uuid,
                    rating=item.rating
                )


        print(f"Display Seller Items request from {seller_address}[ip:port]")
        return seller_proto.DisplayItemsResponse(items=[response])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_service = MarketServiceImplementation()
    market_seller_pb2_grpc.add_MarketServiceServicer_to_server(market_service, server)
    # market_buyer_pb2_grpc.add_BuyerServiceServicer_to_server(market_service, server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Market server started. Listening on port 50053.")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
