import csv
import urllib.request

#Implement Queue Class (from book).
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

#Implement Server Class (similar to Printer class from book)
class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_processing_time()


#Implement Request Class (similar to Task class from book)
class Request:
    def __init__(self, timestamp, processing_time):
        self.timestamp = int(timestamp)
        self.processing_time = int(processing_time)

    def get_stamp(self):
        return self.timestamp

    def get_processing_time(self):
        return self.processing_time

    def wait_time(self, timestamp):
        return self.timestamp - self.processing_time

#Function to process 1 server.
def simulateOneServer(csv_data):
    #Instantialization
    server = Server()
    queue = Queue()
    waiting_times = []

    #Pass each row to calculate the
    for row in csv_data:
        #print(row[0])
        timestamp = int(row[0])
        processing_time = int(row[2])
        request = Request(timestamp, processing_time)
        queue.enqueue(request)
        # Check if the server is not busy and its queue is not empty

        if (not server.busy()) and (not queue.is_empty()):
            new_request = queue.dequeue()
            waiting_times.append(new_request.wait_time(timestamp))
            server.start_next(request)

        server.tick()

    average_wait = (sum(waiting_times)) / (len(waiting_times))
    print(f"For 1 Server, average wait time is {average_wait:.4f} secs." )

#Function to simulate many servers
def simulateManyServers(csv_data, num_servers):
    server_pool = [Server() for _ in range(num_servers)]
    queues = [Queue() for _ in range(num_servers)]
    waiting_times = [0] * num_servers
    current_server = 0

    for row in csv_data:
        timestamp = int(row[0])
        processing_time = int(row[2])
        request = Request(timestamp, processing_time)
        
        # Enqueue the request into the current server's queue
        queues[current_server].enqueue(request)
        
        # Check if the current server is not busy and its queue is not empty
        if (not server_pool[current_server].busy()) and (not queues[current_server].is_empty()):
            new_request = queues[current_server].dequeue()
            waiting_times[current_server] += new_request.wait_time(timestamp)
            server_pool[current_server].start_next(request)
        
        server_pool[current_server].tick()
        # Move to the next server in round-robin fashion
        current_server = (current_server + 1) % num_servers  
    total=0
    for i in range(num_servers):
        average_wait = waiting_times[i] / queues[i].size()
        total+=average_wait
        print(f"For Server {i + 1}, average wait time is {average_wait:.4f} secs")
    overallAverage=total/num_servers 
    print ("\n")   
    print (f"Overall average wait time for {num_servers} servers is {overallAverage:.4f}")


def main(file, servers=None):
    if servers is None:
        simulateOneServer(file)
    else:
        simulateManyServers(file, servers)
    

if __name__ == "__main__":
    url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    # Replace 3 with the desired number of servers
    
    num_servers = 3
    main(cr,num_servers)

