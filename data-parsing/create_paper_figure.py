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
        self.linestyle = None

        self.tnrfont = {'fontname':'Times New Roman'}
        
        # colors chosen from the Color Universal Design pallete http://people.apache.org/~crossley/cud/cud.html
        colors = ["#e69f00",
                  "#0072b2",
                  "#cc79a7",
                  "#56b4e9",
                  "#009e73",
                  "#f0e442",
                  "#d55e00"]
        
        self.unused_colors = colors
        self.last_used_color = None

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
        
        self.ax.set_ylabel(self.ylabel, **self.tnrfont, fontsize=14)
        self.ax.set_xlabel(self.xlabel, **self.tnrfont, fontsize=14)
        self.ax.set_title(self.title, **self.tnrfont, fontsize=16)

        if self.data_label is not None:
            self.ax.plot(self.x, self.y, 
                         label=self.data_label, 
                         color=self.unused_colors[0],
                         linestyle=self.linestyle)

        else:
            self.ax.plot(self.x, self.y, 
                         label=self.data_label, 
                         color=self.unused_colors[0],
                         linestyle = self.linestyle)

        if self.stdev is not None:
            self.ax.fill_between(self.x, self.y - self.stdev, self.y + self.stdev, 
                                 alpha=0.3, 
                                 color=self.unused_colors[0])

        self.last_used_color = self.unused_colors.pop(0)

        self.reset_params()

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




        

        

    

    
