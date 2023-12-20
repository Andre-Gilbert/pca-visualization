"""Introduction scene."""
from manim import *
from sigma_creature import SigmaCreature
from constants import FontSize
from utils import create_wind_turbine, create_large_table


class Introduction(Scene):
    """Class that implements the PCA introduction scene."""

    def construct(self) -> None:
        scene_heading = Text("Problem Statement", color=WHITE, font_size=FontSize.HEADING1).to_edge(UP)
        self.add(scene_heading)

        sigma_creature = SigmaCreature(creature_height=2)
        self.add(sigma_creature)
        self.wait(1)
        
        self.play(sigma_creature.animate.to_edge(DR))
        self.wait(1)
        
        ds_tag = Text("Data Scientist", color=WHITE, font_size=FontSize.HEADING4).next_to(sigma_creature, UP)
        self.play(Write(ds_tag))
        self.wait(1)
        
        # First, we only define the turbine.
        wind_turbine = create_wind_turbine(self)
        self.add(wind_turbine)
        wind_turbine.to_edge(RIGHT*1.5 + UP*2)
        self.play(Rotate(wind_turbine[1:4], 2 * PI, about_point=wind_turbine[1:4].get_center_of_mass()), run_time=5)

        # Now show the way too big 
        table = create_large_table()
        self.play(Write(table))
        self.wait(2)
