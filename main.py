import os
import random
import uuid
import time
from threading import Thread
import ntplib
import zmq

server = "pool.ntp.org"


def generateNodeUUID() -> str:
    return str(uuid.uuid4())


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Position[X={self.x}, Y={self.y}]"


class Node:
    def __init__(self, name: str, position: Position):
        self.name = name
        self.position = position
        self.thresholdAvailability = ThresholdAvailabilityCounter(0, name)
        self.listner = Listener(name)
        self.publisher = Publisher(name)

    def main(self):
        print(f"{self.name} is starting...")
        self.thresholdAvailability.start()
        self.listner.start()
        self.publisher.start()

    def close(self):
        self.thresholdAvailability.kill_received = True
        self.listner.kill_received = True
        self.publisher.kill_received = True

    def wait(self):
        self.thresholdAvailability.join()
        self.listner.join()
        self.publisher.join()

    def __str__(self):
        return f"Node[id={self.name}]"


class Listener(Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.kill_received = False
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.SUB)
        self.receiver.setsockopt(zmq.SUBSCRIBE, b"")
        self.receiver.bind("tcp://*:5555")

    def run(self):
        print(f"{self.name} is listening...")
        while not self.kill_received:
            try:
                # check for a message, this will not block
                message = self.receiver.recv(flags=zmq.NOBLOCK)

                # a message has been received
                print("Message received:", message)

            except zmq.Again as e:
                pass


class Publisher(Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.kill_received = False
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)

    def submit_message(self, message: str):
        self.publisher.connect("tcp://localhost:5555")
        time.sleep(0.1)
        self.publisher.send_string(message)

    def run(self):
        print(f"{self.name} is publishing...")
        self.submit_message("Hello World")
        while not self.kill_received:
            # Publish messages
            time.sleep(1)


class ThresholdAvailabilityCounter(Thread):
    def __init__(self, threshold: float, name: str):
        super().__init__()
        self.threshold = threshold
        self.name = name
        self.kill_received = False
        self.ntp_client = ntplib.NTPClient()

    def sync(self):
        # Sync the clock to NTP every 100 seconds.
        resp = self.ntp_client.request(server, version=3)
        wait_period = 20 - (resp.orig_time % 20)
        time.sleep(wait_period)

    def run(self):
        print(f"{self.name} is syncing...")
        self.sync()

        # Update threshold value every second.
        while not self.kill_received:
            self.threshold += 1
            time.sleep(1)


def start_nodes(nodes: list[Node]):
    for node in nodes:
        print("Starting node", node.name)
        node.main()
        print("Ending node", node.name)
        time.sleep(10)


def main():
    nodes = [
        Node(generateNodeUUID(), Position(0, 0)),
        Node(generateNodeUUID(), Position(0, 1)),
    ]
    # Node(generateNodeUUID(), Position(0, 2)),
    # Node(generateNodeUUID(), Position(0, 3))]

    Thread(target=start_nodes, args=(nodes,)).start()

    try:
        # Every 5 minutes print the threshold of each node
        while True:
            # os.system('cls')
            for node in nodes:
                print(
                    f"{node.name} has threshold {node.thresholdAvailability.threshold}"
                )
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exciting gracefully...")

    for node in nodes:
        node.close()

    for node in nodes:
        node.wait()


if __name__ == "__main__":
    main()

# Upon connecting, nodes need to syncronise their availability clocks.
# Every X minutes (configurable) the nodes collectively decide which SC layer they belong to.
# If there is a change in SC layer, the nodes need to adjust resources they are holding.


# Miner validates new transactions. Doing proof of work.

# Once they verify most recent block is valid. Try create candidate block by adding uncomfirmed transactions from the pool.
