"""
In this model, an edge server is modelled as a knapsack
The scheduler aims to place tasks in such a way as to maximize
the number of tasks that are placed on the edge server at any time.
The TaskScheduler class which implements the knapsack scheduler,
is based on Google OR-Tools. The code is modified from
https://developers.google.com/optimization/bin/bin_packing
The use of python to model task placement allows for seamless
integration of the scheduler with many python-based modules,
which enhances model robustness and wide spread usability.
Salabim is one of the most powerful python-based simulation modelling frameworks
which allows building of discrete event simulation as well as agent based models,
with in-built gui and animation engines.
"""

import salabim as sim
from ortools.linear_solver import pywraplp

# some initial settings
min_cpu0 = 250
max_cpu0 = 1200

cpu_requested = 0
route_id = 0

cpu = []
values = []


class TaskGenerator(sim.Component):
    def __init__(self, cpu_requested, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.cpu_requested = cpu_requested

    def process(self):
        while True:
            self.cpu_requested = sim.IntUniform(min_cpu0, max_cpu0).sample()
            cpu.append(self.cpu_requested)
            values.append(1)
            TaskScheduler.main(self)
            yield self.hold(sim.Uniform(0, 3).sample())
            # print(self.cpu_requested)
            # print(cpu)

"""
The taskScheduler class was incorporated from the example model from
https://developers.google.com/optimization/bin/multiple_knapsack
"""
class TaskScheduler(sim.Component):
    def __init__(self, cpu_requested, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.cpu_requested = cpu_requested

    def create_data_model(self):
        """Create the data for the example."""
        data = {}
        data['cpu'] = cpu
        data['values'] = values
        data['items'] = list(range(len(cpu)))
        data['bins'] = list(range(1))
        data['bin_capacities'] = [serve0.available_quantity()]  # capacities of each knapsack
        return data

    def main(self):
        data = TaskScheduler.create_data_model(self)

        # Create the mip solver with the SCIP backend.
        solver = pywraplp.Solver.CreateSolver('SCIP')

        # Create the variables to the problem
        x = {}
        for i in data['items']:
            for j in data['bins']:
                x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

        # Define the constraints
        # Each item can be placed in at most one server
        for i in data['items']:
            solver.Add(sum(x[i, j] for j in data['bins']) <= 1)

        # The amount packed in each bin cannot exceed its capacity.
        # This constraint is set by requiring the sum of the cpu of
        # items placed in bin j to be less than or equal to the capacity of the bin
        for j in data['bins']:
            solver.Add(
                sum(x[(i, j)] * data['cpu'][i]
                    for i in data['items']) <= data['bin_capacities'][j])

        # Define the objective, which is the total value of the packed items
        objective = solver.Objective()

        # Note that x(i, j)] * data['values'[i] adds the value of item i to
        # the objective if the item is placed in bin j. If i is not placed
        # in any bin, its value doesn't contribute to the objective
        for i in data['items']:
            for j in data['bins']:
                objective.SetCoefficient(x[(i, j)], data['values'][i])
        objective.SetMaximization()

        # call the solver and allocate the cpu requests
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            total_weight = 0
            for j in data['bins']:
                bin_cpu = 0
                for i in data['items']:
                    if x[i, j].solution_value() > 0:
                        bin_cpu += data['cpu'][i]
                        TaskService(self.cpu_requested)
                total_weight += bin_cpu

class TaskService(sim.Component):
    def __init__(self, cpu_requested, *args, **kwargs):
        sim.Component.__init__(self, *args, **kwargs)
        self.cpu_requested = cpu_requested

    def animation_objects(self, id):
        title, number = self.name().split('.')
        ao0 = sim.AnimateRectangle((-18, 0, 18, 18), text=number, fillcolor=id, fontsize=10, font='narrow',
                                   textcolor='black', arg=self)
        return 45, 0, ao0

    def process(self):
        global min_cpu0
        global max_cpu0

        if self.cpu_requested > 700:
            processing_time = sim.Uniform(10, 15).sample()
        else:
            processing_time = sim.Uniform(3, 6).sample()

        yield self.request((serve0, self.cpu_requested))
        yield self.hold(processing_time)

def set_max_cpu0(val):
    global max_cpu0
    max_cpu0 = int(val)


def set_min_cpu0(val):
    global min_cpu0
    min_cpu0 = int(val)


# Setup and start the simulation
env = sim.Environment(trace=False)

# Model the resource with the animation and monitor
# resource
serve0 = sim.Resource('serve0', capacity=1500)

# animate resource queue
serve0.requesters().animate(x=300, y=100, title='Tasks waiting to enter server0', direction="e", id='deepskyblue')
serve0.claimers().animate(x=300, y=180, title='Tasks in server0', direction="e", id='yellowgreen')

# monitor resource using text
sim.AnimateText(text=lambda: serve0.occupancy.print_statistics(as_str=True), x=10, y=435, text_anchor='nw',
                font='narrow', fontsize=12, textcolor=lambda: 'red' if serve0.occupancy.value > 0.7 else 'black')

# monitor the resource using charts
sim.AnimateMonitor(serve0.requesters().length, x=10, y=450, width=480, height=100, horizontal_scale=5, vertical_scale=5,
                   title='Number of tasks in waiting')
sim.AnimateMonitor(serve0.requesters().length_of_stay, x=10, y=580, width=480, height=100, horizontal_scale=5, vertical_scale=5,
                   title='Wait time to be serviced')

# dynamic sliders
# sliders for adjusting the minimum and maximum cpu that can be requested
sim.AnimateSlider(x=60, y=-700, width=90, height=20, vmin=100, vmax=400, resolution=1, v=min_cpu0,
                  label="adjust min cpu0", action=set_min_cpu0, xy_anchor="nw", )

sim.AnimateSlider(x=180, y=-700, width=90, height=20, vmin=500, vmax=1200, resolution=1, v=max_cpu0,
                  label="adjust max cpu0", action=set_max_cpu0, xy_anchor="nw", )

sim.AnimateText(text='Your dashboard and controls', x=200, y=690, font='narrow', fontsize=30)

# text for the pdf sliders

# Create environment and start processes
TaskGenerator(cpu_requested=cpu_requested)


env.background_color('white')
env.animate(True)
env.speed(1)  # 5 times the wall clock speed
env.run(500)


"""
r = sim.Resource("r non premeptive", 3, preemptive=False)
rp = sim.Resource("r preemptive", 3, preemptive=True)
r.requesters().animate(x=700, y=100)
r.claimers().animate(x=850, y=100, direction="e")
rp.requesters().animate(x=700, y=200)
rp.claimers().animate(x=850, y=200, direction="e")
"""