import boto3
import requests
import time


INTERVAL = 5


def main():
    print("Starting AI worker")
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName="CheckersOnlineAI")
    while True:
        print("Receiving queue messages")
        for message in queue.receive_messages():
            print("Found message: {}".format(message.body))
            requests.post("http://ai/play-ai", json=message.body)
            message.delete()
            print("Message deleted")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
