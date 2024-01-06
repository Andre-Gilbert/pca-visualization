"""PCA scene."""
import pandas as pd
from manim import *

from constants import Formulas


def pca_graph(scene: ThreeDScene):
    # Create axes
    axes = ThreeDAxes()
    scene.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
    scene.begin_ambient_camera_rotation(rate=0.2)

    # Read data from CSV
    # For debugging, we use only a small number of points.
    data = pd.read_csv(
        "src/assets/data_points.csv"
    )  # NOTE: Eventually we want to create and use a synthetic dataset that is comprised hundreds of points.
    points_data = data.values  # Assuming columns are x, y, z
    points_meaned = points_data - np.mean(points_data, axis=0)

    # Create scatter plot using Points class
    scatter_points = VGroup(*[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_data])

    # Add scatter plot to the scene
    scene.play(Create(axes))
    scene.play(Create(scatter_points))
    scene.wait(2)

    # Now set morph the points into centered position around the origin.
    scatter_points_meaned = VGroup(*[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_meaned])

    scene.play(Transform(scatter_points, scatter_points_meaned))

    # Now perform the PCA transformation
    num_features = data.shape[1]
    cov_matrix = (1 / num_features) * (points_meaned.T @ points_meaned)

    eigen_values, eigen_vectors = np.linalg.eigh(cov_matrix)

    sorted_indices = np.argsort(eigen_values)[::-1]  # Get indices that would sort eigen_values in descending order
    eigen_values_sorted = eigen_values[sorted_indices]  # For later animations
    eigen_vectors_sorted = eigen_vectors[:, sorted_indices]

    # num_components = 2 # Later/optional: perform dimensionality reduction.
    points_transformed = (eigen_vectors_sorted.T @ points_meaned.T).T

    # Animate transformation
    scatter_points_transformed = VGroup(
        *[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_transformed]
    )
    scatter_points.set_opacity(0)
    scene.play(Transform(scatter_points_meaned, scatter_points_transformed))

    # self.stop_ambient_camera_rotation()
    # self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
    scene.wait(1)


class PCAExplained(ThreeDScene):
    def construct(self):
        # TODO: Add the corresponding formulas.
        # TODO: Since we re-use this scene multiple times throughout the video, we want to make the rendering of the formulas optional.
        # TODO: When performing the transformation, move the camera so that we watch the transfromation from the direction of first eigenvector.
        # --> Ideally this should be calculated on the fly so that the scene also works with other datasets.
        pca_graph(self)


class PCAExplainedWithFormulas(ThreeDScene):
    def construct(self):
        # Displaying the MathTex object using Write animation
        self.play(Write(Formulas.COVARIANCE))
        self.wait(1)

        # Removing the MathTex object using Uncreate animation
        self.play(Uncreate(Formulas.COVARIANCE))
        self.wait(1)

        pca_graph(self)
