from __future__ import annotations
from functools import reduce
from typing import List, LiteralString, Optional

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from janim.imports import (
    DOWN,
    # LEFT,
    ORIGIN,
    # RIGHT,
    UP,
    AnimGroup,
    FadeIn,
    FadeOut,
    Group,
    MoveToTarget,
    # Succession,
    Timeline,
    TransformMatchingShapes,
    TypstText,
    Write,
)
from numpy.char import join

SCALE = 1.6


class Writing:
    devanagari: LiteralString
    iast: LiteralString

    def __init__(self, itrans):
        self.devanagari = transliterate(itrans, sanscript.ITRANS, sanscript.DEVANAGARI)
        self.iast = transliterate(itrans, sanscript.ITRANS, sanscript.IAST)

    def render(self, direction=DOWN):
        devanagari = Jaini(self.devanagari)
        iast = Jaini(self.iast)
        group = Group(devanagari)
        group.points.arrange(direction)
        return group


class Children:
    nodes: List[Node]
    delimiter: LiteralString

    def __init__(
        self,
        nodes: List[Node],
        delimiter: LiteralString,
    ):
        self.nodes = nodes
        self.delimiter = delimiter


class Node:
    before: Writing
    children: Optional[Children]
    after: Optional[Writing]

    bg: Group[TypstText]
    ag: Optional[Group[TypstText]]

    def __init__(
        self,
        before: LiteralString,
        children: Optional[Children] = None,
        after: Optional[LiteralString] = None,
    ):
        self.before = Writing(before)
        self.children = children
        if after is None:
            self.after = after
            self.ag = None
        else:
            self.after = Writing(after)
            self.ag = self.after.render()

        self.bg = self.before.render()

    # def initialize(self, j: Timeline):
    #     word = self.before.render()
    #     self.group = word
    def morph(self):
        if self.bg is not None and self.ag is not None:
            self.bg.points.move_to(self.ag)
            return TransformMatchingShapes(self.bg, self.ag, duration=1.0)

    def safe_ag(self):
        if self.ag is None:
            return self.bg
        else:
            return self.ag

    def deconstruct(self, j: Timeline):
        # Render the parent if required
        if self.children is not None:
            # Duplicate the phrase
            clone = self.bg.copy()

            self.bg.generate_target()
            clone.generate_target()

            # Move the word and its clone away from the center
            self.bg.target.points.move_to(UP * SCALE / 2.0)
            clone.target.points.move_to(DOWN * SCALE / 2.0)

            j.play(AnimGroup(MoveToTarget(self.bg), MoveToTarget(clone)))

            # Create a group of the components
            before_children = Group(
                *[(lambda child: child.bg)(node) for node in self.children.nodes]
            )

            after_children = Group(
                *[
                    (lambda child: child.safe_ag())(node)
                    for node in self.children.nodes
                ],
            )

            # Create a group of the joiners
            connectors = Jaini("$%s$" % self.children.delimiter) * (
                len(after_children) - 1
            )

            # Create a group of the full equation
            equation = Group()

            for i in range(len(after_children)):
                bg = before_children[i]
                ag = after_children[i]
                if ag is not None:
                    equation.add(ag)
                else:
                    equation.add(bg)

                if i < len(connectors):
                    equation.add(connectors[i])

            equation.points.arrange()
            equation.points.move_to(clone.target)

            # Precreate the morph animations
            animations = []
            for node in self.children.nodes:
                if node.ag is not None:
                    animations.append(node.morph())

            j.play(
                TransformMatchingShapes(clone, before_children, duration=1.0),
            )

            if len(animations) > 0:
                j.play(AnimGroup(*animations, FadeIn(connectors, duration=1.0)))

            j.forward(3)

            # Determine if any of the nodes in the components also have children
            children_exist = reduce(
                lambda x, y: x or y,
                [(lambda c: c.children is not None)(n) for n in self.children.nodes],
            )

            if children_exist:
                # Shift everything already renderd upwards
                current = Group(self.bg, equation)
                current.generate_target()
                current.points.move_to(UP * SCALE)
                j.play(
                    MoveToTarget(current),
                )

                # Recurse
                for component in self.children.nodes:
                    if component.children is not None:
                        component.deconstruct(j)
            else:
                # Otherwise fade out
                j.play(
                    AnimGroup(FadeOut(self.bg), FadeOut(equation)),
                )


