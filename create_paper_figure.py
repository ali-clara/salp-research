import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')
import matplotlib.font_manager as font_manager
import random
import numpy as np

csfont = {'fontname':'Comic Sans MS'}

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

class MakePlot:
    def __init__(self, subplots=None):
        fig, ax = plt.subplots(1,1, figsize=(9,4))
        self.ax = ax

        if subplots is not None:
            fig, ax = plt.subplots(subplots[0], subplots[1], figsize=(9,5))
            self.axs = ax
            self.ax = None
            self.num_subplots = subplots[0] + subplots[1]

        self.xlabel = None
        self.ylabel = None
        self.title = None
        self.filename = None

        self.x = None
        self.y = None
        self.stdev = None

        self.xlim = None

        self.data_label = None
        self.linestyle = None

        self.tnrfont = {'fontname':'Times New Roman'}
        
        # colors chosen from the Color Universal Design pallete http://people.apache.org/~crossley/cud/cud.html
        colors = ["#e69f00",
                  "#0072b2",
                  "#d55e00",
                #   "#56b4e9",
                  "#cc79a7",
                #   "#f0e442",
                  "#009e73"]
        
        self.unused_colors = colors
        self.last_used_color = None

    def set_subplot(self, subplot):
        self.ax = self.axs[subplot]

    def set_xlim(self, xlim):
        self.xlim = xlim
    
    def set_xy(self, x, y, linestyle="-"):
        self.x = np.array(x)
        self.y = np.array(y)
        self.linestyle = linestyle
    
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

    def reset_params(self):
        self.x = None
        self.y = None
        self.stdev = None
        self.data_label = None

    def use_same_color(self):
        self.unused_colors.insert(0, self.last_used_color)

    def plot_xy(self):

        self.ax.spines.right.set_visible(False)
        self.ax.spines.top.set_visible(False)
        
        self.ax.set_ylabel(self.ylabel, **self.tnrfont, fontsize=20)
        self.ax.set_xlabel(self.xlabel, **self.tnrfont, fontsize=20)
        self.ax.set_title(self.title, **self.tnrfont, fontsize=20)

        fontname = "Times New Roman"
        labels = self.ax.get_xticklabels() + self.ax.get_yticklabels()
        [label.set_fontname(fontname) for label in labels]
        [label.set_fontsize(18) for label in labels]

        # if self.data_label is not None:
        self.ax.plot(self.x, self.y,
                        self.linestyle, 
                         markersize=3,
                         label=self.data_label, 
                         color=self.unused_colors[0])
                        #  linestyle=self.linestyle)

        # else:
        #     self.ax.plot(self.x, self.y, 
        #                  label=self.data_label, 
        #                  color=self.unused_colors[0],
        #                  linestyle = self.linestyle)

        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        
        if self.stdev is not None:
            self.ax.fill_between(self.x, self.y - self.stdev, self.y + self.stdev, 
                                 alpha=0.3, 
                                 color=self.unused_colors[0])

        self.last_used_color = self.unused_colors.pop(0)

        self.reset_params()
    
    def label_and_save(self):
        font = font_manager.FontProperties(family='Times New Roman',
                                    weight='normal',
                                    size='large',
                                    style='normal')
        
        # if self.data_label is not None:
        #     plt.legend(loc=0, prop=font)

        plt.legend(loc="center right", prop=font)

        plt.tight_layout()
        plt.savefig(self.filename)
        
        plt.show()


if __name__ == "__main__":
    n = 10
    x = np.linspace(0, n, n)

    my_plot = MakePlot()

    for i in range(4):
        y = random.sample(range(0,n), n)
    
        my_plot.set_xy(x, y)
        my_plot.set_data_labels("data "+str(i))
        my_plot.set_stdev(0.2)
        my_plot.plot_xy()

        my_plot.use_same_color()
        my_plot.set_xy(x, np.array(y)+0.5, '--')
        my_plot.plot_xy()
    
    my_plot.set_axis_labels("x", "y", "title")
    my_plot.set_savefig("testfig")
    my_plot.label_and_save()

    my_subplots = MakePlot(subplots=(1,2))
    my_subplots.set_subplot(0)
    my_subplots.set_xy(x, x)
    my_subplots.plot_xy()
    
    my_subplots.set_subplot(1)
    my_subplots.set_xy(x, x)
    my_subplots.plot_xy()

    my_subplots.set_savefig("testfig-subplots.png")
    my_subplots.label_and_save()
    




        

        

    

    
