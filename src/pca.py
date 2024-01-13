"""PCA scene."""
from manim import *

from constants import Formulas, FontSize
from utils import get_pca_elements, calculate_view_pos, fade_out_scene


def pca_graph(scene: ThreeDScene, formulas: bool = True, variance_vectors: bool = True, show_scree_plot: bool = True):
    # Create axes
    axes = ThreeDAxes(tips=False).set_opacity(0)
    # scene.add(axes) # Comment out before flight

    # scene.set_camera_orientation(phi=75 * DEGREES, theta=-40 * DEGREES, zoom=3)
    # scene.play(Create(Arrow3D(ORIGIN, (-.02, -.03, 0))))

    # Create double arrows for each axis
    axis_extension_for_arrow = .6
    x_axis_double_arrow = DoubleArrow(axes.x_axis.get_end() + (axis_extension_for_arrow, 0, 0), axes.x_axis.get_start() + (-axis_extension_for_arrow, 0, 0), buff=0, stroke_width=2.0)
    y_axis_double_arrow = DoubleArrow(axes.y_axis.get_end() + (0, axis_extension_for_arrow, 0), axes.y_axis.get_start() + (0, -axis_extension_for_arrow, 0), buff=0, stroke_width=2.0)
    
    # Z-Axis arrow was buggy using the DoubleArrow (buckling tip on one side)
    # Thus, we are using two seperate arrows.
    z_axis_negative_arrow = Arrow((0, 0, 0), axes.z_axis.get_start() + (0, 0, -axis_extension_for_arrow), buff=0, stroke_width=2.0)
    z_axis_positive_arrow = Arrow((0, 0, 0), axes.z_axis.get_end() + (0, 0, axis_extension_for_arrow), buff=0, stroke_width=2.0)

    axes_arrows = x_axis_double_arrow, y_axis_double_arrow, z_axis_negative_arrow, z_axis_positive_arrow

    # Add arrows to the scene
    scene.add(axes, *axes_arrows)

    # Optionally, add labels or other elements to enhance the visualization
    # They look a little ugly in 3D though.
    # x_label = axes.get_x_axis_label("x")
    # y_label = axes.get_y_axis_label("y")
    # z_label = axes.get_z_axis_label("z")
    # scene.add(x_label, y_label, z_label)

    scene.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
    scene.begin_ambient_camera_rotation(rate=0.2)

    points_data, points_meaned, cov_matrix, (eigen_values_sorted, eigen_vectors_sorted), points_transformed = get_pca_elements()

    # Create scatter plot using Points class
    scatter_points = VGroup(*[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_data])

    # Add scatter plot to the scene
    scene.play(Create(x_axis_double_arrow), Create(y_axis_double_arrow), Create(z_axis_negative_arrow), Create(z_axis_positive_arrow))
    axes = axes.set_opacity(1)
    scene.play(Create(axes))
    scene.wait(.5)
    scene.play(Create(scatter_points))
    scene.wait(2)

    # Stop rotation for upcoming animations
    scene.stop_ambient_camera_rotation()

    # Move the 3D plot to the left a little to make space for the formulas
    shift_amount = 2
    scale_factor = 0.8
    if formulas:
        scene.move_camera(phi=75 * DEGREES, theta=135 * DEGREES)

        # Play the shift and scale animations in parallel
        group = VGroup(axes, scatter_points, *axes_arrows)
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
        group = VGroup(scatter_points, scatter_points_meaned, axes, *axes_arrows)
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


    if variance_vectors:
        scene.begin_ambient_camera_rotation(rate=0.2)
        # Add colored infinite lines indicating the directions of greatest variance.
        eigenvector_lines = VGroup()
        for i, eigenvector in enumerate(eigen_vectors_sorted):
            color = [RED, GREEN, BLUE][i]  # Use different colors for each eigenvector
            infinite_line_positive = Line(start=ORIGIN, end=10 * eigenvector, color=color)
            infinite_line_negative = Line(start=ORIGIN, end=-10 * eigenvector, color=color)
            eigenvector_lines.add(infinite_line_positive)
            eigenvector_lines.add(infinite_line_negative)

        scene.play(Create(eigenvector_lines))
        scene.wait(1)

        # Add eigenvectors
        eigenvector_arrows = VGroup(*[Arrow3D(start=ORIGIN, end=eigenvector, color=color, thickness=0.015, base_radius=0.05) for eigenvector, color in zip(eigen_vectors_sorted, [RED, GREEN, BLUE])])
        scene.play(Create(eigenvector_arrows))
        scene.wait(1)

        # Fade out the lines that got replaced by the arrows.
        scene.play(FadeOut(eigenvector_lines))
        scene.wait(1)

        # Scale eigenvectors by eigenvalues and display eigenvalues
        scaled_eigenvectors = VGroup()
        for i, (eigenvector, eigenvalue) in enumerate(zip(eigen_vectors_sorted, eigen_values_sorted)):
            color = [RED, GREEN, BLUE][i]  # Use different colors for each eigenvector
            scaled_eigenvector = Arrow3D(start=ORIGIN, end=eigenvalue * eigenvector, color=color, thickness=0.015, base_radius=0.05)
            scaled_eigenvectors.add(scaled_eigenvector)

        # Display eigenvalues next to scaled eigenvectors
        # NOTE: Keeping the orientation so that the number faces the viewer frontally at all times is not natively possible in Manim, hence we omit the eigenvalue labels as they are not needed to convey the message.
        # eigenvalue_labels = VGroup(*[Text(f"{eigenvalue:.2f}", color=WHITE).next_to(scaled_eigenvector, direction=DOWN, buff=0.1) for eigenvalue, scaled_eigenvector in zip(eigen_values_sorted, scaled_eigenvectors)])

        scene.play(Transform(eigenvector_arrows, scaled_eigenvectors))
        scene.wait(2)

        scene.play(FadeOut(scaled_eigenvectors), FadeOut(eigenvector_arrows))
        scene.stop_ambient_camera_rotation()
        scene.wait(0.5)

    # Move camera for transformation
    # Looking from the angle of the third PC, we can observe how most of the variance is preserved.
    phi, theta = calculate_view_pos(eigen_vectors_sorted[-1])
    scene.move_camera(phi=phi, theta=theta, run_time=4)
    scene.wait(1)

    # Animate transformation
    scatter_points_transformed = VGroup(
        *[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_transformed]
    )
    scatter_points.set_opacity(0)
    scene.play(Transform(scatter_points_meaned, scatter_points_transformed))


class PCAExplained(ThreeDScene):
    def construct(self):
        # TODO: Add the corresponding formulas.
        # TODO: Since we re-use this scene multiple times throughout the video, we want to make the rendering of the formulas optional.
        # TODO: When performing the transformation, move the camera so that we watch the transfromation from the direction of first eigenvector.
        # --> Ideally this should be calculated on the fly so that the scene also works with other datasets.
        pca_graph(self, formulas=False, variance_vectors=False, show_scree_plot=True)


class PCAExplainedDetail(ThreeDScene):
    def construct(self):
        pca_graph(self, formulas=True, variance_vectors=True, show_scree_plot=True)