class Sloka:
    lines: List[Node]

    def __init__(self, lines):
        self.lines = lines

    # def render(self):
    #     full_text = (la)
    #     for i, line in enumerate(self.lines):
    #         "%s |" % line.before

    # node.bg.points.move_to(ORIGIN)
    # self.play(Write(node.bg))
    # node.deconstruct(self)


class Word:
    before: LiteralString
    after: Optional[LiteralString]

    def __init__(self, before, after=None):
        self.before = before
        self.after = after

    def safe_after(self):
        if self.after is None:
            return self.before
        else:
            return self.after


def Jaini(text: LiteralString, scale: Optional[float] = SCALE):
    return TypstText('#text(font: "Jaini")[%s]' % text, scale=scale)


# c = a == true then 5 else 4


def external_sandhi_v2(words: List[Word]):
    def aft(a, b):
        if a == b:
            return None
        else:
            return a

    before = " ".join([(lambda w: w.before)(w) for w in words])
    after = " ".join([(lambda w: w.safe_after())(w) for w in words])
    return external_sandhi(before, after)


def external_sandhi(before: LiteralString, after: LiteralString):
    def aft(a, b):
        if a == b:
            return None
        else:
            return a

    return Node(
        before=before,
        children=Children(
            [
                (lambda b, a: Node(before=b, after=aft(a, b)))(b, a)
                for (b, a) in list(zip(before.split(" "), after.split(" ")))
            ],
            "-",
        ),
        after=None,
    )


class SlokaTime(Timeline):
    def construct(self):
        # node = Node(
        #     "yo mAM pashyati sarvatra sarvaM cha mayi pashyati tasyAhaM na praNashyAmi sa ca me na praNashyati",
        #     Children(
        #         [
        #             # Node(
        #             #     "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
        #             #     Children(
        #             #         [
        #             #             Node("yo mAM pashyati sarvatra", None),
        #             #             Node("sarvaM cha mayi pashyati", None),
        #             #         ],
        #             #         "+",
        #             #     ),
        #             # ),
        #             Node(
        #                 "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
        #                 Children(
        #                     [
        #                         (lambda s: Node(s, None))(s)
        #                         for s in "yo mAm pashyati sarvatra sarvam cha mayi pashyati".split(
        #                             " "
        #                         )
        #                     ],
        #                     "+",
        #                 ),
        #             ),
        #             Node(
        #                 "tasyAhaM na praNashyAmi sa ca me na praNashyati",
        #                 Children(
        #                     [
        #                         Node("tasyAhaM na praNashyAmi", None),
        #                         Node("sa ca me na praNashyati", None),
        #                     ],
        #                     "+",
        #                 ),
        #             ),
        #         ],
        #         "|",
        #     ),
        # )

        # node = Node(
        #     before="yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
        #     children=Children(
        #         [
        #             (lambda s: Node(s, None, None))(s)
        #             for s in "yo mAm pashyati sarvatra sarvam cha mayi pashyati".split(
        #                 " "
        #             )
        #         ],
        #         "+",
        #     ),
        #     after=None,
        # )

        # node = node

        node = external_sandhi(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
            "yo mAm pashyati sarvatra sarvam cha mayi pashyati",
        )
        node = external_sandhi(
            "tasyAhaM na praNashyAmi sa ca me na praNashyati",
            "tasyAham na praNashyAmi sa ca me na praNashyati",
        )

        words = [
            Word("tasyAhaM", "tasyAham"),
            Word("na"),
            Word("praNashyAmi"),
            Word("sa"),
            Word("ca"),
            Word("me"),
            Word("na"),
            Word("praNashyati"),
        ]
        node = external_sandhi_v2(words)

        # node =

        node.bg.points.move_to(ORIGIN)
        self.play(Write(node.bg))
        node.deconstruct(self)
