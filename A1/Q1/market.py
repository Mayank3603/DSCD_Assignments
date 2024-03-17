import grpc
from concurrent import futures
import market_pb2 as proto
import market_pb2_grpc
import notification_server_pb2_grpc
import notification_server_pb2

wishlist={}
market_ip = "localhost"
market_port = 50053


# market_ip = sys.argv[1] if len(sys.argv) > 1 else "localhost/"
# market_port = int(sys.argv[2]) if len(sys.argv) > 2 else 50053

# seller_ip = "34.131.79.18"
# seller_port = 50054
# buyer_ip = "34.131.8.241"
# buyer_port = 50055

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


        self.items.append(Item(item_id, request.product_name, request.category, request.quantity, request.description, seller_address, request.price_per_unit, seller_uuid,0.0))

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
                try:
                    for buyer in wishlist[item.id]:
                        channel = grpc.insecure_channel(buyer)
                        stub = notification_server_pb2_grpc.NotificationServiceStub(channel)

                        message = f"SUCCESS: {item.quantity} units of {item.id} bought from {item.seller_address}."
                        response = stub.ReceiveNotification(notification_server_pb2.Items(
                                item_id=item.id,
                                product_name=item.product_name,
                                category=item.category, 
                                quantity=item.quantity,
                                description=item.description,
                                seller_address=item.seller_address,
                                price_per_unit=item.price_per_unit,
                                rating=item.rating  
                        )) 
                    print(f"Update Item request from {seller_address}[ip:port]")
                except:
                    print(f"Update Item request from {seller_address}[ip:port]")
                    pass    

               
                # notify_customers(item)
 
                return proto.UpdateItemResponse(status=proto.UpdateItemResponse.Status.SUCCESS)

        return proto.UpdateItemResponse(status=proto.UpdateItemResponse.Status.FAILED)


    def DeleteItem(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            return proto.DeleteItemResponse(status=proto.DeleteItemResponse.Status.FAILED)

        for item in self.items:
            if item.id == request.item_id:
                self.items.remove(item)
                print(f"Delete Item request from {seller_address}[ip:port]")
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
        try:
            if request.item_name != "" and any(item.product_name == request.item_name for item in self.items):
                for item in self.items:
                    if request.item_name.lower() in item.product_name.lower() and (request.item_category == item.category):
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

                print(f"Search Item request for {request.item_name} category {request.item_category} SUCCESSFUL")
                return proto.SearchItemResponse(items=items_response)
            else:
                print(f"Search Item request for {request.item_name} category {request.item_category} FAILED")
                return proto.SearchItemResponse(items=items_response)
        except:
            print(f"Search Item request for {request.item_name} category {request.item_category} FAILED")

    def BuyItem(self, request, context):
        buyer_address = request.buyer_address
        item_id = request.item_id
        quantity = request.quantity 

        for item in self.items:
            if item.id == item_id:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    print(f"{buyer_address}[ip:port] bought {quantity} units of {item_id} from {item.seller_address}.")
                    # notify_seller(item)
                    success = True
                    channel = grpc.insecure_channel(item.seller_address)
                    stub = notification_server_pb2_grpc.NotificationServiceStub(channel)

                    message = f"SUCCESS: {quantity} units of {item_id} bought from {item.seller_address}."
                    response = stub.ReceiveNotification(notification_server_pb2.Items(
                        item_id=item.id,
                        product_name=item.product_name,
                        category=item.category, 
                        quantity=item.quantity,
                        description=item.description,
                        seller_address=item.seller_address,
                        price_per_unit=item.price_per_unit,
                        rating=item.rating  
                    ))               

                else:
                    success = False
                    message = f"FAILED: {quantity} units of {item_id} not available from {item.seller_address}."
                    print(message)
                    return proto.BuyResponse(status=proto.BuyResponse.Status.FAILED)
        print(f"Buy Item request from {buyer_address}[ip:port] {message}")
        return proto.BuyResponse(status=proto.RateItemResponse.Status.SUCCESS)

    def AddToWishList(self, request, context):
        item_id = request.item_id
        buyer_address = request.buyer_address

        if item_id not in wishlist:
            wishlist[item_id] = [buyer_address]
        else:
            wishlist[item_id].append(buyer_address)

        print(f"{buyer_address}[ip:port] added {item_id} to wishlist.")
        return proto.AddToWishListResponse(status=proto.AddToWishListResponse.Status.SUCCESS)
        

    def RateItem(self, request, context):
        for item in self.items:
            if item.id == request.item_id:
                if(item.rating == 0):
                    item.rating = request.rating
                else:
                    item.rating = (item.rating + request.rating) / 2
                print(f"{request.buyer_address}[ip:port] rated {item.id} with {request.rating} stars.")
                return proto.RateItemResponse(status=proto.RateItemResponse.Status.SUCCESS)
        
        return proto.RateItemResponse(status=proto.RateItemResponse.Status.FAILED)


if __name__ == '__main__':
    # try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        market_service = MarketServiceImplementation()
        market_pb2_grpc.add_MarketServiceServicer_to_server(market_service, server)
        # server.add_insecure_port(market_ip + ':' + str(market_port))
        server.add_insecure_port('[::]:' + str(market_port))
        server.start()
        print("Market server started. Listening on port " + str(market_port) + " ...")
        server.wait_for_termination()
    # except :
    #     pass

