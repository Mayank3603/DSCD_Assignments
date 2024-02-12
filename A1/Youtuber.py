import sys
import pika
import json

class Youtuber:
    def __init__(self, youtuber_name):
        # Initialize Youtuber with a name and RabbitMQ connection
        self.youtuber_name = youtuber_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='youtuber_queue')

    def publish_video(self, video_name):
        # Publish video information to 'youtuber_queue'
        request_data = {
            "youtuber": self.youtuber_name,
            "videoName": video_name
        }

        self.channel.basic_publish(exchange='',
                                   routing_key='youtuber_queue',
                                   body=json.dumps(request_data))
        print("SUCCESS")

    def run(self):
        # Ensure Youtuber is registered and publish a video
        self.register_youtuber()

        if len(sys.argv) != 3:
            print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
            sys.exit(1)

        video_name = sys.argv[2]
        self.publish_video(video_name)

    def register_youtuber(self):
        # Register Youtuber with the YouTube server
        request_data = {
            "youtuber": self.youtuber_name,
            "action": "register"
        }

        self.channel.basic_publish(exchange='',
                                   routing_key='youtuber_queue',
                                   body=json.dumps(request_data))

if __name__ == '__main__':
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)

    youtuber_name = sys.argv[1]
    youtuber_service = Youtuber(youtuber_name)
    youtuber_service.run()
