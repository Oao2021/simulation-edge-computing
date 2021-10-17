"""
Attempts to balance the workload amongst the three servers
"""

# import the map module. In this example, only the ant path is utilized
from ipyleaflet import (AntPath)

# import the simulation module
import salabim as sim

# import package for computing distance
import mpu

# fixed location for server0
server0_lat = 6.516060111018401
server0_lon = 3.3942876621261657

# fixed location for server1
server1_lat = 6.5129475190442365
server1_lon = 3.391069011343227

# fixed location for server2
server2_lat = 6.518874218644982
server2_lon = 3.3970771594713787

# set the ant path through which the moving user will travel
ant_path = AntPath(
    locations=[
        [6.51746, 3.387809], [6.517765, 3.38888],
        [6.51787, 3.389167], [6.518012, 3.389444], [6.518155, 3.389655], [6.518613, 3.390258],
        [6.518714, 3.390429], [6.518853, 3.390723], [6.518918, 3.390906], [6.518962, 3.391101],
        [6.518987, 3.391336], [6.518953, 3.39136], [6.518938, 3.391409], [6.518958, 3.391456],
        [6.518996, 3.391478], [6.519081, 3.392472], [6.519061, 3.392809], [6.518588, 3.395111],
        [6.518573, 3.395146], [6.518581, 3.395172], [6.518524, 3.395528], [6.518519, 3.395746],
        [6.518543, 3.395964], [6.518633, 3.396351], [6.518885, 3.396932], [6.518885, 3.396951],
        [6.518558, 3.397097], [6.518337, 3.397163], [6.51809, 3.397207], [6.5181, 3.397415],
        [6.517817, 3.397375], [6.517817, 3.397375], [6.517697, 3.397358], [6.517421, 3.397361],
        [6.517129, 3.397372], [6.517122, 3.39718], [6.516851, 3.397201], [6.516615, 3.397247],
        [6.516186, 3.397415], [6.515613, 3.397588], [6.515248, 3.39763], [6.514928, 3.397589],
        [6.514331, 3.397446], [6.513938, 3.397392], [6.513805, 3.397393], [6.513803, 3.39705],
        [6.513803, 3.39705], [6.5138, 3.395799], [6.513733, 3.395255], [6.513587, 3.394569],
        [6.51326, 3.393188], [6.512997, 3.39195], [6.512791, 3.391198], [6.512791, 3.391198],
        [6.512766, 3.391138], [6.512776, 3.391118], [6.512986, 3.391188], [6.515244, 3.39174],
        [6.515645, 3.39179], [6.516234, 3.391781], [6.5174, 3.391643], [6.5174, 3.391643],
        [6.518958, 3.391456], [6.518996, 3.391478], [6.519062, 3.391459], [6.519084, 3.391414],
        [6.518946, 3.390819], [6.518845, 3.39055], [6.518786, 3.390418], [6.518631, 3.390174],
        [6.518152, 3.38954], [6.518025, 3.389333], [6.517852, 3.388948], [6.51758, 3.388034],
        [6.517636, 3.387979], [6.517604, 3.387691], [6.51746, 3.387809], [6.517765, 3.38888],
        [6.51787, 3.389167], [6.518012, 3.389444], [6.518155, 3.389655], [6.518613, 3.390258],
        [6.518714, 3.390429], [6.518853, 3.390723], [6.518918, 3.390906], [6.518962, 3.391101],
        [6.518987, 3.391336], [6.518953, 3.39136], [6.518938, 3.391409], [6.518958, 3.391456],
        [6.518996, 3.391478], [6.519081, 3.392472], [6.519061, 3.392809], [6.518588, 3.395111],
        [6.518573, 3.395146], [6.518581, 3.395172], [6.518524, 3.395528], [6.518519, 3.395746],
        [6.518543, 3.395964], [6.518633, 3.396351], [6.518885, 3.396932], [6.518885, 3.396951],
        [6.518558, 3.397097], [6.518337, 3.397163], [6.51809, 3.397207], [6.5181, 3.397415],
        [6.517817, 3.397375], [6.517817, 3.397375], [6.517697, 3.397358], [6.517421, 3.397361],
        [6.517129, 3.397372], [6.517122, 3.39718], [6.516851, 3.397201], [6.516615, 3.397247],
        [6.516186, 3.397415], [6.515613, 3.397588], [6.515248, 3.39763], [6.514928, 3.397589],
        [6.514331, 3.397446], [6.513938, 3.397392], [6.513805, 3.397393], [6.513803, 3.39705],
        [6.513803, 3.39705], [6.5138, 3.395799], [6.513733, 3.395255], [6.513587, 3.394569],
        [6.51326, 3.393188], [6.512997, 3.39195], [6.512791, 3.391198], [6.512791, 3.391198],
        [6.512766, 3.391138], [6.512776, 3.391118], [6.512986, 3.391188], [6.515244, 3.39174],
        [6.515645, 3.39179], [6.516234, 3.391781], [6.5174, 3.391643], [6.5174, 3.391643],
        [6.518958, 3.391456], [6.518996, 3.391478], [6.519062, 3.391459], [6.519084, 3.391414],
        [6.518946, 3.390819], [6.518845, 3.39055], [6.518786, 3.390418], [6.518631, 3.390174],
        [6.518152, 3.38954], [6.518025, 3.389333], [6.517852, 3.388948], [6.51758, 3.388034],
        [6.517636, 3.387979], [6.517604, 3.387691]
    ]
)


