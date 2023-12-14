"""Manim entrypoint."""
from manim import *

from introduction import Introduction
from pca import PCAExplained
from utils import fade_out_scene


class PCA(Scene):
    """Class that implements a manim scene for visualizing principal component analysis."""

    def construct(self) -> None:
        scenes = [Introduction, PCAExplained]
        for scene in scenes:
            scene.construct(self)
            fade_out_scene(self)
