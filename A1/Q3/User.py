import sys
import json
import pika
import threading

class User:
    def __init__(self, username):
        
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
        self.channel.queue_declare(queue=username)
        def callback(ch, method, properties, body):
            print(body.decode())
            ch.basic_ack(delivery_tag = method.delivery_tag)

        self.channel.basic_consume(queue=self.username, on_message_callback=callback)
        
        self.channel.start_consuming()

    def login(self):
        print(f"Logged in as username: {self.username}. Waiting for notifications. ")
        self.receive_notifications()
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:  python User.py <Username> s/u [YouTuberName]")
        sys.exit(1)

    username = sys.argv[1]
    user_service = User(username)
    if(len(sys.argv)==2):
        user_service.login()
    elif (len(sys.argv)) == 4:

        action = sys.argv[2].lower()
        youtuber_name = sys.argv[3]
        if action not in ('s', 'u'):
            print("Invalid action. Use 's' to subscribe or 'u' to unsubscribe.")
            sys.exit(1)

        if action == 's':
            user_service.update_subscription(youtuber_name, True)
        elif action == 'u':
            user_service.update_subscription(youtuber_name, False)

        user_service.login()
    else:
        print("Usage:  python User.py <Username> s/u [YouTuberName]")
        sys.exit(1)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print(f"User {username} logged out.")
