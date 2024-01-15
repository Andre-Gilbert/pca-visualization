"""Scene utilities."""
from manim import *
import pandas as pd


def fade_out_scene(scene):
    """Fades all objects in the scene."""
    animations = [FadeOut(mobject) for mobject in scene.mobjects]
    scene.play(*animations)


### For Intro Scene ###
def create_wind_turbine():
    "Create a wind turbine with three blades."
    base = Rectangle(width=0.1, height=2, color=LIGHT_GRAY, fill_opacity=1)

    # Create blades
    blade1 = create_blade().move_to(UP * 0.85 + LEFT * 0.55).rotate(2.1)
    blade2 = create_blade().move_to(UP * 0.6 + RIGHT * 0.35).rotate(4.2)
    blade3 = create_blade().move_to(UP * 1.5 + RIGHT * 0.1)

    return Group(base, blade1, blade2, blade3)


def create_blade() -> VMobject:
    "Create a realistic blade for the wind turbine."

    blade_path = VMobject()
    blade_path.set_points_as_corners(
        [
            [0, 0, 0],  # Bottom-left corner
            [0, 4, 0],  # Pointy tip
            [1.5, -1, 0],  # Bottom-right corner
            [0, -2, 0],  # Shorter side corner
        ]
    )
    blade_path.add_line_to(ORIGIN).close_path()
    blade = blade_path.set_color(LIGHT_GRAY).set_fill(LIGHT_GRAY, opacity=0.7).set_height(1)
    return blade


def create_large_table():
    table = r"""
        \begin{table}[h]
            \centering
            \begin{tabular}{|c|c|c|c|c|c|c|}
                \hline
                $$ & $f_1$ & $f_2$ & $\cdots$ & $f_{m-1}$ & $f_m$ \\
                \hline
                $x_1$ & $1.23$ & $4.56$ & $\cdots$ & $7.89$ & $0.12$ \\
                \hline
                $x_2$ & $1.23$ & $4.56$ & $\cdots$ & $7.89$ & $0.12$ \\
                \hline
                $\vdots$ & $\vdots$ & $\vdots$ & $\ddots$ & $\vdots$ & $\vdots$ \\
                \hline
                $x_{n-1}$ & $1.23$ & $4.56$ & $\cdots$ & $7.89$ & $0.12$ \\
                \hline
                $x_n$ & $1.23$ & $4.56$ & $\cdots$ & $7.89$ & $0.12$ \\
                \hline
            \end{tabular}
            \caption{Wind turbine sensor data}
            \label{tab:my_table}
        \end{table}
        """
    return Tex(table).shift(LEFT * 1.5)


def create_schema_cov_matrix():
    table = r"""
        \begin{table}[h]
            \centering
            \begin{tabular}{|c|c|c|c|}
                \hline
                $$ & $X_1$ & $X_2$ & $X_3$ \\
                \hline
                $X_1$ & $\operatorname{cov}[X_1, X_1]$ & $\operatorname{cov}[X_1, X_2]$ & $\operatorname{cov}[X_1, X_3]$ \\
                \hline
                $X_2$ & $\operatorname{cov}[X_2, X_1]$ & $\operatorname{cov}[X_2, X_2]$ & $\operatorname{cov}[X_2, X_3]$ \\
                \hline
                $X_3$ & $\operatorname{cov}[X_3, X_1]$ & $\operatorname{cov}[X_3, X_2]$ & $\operatorname{cov}[X_3, X_3]$ \\
                \hline
            \end{tabular}
            \caption{Schematic covariance matrix}
            \label{tab:cov_schema}
        \end{table}
        """
    return Tex(table)


def get_pca_elements(data_path: str = "assets/data_points.csv") -> tuple:
    "Returns all elements that are part of the PCA calculation for the dataset at the specified path."

    # Read data from CSV

    # For debugging, we use only a small number of points.
    # NOTE: Eventually we want to create and use a synthetic dataset that is comprised hundreds of points.
    data = pd.read_csv(data_path)
    
    points_data = data.values  # Assuming columns are x, y, z
    points_meaned = points_data - np.mean(points_data, axis=0)

    # Now perform the PCA transformation
    num_features = data.shape[1]
    cov_matrix = (1 / num_features) * (points_meaned.T @ points_meaned)

    eigen_values, eigen_vectors = np.linalg.eigh(cov_matrix)

    sorted_indices = np.argsort(eigen_values)[::-1]  # Get indices that would sort eigen_values in descending order
    eigen_values_sorted = eigen_values[sorted_indices]  # For later animations
    eigen_vectors_sorted = eigen_vectors[:, sorted_indices]

    points_transformed = (eigen_vectors_sorted.T @ points_meaned.T).T

    return points_data, points_meaned, cov_matrix, (eigen_values_sorted, eigen_vectors_sorted), points_transformed


def calculate_view_pos(vector: np.ndarray, ndigits: int = 3) -> tuple[float]:

    """
    Calculates the azimuthal and vertical angle to look from the direction
    of a given vector.

    Parameters:
    - vector: np.array, the 3D vector.
    - ndigits: int, number of after decimal digits when rounding.

    Returns:
    - phi: float, the polar angle in radiants.
    - theta: float, the azimuthal angle in radiants.
    """

    # Calculate the polar angle (phi)
    phi = np.arccos(vector[2] / np.linalg.norm(vector))

    theta = np.arccos

    # Calculate the azimuthal angle (theta)
    if vector[0] == 0:
        theta = np.pi / 2 if vector[1] > 0 else -np.pi / 2
    else:
        theta = np.arctan(vector[1] / vector[0])

    return round(phi, ndigits=ndigits), round(theta, ndigits=ndigits)


def get_axes(scene: ThreeDScene, animation: FadeIn or Create = Create) -> tuple:
    """
    Returns axes with arrow tips on all ends.
    This function animates the creation of the axes and the initial scatter points
    and begins an ambient rotation.
    """

    # Create axes
    axes = ThreeDAxes(tips=False).set_opacity(0)

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

    scene.play(animation(x_axis_double_arrow), animation(y_axis_double_arrow), animation(z_axis_negative_arrow), animation(z_axis_positive_arrow))
    axes = axes.set_opacity(1)
    scene.play(animation(axes))
    scene.wait(.5)

    return scene, axes, axes_arrows
