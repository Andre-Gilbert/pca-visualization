"""Scene utilities."""
from manim import *
import pandas as pd


def fade_out_scene(scene):
    """Fades all objects in the scene."""
    animations = [FadeOut(mobject) for mobject in scene.mobjects]
    scene.play(*animations)


### For Intro Scene ###
def create_wind_turbine(scene):
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
