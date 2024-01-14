from manim import *


class ShowSigmaCreature(Scene):
    "Utility class for debugging the Sigma Creature."

    def construct(self):
        # Create Sigma creature
        sigma_creature = SigmaCreature(creature_height=2)
        self.play(sigma_creature.animate.shift(RIGHT))
        self.wait(3)

        # Blink eyes
        self.play(Blink(sigma_creature.eyes))
        self.wait(2)


class SigmaCreature(SVGMobject):
    def __init__(self, creature_height: int = 2, **kwargs):
        "Creature initialization"

        SVGMobject.__init__(self, file_name="./assets/sigma_blue.svg", **kwargs)
        self.set_height(creature_height)

        # Create a separate VMobject for the body
        self.body = VMobject()
        self.body.set_points(self.points)

        self.eyes = Eyes(self.body)
        self.eyes.shift(LEFT * creature_height * 0.35 + UP * creature_height * 0.38)
        self.add(self.body, self.eyes)


class Eyes(VMobject):
    CONFIG = {
        "height": 0.3,
    }

    def __init__(self, body, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.body = body
        eyes = self.create_eyes()
        self.add(eyes)

    def create_eyes(self, eye_radius: float = 0.2):
        left_eye = Ellipse(width=eye_radius * 1.2, height=eye_radius * 0.9, color=WHITE, fill_opacity=1)
        left_eye.rotate(45 * DEGREES)
        left_pupil = Circle(color=BLACK, radius=eye_radius * 0.28, fill_opacity=1).shift(
            0.18 * eye_radius * UP + 0.2 * eye_radius * LEFT
        )
        left_pupil_reflection = Circle(color=WHITE, radius=eye_radius * 0.03, fill_opacity=1).shift(
            0.12 * eye_radius * UP + 0.3 * eye_radius * LEFT
        )
        left_eye_group = VGroup(left_eye, left_pupil, left_pupil_reflection)

        right_eye = Ellipse(width=eye_radius * 1.2, height=eye_radius * 0.9, color=WHITE, fill_opacity=1)
        right_eye.rotate(45 * DEGREES)
        right_pupil = Circle(color=BLACK, radius=eye_radius * 0.28, fill_opacity=1).shift(
            0.18 * eye_radius * UP + 0.2 * eye_radius * LEFT
        )
        right_pupil_reflection = Circle(color=WHITE, radius=eye_radius * 0.03, fill_opacity=1).shift(
            0.12 * eye_radius * UP + 0.3 * eye_radius * LEFT
        )
        right_eye_group = VGroup(right_eye, right_pupil, right_pupil_reflection)

        # Position eyes next to each other
        left_eye_group.shift(LEFT * eye_radius * 0.55)
        right_eye_group.shift(RIGHT * eye_radius * 0.55)

        eyes = VGroup(left_eye_group, right_eye_group)
        eyes.rotate(-25 * DEGREES)
        return eyes

    def blink(self):
        return ApplyMethod(self[0].set_opacity, 0.2), ApplyMethod(self[0].set_opacity, 1)


class Blink(Animation):
    def __init__(self, eyes, **kwargs):
        self.eyes = eyes
        Animation.__init__(self, eyes, **kwargs)

    def interpolate_mobject(self, alpha):
        self.eyes.blink()
