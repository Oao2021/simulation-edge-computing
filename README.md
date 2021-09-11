# simulation-edge-computing
A python-based simulation model for testing task placement policies in edge servers.

The model (main.py) is built upon the simpy framework (https://simpy.readthedocs.io/en/latest/). Matplotlib is used in graphing.
The jupyter notebook (# dynamic-scaling-of-edge-nodes.ipynb) implements dynamic scaling up or down, the number of edge nodes in the network. The notebook (auto-scaling-of-edge-nodes.ipynb) implements auto scling up and down of the number of edge nodes.

To add animation and GUI features to the simpy model, jupyter notebook is used. Ipyleaflet (https://ipyleaflet.readthedocs.io/en/latest/) and ipywidgets (https://ipywidgets.readthedocs.io/en/stable/) are the frameworks used for enabling animation and GUI enhancements. In the accompanying notebook (build-an-animated-and-GUI-simumalation-model.ipynb), only 1 edge computing server is modelled. Other animation objects are added to enhance the animation.
