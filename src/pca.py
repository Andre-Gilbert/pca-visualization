"""PCA scene."""
from manim import *

from constants import Formulas, FontSize
from utils import get_pca_elements, calculate_view_pos, fade_out_scene, get_axes, create_schema_cov_matrix


def pca_graph(
        scene: ThreeDScene, 
        formulas: bool = True, 
        variance_vectors: bool = True, 
        show_scree_plot: bool = True,
        change_view_on_transformation: bool = True
    ):

    points_data, points_meaned, cov_matrix, (eigen_values_sorted, eigen_vectors_sorted), points_transformed = get_pca_elements()
    scene, axes, axes_arrows = get_axes(scene, Create)

    # Create scatter plot using Points class
    scatter_points = VGroup(*[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_data])

    # Add scatter plot to the scene
    scene.play(Create(scatter_points))
    scene.wait(1)

    # Move the 3D plot to the left a little to make space for the formulas
    shift_amount = 2
    scale_factor = 0.8
    if formulas:
        # Stop rotation for upcoming animations
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=75 * DEGREES, theta=135 * DEGREES, rate_func=rate_functions.ease_out_cubic, run_time=5)

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
        
        # Schematic Cov Matrix to the right
        cov_schema = create_schema_cov_matrix().set_opacity(0)
        scene.add_fixed_in_frame_mobjects(cov_schema)

        # First fade out the description
        scene.play(FadeOut(cov_description))
        scene.wait(1)

        # Move down the formula for the cov schema
        scene.play(cov_formula_simplified.animate.next_to(cov_schema, DOWN, buff=0.5))
        scene.wait(0.5)

        cov_schema = cov_schema.set_opacity(1)
        scene.play(Write(cov_schema))
        scene.wait(1)

        scene.play(FadeOut(cov_schema))
        scene.play(cov_formula_simplified.animate.move_to(ORIGIN))

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
        if formulas:
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
        if change_view_on_transformation:
            scene.stop_ambient_camera_rotation()
        scene.wait(0.5)

    # Move camera for transformation
    # Looking from the angle of the third PC, we can observe how most of the variance is preserved.
    if change_view_on_transformation:
        phi, theta = calculate_view_pos(eigen_vectors_sorted[-1])
        if not variance_vectors:
            scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=phi, theta=theta, run_time=4)
        scene.wait(1)

    # Animate transformation
    scatter_points_transformed = VGroup(
        *[Dot3D(point=np.array(point), color=BLUE, radius=0.05) for point in points_transformed]
    )
    scatter_points.set_opacity(0)
    scene.play(Transform(scatter_points_meaned, scatter_points_transformed))

    scene.wait(0.5)
    
    # Show off how now most of the variance is on the first two dimensions.
    if change_view_on_transformation:
        scene.move_camera(phi=90 * DEGREES, theta=theta, run_time=3)
        scene.begin_ambient_camera_rotation(0.2)

    scene.wait(5)

    if show_scree_plot:
        fade_out_scene(scene)
        scree_plot(scene, eigen_values_sorted)
        scene.wait(1)


def scree_plot(scene: ThreeDScene, eigen_values: np.ndarray) -> None:
    """
    Scene to show the Scree plot belonging to the PCA.

    Parameters:
    - scene: ThreeDScene, Scene to render into
    - eigen_values: np.ndarray, Ordered list of eigenvalues.

    returns: None
    """

    eigen_values_sum = eigen_values.sum()
    variance_shares = [round((eigen_value/eigen_values_sum) * 100, 1) for eigen_value in eigen_values]
    agg_variance_shares = [round(value + sum(variance_shares[:i]), 3) if i > 0 else value for i, value in enumerate(variance_shares)]
    chart = BarChart(
        values=agg_variance_shares,
        bar_names=["1 PC", "2 PCs", "3 PCs"],
        bar_colors=[DARK_BLUE, DARK_BLUE, DARK_BLUE],
        y_range=[0, 100, 10],
        y_length=6,
        x_length=8,
        x_axis_config={"font_size": FontSize.HEADING3}
    )
    c_bar_lbls = chart.get_bar_labels(font_size=48, color=WHITE)
    y_label = Text("Variance Explained (%)", font_size=FontSize.HEADING3).rotate(90*DEGREES).next_to(chart.y_axis, LEFT)
    scene.add_fixed_in_frame_mobjects(chart)
    scene.add_fixed_in_frame_mobjects(c_bar_lbls)
    scene.add_fixed_in_frame_mobjects(y_label)
    scene.play(Create(chart), Create(c_bar_lbls), Write(y_label))
    scene.wait(2)
    scene.play(FadeOut(chart), FadeOut(c_bar_lbls), FadeOut(y_label))


class Intuition(ThreeDScene):
    def construct(self):
        "Fast & lite version for intuition."
        pca_graph(self, formulas=False, variance_vectors=False, show_scree_plot=False, change_view_on_transformation=True)


class PCAExplained(ThreeDScene):
    def construct(self):
        # TODO: Add the corresponding formulas.
        pca_graph(self, formulas=True, variance_vectors=False, show_scree_plot=False, change_view_on_transformation=False)


class PCAExplainedDetail(ThreeDScene):
    def construct(self):
        pca_graph(self, formulas=True, variance_vectors=True, show_scree_plot=True)
