# simulation-edge-computing
This repository is intended to aggregate a set of reproducible and reconfigurable codes and notebooks for testing various task placement policies for edge and fog server networks. 

The simulation models are based on two of the most powerful python-based simulation modeling frameworks, namely salabim and simpy. 

The systems that are modelled cover the basic types of task placement problems in edge computing servers. The models are useful for managing a network of edge computing servers. There are animation and GUI options which are indispensable in simulation modelling.

There is a base model (base_model_EdgePolicySim.ipynb) which models a network area with stationary and mobile users. The model conisders task migration from one server to another as a mobile user journeys within the network area. The base model is provisioned to implement a task scheduling algorithm. In the extended model (EdgePolicySim_with_task_placement_policy.ipynb) a task placement policy is introduced.
