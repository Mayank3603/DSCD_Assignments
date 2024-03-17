import pika
import threading
import json

class YoutubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', credentials=pika.PlainCredentials('mayank', 'joy')))

        self.user_channel = self.user_connection.channel()
      
        
        self.user_channel.queue_declare(queue='user_queue')
        self.user_channel.queue_declare(queue='youtuber_queue')

        self.uploaded_videos = set()
        self.subscriptions = {}

    def consume_user_requests(self,ch,method,properties,body):
     
           
            request_data = json.loads(body.decode())
            user_name = request_data.get("user")
            youtuber_name = request_data.get("youtuber")
            action = request_data.get("subscribe")
            self.user_channel.queue_declare(queue=user_name)


            # print(user_name,youtuber_name,action)

            if action == "true":
                print(f"Received request from {user_name} to subscribe {youtuber_name}")
            else:
                print(f"Received request from {user_name} to unsubscribe {youtuber_name}")
    
            if action == "true":
                self.subscribe_user(user_name, youtuber_name)
                print(f"{user_name} subscribed to {youtuber_name}")
            elif action == "false":
                self.unsubscribe_user(user_name, youtuber_name)
              
            ch.basic_ack(delivery_tag = method.delivery_tag)

            print("Waiting for user requests.")
        

    def consume_youtuber_requests(self,ch,method,properties,body):
       
        
            request_data = json.loads(body.decode())
            youtuber_name = request_data.get("youtuber")
            video_name = request_data.get("videoName")
          
           
            if youtuber_name is not None and video_name is not None:
              
                if video_name not in self.uploaded_videos:
                    
                    print(f"{youtuber_name} uploaded {video_name}")
                    
                    self.notify_users(youtuber_name, video_name)

                    self.uploaded_videos.add(video_name)
                else: 
                    print("Same video has been uploaded")
            ch.basic_ack(delivery_tag = method.delivery_tag)

            print("Waiting for Video to be uploaded")

    def notify_users(self, youtuber_name, video_name):
        subscribers = self.subscriptions.get(youtuber_name, [])

        for username in subscribers:
         
            message = f"New video from {youtuber_name} : {video_name}"
            self.publish_to_user_queue(username, message)

        print(f"Notified {len(subscribers)} users about {youtuber_name}'s new video")

    def publish_to_user_queue(self, username, message):
        print(f"Publishing to {username}: {message}")

        self.user_channel.basic_publish(exchange='',
                                   routing_key=username,
                                   body=message)

    def subscribe_user(self, username, youtuber_name):
        if youtuber_name not in self.subscriptions:
            self.subscriptions[youtuber_name] = set()
       
        self.subscriptions[youtuber_name].add(username)

    def unsubscribe_user(self, username, youtuber_name):
        if youtuber_name in self.subscriptions:
            self.subscriptions[youtuber_name].remove(username)
        else:
            print("You have not subscribed to this user in the first place")
    def stop(self):
        print("Server stopped.")
        self.user_connection.close()
        self.youtuber_connection.close()


if __name__ == '__main__':

    youtube_server = YoutubeServer()

    youtube_server.user_channel.basic_consume(queue='user_queue', on_message_callback=youtube_server.consume_user_requests)
    youtube_server.user_channel.basic_consume(queue='youtuber_queue', on_message_callback=youtube_server.consume_youtuber_requests)
    youtube_server.user_channel.start_consuming()

  
        
    #     threading.Thread(target=youtube_server.consume_user_requests).start()
    #     youtube_server.consume_youtuber_requests()

    
 