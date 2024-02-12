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

    def consume_user_requests(self):
        def callback(ch, method, properties, body):
            # Assuming the message format is 'username action youtuberName'
            message_parts = body.decode().split()
            username = message_parts[0]
            action = message_parts[1]
            youtuber_name = message_parts[2]
            print(f"Received request from {username} to {action} to {youtuber_name}")

            if action == 'login':
                print(f"{username} logged in")
                # Publish a message to the user's personal queue
                self.publish_to_user_queue(username, f"Welcome, {username}!")
            elif action in ['subscribe', 'unsubscribe']:
                print(f"{username} {action}d to {youtuber_name}")

        self.user_channel.basic_consume(queue='user_queue', on_message_callback=callback, auto_ack=True)
        print("Waiting for user requests. To exit press CTRL+C")
        self.user_channel.start_consuming()

    def consume_youtuber_requests(self):
        def callback(ch, method, properties, body):
           
            # Assuming the message format is 'youtuberName upload videoName'
            message_parts = body.decode().split()
            print(message_parts)
            youtuber_name = message_parts[0]
            video_name = message_parts[2]


            print(f"{youtuber_name} uploaded {video_name}")

                # Notify users about the new video
            self.notify_users(youtuber_name, video_name)

        self.youtuber_channel.basic_consume(queue='youtuber_queue', on_message_callback=callback, auto_ack=True)
        print("Waiting for video upload requests. To exit press CTRL+C")
        self.youtuber_channel.start_consuming()

    def notify_users(self, youtuber_name, video_name):
        # Code to send notifications to users subscribed to the given YouTuber
        # You can implement this based on your notification mechanism (e.g., push notification, email, etc.)
        print(f"Notifying users subscribed to {youtuber_name} about the new video: {video_name}")

    def publish_to_user_queue(self, username, message):
        # Publish a message to the user's personal queue
        print(f"Publishing to {username}: {message}")
        self.user_channel.basic_publish(exchange='',
                                   routing_key=username,
                                   body=message)

if __name__ == '__main__':
    youtube_server = YoutubeServer()

    try:
        # Start consuming user and YouTuber requests in separate threads or processes
        print("hello")
        threading.Thread(target=youtube_server.consume_user_requests).start()
        youtube_server.consume_youtuber_requests()
    except KeyboardInterrupt:
        print("Server stopped.")
