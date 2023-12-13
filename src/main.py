"""Manim entrypoint."""
from manim import PINK, YELLOW, Circle, Create, Scene

from utils import fade_out_scene


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class CreateCircle2(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(YELLOW, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class PCA(Scene):
    """Class that implements a manim scene for visualizing principal component analysis."""

    def construct(self) -> None:
        scenes = [CreateCircle, CreateCircle2]
        for scene in scenes:
            scene.construct(self)
            fade_out_scene(self)
