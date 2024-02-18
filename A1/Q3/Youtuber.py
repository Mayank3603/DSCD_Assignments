import sys
import pika
import json

class Youtuber:
    def __init__(self, youtuber_name):
        self.youtuber_name = youtuber_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("34.131.242.59", credentials=pika.PlainCredentials('mayank','joy')))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='youtuber_queue')

    def publish_video(self, video_name):
        request_data = {
            "youtuber": self.youtuber_name,
            "videoName": video_name
        }

        self.channel.basic_publish(exchange='',
                                   routing_key='youtuber_queue',
                                   body=json.dumps(request_data))
        print("SUCCESS")
    def run(self):
        video_name = ' '.join(sys.argv[2:])
        self.publish_video(video_name)
if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)

    youtuber_name = sys.argv[1]
  
    youtuber_service = Youtuber(youtuber_name)
    youtuber_service.run()
