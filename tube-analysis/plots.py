import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

def trim(array):
    fps = 30
    start_time = 0*fps # sec
    # stop_time = 50*fps
    stop_time=85*fps

    array = array[start_time:stop_time]
    return array

def preprocess(folder_path):

    area_list = []
    t_list = []

    data_name = [1,2,3]
    for name in data_name:
        area = np.load(folder_path+str(name)+"-area.npy")
        t = np.load(folder_path+str(name)+"-t.npy")

        area = np.array(area, dtype=float)

        area = trim(area)
        t = trim(t)

        area_list.append(area)
        t_list.append(t)

    return area_list, t_list

def plot(my_plot, t, area_avg, area_std, data_label):
    my_plot.set_xy(t, area_avg, '.')
    my_plot.set_stdev(area_std)
    my_plot.set_data_labels(data_label)
    my_plot.set_axis_labels(xlabel="Time (sec)", ylabel="Area (mm^2)")
    my_plot.plot_xy()

    
def shell():
    shell_plot = MakePlot()

    folder_path = "data/shell/all-on/"
    area_list, t_list = preprocess(folder_path)

    area_list[1] = area_list[1][0:len(area_list[0])]
    area_list[0] = area_list[0] + 40

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)

    plot(shell_plot, t_list[0], area_avg, area_std, "Activated simultaneously")
    ########
    folder_path = "data/shell/pulse-hold/"
    area_list, t_list = preprocess(folder_path)

    print(area_list[0][0], area_list[1][0], area_list[2][0])

    area_list[0] = area_list[0] + 20
    area_list[1] = area_list[1] - 30
    area_list[2] = area_list[2] - 30

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)

    plot(shell_plot, t_list[0], area_avg, area_std, "Activated in sequence")

    ########
    folder_path = "data/shell/pulse-release/"
    area_list, t_list = preprocess(folder_path)

    area_list[0] = area_list[0] + 90
    area_list[2] = area_list[2] + 40

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)

    plot(shell_plot, t_list[0], area_avg, area_std, "Activated and released")

    shell_plot.set_savefig("shell-3-responses.png")
    shell_plot.label_and_save()

    
def tube(): 
    tube_plot = MakePlot()

    folder_path = "data/tube/all-on/"
    area_list, t_list = preprocess(folder_path)

    # area_list[1] = area_list[1][0:len(area_list[0])]
    area_list[2] = area_list[2] - 10

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)

    plot(tube_plot, t_list[0], area_avg, area_std, "Activated simultaneously")

    tube_plot.set_savefig("tube-1-response.png")
    tube_plot.label_and_save()


shell()

