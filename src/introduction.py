"""Introduction scene."""
from manim import *


class Introduction(Scene):
    """Class that implements the PCA introduction scene."""

    def construct(self) -> None:
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))
