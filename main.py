"""
Simpy-based simulation of three edge computing servers (node 0, node1 and node2)
The three nodes serve a wide area.
"""

# import the libraries
import simpy
import numpy as np
import matplotlib.pyplot as plt

# the variables to append specific simulation data. These data will be used to plot the outputs
total_in_append = []
tasks_processing_append = []
still_processing_append = []
total_out_append = []
tasks_in_queue_append = []
simulation_time_append = []


class TaskGenerator:
    """Generates the task"""

    def __init__(self, env):
        self.env = env
        self.cpu_requested = 0
        self.task_id = 0
        self.process_time = 0
        self.initiate = env.process(self.generate_task())

    def generate_task(self):
        global schedule_id

        while True:
            # inter_arrival time for tasks
            inter_arrival = np.random.uniform(0, 6)

            # append the task to the list
            total_in_append.append(1)

            # increment the task id
            self.task_id += 1

            # the cpu that is requested by the task
            self.cpu_requested = np.random.randint(200, 500)

            # the normal process time for the task
            self.process_time = np.random.randint(5, 50)

            # schedule_id is used as a routing mechanism. By changing the probability (p) values,
            # the number of tasks to each node is changed
            schedule_id = np.random.choice([i for i in range(3)], p=[0.33, 0.33, 0.34])

            # Servicing of task in the node
            self.env.process(ServiceTask(self.env,
                                         self.cpu_requested,
                                         self.process_time).service_task_in_node())

            # yield next task generation
            yield self.env.timeout(inter_arrival)

            # tasks in queue
            tasks_in_system = len(total_in_append) - len(total_out_append)
            tasks_in_process = len(tasks_processing_append) - len(total_out_append)
            if tasks_in_process > tasks_in_system:
                tasks_in_queue = 0
            else:
                tasks_in_queue = tasks_in_system - tasks_in_process

            # cpu utilization
            cpu0_util = (cpu_node0.capacity - cpu_node0.level) / cpu_node0.capacity
            cpu1_util = (cpu_node1.capacity - cpu_node1.level) / cpu_node1.capacity
            cpu2_util = (cpu_node2.capacity - cpu_node2.level) / cpu_node2.capacity

            # parameters to graph
            simulation_time_append.append(self.env.now)
            still_processing_append.append(tasks_in_process)
            tasks_in_queue_append.append(tasks_in_queue)
            cpu0_util_append.append(cpu0_util)
            cpu1_util_append.append(cpu1_util)
            cpu2_util_append.append(cpu2_util)


class ServiceTask:
    """Services the task"""

    def __init__(self, env, cpu_requested, process_time):
        self.env = env
        self.cpu_requested = cpu_requested
        self.process_time = process_time

    def service_task_in_node(self):
        global cpu_util
        global time_spent

        # Using the for loop in this method enables the scaling up or scaling down of nodes
        for i in range(3):
            if schedule_id == i:
                # register the time that the task is received
                time_in = self.env.now

                # seize the requested cpu from the ith cpu_resource list
                yield cpu_resources[i].get(self.cpu_requested)

                # compute the cpu utilization
                cpu_in_use = cpu_resources[i].capacity - cpu_resources[i].level
                cpu_util = cpu_in_use / cpu_node1.capacity

                # seize the requested cpu for the specified process time
                yield self.env.timeout(self.process_time)

                # append the task to indicate the tasks in process
                tasks_processing_append.append(1)

                # return the cpu that was seized
                yield cpu_resources[i].put(self.cpu_requested)

                # register the time that the task is completed
                time_out = self.env.now

                # compute the time the task spends in the system
                time_spent = round((time_out - time_in), 2)

                # print some output
                print(f"Node{i} was used; its cpu utilization was ",
                      round(cpu_util, 2), '; task latency was ',
                      time_spent)

                # append the task to the total out
                total_out_append.append(1)


# instantiate some variables
schedule_id = 1
cpu_util = 0
time_spent = 0

# run the simulation in real time. The higher the factor the slower the simulation model.
sim_env = simpy.rt.RealtimeEnvironment(factor=0.01, strict=False)

# set up the CPU resources and the variables for appending the utilization results
cpu_node0 = simpy.Container(sim_env, init=1500, capacity=1500)
cpu0_util_append = []
cpu_node1 = simpy.Container(sim_env, init=1500, capacity=1500)
cpu1_util_append = []
cpu_node2 = simpy.Container(sim_env, init=1500, capacity=1500)
cpu2_util_append = []

# the cpu resources as a python list
cpu_resources = [cpu_node0, cpu_node1, cpu_node2]

# activate the simulation environment
actuate = TaskGenerator(sim_env)
sim_env.process(actuate.generate_task())

# run the simulation  until 200 time units
sim_env.run(until=200)

# plot the charts
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True)
fig.suptitle('All plots')
ax1.plot(simulation_time_append, cpu0_util_append, 'k')
ax1.set_title('CPU0 utilization', loc='left', fontsize=6, fontweight='bold', pad=0)
ax1.tick_params(axis='y', which='major', labelsize=5)
ax1.set_ylim([0, 1])
ax2.plot(simulation_time_append, cpu1_util_append, 'g')
ax2.set_title('CPU1 utilization', loc='left', fontsize=6, fontweight='bold', pad=0)
ax2.tick_params(axis='y', which='major', labelsize=5)
ax2.set_ylim([0, 1])
ax3.plot(simulation_time_append, cpu2_util_append, 'r')
ax3.set_title('CPU2 utilization', loc='left', fontsize=6, fontweight='bold', pad=0)
ax3.tick_params(axis='y', which='major', labelsize=5)
ax3.set_ylim([0, 1])
ax4.plot(simulation_time_append, tasks_in_queue_append)
ax4.set_title('Tasks in queue', loc='left', fontsize=6, fontweight='bold', pad=0)
ax4.tick_params(axis='y', which='major', labelsize=5)
plt.show()
