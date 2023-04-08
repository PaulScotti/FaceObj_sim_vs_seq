PsychoPy scripts for Face-Obj 3AFC simultaneous vs. sequential task

PsychoPy > File > Open > sequential/simultaneous.py > Run experiment

Edit the .py files to change sub_num and experiment variables

To analyse, use Python:

data = np.load('data/sub-#/sub-#_sequential_objafc.npy',allow_pickle=True).item()

Example behavioral data output is contained in data/sub-999
