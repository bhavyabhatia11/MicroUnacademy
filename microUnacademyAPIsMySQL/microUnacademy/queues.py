import pika
import json

# credentials = pika.PlainCredentials("unacademy","unacademy")


def push_video_votes_to_queue(video_votes_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
    channel = connection.channel()
    channel.queue_declare(queue='video_votes')
    channel.basic_publish(exchange='', routing_key='video_votes', body= json.dumps(video_votes_data))
    print("Send!", video_votes_data)
    connection.close()