class TaskTypeMobile(sim.Component):
    """Class to generate mobile tasks"""

    def __init__(self, coord_index, server, process_time, cpu, loc_lat, loc_lon, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.coord_index = coord_index
        self.server = server
        self.process_time = process_time
        self.cpu = cpu
        self.loc_lat = loc_lat
        self.loc_lon = loc_lon
        self.name = 'mob'

    def process(self):
        while True:
            # the starting attributes of each generated task
            self.coord_index = sim.IntUniform(10, 30).sample()
            self.server = sim.Pdf((server0, server1, server2), (40, 30, 20)).sample()
            self.process_time = 40
            self.cpu = sim.IntUniform(300, 500).sample()

            # invoke the Task class
            Task(self.coord_index, self.server, self.process_time, self.cpu,
                 self.loc_lat, self.loc_lon)

            # hold till next schedule event
            yield self.hold(sim.Poisson(10).sample())


class TaskType1(sim.Component):
    """Class to generate tasks in segment 1"""

    def __init__(self, coord_index, server, process_time, cpu, loc_lat, loc_lon, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.coord_index = coord_index
        self.server = server
        self.process_time = process_time
        self.cpu = cpu
        self.loc_lat = loc_lat
        self.loc_lon = loc_lon

    def process(self):
        while True:
            # the starting attributes of each generated task
            self.process_time = 9
            self.loc_lat = sim.Uniform(6.513, 6.518).sample()
            self.loc_lon = sim.Uniform(3.397, 3.4).sample()
            self.cpu = sim.Uniform(750, 1000).sample()

            # invoke the Task class
            Task(self.coord_index, self.server, self.process_time, self.cpu,
                 self.loc_lat, self.loc_lon)

            # hold till next schedule event
            yield self.hold(sim.Poisson(25).sample())


class TaskType2(sim.Component):
    """Class to generate tasks in segment 2"""

    def __init__(self, coord_index, server, process_time, cpu, loc_lat, loc_lon, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.coord_index = coord_index
        self.server = server
        self.process_time = process_time
        self.cpu = cpu
        self.loc_lat = loc_lat
        self.loc_lon = loc_lon

    def process(self):
        while True:
            # the starting attributes of each generated task
            self.process_time = 5
            self.loc_lat = sim.Uniform(6.511, 6.518).sample()
            self.loc_lon = sim.Uniform(3.388, 3.397).sample()
            self.cpu = sim.Uniform(400, 750).sample()

            # invoke the Task class
            Task(self.coord_index, self.server, self.process_time, self.cpu,
                 self.loc_lat, self.loc_lon)

            # hold till next schedule event
            yield self.hold(sim.Poisson(14).sample())


class TaskType3(sim.Component):
    """Class to generate tasks in segment 3"""

    def __init__(self, coord_index, server, process_time, cpu, loc_lat, loc_lon, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.coord_index = coord_index
        self.server = server
        self.process_time = process_time
        self.cpu = cpu
        self.loc_lat = loc_lat
        self.loc_lon = loc_lon

    def process(self):
        while True:
            # the starting attributes of each generated task
            self.process_time = 2
            self.loc_lat = sim.Uniform(6.509, 6.513).sample()
            self.loc_lon = sim.Uniform(3.388, 3.398).sample()
            self.cpu = sim.Uniform(100, 400).sample()

            # invoke the Task class
            Task(self.coord_index, self.server, self.process_time, self.cpu,
                 self.loc_lat, self.loc_lon)

            # hold till next schedule event
            yield self.hold(sim.Poisson(8).sample())


class UpdateServerDis(sim.Component):
    """Class to update the distance measure"""

    def __init__(self, coord_index, server, loc_lat, loc_lon, task, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.coord_index = coord_index
        self.server = server
        self.loc_lat = loc_lat
        self.loc_lon = loc_lon
        self.task = task

    def process(self):
        while True:

            yield self.hold(10)  # update server distance every 10 millisecond
            current_server = self.task.server

            # compute the distance measure
            # first increment the task coordinates for the mobile task by moving it some coordinates ahead
            if self.name == 'mob':  # if the task is mobile task, otherwise pass this logic
                self.coord_index += sim.IntUniform(1, 4).sample()

                # then get the current location latitude and longitude
                loc = ant_path.locations[self.coord_index]
                self.loc_lat = loc[0]
                self.loc_lon = loc[1]

            # then compute the distances
            d0 = mpu.haversine_distance((self.loc_lat, self.loc_lon), (server0_lat, server0_lon))
            d1 = mpu.haversine_distance((self.loc_lat, self.loc_lon), (server1_lat, server1_lon))
            d2 = mpu.haversine_distance((self.loc_lat, self.loc_lon), (server2_lat, server2_lon))

            # set the server according to min distance measure and min CPU utilization
            if min([d0, d1, d2]) == d0:
                self.choose_min_cpu()

            if min([d0, d1, d2]) == d1:
                self.choose_min_cpu()

            if min([d0, d1, d2]) == d2:
                self.choose_min_cpu()

            updated_server = self.task.server  # update the task with the new server

            if updated_server != current_server:
                # if the server changes, release the server that was initially seized
                self.task.release()
                # update the server
                self.task.server = updated_server
                # activate or continue the computation in the new server
                self.task.activate()

    def choose_min_cpu(self):
        # the CPU utilization in each server
        cpu0_util = server0.occupancy.value
        cpu1_util = server1.occupancy.value
        cpu2_util = server2.occupancy.value

        if min([cpu0_util, cpu1_util, cpu2_util]) == cpu0_util:
            self.task.server = server0
        if min([cpu0_util, cpu1_util, cpu2_util]) == cpu1_util:
            self.task.server = server1
        if min([cpu0_util, cpu1_util, cpu2_util]) == cpu2_util:
            self.task.server = server2


class Task(sim.Component):
    """Class to process the task"""

    def __init__(self, coord_index, server, process_time, cpu, loc_lat, loc_lon, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.coord_index = coord_index
        self.server = server
        self.process_time = process_time
        self.cpu = cpu
        self.loc_lat = loc_lat
        self.loc_lon = loc_lon
        self.update_server = UpdateServerDis(self.coord_index, self.server,
                                             self.loc_lat, self.loc_lon, task=self)

    def process(self):
        time_remain = self.process_time
        while time_remain > 0:
            yield self.request((self.server, self.cpu))
            if self.isclaiming():  # if the task is claiming a server, then continue with processing
                yield self.hold(time_remain, mode='hold')
                # if the hold was not cancelled, process_time_remain will be set to zero here!
                time_remain -= env.now() - self.mode_time()
        self.release()
        self.update_server.cancel()


# set up the simulation environment
env = sim.Environment(trace=False)

# the dashboard background color
env.background_color("white")

# the resources and their resource usage statistics monitors
server0 = sim.Resource("server 0", capacity=1500)
server1 = sim.Resource("server 1", capacity=1500)
server2 = sim.Resource("server 2", capacity=1500)

# animate task processing (claimers) and task waiting (requesters)
for i, server in enumerate((server0, server1, server2)):
    sim.AnimateQueue(server.claimers(), x=340, y=600 - i * 235, direction="e", title=f'Tasks processing in Server{i}')
    sim.AnimateQueue(server.requesters(), x=40, y=600 - i * 235, direction="e", title=f'Tasks in queue for Server{i}')

# text for the dashboard title
sim.AnimateText(text='Your dashboard and controls', x=120, y=680, font='narrow', fontsize=30, textcolor='darkblue')

# initiate the task generator processes to start
coord_index = sim.IntUniform(10, 30).sample()  # will be used to set the ant path location index
server = sim.Pdf((server0, server1, server2), (40, 30, 20)).sample()  # the server that is seized
process_time = sim.IntUniform(25, 40).sample()  # the process time of the task
cpu = sim.IntUniform(500, 900).sample()  # the cpu that is requested
loc_lat = ant_path.locations[coord_index][0]  # will be used to compute distance measure
loc_lon = ant_path.locations[coord_index][1]  # will be used to compute distance measure

TaskTypeMobile(coord_index, server, process_time, cpu, loc_lat, loc_lon)
TaskType1(coord_index, server, process_time, cpu, loc_lat, loc_lon)
TaskType2(coord_index, server, process_time, cpu, loc_lat, loc_lon)
TaskType3(coord_index, server, process_time, cpu, loc_lat, loc_lon)

# animate the simulation environment
env.animate(True)

# set the animation speed (it can be adjusted later in the dashboard)
env.speed(1)

# run the simulation till you stop the simulation using dashboard stop button
env.run(200)
