"""
This script is a discrete event simulation model to implement and evaluate a TOPSIS-based task scheduler for
edge computing networks. Tasks are scheduled using three criteria namely, distance from server, CPU utilization
at server and RAM utilization at server.
If not specified, the TOPSIS would attempt to execute as soon as a task is generated into the system. In a light
traffic network, this may achieve the desired results. However, in a heavy traffic, heavy workload network,
it is possible that there is a time delay (while in queue), between when the task is generated/scheduled and when it is
placed on a server. With this time delay, the conditions at the server(s) may have changed between when the task was
scheduled and when it is actually placed. As a result, the TOPSIS decision at task generation becomes stale.
To overcome this, the TOPSIS is only executed when the job is exactly ready to be placed on a server.
"""

import salabim as sim
import topsispy as tp

# import numpy


class Task(sim.Component):
    def __init__(self, cpu, ram, pt, seq_num, selected_server, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.cpu = cpu
        self.ram = ram
        self.pt = pt
        self.seq_num = seq_num
        self.selected_server = selected_server

    def process(self):
        while True:
            self.cpu = cpu()
            self.ram = ram()
            self.pt = pt()
            self.seq_num += 1
            Broker(self.cpu, self.ram, self.pt, self.seq_num,
                   self.selected_server, priority=self.seq_num)
            yield self.hold(task_iat())


class Broker(sim.Component):
    def __init__(self, cpu, ram, pt, seq_num, selected_server, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.cpu = cpu
        self.ram = ram
        self.pt = pt
        self.seq_num = seq_num
        self.selected_server = selected_server
        self.a = []

    def process(self):
        '''
        The TOPSIS package (https://pypi.org/project/topsispy/) require three parameters as inputs:
        i) set of criteria (a), ii) set of weights (w) and iii) set of signs ( in the current case,
        -1 is used where a minimum is ideal or +1 if maximum is ideal)
        In this example, the set of criteria (a) are respectively:
        1) distance of task from each server, the lower the ideal for placing the task (sim.Uniform(0.1, 0.5))
        2) the CPU utilization, the lower the ideal for placing the task (server0_cpu.occupancy)
        3) the RAM utilization, the lower the ideal for placing the task (server0_ram.occupancy)
        '''
        self.enter_sorted(initial_q, self.seq_num)
        # with the if statement, TOPSIS is only executed when the job is exactly ready to be placed on a server
        # otherwise it stays in the initial queue
        if len(ready_to_place) < 1:
            self.a = [[sim.Uniform(0.1, 0.5)(), server0_cpu.occupancy.value, server0_ram.occupancy.value],
                      [sim.Uniform(0.1, 0.5)(), server1_cpu.occupancy.value, server1_ram.occupancy.value],
                      [sim.Uniform(0.1, 0.5)(), server2_cpu.occupancy.value, server2_ram.occupancy.value]
                      ]

            decision = tp.topsis(self.a, w, sign)
            print('task #=', self.seq_num - 1, 'is on server=', decision[0], 'queue size=', len(initial_q))

            self.selected_server = decision[0]

            Service(self.cpu, self.ram, self.pt, self.seq_num, self.selected_server, priority=self.seq_num)
            initial_q.pop()


class Service(sim.Component):
    def __init__(self, cpu, ram, pt, seq_num, selected_server, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.cpu = cpu
        self.ram = ram
        self.pt = pt
        self.seq_num = seq_num
        self.selected_server = selected_server

    def process(self):
        self.enter_sorted(ready_to_place, self.seq_num)
        yield self.request(FIFO)  # ensures a strict first-in-first-out policy
        yield self.request((servers_cpu[self.selected_server], self.cpu, self.seq_num))
        yield self.request((servers_ram[self.selected_server], self.ram, self.seq_num))
        self.release(FIFO)
        self.leave(ready_to_place)
        yield self.hold(self.pt, mode='hold')
        self.release()


def number_of_tasks():
    if len(initial_q) > 10:
        return len(initial_q) - 10
    else:
        return 0


env = sim.Environment(trace=False)

w = [0.33, 0.33, 0.34]  # importance weights of the three criteria
sign = [-1, -1, -1]  # TOPSIS sign

initial_q = sim.Queue()  # initial queue
ready_to_place = sim.Queue()  # ready_to_place queue

FIFO = sim.Resource()  # ensures first-come-first-serve policy

# CPU resources
server0_ram = sim.Resource(capacity=1500)
server1_ram = sim.Resource(capacity=1500)
server2_ram = sim.Resource(capacity=1500)
servers_ram = [server0_ram, server1_ram, server2_ram]

# RAM resources
server0_cpu = sim.Resource(capacity=1500)
server1_cpu = sim.Resource(capacity=1500)
server2_cpu = sim.Resource(capacity=1500)
servers_cpu = [server0_cpu, server1_cpu, server2_cpu]

# parameters and values
task_iat = sim.Uniform(0.1, 0.8)
cpu = sim.IntUniform(100, 900)  # in vCPU
ram = sim.IntUniform(50, 600)  # in MB
pt = sim.Uniform(1, 4)
seq_num = 0
selected_server = sim.Pdf((0, 1, 2), (33, 33, 33))

Task(cpu=cpu(), ram=ram(), pt=pt(), seq_num=seq_num, selected_server=selected_server())

env.animate(True)

# animate the queue bins
sim.AnimateQueue(ready_to_place, x=50, y=550, title="Ready to process", direction="e")
sim.AnimateQueue(initial_q, x=250, y=650, title="Waiting to schedule", direction="e", max_length=10)
sim.AnimateText(text=lambda t: f"plus {number_of_tasks()} more tasks waiting", x=750, y=650,
                text_anchor='nw', fontsize=20, textcolor='red')

for i, j in enumerate((server0_cpu, server1_cpu, server2_cpu)):
    sim.AnimateQueue(j.claimers(), x=50 + i * 100, y=100, direction="n",
                     title=f'Server{i}')

env.an_menu()
env.speed(0.5)
env.run(200)
