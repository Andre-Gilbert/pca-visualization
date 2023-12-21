"""PCA scene."""
from manim import *
import pandas as pd


class PCAExplained(ThreeDScene):
    def construct(self):
        # Create axes
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        
        # Read data from CSV
        data = pd.read_csv("assets/data_points.csv")
        points_data = data.values  # Assuming columns are x, y, z
        
        # Create scatter plot using Points class
        scatter_points = VGroup(
            *[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_data]
        )
        
        # Add scatter plot to the scene
        self.play(Create(axes), Create(scatter_points))
        self.wait(4)
        
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait()
