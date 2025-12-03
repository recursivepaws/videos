from janim.imports import *


class HelloJAnimExample(Timeline):
    def construct(self):
        # define items
        left = TypstText("पर")
        right = TypstText("उपकार")
        plus = TypstText("$+$")
        whole = TypstText("परोपकार")
        equals = TypstText("$=$")

        # do animations
        self.forward()

        left.points.next_to(plus, LEFT)
        right.points.next_to(plus, RIGHT)
        equals.points.next_to(right, RIGHT)

        whole.points.shift(DOWN)

        self.play(Write(left), Write(plus), Write(right))

        self.forward()

        # Create copies and add them to the scene
        left_copy = left.copy()
        right_copy = right.copy()
        left_copy.generate_target()
        right_copy.generate_target()
        left_copy.target.points.shift(DOWN)
        right_copy.target.points.shift(DOWN)

        self.play(MoveToTarget(left_copy), MoveToTarget(right_copy))
        self.forward()

        # Transform the copies
        self.play(
            TransformMatchingShapes(Group(left_copy, right_copy), Group(whole)),
        )

        self.forward()

        # Now fade out the originals
        self.play(FadeOut(left), FadeOut(plus), FadeOut(right))

        whole.generate_target()
        whole.target.points.shift(UP)
        self.play(MoveToTarget(whole))

        self.forward()
