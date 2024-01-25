import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
from matplotlib.animation import FuncAnimation
import matplotlib.patches as ptchs

class Geometry():
    def __init__(self, a=25.0, c=21.4, alpha=60, N=6) -> None:
        """Initializes an instance of the Miura class. 
        
        Option to set the geometric parameters of a Miura tube:
            a (cell base width/length, mm), c (half cell height, mm), alpha (cell angle, deg), N (number of cells)"""
        
        self.a = a
        self.N = N

        self.L_expanded = self._calculate_tube_length(c)
        self.L_contracted = 2*2*N     # rough guess for now
        self.cell_hypotenuse = self._calculate_cell_hypotenuse(c, alpha)

    def _calculate_tube_length(self, c):
        """Calculates the length of the tube based on the initial height of each parallelepipid"""
        l = c*2*self.N
        return l
    
    def _calculate_cell_hypotenuse(self, c, alpha):
        """Calculates the length of the sloped side of the parallelepipid. Based on the initial cell height"""
        d = c / np.sin(np.deg2rad(alpha))
        return d
    
    def calculate_base_area(self, L_current):
        """Finds the area of the parallelogram base of each parallelepipid"""

        area_expanded = self.a**2
        area_contracted = np.sqrt(3)/2*self.a**2

        area_current = np.interp(L_current, [self.L_contracted, self.L_expanded], [area_contracted, area_expanded])
        return area_current
    
    def calculate_cell_height(self, L):
        """Calculates the height of each parallelepipid based on the total length.
        
            L - current length of the tube. Changes with time"""
        c = L / (2*self.N)
        return c
    
    def calculate_tube_volume(self, L):
        base_area = self.calculate_base_area(L)
        v = base_area*L
        return v

    def find_top_points(self, c, plotting):
        top_points = []
        for i in range(2*self.N+1):
            x = i*c
            # even numbers = lower half of the top zig zag (changes with length)
            if i%2 == 0:
                y = -np.sqrt(self.cell_hypotenuse**2 - c**2)
            # odd numbers = upper half of the top zig zag (constant)
            else:
                y = 0

            top_points.append([x,y])
            if plotting:
                top_points.append([x,y])

        # remove the first and last element from list (only plot those points once)
        if plotting:
            top_points.pop(0)
            top_points.pop()

        return top_points
    
    def find_bottom_points(self, c, plotting):
        bottom_points = []
        for i in range(2*self.N+1):
            x = i*c
            # even numbers = the lower half of the bottom zig zag (constant)
            if i%2 == 0:
                y = -2*self.a
            # odd numbers = the upper half of the bottom zig zag (changes with length)
            else:
                y = -2*self.a + np.sqrt(self.cell_hypotenuse**2 - c**2)

            bottom_points.append([x,y])
            if plotting:
                bottom_points.append([x,y])

        # remove the first and last element from list (only plot those points once)
        if plotting:
            bottom_points.pop(0)
            bottom_points.pop()

        return bottom_points
    
    def find_tube_points(self, L, plotting=True):
        """Finds the (x,y) points of the Miura tube vertices. \\
                L - current length of the tube \\
                plotting - boolean, if True returns each point twice to format for plotting \\
                Returns - np.array of (x,y) points"""
        
        # find the height of each cell based on the current tube length
        c = self.calculate_cell_height(L)
        # calculate and collect the zig zag pattern of the 2D Miura tube side profile
        top_points = self.find_top_points(c, plotting)
        bottom_points = self.find_bottom_points(c, plotting)

        return np.array(top_points), np.array(bottom_points)
    
    def plot_tube_side(self, L):
        top_points, bottom_points = self.find_tube_points(L)

        # collect x and y into pairs
        tx = np.vstack([top_points[:,0][0::2],top_points[:,0][1::2]])
        ty = np.vstack([top_points[:,1][0::2],top_points[:,1][1::2]])
        bx = np.vstack([bottom_points[:,0][0::2],bottom_points[:,0][1::2]])
        by = np.vstack([bottom_points[:,1][0::2],bottom_points[:,1][1::2]])

        plt.plot(tx, ty)
        plt.plot(bx, by)
        plt.xlim([-5, self.L_expanded+5])
        plt.ylim([-2*(self.a+1), 2])
        plt.show()
    
    def animate_shape_and_volume(self, shape_name, shape, ref_length_name, ref_length, volume):
        """
        Animates the shape change over time and plots the volume change with 
        respect to the reference length (i.e radius, length, circumference, etc)\\
        Inputs: \\
            shape_name (str) - what shape we're plotting \\
            shape (list with floats or np arrays) - list of points representing the shape to plot, each row is a pair of points or a pair of arrays to plot together \\ 
            ref_length_name (str) - what length we're referencing \\
            ref_length (np array) - reference length (mm) \\
            volume (np array) - volume calculated across the refernce length (mL) \\

        """
        fig, ax = plt.subplots(2,1, figsize=(5,5))
        plt.tight_layout(pad=2)

        def animate(i):
            # plot the shape
            ax[0].clear()
            for row in shape:
                ax.plot(row[0], row[1])
            ax[0].set_xlim([min(ref_length)-5, max(ref_length)+5])
            ax[0].set_ylim([-50, 50])
            ax[0].set_title(shape_name)

            # plot the volume
            ax[1].clear()
            ax[1].plot(ref_length[0:i], volume[0:i])
            ax[1].set_xlim([min(ref_length)-5, max(ref_length)+5])
            ax[1].set_ylim([min(volume)-5, max(volume)+5])
            ax[1].set_xlabel(ref_length_name+" Length (mm)")
            ax[1].set_ylabel("Volume (mL)")

    
    def animate_tube_side(self, save=True):
        fig, ax = plt.subplots(2,1, figsize=(5,5))
        plt.tight_layout(pad=2)

        L_array = np.linspace(self.L_expanded, self.L_contracted, 100)
        volume_array = self.calculate_tube_volume(L_array) / 1000 # mL

        def animate(i):
            # get the vertices of the tube
            top_points, bottom_points = self.find_tube_points(L_array[i])
            # collect x and y into pairs
            tx = np.vstack([top_points[:,0][0::2],top_points[:,0][1::2]])
            ty = np.vstack([top_points[:,1][0::2],top_points[:,1][1::2]])
            bx = np.vstack([bottom_points[:,0][0::2],bottom_points[:,0][1::2]])
            by = np.vstack([bottom_points[:,1][0::2],bottom_points[:,1][1::2]])

            ax[0].clear()
            ax[0].plot(tx, ty)
            ax[0].plot(bx, by)
            ax[0].set_xlim([-5, self.L_expanded+5])
            ax[0].set_ylim([-2*(self.a+1), 2])
            ax[0].set_title("Miura Tube")

            ax[1].clear()
            ax[1].plot(L_array[0:i], volume_array[0:i])
            ax[1].set_ylabel("Volume (mL)")
            ax[1].set_xlabel("Tube Length (mm)")
            ax[1].set_xlim([-5, self.L_expanded+5])
            ax[1].set_ylim([4, 170])

        ani = FuncAnimation(fig, animate, len(L_array), repeat=False, interval=100)
        plt.show()
        # ani.save("miura-tube-with-V(L).gif")

    def animate_circle(self, r_max=None):
        if r_max is None:
            r_max = self.a/2

        h = self.L_expanded
        r_min = 5 # mm
        r_array = np.linspace(r_max, r_min, 100)
        volume_array = np.pi*r_array**2*h / 1000 # mL
        circ_array = r_array*2*np.pi

        fig, ax = plt.subplots(2,1, figsize=(5,5))
        plt.tight_layout(pad=2)
        
        def animate(i):
            ax[0].clear()
            circle = ptchs.Circle((2*r_max,0), r_array[i], fill=False, color='g')
            ax[0].add_patch(circle)
            ax[0].set_ylim([-(r_max+1), r_max+1])
            ax[0].set_xlim([-2, 4*(r_max)+2])
            ax[0].set_title("Cylinder")

            ax[1].clear()
            ax[1].plot(circ_array[0:i], volume_array[0:i])
            ax[1].set_ylabel("Volume (mL)")
            ax[1].set_xlabel("Cylinder Circumference (mm)")
            ax[1].set_xlim([0, max(circ_array)+2])
            ax[1].set_ylim([0, max(volume_array)+5])


        ani = FuncAnimation(fig, animate, len(r_array), repeat=False, interval=100)
        plt.show()
        ani.save("cylinder-with-V(c).gif")

    def animate_sphere(self, r_max=None):
        if r_max is None:
            r_max = self.a/2

        h = self.L_expanded
        r_min = 5 # mm
        r_array = np.linspace(r_max, r_min, 100)
        volume_array = 4/3*np.pi*r_array**3 / 1000 # mL
        circ_array = r_array

        fig, ax = plt.subplots(2,1, figsize=(5,5))
        plt.tight_layout(pad=2)
        
        def animate(i):
            ax[0].clear()
            circle = ptchs.Circle((2*r_max,0), r_array[i], fill=False, color='g')
            ax[0].add_patch(circle)
            ax[0].set_ylim([-(r_max+1), r_max+1])
            ax[0].set_xlim([-2, 4*(r_max)+2])
            ax[0].set_title("Sphere")

            ax[1].clear()
            ax[1].plot(circ_array[0:i], volume_array[0:i])
            ax[1].set_ylabel("Volume (mL)")
            ax[1].set_xlabel("Sphere Radius (mm)")
            ax[1].set_xlim([0, max(circ_array)+2])
            ax[1].set_ylim([0, max(volume_array)+5])


        ani = FuncAnimation(fig, animate, len(r_array), repeat=False, interval=100)
        plt.show()
        ani.save("sphere-with-V(r).gif")
 
if __name__ == "__main__":
    my_geo = Geometry(a=25.0, c=21.4, alpha=60, N=6)

    # my_miura.animate_tube_side()
    # my_miura.plot_tube_side(my_miura.L_contracted)
    # my_miura.plot_tube_side(my_miura.L_expanded)

    my_geo.animate_sphere()