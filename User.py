import sys
import json
import pika
import threading

class User:
    def __init__(self, username):
        # Initialize User with a username and RabbitMQ connection
        self.username = username
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_queue')

    def update_subscription(self, youtuber_name, subscribe):
        request_data = {
            "user": self.username,
            "youtuber": youtuber_name,
            "subscribe": str(subscribe).lower()
        } 

        self.channel.basic_publish(exchange='',
                                   routing_key='user_queue',
                                   body=json.dumps(request_data))
        print("SUCCESS")
 
    def receive_notifications(self):
        def callback(ch, method, properties, body):
            # Assuming the message format is 'YouTuberName uploaded videoName'
            message_data = json.loads(body.decode())
            youtuber_name = message_data.get("youtuber")
            action = "uploaded"
            video_name = message_data.get("videoName")

            print(f"New Notification: {youtuber_name} {action} {video_name}")

        self.channel.basic_consume(queue=self.username, on_message_callback=callback, auto_ack=True)
        print(f"Logged in as {self.username}. Waiting for notifications. To exit press CTRL+C")
        self.channel.start_consuming()

    def login(self):
        # Create a personal queue for the user
        self.channel.queue_declare(queue=self.username)

        # Receive any notifications already in the queue for the user's subscriptions
        self.receive_notifications()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python User.py <username> [s/u YouTuberName]")
        sys.exit(1)

    username = sys.argv[1]
    user_service = User(username)

    if len(sys.argv) == 4:
        action = sys.argv[2].lower()
        youtuber_name = sys.argv[3]

        if action == 's':
            user_service.update_subscription(youtuber_name, True)
        elif action == 'u':
            user_service.update_subscription(youtuber_name, False)

    user_service.login()

    try:
        # Keep the main thread running to receive real-time notifications
        threading.Event().wait()
    except KeyboardInterrupt:
        print(f"User {username} logged out.")
