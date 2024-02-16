import grpc
from concurrent import futures
import market_pb2 as proto
import market_pb2_grpc

wishlist={}

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

class MarketServiceImplementation(market_pb2_grpc.MarketServiceServicer):
    def __init__(self):
        self.sellers = {}
        self.items = []

    def RegisterSeller(self, request, context):
        address = request.address
        uuid = request.uuid
        if address in self.sellers:
            print(f"Seller join request from {address}[ip:port], uuid = {uuid}: FAILED")
            return proto.SellerResponse(status=proto.SellerResponse.Status.FAILED)
        resp=proto.SellerResponse(status=proto.SellerResponse.Status.SUCCESS)

        self.sellers[address] = uuid
        print(f"Seller join request from {address}[ip:port], uuid = {uuid}")

        return resp

    def SellItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            print(f"Sell Item request from {seller_address}[ip:port]: FAILED (Invalid Seller)")
            return proto.ItemResponse(status=proto.ItemResponse.Status.FAILED)

        item_id = str(len(self.items) + 1)

        self.items.append(Item(item_id, request.product_name, request.category, request.quantity, request.description, seller_address, request.price_per_unit, seller_uuid, request.rating))

        print(f"Sell Item request from {seller_address}[ip:port]")


        return proto.ItemResponse(status=proto.ItemResponse.Status.SUCCESS, item_id=item_id)

    def UpdateItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            print(f"Update Item request from {seller_address}[ip:port]: FAILED")
            return proto.UpdateItemResponse(status=proto.UpdateItemResponse.Status.FAILED)

        for item in self.items:
            if item.id== request.item_id:
                item.price_per_unit = request.new_price
                item.quantity = request.new_quantity

                print(f"Update Item request from {seller_address}[ip:port]")
                # notify_customers(item)
 
                return proto.UpdateItemResponse(status=proto.UpdateItemResponse.Status.SUCCESS)

        return proto.UpdateItemResponse(status=proto.UpdateItemResponse.Status.FAILED)


    def DeleteItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            return proto.DeleteItemResponse(status=proto.DeleteItemResponse.Status.FAILED)

        for item in self.items:
            if item['item_id'] == request.item_id:
                self.items.remove(item)
                print(f"Delete Item request from {seller_address}[ip:port]")
                # print(f"Seller prints: {proto.Response.Status.SUCCESS}")
                return proto.DeleteItemResponse(status=proto.DeleteItemResponse.Status.SUCCESS)

        return proto.DeleteItemResponse(status=proto.DeleteItemResponse.Status.FAILED)

    def DisplaySellerItems(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid
        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            print(f"Display Seller Items request from {seller_address}[ip:port]: FAILED (Invalid Seller)")
            return proto.DisplayItemsResponse(status=proto.DisplayItemsResponse.Status.FAILED)

        items_response = []

        for item in self.items:
            if item.seller_address == seller_address:
                item_detail = proto.ItemDetails(
                    item_id=item.id,
                    product_name=item.product_name,
                    category=item.category,
                    quantity=item.quantity,
                    description=item.description,
                    seller_address=item.seller_address,
                    price_per_unit=item.price_per_unit,
                    seller_uuid=item.seller_uuid,
                    rating=item.rating
                )

                items_response.append(item_detail)

        print(f"Display Seller Items request from {seller_address}[ip:port]")
        
        return proto.DisplayItemsResponse(items=items_response)

    def SearchItem(self, request, context):
        items_response = []
        print(self.items)
        if request.item_name != "" and any(item.product_name == request.item_name for item in self.items):
            for item in self.items:
                if request.item_name.lower() in item.product_name.lower() and (request.item_category == proto.Category.ANY or request.item_category == item.category):
                    item_detail = proto.ItemDetails(
                        item_id=item.id,
                        product_name=item.product_name,
                        category=item.category,
                        quantity=item.quantity,
                        description=item.description,
                        seller_address=item.seller_address,
                        price_per_unit=item.price_per_unit,
                        rating=item.rating
                    )

                    items_response.append(item_detail)

            print(f"Search Item request for {request.item_name} from {context.peer()}")
            return proto.SearchItemResponse(items=items_response)
        else:
            print(f"Search Item request for {request.item_name} from {context.peer()}: FAILED")
            return proto.SearchItemResponse(items=items_response)

    def BuyItem(self, request, context):
        buyer_address = request.buyer_address
        item_id = request.item_id
        quantity = request.quantity

        # Implement your logic for buying the item
        # Assume you have a function like 'buy_item' that returns a success message
        success, message = buy_item(buyer_address, item_id, quantity)

        # Return the response
        return market_pb2.BuyItemResponse(success=success, message=message)

    def AddToWishlist(self, request, context):
        pass
        #Buyers can subscribe to some items using this function to receive notifications. 
        # The request must contain the item ID and the buyer's address where the notification server is hosted.

        # if request.item_id in wishlist:
        #     wishlist[request.item_id].append(request.buyer_address)
        # else:
        #     wishlist[request.item_id]=[request.buyer_address]
        # print(f"{request.buyer_address}[ip:port] added {request.item_id} to wishlist.")
        # return proto.AddToWishlistResponse(status=proto.AddToWishlistResponse.Status.SUCCESS)


    def RateItem(self, request, context):
        for item in self.items:
            if item.id == request.item_id:
                item.rating = request.rating
                print(f"{request.buyer_address}[ip:port] rated {item.id} with {request.rating} stars.")
                return proto.RateItemResponse(status=proto.RateItemResponse.Status.SUCCESS)
        
        return proto.RateItemResponse(status=proto.RateItemResponse.Status.FAILED)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_service = MarketServiceImplementation()
    market_pb2_grpc.add_MarketServiceServicer_to_server(market_service, server)
    # market_buyer_pb2_grpc.add_BuyerServiceServicer_to_server(market_service, server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Market server started. Listening on port 50053.")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
