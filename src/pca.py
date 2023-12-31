"""PCA scene."""
from manim import *

from constants import Formulas
from utils import get_pca_elements


def pca_graph(scene: ThreeDScene, formulas: bool = True):
    # Create axes
    # TODO: Create custom axes with tips on both sides.
    axes = ThreeDAxes()
    scene.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
    scene.begin_ambient_camera_rotation(rate=0.2)

    points_data, points_meaned, cov_matrix, (eigen_values_sorted, eigen_vectors_sorted), points_transformed = get_pca_elements()

    # Create scatter plot using Points class
    scatter_points = VGroup(*[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_data])

    # Add scatter plot to the scene
    scene.play(Create(axes))
    scene.play(Create(scatter_points))
    scene.wait(2)

    # Stop rotation for upcoming animations
    scene.stop_ambient_camera_rotation()

    # Move the 3D plot to the left a little to make space for the formulas
    shift_amount = 2
    scale_factor = 0.8
    if formulas:
        scene.move_camera(phi=75 * DEGREES, theta=76.5 * DEGREES)

        # Play the shift and scale animations in parallel
        group = VGroup(axes, scatter_points)
        scene.play(group.animate.scale(scale_factor))
        scene.play(group.animate.shift(RIGHT * shift_amount))

        # First, show the centering formula
        data_centering_formula = Formulas.CENTERED_MATRIX.to_edge(RIGHT)
        scene.add_fixed_in_frame_mobjects(data_centering_formula)
        scene.play(Write(data_centering_formula))

    scene.wait(1)

    # Now set morph the points into centered position around the origin.
    scatter_points_meaned = VGroup(*[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_meaned])

    if formulas:
        scatter_points_meaned.shift(RIGHT * shift_amount)
        scatter_points_meaned.scale(scale_factor)

    scene.play(Transform(scatter_points, scatter_points_meaned))

    scene.wait(1)

    if formulas:
        # First let the axes and points disappear temoprarily.
        group = VGroup(scatter_points, scatter_points_meaned, axes)
        scene.play(FadeOut(group), Unwrite(data_centering_formula))

        # Now show the derivation of the covariance calculation.
        cov_formula = Formulas.COVARIANCE.set_opacity(opacity=0)
        cov_description = Formulas.COVARIANCE_DESCRIPTION.next_to(cov_formula, UP*1.3)
        scene.add_fixed_in_frame_mobjects(cov_formula)
        scene.add_fixed_in_frame_mobjects(cov_description)
        scene.play(Write(cov_description, run_time=4))
        scene.wait(0.5)
        cov_formula.set_opacity(opacity=1)
        scene.play(Write(cov_formula))
        scene.wait(2)

        cov_formula_simplified = Formulas.COVARIANCE_SIMPLIFIED
        scene.play(ReplacementTransform(cov_formula, cov_formula_simplified))
        scene.add_fixed_in_frame_mobjects(cov_formula_simplified)
        scene.wait(1)
        scene.play(FadeOut(cov_description))
        scene.wait(1)
        cov_formula_matrix = Formulas.COVARIANCE_MATRIX
        scene.play(ReplacementTransform(cov_formula_simplified, cov_formula_matrix))
        scene.add_fixed_in_frame_mobjects(cov_formula_matrix)
        scene.wait(1)
        scene.play(FadeOut(cov_formula_matrix))
        scene.wait(0.5)
        
        # Get points back to original state
        group.center()
        group.scale(1/scale_factor)
        
        scene.play(FadeIn(group))
        scene.wait(2)


    # Animate transformation
    scatter_points_transformed = VGroup(
        *[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_transformed]
    )
    scatter_points.set_opacity(0)
    scene.play(Transform(scatter_points_meaned, scatter_points_transformed))

    scene.wait(1)


class PCAExplained(ThreeDScene):
    def construct(self):
        # TODO: Add the corresponding formulas.
        # TODO: Since we re-use this scene multiple times throughout the video, we want to make the rendering of the formulas optional.
        # TODO: When performing the transformation, move the camera so that we watch the transfromation from the direction of first eigenvector.
        # --> Ideally this should be calculated on the fly so that the scene also works with other datasets.
        pca_graph(self)
