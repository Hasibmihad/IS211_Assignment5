import csv
import random
import urllib.request

class Request:
    def __init__(self, timestamp, url, processing_time):
        self.timestamp = timestamp
        self.url = url
        self.processing_time = processing_time

    def get_timestamp(self):
        return self.timestamp

    def get_processing_time(self):
        return self.processing_time

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def process_request(self, request):
        self.current_request = request
        self.time_remaining = request.get_processing_time()

    def tick(self):
        if self.current_request:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None


def random_load_balancing(servers):
    return random.choice(servers)

def simulateOneServer(csv_data):
    server = Server()
    waiting_times = []

    for line in csv_data:
        timestamp, url, processing_time = int(line[0]), line[1], int(line[2])
        #print(timestamp, url, processing_time)
        request = Request(timestamp, url, processing_time)

        while timestamp > server.time_remaining:
            server.tick()

        if not server.current_request:
            server.process_request(request)
        else:
            waiting_times.append(timestamp)

    while server.current_request:
        server.tick()

    average_wait_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    return average_wait_time

def simulateManyServersRandom(csv_data, servers):
    server_pool = [Server() for _ in range(servers)]
    waiting_times = [[] for _ in range(servers)]

    for line in csv_data:

        timestamp, url, processing_time = int(line[0]), line[1], line[2]
        request = Request(timestamp, url, processing_time)

        # Choose a server using random load balancing
        server = random_load_balancing(server_pool)

        while timestamp > server.time_remaining:
            server.tick()
            server_pool.append(server)
            server = random_load_balancing(server_pool)

        if not server.current_request:
            server.process_request(request)
        else:
            waiting_times[server_pool.index(server)].append(timestamp)

    for server in server_pool:
        while server.current_request:
            server.tick()
            server_pool.append(server)
            server = random_load_balancing(server_pool)

    total_waiting_time = sum(sum(times) for times in waiting_times)
    total_requests = sum(len(times) for times in waiting_times)
    average_wait_time = total_waiting_time / total_requests if total_requests else 0
    return average_wait_time


def main(file, servers=None):
    if servers is None:
        average_wait_time = simulateOneServer(file)
    else:
        average_wait_time = simulateManyServersRandom(file, servers)
    print(f"Average Wait Time: {average_wait_time:.2f} seconds")

if __name__ == "__main__":
    url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    # Replace 3 with the desired number of servers
    num_servers = 3
    main(cr)

