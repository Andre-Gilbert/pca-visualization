"""Introduction scene."""
from manim import *
from sigma_creature import SigmaCreature
from constants import FontSize


class Introduction(Scene):
    """Class that implements the PCA introduction scene."""

    def construct(self) -> None:
        sigma_creature = SigmaCreature(creature_height=2)
        self.add(sigma_creature)
        self.wait(1)
        self.play(sigma_creature.animate.to_edge(DR))
        self.wait(1)
        ds_tag = Text("Data Scientist", color=WHITE, font_size=FontSize.HEADING4).next_to(sigma_creature, UP)
        self.play(Write(ds_tag))
        self.wait(1)
        scene_heading = Text("Problem Statement", color=WHITE, font_size=FontSize.HEADING1).to_edge(UP)
        self.play(Write(scene_heading))
        self.wait(1)