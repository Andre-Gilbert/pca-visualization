"""PCA scene."""
from manim import *


class PCAExplained(Scene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        text3d = Text("This is a 3D text")
        self.add_fixed_in_frame_mobjects(text3d)
        text = MathTex("\\frac{d}{dx}f(x)g(x)=", "f(x)\\frac{d}{dx}g(x)", "+", "g(x)\\frac{d}{dx}f(x)")
        self.play(Write(text))
        text3d.to_corner(UL)
        self.add(axes)
        self.wait()
