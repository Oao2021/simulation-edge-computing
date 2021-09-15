# simulation-edge-computing
This repository is intended to aggregate a set of reproducible and reconfigurable notebooks for testing various task placement policies for edge and fog server networks. Contributors are welcome to populate this repository with models to cover all manner of scenarios.

The simulation model (main.py) is built upon the simpy framework (https://simpy.readthedocs.io/en/latest/). Matplotlib is used in graphing purposes

The jupyter notebook (dynamic-scaling-of-edge-nodes.ipynb) implements dynamic scaling up or down, the number of edge nodes in the network. Notebook (auto-scaling-of-edge-nodes.ipynb) implements auto scaling up and down of the number of edge nodes

Notebook base-model.ipynb is an example of the starting model. In notebook (locality-aware-edge-scheduler-simulation.ipynb), the base model is modified to test a locality-aware task placement policy. In a network of edge nodes, placement and scheduling of tasks on edge nodes considers the nearest edge node to place the received task. This is referred to as a locality-aware task placement/ scheduling policy.  The base model, in a similar fashion, can be easily re-configured to test energy-aware, resource-aware, bandwidth-aware, cost-aware, latency-aware policies.

To test a mobile edge node, the moving car is used as a fourth node, see the notebook, locality-aware-edge-scheduler-simulation-V2.ipynb

To add animation and GUI features ipyleaflet (https://ipyleaflet.readthedocs.io/en/latest/) and ipywidgets (https://ipywidgets.readthedocs.io/en/stable/) are the frameworks used for enabling animation and GUI enhancements. 
