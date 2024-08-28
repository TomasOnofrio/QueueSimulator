import random
import numpy as np

class QueueSimulation:
    def __init__(self, num_servers, max_queue_length, num_events, arrival_range, service_range):
        self.num_servers = num_servers
        self.max_queue_length = max_queue_length
        self.num_events = num_events
        self.arrival_range = arrival_range
        self.service_range = service_range
        self.queue = []
        self.events = []
        self.time = 0
        self.lost_customers = 0
        self.state_times = np.zeros(self.max_queue_length + 1)
    
    def run(self):
        for _ in range(self.num_events):
            arrival_time = random.uniform(*self.arrival_range)
            self.time += arrival_time

            self.events = [e for e in self.events if e > self.time]

            if len(self.events) < self.num_servers:
                service_time = random.uniform(*self.service_range)
                self.events.append(self.time + service_time)
            elif len(self.queue) < self.max_queue_length:
                self.queue.append(self.time)
            else:
                self.lost_customers += 1

            while self.queue and len(self.events) < self.num_servers:
                service_time = random.uniform(*self.service_range)
                start_time = self.queue.pop(0)
                self.events.append(start_time + service_time)
            
            self.state_times[len(self.queue)] += arrival_time

        total_time = np.sum(self.state_times)
        state_probabilities = self.state_times / total_time

        return {
            'state_probabilities': state_probabilities,
            'lost_customers': self.lost_customers,
            'total_time': self.time
        }

sim_gg_1_5 = QueueSimulation(num_servers=1, max_queue_length=5, num_events=100000, arrival_range=(2, 5), service_range=(3, 5))
result_gg_1_5 = sim_gg_1_5.run()

sim_gg_2_5 = QueueSimulation(num_servers=2, max_queue_length=5, num_events=100000, arrival_range=(2, 5), service_range=(3, 5))
result_gg_2_5 = sim_gg_2_5.run()

print("G/G/1/5 Simulation Results")
print(f"State Probabilities: {result_gg_1_5['state_probabilities']}")
print(f"Lost Customers: {result_gg_1_5['lost_customers']}")
print(f"Total Time: {result_gg_1_5['total_time']}")

print("\nG/G/2/5 Simulation Results")
print(f"State Probabilities: {result_gg_2_5['state_probabilities']}")
print(f"Lost Customers: {result_gg_2_5['lost_customers']}")
print(f"Total Time: {result_gg_2_5['total_time']}")
