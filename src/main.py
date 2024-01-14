"""Manim entrypoint."""
from manim import *

from introduction import Introduction
from pca import Intuition, PCAExplained, PCAExplainedDetail
from utils import fade_out_scene


class PCA(ThreeDScene):
    """Class that implements a manim scene for visualizing principal component analysis."""

    def construct(self) -> None:
        scenes = [Introduction, Intuition, PCAExplained, PCAExplainedDetail]
        for scene in scenes:
            scene.construct(self)
            fade_out_scene(self)
