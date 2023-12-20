"""Scene utilities."""
from manim import *


def fade_out_scene(scene: Scene) -> None:
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
    blade_path.set_points_as_corners([[0, 0, 0],  # Bottom-left corner
                                  [0, 4, 0],     # Pointy tip
                                  [1.5, -1, 0],       # Bottom-right corner
                                  [0, -2, 0],  # Shorter side corner
                                  ])
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
    
