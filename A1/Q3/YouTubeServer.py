import pika
import threading
import json

class YoutubeServer:
    def __init__(self):
        # Initialize RabbitMQ connection and declare queues
        self.user_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.user_channel = self.user_connection.channel()
        self.user_channel.queue_declare(queue='user_queue')

        self.youtuber_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.youtuber_channel = self.youtuber_connection.channel()
        self.youtuber_channel.queue_declare(queue='youtuber_queue')

        # Set to keep track of uploaded videos
        self.uploaded_videos = set()

        # Dictionary to store user subscriptions
        self.subscriptions = {}

    def consume_user_requests(self):
        def callback(ch, method, properties, body):
            # Assuming the message format is 'username action youtuberName'
            
            request_data = json.loads(body.decode())
            user_name = request_data.get("user")
            youtuber_name = request_data.get("youtuber")
            action = request_data.get("subscribe")
            self.user_channel.queue_declare(queue=user_name)

            print(action)

            if action == "true":
                print(f"Received request from {user_name} to subscribe {youtuber_name}")
            else:
                print(f"Received request from {user_name} to unsubscribe {youtuber_name}")
    
            if action == "true":
                self.subscribe_user(user_name, youtuber_name)
                print(f"{user_name} subscribed to {youtuber_name}")
            elif action == "false":
                self.unsubscribe_user(user_name, youtuber_name)
                print(f"{user_name} unsubscribed from {youtuber_name}")

        self.user_channel.basic_consume(queue='user_queue', on_message_callback=callback, auto_ack=True)
        print("Waiting for user requests. To exit press CTRL+C")
        self.user_channel.start_consuming()

    def consume_youtuber_requests(self):
        def callback(ch, method, properties, body):
            # Assuming the message format is a JSON-encoded dictionary
            request_data = json.loads(body.decode())

            youtuber_name = request_data.get("youtuber")
            video_name = request_data.get("videoName")

            # Check if both youtuber_name and video_name are present
            if youtuber_name is not None and video_name is not None:
                # Check if the video is already processed
                if video_name not in self.uploaded_videos:
                    print(f"{youtuber_name} uploaded {video_name}")

                    # Notify users about the new video
                    self.notify_users(youtuber_name, video_name)

                    # Add the video to the processed set
                    self.uploaded_videos.add(video_name)

        self.youtuber_channel.basic_consume(queue='youtuber_queue', on_message_callback=callback, auto_ack=True)
        print("Waiting for video upload requests. To exit press CTRL+C")
        self.youtuber_channel.start_consuming()

    def notify_users(self, youtuber_name, video_name):
        # Get the list of users subscribed to the given YouTuber
        subscribers = self.subscriptions.get(youtuber_name, [])

        # Notify each subscriber individually
        for username in subscribers:

            message = f"New video from {youtuber_name} : {video_name}"
            self.publish_to_user_queue(username, message)

        print(f"Notified {len(subscribers)} users about {youtuber_name}'s new video")

    def publish_to_user_queue(self, username, message):
        # Publish a message to the user's personal queue
        print(f"Publishing to {username}: {message}")
        self.user_channel.basic_publish(exchange='',
                                   routing_key=username,
                                   body=message)

    def subscribe_user(self, username, youtuber_name):
        # Subscribe the user to the given YouTuber
        if youtuber_name not in self.subscriptions:
            self.subscriptions[youtuber_name] = set()
        self.subscriptions[youtuber_name].add(username)

    def unsubscribe_user(self, username, youtuber_name):
        # Unsubscribe the user from the given YouTuber
        if youtuber_name in self.subscriptions:
            self.subscriptions[youtuber_name].remove(username)

if __name__ == '__main__':
    youtube_server = YoutubeServer()

    try:
        # Start consuming user and YouTuber requests in separate threads or processes
        print("Server started.")
        threading.Thread(target=youtube_server.consume_user_requests).start()
        youtube_server.consume_youtuber_requests()
    except KeyboardInterrupt:
        print("Server stopped.")
