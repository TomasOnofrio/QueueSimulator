import random
import numpy as np

class TandemQueueSimulation:
    def __init__(self, num_events, arrival_range1, service_range1, num_servers1, max_queue_length1,
                 service_range2, num_servers2, max_queue_length2):
        
        self.num_events = num_events
        self.arrival_range1 = arrival_range1
        self.service_range1 = service_range1
        self.num_servers1 = num_servers1
        self.max_queue_length1 = max_queue_length1
        
        self.service_range2 = service_range2
        self.num_servers2 = num_servers2
        self.max_queue_length2 = max_queue_length2
        
        self.time = 0
        self.queue1 = []
        self.queue2 = []
        self.lost_customers1 = 0
        self.lost_customers2 = 0
        self.state_times1 = np.zeros(self.max_queue_length1 + 1)
        self.state_times2 = np.zeros(self.max_queue_length2 + 1)
        self.events1 = []
        self.events2 = []
        self.last_event_time = 0
    
    def update_state_times(self):
        self.state_times1[len(self.queue1)] += self.time - self.last_event_time
        self.state_times2[len(self.queue2)] += self.time - self.last_event_time
    
    def process_queue1(self):
        self.events1 = [e for e in self.events1 if e > self.time]
        if len(self.events1) < self.num_servers1:
            service_time = random.uniform(*self.service_range1)
            self.events1.append(self.time + service_time)
        elif len(self.queue1) < self.max_queue_length1:
            self.queue1.append(self.time)
        else:
            self.lost_customers1 += 1
        
        while self.queue1 and len(self.events1) < self.num_servers1:
            service_time = random.uniform(*self.service_range1)
            start_time = self.queue1.pop(0)
            self.events1.append(start_time + service_time)
    
    def process_queue2(self):
        self.events2 = [e for e in self.events2 if e > self.time]
        while self.events1 and self.events1[0] <= self.time:
            self.events1.pop(0)
            if len(self.queue2) < self.max_queue_length2:
                service_time = random.uniform(*self.service_range2)
                self.events2.append(self.time + service_time)
            else:
                self.lost_customers2 += 1
        
        while self.queue2 and len(self.events2) < self.num_servers2:
            service_time = random.uniform(*self.service_range2)
            start_time = self.queue2.pop(0)
            self.events2.append(start_time + service_time)
    
    def run(self):
        self.time = 1.5
    
        for i in range(self.num_events):
            if i > 0: 
                arrival_time = random.uniform(*self.arrival_range1)
                self.time += arrival_time
        
            self.update_state_times()
            self.last_event_time = self.time
        
            self.process_queue1()
            self.process_queue2()
        
        total_time1 = np.sum(self.state_times1)
        print(f"Lost customers in Queue 1: {self.lost_customers1}")
        print(f"Lost customers in Queue 2: {self.lost_customers2}")
        print(f"Total time: {self.time}")
        
        print("\nState Probabilities and accumulated time for Queue 1:")
        for state, time in enumerate(self.state_times1):
            print(f"State {state}: {time / total_time1:.4f} (accumulated time: {time:.2f})")
        
        total_time2 = np.sum(self.state_times2)
        print("\nState Probabilities and accumulated time for Queue 2:")
        for state, time in enumerate(self.state_times2):
            print(f"State {state}: {time / total_time2:.4f} (accumulated time: {time:.2f})")

simulator = TandemQueueSimulation(num_events=100000,arrival_range1=(1, 4),service_range1=(3, 4),num_servers1=2,
                                  max_queue_length1=3, service_range2=(2, 3), num_servers2=1, max_queue_length2=5)
simulator.run()
