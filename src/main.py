"""Manim entrypoint."""
from manim import *

from introduction import Introduction
from pca import PCAExplained, PCAExplainedWithFormulas
from utils import fade_out_scene


class PCA(ThreeDScene):
    """Class that implements a manim scene for visualizing principal component analysis."""

    def construct(self) -> None:
        scenes = [Introduction, PCAExplained, PCAExplainedWithFormulas]
        for scene in scenes:
            scene.construct(self)
            fade_out_scene(self)
