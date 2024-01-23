from manim import *


class EigenScene(Scene):
    "Scene to illustrate how eigenvectors stay on their span during a transformation."

    def construct(self):
        """
        The following code in this function is inspired by Grant Sanderson.
        https://github.com/3b1b/videos/blob/master/_2021/quick_eigen.py#L337
        """
        
        plane = NumberPlane(faded_line_ratio=0)
        plane.set_stroke(width=3)
        coords = [-1, 1]
        vector = Vector(plane.c2p(*coords), color=YELLOW)
        array = IntegerMatrix([[-1], [1]], v_buff=0.9)
        array.scale(0.7)
        array.set_color(vector.get_color())
        array.add_to_back(BackgroundRectangle(array))
        array.generate_target()
        array.next_to(vector.get_end(), LEFT)
        array.target.next_to(2 * vector.get_end(), LEFT)
        two_times = Tex(r"2 \(\cdot\)")
        two_times.set_stroke(BLACK, 8, background=True)
        two_times.next_to(array.target, LEFT)
        span_line = Line(-4 * vector.get_end(), 4 * vector.get_end())
        span_line.set_stroke(YELLOW_E, 1)

        matrix = [[3, 1], [0, 2]]
        mat_mob = IntegerMatrix(matrix)
        mat_mob.set_x(4).to_edge(UP)
        mat_mob.set_column_colors(GREEN, RED)
        mat_mob.add_to_back(BackgroundRectangle(mat_mob))
        plane.set_stroke(background=True)

        bases = VGroup(
            Vector(RIGHT, color=GREEN_E),
            Vector(UP, color=RED_E),
        )
        faint_plane = plane.copy()
        faint_plane.set_stroke(GREY, width=1, opacity=0.5)

        self.add(faint_plane, plane, bases)
        self.add(vector)
        self.add(mat_mob)

        self.play(Write(array))
        self.add(span_line, vector, array)
        self.play(Create(span_line))
        self.wait()
        self.play(
            plane.animate.apply_matrix(matrix),
            bases[0].animate.put_start_and_end_on(ORIGIN, plane.c2p(3, 0)),
            bases[1].animate.put_start_and_end_on(ORIGIN, plane.c2p(1, 2)),
            vector.animate.scale(2, about_point=ORIGIN),
            MoveToTarget(array),
            GrowFromPoint(two_times, array.get_left() + SMALL_BUFF * LEFT),
            run_time=3,
            path_arc=0,
        )
        self.wait()

        self.remove(mat_mob)
        self.remove(array)
        self.remove(two_times)