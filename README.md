# simulation-edge-computing
This repository is intended to aggregate a set of reproducible and reconfigurable codes and notebooks for testing various task placement policies for edge and fog server networks. 

The simulation models are based on two of the most powerful python-based simulation modeling frameworks, namely salabim and simpy. 

The systems that are modelled cover the basic types of task placement problems in edge computing servers. The models are useful for managing a network of edge computing servers. There are animation and GUI options which are indispensable in simulation modelling.

The model- load_balancing_with_mobllity_aware_task_placement.py -models an edge network with mobile and stationary users. The objective is to assign computing requests to a) the nearest edge server and b) to the least utilized server. This implements a policy to reduce bandwidth usage and ensure load balancing within the edge network.
