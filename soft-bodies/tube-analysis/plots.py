import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

def trim(array, stop_time):
    fps = 30
    start_time = 0*fps # sec
    # stop_time = 50*fps
    stop_time = stop_time*fps

    array = array[start_time:stop_time]
    return array

def preprocess(folder_path, stop_time):

    area_list = []
    t_list = []

    data_name = [1,2,3]
    for name in data_name:
        area = np.load(folder_path+str(name)+"-area.npy")
        t = np.load(folder_path+str(name)+"-t.npy")

        area = np.array(area, dtype=float)

        area = trim(area, stop_time)
        t = trim(t, stop_time)

        area_list.append(area)
        t_list.append(t)

    return area_list, t_list

def plot(my_plot, t, area_avg, area_std, data_label):
    my_plot.set_xy(t, area_avg, '.')
    my_plot.set_stdev(area_std)
    my_plot.set_data_labels(data_label)
    my_plot.set_axis_labels(xlabel="Time (sec)", ylabel="Area (mm$^2$)")
    my_plot.plot_xy()
    
def shell():
    shell_plot = MakePlot()

    folder_path = "data/shell/all-on/"
    area_list, t_list = preprocess(folder_path, stop_time=85)

    area_list[1] = area_list[1][0:len(area_list[0])]
    area_list[0] = area_list[0] + 40

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)
    print("all on")
    print(area_avg[0])
    print(min(area_avg))

    plot(shell_plot, t_list[0], area_avg, area_std, "Activated simultaneously")

    np.save("data/averages/shell_all-on_avg.npy", area_avg)
    np.save("data/averages/shell_all-on_t.npy", t_list[0])
   
    ########
    folder_path = "data/shell/pulse-hold/"
    area_list, t_list = preprocess(folder_path, stop_time=85)

    area_list[0] = area_list[0] + 20
    area_list[1] = area_list[1] - 30
    area_list[2] = area_list[2] - 30

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)
    print("pulse hold")
    print(area_avg[0])
    print(min(area_avg))

    plot(shell_plot, t_list[0], area_avg, area_std, "Activated in sequence")

    np.save("data/averages/shell_pulse-hold_avg.npy", area_avg)
    np.save("data/averages/shell_pulse-hold_t.npy", t_list[0])

    ########
    folder_path = "data/shell/pulse-release/"
    area_list, t_list = preprocess(folder_path, stop_time=85)

    area_list[0] = area_list[0] + 90
    area_list[2] = area_list[2] + 40

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)
    print("pulse release")
    print(area_avg[0])
    print(min(area_avg))

    plot(shell_plot, t_list[0], area_avg, area_std, "Activated and released")

    shell_plot.set_savefig("shell-3-responses.pdf")
    shell_plot.label_and_save()

    np.save("data/averages/shell_pulse-release_avg.npy", area_avg)
    np.save("data/averages/shell_pulse-release_t.npy", t_list[0])

    
def tube(): 
    tube_plot = MakePlot()

    #######
    folder_path = "data/tube/all-on/"
    area_list, t_list = preprocess(folder_path, stop_time=90)
    
    area_list[0] = area_list[0] + 32
    area_list[1] = area_list[1] + 12
    area_list[2] = area_list[2] + 20
    
    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)
    print("all on")
    print(area_avg[0])
    print(min(area_avg))

    plot(tube_plot, t_list[0], area_avg, area_std, "Activated simultaneously")

    np.save("data/averages/tube_all-on_avg.npy", area_avg)
    np.save("data/averages/tube_all-on_t.npy", t_list[0])

    #######
    folder_path = "data/tube/pulse-hold/"
    area_list, t_list = preprocess(folder_path, stop_time=90)

    area_list[0] = area_list[0] - 7
    area_list[1] = area_list[1] - 2
    area_list[2] = area_list[2] - 2

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)
    print("pulse-hold")
    print(area_avg[0])
    print(min(area_avg))

    plot(tube_plot, t_list[0], area_avg, area_std, "Activated in sequence")

    np.save("data/averages/tube_pulse-hold_avg.npy", area_avg)
    np.save("data/averages/tube_pulse-hold_t.npy", t_list[0])

    #######
    folder_path = "data/tube/pulse-release/"
    area_list, t_list = preprocess(folder_path, stop_time=90)

    area_list[0] = area_list[0] + 20
    area_list[1] = area_list[1] + 30
    area_list[2] = area_list[2] + 25

    area_avg = np.mean(area_list, axis=0)
    area_std = np.std(area_list, axis=0)
    print("pulse-release")
    print(area_avg[0])
    print(min(area_avg))

    plot(tube_plot, t_list[0], area_avg, area_std, "Activated and released")

    tube_plot.set_savefig("tube-3-responses2.png")
    tube_plot.label_and_save()

    np.save("data/averages/tube_pulse-release_avg.npy", area_avg)
    np.save("data/averages/tube_pulse-release_t.npy", t_list[0])

tube()