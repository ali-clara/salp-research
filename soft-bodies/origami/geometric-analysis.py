import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
from matplotlib.animation import FuncAnimation
import matplotlib.patches as ptchs

class Miura():
    def __init__(self, a, c, alpha, N) -> None:
        """Initializes an instance of the Miura class. 
        
        Set the geometric parameters of a Miura tube:
            a (cell base width/length, mm), c (half cell height, mm), alpha (cell angle, deg), N (number of cells)"""
        
        self.a = a
        self.N = N

        self.L_expanded = self._calculate_miura_tube_length(c)
        self.L_contracted = 2*2*N     # rough guess for now
        self.cell_hypotenuse = self._calculate_miura_cell_hypotenuse(c, alpha)

    def _calculate_miura_tube_length(self, c):
        """Calculates the length of the tube based on the initial height of each parallelepipid"""
        l = c*2*self.N
        return l
    
    def _calculate_miura_cell_hypotenuse(self, c, alpha):
        """Calculates the length of the sloped side of the parallelepipid. Based on the initial cell height"""
        d = c / np.sin(np.deg2rad(alpha))
        return d
    
    def calculate_miura_base_area(self, L_current):
        """Finds the area of the parallelogram base of each parallelepipid"""

        area_expanded = self.a**2
        area_contracted = np.sqrt(3)/2*self.a**2

        area_current = np.interp(L_current, [self.L_contracted, self.L_expanded], [area_contracted, area_expanded])
        return area_current
    
    def calculate_miura_cell_height(self, L):
        """Calculates the height of each parallelepipid based on the total length.
        
            L - current length of the tube. Changes with time"""
        c = L / (2*self.N)
        return c
    
    def calculate_miura_tube_volume(self, L):
        base_area = self.calculate_miura_base_area(L)
        v = base_area*L / 1000 # mL
        return v

    def find_miura_top_points(self, c, plotting):
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

        return np.array(top_points)
    
    def find_miura_bottom_points(self, c, plotting):
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

        return np.array(bottom_points)

