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
        children: Optional[Children],
        after: Optional[LiteralString],
    ):
        self.before = Writing(before)
        self.children = children
        if after is None:
            self.after = after
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
            return TransformMatchingShapes(self.bg, self.ag)

    def deconstruct(self, j: Timeline):
        # Render the parent if required
        if self.children is not None:
            # Duplicate the phrase
            clone = self.bg.copy()

            self.bg.generate_target()
            clone.generate_target()

            # Move the word and its clone away from the center
            self.bg.target.points.move_to(UP)
            clone.target.points.move_to(DOWN)

            j.play(AnimGroup(MoveToTarget(self.bg), MoveToTarget(clone)))

            # Create a group of the components
            before_children = Group(
                *[(lambda child: child.bg)(node) for node in self.children.nodes]
            )

            after_children = Group(
                *[(lambda child: child.ag)(node) for node in self.children.nodes]
            )

            # Create a group of the joiners
            connectors = Jaini("$%s$" % self.children.delimiter) * (
                len(before_children) - 1
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
                TransformMatchingShapes(clone, before_children),
            )

            if len(animations) > 0:
                j.play(AnimGroup(*animations, FadeIn(connectors)))

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
                current.points.move_to(UP)
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
                    duration=1.0,
                )


class Sloka:
    padas: List[Node]

    def __init__(self, padas):
        self.padas = padas


def Jaini(text: LiteralString, scale: Optional[float] = 1.5):
    return TypstText('#text(font: "Jaini")[%s]' % text, scale=scale)


def external_sandhi(before: LiteralString, after: LiteralString):
    return Node(
        before=before,
        children=Children(
            [
                (lambda b, a: Node(b, None, a))(b, a)
                for (b, a) in list(zip(before.split(" "), after.split(" ")))
            ],
            "+",
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

        node = external_sandhi(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
            "yo mAm pashyati sarvatratratratratratra sarvam cha mayi pashyati",
        )
        node.bg.points.move_to(ORIGIN)
        self.play(Write(node.bg))
        node.deconstruct(self)
