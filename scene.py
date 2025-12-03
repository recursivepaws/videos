from manim import *
import manim_devanagari as m_deva


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class TransformMatchingShapesFromCopy(Scene):
    def construct(self):
        # Method 2: More explicit - add copies first, then transform
        left = m_deva.Deva_Tex("पर", font_size=72)
        plus = Text("+", font_size=72)
        right = m_deva.Deva_Tex("उपकार", font_size=72)
        whole = m_deva.Deva_Tex("पर", "ो", "पकार", font_size=72)

        left.next_to(plus, LEFT)
        right.next_to(plus, RIGHT)
        whole.next_to(plus, DOWN)

        self.play(Write(left), Write(plus), Write(right))
        self.wait()

        # Create copies and add them to the scene
        left_copy = left.copy()
        right_copy = right.copy()
        left_copy.generate_target()
        right_copy.generate_target()
        left_copy.target.shift(DOWN)
        right_copy.target.shift(DOWN)
        self.add(left_copy, right_copy)

        self.play(MoveToTarget(left_copy), MoveToTarget(right_copy))

        # Transform the copies
        self.play(
            TransformMatchingShapes(Group(left_copy, right_copy), Group(whole)),
            run_time=2,
        )

        self.wait(1)

        # Now fade out the originals
        self.play(FadeOut(left), FadeOut(plus), FadeOut(right))

        whole.generate_target()
        whole.target.shift(UP)
        self.play(MoveToTarget(whole))

        self.wait(2)


class Meow(Scene):
    def construct(self):
        word1 = m_deva.Deva_Tex("पर", font_size=72)
        word2 = m_deva.Deva_Tex("उपकार", font_size=72)
        plus = Text("+", font_size=72)

        group = Group(word1, plus, word2).arrange(RIGHT, aligned_edge=DOWN)
        group.shift(-plus.get_center())

        self.play(
            Write(word1),
            Write(word2),
            Write(plus),
        )
        self.wait()

        combined = m_deva.Deva_Tex("परोपकार", font_size=72).move_to(ORIGIN)
        combined.set_y(word1.get_y())

        # transform_title.to_corner(UP + LEFT)
        self.play(
            FadeOut(plus),
            TransformMatchingShapes(Group(word1, word2), combined),
        )
        self.wait()
        self.wait(1.0)


class TransformTypes(Scene):
    def construct(self):
        # 1. Transform - morphs object but keeps original reference
        title1 = Text("Transform", font_size=24).to_edge(UP)
        self.add(title1)

        square = Square(color=BLUE)
        circle = Circle(color=RED)

        self.play(Create(square))
        self.wait(0.5)
        self.play(Transform(square, circle))  # square morphs to circle shape
        self.wait(0.5)
        self.play(FadeOut(square))  # Note: still reference 'square', not 'circle'
        self.remove(title1)
        self.wait(0.5)

        # 2. ReplacementTransform - replaces the object
        title2 = Text("ReplacementTransform", font_size=24).to_edge(UP)
        self.add(title2)

        square = Square(color=BLUE)
        circle = Circle(color=RED)

        self.play(Create(square))
        self.wait(0.5)
        self.play(ReplacementTransform(square, circle))  # square becomes circle
        self.wait(0.5)
        self.play(FadeOut(circle))  # Now reference 'circle'
        self.remove(title2)
        self.wait(0.5)

        # 3. TransformFromCopy - original stays, copy transforms
        title3 = Text("TransformFromCopy", font_size=24).to_edge(UP)
        self.add(title3)

        square = Square(color=BLUE).shift(LEFT * 2)
        circle = Circle(color=RED).shift(RIGHT * 2)

        self.play(Create(square))
        self.wait(0.5)
        self.play(
            TransformFromCopy(square, circle)
        )  # square stays, copy becomes circle
        self.wait(0.5)
        self.play(FadeOut(square), FadeOut(circle))
        self.remove(title3)
        self.wait(0.5)

        # 4. ClockwiseTransform - transforms with rotation
        title4 = Text("ClockwiseTransform", font_size=24).to_edge(UP)
        self.add(title4)

        square = Square(color=BLUE)
        circle = Circle(color=RED)

        self.play(Create(square))
        self.wait(0.5)
        self.play(
            ClockwiseTransform(square, circle)
        )  # Rotates clockwise while morphing
        self.wait(0.5)
        self.play(FadeOut(square))
        self.remove(title4)
        self.wait(0.5)

        # 5. FadeTransform - fades while transforming
        title5 = Text("FadeTransform", font_size=24).to_edge(UP)
        self.add(title5)

        text1 = Text("Hello", color=BLUE)
        text2 = Text("World!", color=RED)

        self.play(Write(text1))
        self.wait(0.5)
        self.play(FadeTransform(text1, text2))  # Smooth fade between objects
        self.wait(0.5)
        self.play(FadeOut(text2))
        self.remove(title5)
        self.wait(0.5)

        # 6. MoveToTarget - set a target and transform to it
        title6 = Text("MoveToTarget", font_size=24).to_edge(UP)
        self.add(title6)

        square = Square(color=BLUE)
        self.play(Create(square))

        # Set target state
        square.generate_target()
        square.target.shift(RIGHT * 2).scale(0.5).set_color(RED)

        self.wait(0.5)
        self.play(MoveToTarget(square))
        self.wait(0.5)
        self.play(FadeOut(square))
        self.remove(title6)
        self.wait(0.5)

        # 7. TransformMatchingShapes - matches shapes intelligently
        title7 = Text("TransformMatchingShapes", font_size=24).to_edge(UP)
        self.add(title7)

        text1 = Text("ABC")
        text2 = Text("BCD").shift(RIGHT * 0.5)

        self.play(Write(text1))
        self.wait(0.5)
        self.play(TransformMatchingShapes(text1, text2))  # Keeps matching letters
        self.wait(0.5)
        self.play(FadeOut(text2))
        self.remove(title7)

        self.wait(1)


