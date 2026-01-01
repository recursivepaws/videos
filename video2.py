from __future__ import annotations
from typing import List, LiteralString, Optional

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from janim.imports import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    AnimGroup,
    FadeIn,
    FadeOut,
    Group,
    MoveToTarget,
    Succession,
    Timeline,
    TransformMatchingShapes,
    TypstText,
    Write,
)


class Node:
    phrase: LiteralString
    components: Optional[List[Node]]

    def __init__(self, phrase, components):
        self.phrase = phrase
        self.components = components


class Sloka:
    padas: List[Node]

    def __init__(self, padas):
        self.padas = padas


node = Node(
    "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
    [Node("yo mAM pashyati sarvatra", None), Node("sarvaM cha mayi pashyati", None)],
)

# Input data for transliteration
data = "idam adbhutam"
padas = ["yo mAM pashyati sarvatra", ""]
data = "yo mAM pashyati sarvatra sarvaM cha mayi pashyati"
# secontasyAhaM na praNashyAmi sa cha me na praNashyati ||'
print(transliterate(data, sanscript.ITRANS, sanscript.DEVANAGARI))

scale = 2.0


def Devanagari(text):
    return TypstText('#text(font: "Jaini")[%s]' % text, scale=scale)


class Sandhi(Timeline):
    def construct(self):
        dur = 5
        # define items
        left = Devanagari("पर")
        right = Devanagari("उपकार")
        plus = Devanagari("$+$")
        whole = Devanagari("परोपकार")

        # do animations
        self.forward()

        left.points.next_to(plus, LEFT)
        right.points.next_to(plus, RIGHT)

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


class Shloka(Timeline):
    def construct(self):
        # define items
        first = Devanagari("परोपकाराय फलन्ति वृक्षाः परोपकाराय वहन्ति नद्यः ।")
        second = Devanagari("परोपकाराय दुहन्ति गावः परोपकारार्थमिदं शरीरम् ॥")

        first.points.next_to(ORIGIN, UP)
        second.points.next_to(ORIGIN, DOWN)

        self.play(Write(first))
        self.play(Write(second))

        self.forward(4)

        self.play(FadeOut(first), FadeOut(second))

        self.forward()


class Pada(Timeline):
    def construct(self):
        dur = 5
        # define items
        first = Devanagari("परोपकाराय फलन्ति वृक्षाः")
        second = Devanagari("परोपकाराय वहन्ति नद्यः")
        third = Devanagari("परोपकाराय दुहन्ति गावः")
        fourth = Devanagari("परोपकारार्थमिदं शरीरम्")
        d1 = Devanagari("।")
        d2 = Devanagari("॥")

        second.points.next_to(ORIGIN, UP)
        first.points.next_to(second, UP)

        third.points.next_to(ORIGIN, DOWN)
        fourth.points.next_to(third, DOWN)

        second.points.align_to(first, LEFT)
        third.points.align_to(first, LEFT)
        fourth.points.align_to(first, LEFT)

        d1.points.next_to(second, RIGHT)
        d2.points.next_to(fourth, RIGHT)

        self.play(
            Succession(Write(first), Write(second), duration=dur),
            AnimGroup(FadeIn(d1), at=dur * 0.9),
        )
        self.play(
            Succession(Write(third), Write(fourth), duration=dur),
            AnimGroup(FadeIn(d2), at=dur * 0.9),
        )

        self.forward(3)

        self.play(
            FadeOut(first),
            FadeOut(second),
            FadeOut(third),
            FadeOut(fourth),
            FadeOut(d1),
            FadeOut(d2),
        )

        self.forward()


class Quantity(Timeline):
    def construct(self):
        dur = 2
        # define items
        # singular = Devanagari("वृक्षः")
        # plural = Devanagari("वृक्षाः")
        singular = Devanagari("फलति")
        plural = Devanagari("फलन्ति")

        d1 = Devanagari("(SG)")
        d2 = Devanagari("(PL)")

        singular.points.next_to(ORIGIN, UP)
        plural.points.next_to(ORIGIN, DOWN).align_to(singular, LEFT)

        d1.points.next_to(singular, RIGHT)
        d2.points.next_to(plural, RIGHT)

        self.play(
            Succession(Write(singular), Write(plural), duration=dur),
            AnimGroup(FadeIn(d1), FadeIn(d2), at=dur * 0.9),
        )

        self.forward(3)


class Deconstruct(Timeline):
    def deconstruct(self, word, left, right):
        word = Devanagari(word)
        left = Devanagari(left)
        right = Devanagari(right)

        word.points.next_to(ORIGIN, UP)

        self.play(Write(word))

        child = word.copy()
        child.generate_target()
        child.target.points.move_to(DOWN)
        self.play(MoveToTarget(child))

        plus = Devanagari("$+$")
        plus.points.move_to(child)
        left.points.next_to(child, LEFT)
        right.points.next_to(child, RIGHT)

        self.forward(1)

        self.play(
            AnimGroup(
                FadeIn(plus),
                TransformMatchingShapes(child, Group(left, right)),
            ),
            duration=1.0,
        )

        self.forward(3)

    def construct(self):
        # self.deconstruct("परोपकाराय", 'परोपकार','आय')
        self.deconstruct("परोपकार", "पर", "उपकार")


class Deconstruct2(Timeline):
    def deconstruct(self, word, left, middle, right):
        word = Devanagari(word)
        left = Devanagari(left)
        middle = Devanagari(middle)
        right = Devanagari(right)

        word.points.next_to(ORIGIN, UP)

        self.play(Write(word))

        child = word.copy()
        child.generate_target()
        child.target.points.move_to(DOWN)
        self.play(MoveToTarget(child))

        p1 = Devanagari("$+$")
        p2 = Devanagari("$+$")
        # p1.points.move_to(child)
        # p1.points.move_to(child)
        middle.points.move_to(child)

        p1.points.next_to(middle, LEFT)
        left.points.next_to(p1, LEFT)

        p2.points.next_to(middle, RIGHT)
        right.points.next_to(child, RIGHT)

        self.forward(1)

        self.play(
            AnimGroup(
                FadeIn(p1),
                FadeIn(p2),
                TransformMatchingShapes(child, Group(left, middle, right)),
            ),
            duration=1.0,
        )

        self.forward(3)

    def construct(self):
        self.deconstruct("परोपकारार्थमिदं", "परोपकार", "अर्थम्", "इदं")


class Word(Timeline):
    def construct(self):
        scale = 2.0
        word = TypstText("परोपकाराय", scale=scale)
        word.points.move_to(ORIGIN)
        self.play(Write(word))

        self.forward(3)

        self.play(FadeOut(word))

        self.forward()
