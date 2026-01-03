from __future__ import annotations
from functools import reduce
from operator import contains
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
    Typst,
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
        group = Group(devanagari, iast)
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
    writing: Writing
    children: Optional[Children]

    def __init__(
        self,
        writing: LiteralString,
        children: Optional[Children],
    ):
        self.writing = Writing(writing)
        self.children = children

    def deconstruct(self, j: Timeline):
        word = self.writing.render()
        word.points.next_to(ORIGIN, UP)

        j.play(Write(word))

        # pretransformationchildren =
        if contains(self.writing.devanagari, " "):
            print("meow")

        if self.children is not None:
            # Duplicate the phrase
            clone = word.copy()
            clone.generate_target()
            clone.target.points.move_to(DOWN)
            j.play(MoveToTarget(clone))

            # Create a group of the components
            children = Group(
                *[
                    (lambda child: child.writing.render())(c)
                    for c in self.children.nodes
                ]
            )

            # Create a group of the joiners
            connectors = Jaini("$%s$" % self.children.delimiter) * (len(children) - 1)

            # Create a group of the full equation
            equation = Group()
            for i in range(len(children)):
                equation.add(children[i])
                if i < len(connectors):
                    equation.add(connectors[i])

            equation.points.arrange()
            equation.points.move_to(clone.target)

            j.forward(1)

            j.play(
                TransformMatchingShapes(clone, children),
            )
            j.play(
                FadeIn(connectors),
            )

            j.forward(3)

            # Determine if any of the nodes in the components also have children
            children_exist = reduce(
                lambda x, y: x or y,
                [(lambda c: c.children is not None)(n) for n in self.children.nodes],
            )

            if children_exist:
                # Shift everything already renderd upwards
                current = Group(word, equation)
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
                    AnimGroup(FadeOut(word), FadeOut(equation)),
                    duration=1.0,
                )


class Sloka:
    padas: List[Node]

    def __init__(self, padas):
        self.padas = padas


def Jaini(text: LiteralString, scale: Optional[float] = 2.0):
    return TypstText('#text(font: "Jaini")[%s]' % text, scale=scale)


class SlokaTime(Timeline):
    def construct(self):
        node = Node(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati tasyAhaM na praNashyAmi sa ca me na praNashyati",
            Children(
                [
                    # Node(
                    #     "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
                    #     Children(
                    #         [
                    #             Node("yo mAM pashyati sarvatra", None),
                    #             Node("sarvaM cha mayi pashyati", None),
                    #         ],
                    #         "+",
                    #     ),
                    # ),
                    Node(
                        "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
                        Children(
                            [
                                (lambda s: Node(s, None))(s)
                                for s in "yo mAm pashyati sarvatra sarvam cha mayi pashyati".split(
                                    " "
                                )
                            ],
                            "+",
                        ),
                    ),
                    Node(
                        "tasyAhaM na praNashyAmi sa ca me na praNashyati",
                        Children(
                            [
                                Node("tasyAhaM na praNashyAmi", None),
                                Node("sa ca me na praNashyati", None),
                            ],
                            "+",
                        ),
                    ),
                ],
                "|",
            ),
        )

        node = Node(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
            Children(
                [
                    (lambda s: Node(s, None))(s)
                    for s in "yo mAm pashyati sarvatra sarvam cha mayi pashyati".split(
                        " "
                    )
                ],
                "+",
            ),
        )

        node.deconstruct(self)