class TransformGroupTest(Scene):
    def construct(self):
        # Test 1: TransformMatchingShapes with Group
        word1 = m_deva.Deva_Tex("पर", font_size=72)
        word2 = m_deva.Deva_Tex("उपकार", font_size=72)
        combined = m_deva.Deva_Tex("परोपकार", font_size=72)

        # Arrange them
        word1.shift(LEFT * 2)
        word2.shift(RIGHT * 2)
        combined.move_to(ORIGIN)

        self.add(word1, word2)
        self.wait(1)

        # Try transforming the group
        self.play(TransformMatchingShapes(Group(word1, word2), combined), run_time=2)

        self.wait(2)

        # Test 2: For comparison - ReplacementTransform
        self.clear()

        word1 = m_deva.Deva_Tex("पर", font_size=72)
        word2 = m_deva.Deva_Tex("उपकार", font_size=72)
        combined2 = m_deva.Deva_Tex("परोपकार", font_size=72)

        word1.shift(LEFT * 2)
        word2.shift(RIGHT * 2)
        combined2.move_to(ORIGIN)

        self.add(word1, word2)
        self.wait(1)

        # Try with ReplacementTransform
        self.play(ReplacementTransform(Group(word1, word2), combined2), run_time=2)

        self.wait(2)


class WordSmash(Scene):
    def construct(self):
        # Create the two words
        word1 = m_deva.Deva_Tex("पर", font_size=72)
        word2 = m_deva.Deva_Tex("उपकार", font_size=72)
        plus = Text("+", font_size=72).move_to(ORIGIN)

        # Position them on opposite sides
        word1.to_edge(LEFT, buff=1.5)
        word2.to_edge(RIGHT, buff=1.5)

        # Show the words with a fade in
        self.play(FadeIn(word1), FadeIn(word2), FadeIn(plus))
        self.wait(0.5)

        # Animate words moving toward center
        self.play(FadeOut(plus, scale=0.5), run_time=0.3)

        # Create the combined word
        combined = m_deva.Deva_Tex("परोपकार", font_size=72).move_to(ORIGIN)
        flash = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8).move_to(ORIGIN)
        self.add(flash)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    word1.animate.move_to(ORIGIN).scale(1.2),
                    word2.animate.move_to(ORIGIN).scale(1.2),
                    flash.animate.scale(8).set_opacity(0),
                ),
                AnimationGroup(
                    # FadeOut(word1, scale=0.8),
                    # FadeOut(word2, scale=0.8),
                    FadeIn(combined, scale=1.2),
                ),
                lag_ratio=0.8,
            ),
            run_time=1,
            rate_func=rush_into,
        )
        self.play(
            FadeOut(word1, scale=0.8),
            FadeOut(word2, scale=0.8),
            combined.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.4,
        )

        # Create flash effect on collision
        # self.remove(flash)

        # Transform to combined word
        # self.play(
        #     FadeOut(word1, scale=0.8),
        #     FadeOut(word2, scale=0.8),
        #     FadeIn(combined, scale=1.2),
        #     run_time=0.8
        # )

        # Final emphasis - slight bounce
        # self.play(
        #     combined.animate.scale(1.1),
        #     rate_func=there_and_back,
        #     run_time=0.5
        # )

        self.wait(1)


class Deconstruct(Scene):
    def construct(self):
        word = m_deva.Deva_Tex("प", "रो", "पकार")
        left = m_deva.Deva_Tex("पर")
        right = m_deva.Deva_Tex("उपकार")

        word.move_to(ORIGIN)

        left.shift(LEFT * 2)
        right.shift(RIGHT * 2)

        self.play(Write(word))
        self.wait()

        # Create copies and add them to the scene
        child = word.copy()
        self.play(child.animate.move_to(DOWN))

        plus = Text("+")
        plus.move_to(child)
        left.next_to(plus, LEFT)
        right.next_to(plus, RIGHT)

        # Transform the copies
        self.play(
            AnimationGroup(
                FadeIn(plus),
                TransformMatchingShapes(child, Group(left, right)),
            ),
            run_time=2,
        )

        # Now fade out the originals
        # self.play(combin)

        self.wait(2)
