import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')
import matplotlib.font_manager as font_manager
import random
import numpy as np

csfont = {'fontname':'Comic Sans MS'}


class MakePlot:
    def __init__(self):
        fig, ax = plt.subplots(1,1, figsize=(9,5))
        self.ax = ax

        self.xlabel = None
        self.ylabel = None
        self.title = None
        self.filename = None

        self.x = None
        self.y = None
        self.stdev = None

        self.data_label = None

        self.tnrfont = {'fontname':'Times New Roman'}

    def set_xy(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
    
    def set_axis_labels(self, xlabel, ylabel, title=None):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

    def set_data_labels(self, label):
        self.data_label = label

    def set_stdev(self, stdev):
        self.stdev = stdev

    def set_savefig(self, filename):
        self.filename = filename

    def plot_xy(self):

        self.ax.spines.right.set_visible(False)
        self.ax.spines.top.set_visible(False)
        
        self.ax.set_ylabel(self.ylabel, **self.tnrfont, fontsize=14)
        self.ax.set_xlabel(self.xlabel, **self.tnrfont, fontsize=14)
        self.ax.set_title(self.title, **self.tnrfont, fontsize=16)

        for i, y in enumerate(self.y):
            self.ax.plot(self.x, y, label=self.data_label[i])

            if self.stdev is not None:
                self.ax.fill_between(self.x, y - self.stdev[i], y + self.stdev[i], alpha=0.3)

    def label_and_save(self):
        font = font_manager.FontProperties(family='Times New Roman',
                                    weight='normal',
                                    style='normal')
        
        plt.legend(loc=0, prop=font, fontsize=13)
        plt.xticks(**self.tnrfont, fontsize=13)
        plt.yticks(**self.tnrfont, fontsize=13)

        plt.savefig(self.filename)

        plt.show()


if __name__ == "__main__":
    n = 10
    y1 = random.sample(range(0,n), n)
    y2 = random.sample(range(0,n), n)
    x = np.linspace(0, n, n)

    my_plot = MakePlot()
    my_plot.set_xy(x, [y1, y2])
    my_plot.set_data_labels(["data1", "data2"])
    my_plot.set_axis_labels("x", "y", "title")
    my_plot.set_stdev([0.2, 0.1])
    my_plot.set_savefig("testfig")

    my_plot.plot_xy()
    my_plot.label_and_save()




        

        

    

    