class Geometry(Miura):
    def __init__(self, a=25.0, c=21.4, alpha=60, N=3):
        # maybe have a set_miura_params function called here instead of instantiating in the init
        super().__init__(a, c, alpha, N)

        self.default_array_length = 100

        # cylinder params
        self.cylinder_rmax = 16 # mm
        self.cylinder_rmin = 5 # mm
        self.cylinder_h = self.L_expanded

        # sphere params
        self.sphere_rmax = 30 #mm
        self.sphere_rmin = 8 #mm

        self.a0 = 10    # outlet nozzle area, mm2

        # functions for setting circle, sphere params, etc
    
    def find_miura_tube_points(self, length, plotting=True):
        """Finds the [(x,y)] points of the Miura tube vertices. \\
                L - current length of the tube \\
                plotting (boolean) - if False returns vertices as np array, if True returns in a format for plotting \\
                Returns - np.array of [top_points, bottom_points]"""
        
        # find the height of each cell based on the current tube length
        c = self.calculate_miura_cell_height(length)
        # calculate and collect the zig zag pattern of the 2D Miura tube side profile
        top_points = self.find_miura_top_points(c, plotting)
        bottom_points = self.find_miura_bottom_points(c, plotting)

        if not plotting:
            return top_points, bottom_points

        else:
            tx = np.vstack([top_points[:,0][0::2],top_points[:,0][1::2]])
            ty = np.vstack([top_points[:,1][0::2],top_points[:,1][1::2]])
            bx = np.vstack([bottom_points[:,0][0::2],bottom_points[:,0][1::2]])
            by = np.vstack([bottom_points[:,1][0::2],bottom_points[:,1][1::2]])

            top_points = [tx, ty]
            bottom_points = [bx, by]
            
            return np.array([top_points, bottom_points])
        
    def find_cylinder_points(self, circumference):
        """Returns a matplotlib patches object of a circle centered at (0,0) with circumference specified"""
        radius = circumference / (2*np.pi)
        circle = ptchs.Circle((0,0), radius, fill=False, color='g')
        return circle
    
    def find_sphere_points(self, radius):
        """Returns a matplotlib patches object of a circle centered at (0,0) with radius specified"""
        circle = ptchs.Circle((0,0), radius, fill=False, color='m')
        return circle
    
    def get_shape_points(self, shape_name, ref_length):
        """
        Calculates the points for the given shape and compiles them for plotting
        Returns - [[x_points, y_points]], may have multiple if the shape is discontinuous
        """
        if shape_name == "miura":
            shape_points = self.find_miura_tube_points(ref_length)
        elif shape_name == "cylinder":
            shape_points = self.find_cylinder_points(ref_length)
        elif shape_name == "sphere":
            shape_points = self.find_sphere_points(ref_length)
        else:
            raise Exception(f"Invalid shape name {shape_name} given")
        
        return shape_points
    
    def get_miura_values(self):
        """Returns miura tube length and volume"""
        length = np.linspace(self.L_expanded, self.L_contracted, self.default_array_length)
        volume = self.calculate_miura_tube_volume(length)
        return length, volume
    
    def get_cylinder_values(self):
        """Returns cylinder circumference and volume"""
        radius = np.linspace(self.cylinder_rmax, self.cylinder_rmin, self.default_array_length)
        volume = np.pi*radius**2*self.cylinder_h / 1000  # mL
        circumference = radius*2*np.pi
        return circumference, volume
    
    def get_sphere_values(self):
        """Returns sphere diameter and volume"""
        radius = np.linspace(self.sphere_rmax, self.sphere_rmin, self.default_array_length)
        diameter = 2*radius
        volume = 4/3*np.pi*radius**3 / 1000 # mL
        return diameter, volume
    
    def animate_shape_and_volume(self, shape_name, ref_length_name, ref_length, volume, save=True):
        """
        Animates the shape change over time and plots the volume change with 
        respect to the reference length (i.e radius, length, circumference, etc)\\
        Inputs: \\
            shape_name (str) - what shape we're plotting \\
            ref_length_name (str) - what length we're referencing \\
            ref_length (np array) - reference length (mm) \\
            volume (np array) - volume calculated across the refernce length (mL) \\

        """
        fig, ax = plt.subplots(2,1, figsize=(5,5))
        plt.tight_layout(pad=2)

        def animate(i):
            ax[0].clear()
            # grab the points of the shape
            shape_points = self.get_shape_points(shape_name, ref_length[i])
            # plot the shape with appropriate axis limits
            if shape_name == "miura":
                ax[0].set_xlim([min(ref_length)-5, max(ref_length)+5])
                ax[0].set_ylim([-50, 50])
                for row in shape_points:
                    ax[0].plot(row[0], row[1])
            elif shape_name == "cylinder":
                ax[0].add_patch(shape_points)
                ax[0].set_xlim([-2*(self.cylinder_rmax+1), 2*self.cylinder_rmax+1])
                ax[0].set_ylim([-(self.cylinder_rmax+1), self.cylinder_rmax+1])
            elif shape_name == "sphere":
                ax[0].add_patch(shape_points)
                ax[0].set_xlim([-2*(self.sphere_rmax+1), 2*self.sphere_rmax+1])
                ax[0].set_ylim([-(self.sphere_rmax+1), self.sphere_rmax+1])
            ax[0].set_title(shape_name)

            # plot the volume
            ax[1].clear()
            ax[1].plot(ref_length[0:i], volume[0:i])
            ax[1].set_xlim([min(ref_length)-5, max(ref_length)+5])
            ax[1].set_ylim([min(volume)-5, max(volume)+5])
            ax[1].set_xlabel(ref_length_name+" (mm)")
            ax[1].set_ylabel("volume (mL)")

        ani = FuncAnimation(fig, animate, len(ref_length), repeat=False, interval=100)
        plt.show()
        if save:
            ani.save(shape_name+"_V("+ref_length_name+").gif")

    def make_animated_plots(self, miura=True, cylinder=True, sphere=True):
        """Highest level function, call this one for animations
            Miura, cylinder, sphere - booleans, if True makes and saves that animation"""
        
        if miura:
            length, volume = self.get_miura_values()
            self.animate_shape_and_volume("miura", "length", length, volume, save=False)
        if cylinder:
            circumference, volume = self.get_cylinder_values()
            self.animate_shape_and_volume("cylinder", "circumference", circumference, volume, save=False)
        if sphere:
            diameter, volume = self.get_sphere_values()
            self.animate_shape_and_volume("sphere", "diameter", diameter, volume, save=False)

    def plot_volumes(self, miura=True, cylinder=True, sphere=True):
        
        fig, ax = plt.subplots()
        if miura:
            length, volume = self.get_miura_values()
            ax.plot(length, volume, label="Miura tube, length")
        if cylinder:
            circumference, volume = self.get_cylinder_values()
            ax.plot(circumference, volume, label="Cylinder, circumference")
        if sphere:
            diameter, volume = self.get_sphere_values()
            ax.plot(diameter, volume, label="Sphere, diameter")

        plt.title("Volume based on reference length")
        plt.ylabel("Volume")
        plt.xlabel("Reference length")
        plt.legend()
        plt.show()

    def get_dvdl(self, miura=True, cylinder=True, sphere=True, show=True):
        """Gets, plots, and returns dv/dl for the different shapes (in mL/mm)"""
        fig, ax = plt.subplots()
        dvdls = []
        labels = []
        if miura:
            length, volume = self.get_miura_values()
            diffv = np.diff(volume, n=1)
            diffl = np.diff(length, n=1)
            dvdl = diffv / diffl
            ax.plot(length[0:-1], dvdl, label="Miura tube, length")
            dvdls.append(dvdl)
            labels.append("miura")
        if cylinder:
            circumference, volume = self.get_cylinder_values()
            diffv = np.diff(volume, n=1)
            diffc = np.diff(circumference, n=1)
            dvdc = diffv / diffc
            ax.plot(circumference[0:-1], dvdc, label="Cylinder, circumference")
            dvdls.append(dvdc)
            labels.append("cylinder*")
        if sphere:
            diameter, volume = self.get_sphere_values()
            diffv = np.diff(volume, n=1)
            diffd = np.diff(diameter, n=1)
            dvdd = diffv / diffd
            ax.plot(diameter[0:-1], dvdd, label="Sphere, diameter")
            dvdls.append(dvdd)
            labels.append("sphere")

        plt.title("Change in volume per reference length")
        plt.legend()
        plt.ylabel("dV/dL (mL/mm)")
        plt.xlabel("Reference length (mm)")
        if show:
            plt.show()

        return dvdls, labels
    
    def get_dldt(self, dvdl, t_stop=10):
        """Creates dL/dt array bsed on TCA data.
            Uses dV/dt to get the correct array length
            Optional input t_stop, how many seconds we're tracking"""
        
        t = np.linspace(0, t_stop, len(dvdl))

        # create dldt array of zeros with the correct length
        dldt = np.zeros(len(dvdl))
        # fill in array based on TCA data - slope is ~5.46 mm/s, and lasts for ~5 seconds
        slope = 5.46   #mm/s
        dldt[0:int(len(dldt)/2)] = slope

        return t, dldt

    def calculate_thrust(self, dvdt):
        """Takes in volumetric change (mL/s) and converts to thrust"""
        dvdt_mm3 = dvdt*1000 # mm3
        rho = 1e-6  # kg/mm3
        c0 = 0.6    # dimensionless
        thrust = rho*dvdt_mm3**2 / (c0*self.a0)

        return thrust
    
    def plot_thrust(self):
        fig, ax = plt.subplots(2,1)
        plt.tight_layout(pad=3)

        dv_dls, labels = self.get_dvdl(show=False)
        t, dldt = self.get_dldt(dv_dls[0])

        for i, dvdl in enumerate(dv_dls):
            dvdt = dvdl*dldt # mL/s
            thrust = self.calculate_thrust(dvdt)
            ax[0].plot(t, dvdt, label=labels[i])
            ax[1].plot(t, thrust, label=labels[i])

        ax[0].set_xlabel("Time (s)")
        ax[0].set_ylabel("dV/dt (mL/s)")
        ax[0].set_title("Projected dV/dt based on TCA displacement data")
        ax[0].legend()

        ax[1].set_xlabel("Time (s)")
        ax[1].set_ylabel("Thrust (mN)")
        ax[1].set_title("Projected thrust based on TCA displcaement data")
        ax[1].legend()

        plt.show()

 
if __name__ == "__main__":
    
    # my_miura = Miura()
    my_geo = Geometry()
    # my_geo.make_animated_plots(miura=False, cylinder=False, sphere=True)
    my_geo.plot_thrust()

    # my_miura.animate_tube_side()
    # my_geo.plot_tube_side(my_geo.L_contracted)
    # my_geo.plot_tube_side(my_geo.L_expanded)

    # my_geo.animate_sphere()

    # have functions to set geometric shape parameters
        # as dictionaries?
