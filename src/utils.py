"""Scene utilities."""
from manim import FadeOut, Scene


def fade_out_scene(scene: Scene) -> None:
    """Fades all objects in the scene."""
    animations = [FadeOut(mobject) for mobject in scene.mobjects]
    scene.play(*animations)
