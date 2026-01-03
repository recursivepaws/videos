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


class Writing:
    devanagari: LiteralString
    iast: LiteralString

    def __init__(self, itrans):
        self.devanagari = transliterate(itrans, sanscript.ITRANS, sanscript.DEVANAGARI)
        self.iast = transliterate(itrans, sanscript.ITRANS, sanscript.IAST)


class Components:
    items: List[Node]
    delimiter: LiteralString

    def __init__(
        self,
        items: List[Node],
        delimiter: LiteralString,
    ):
        self.items = items
        self.delimiter = delimiter


class Node:
    writing: Writing
    components: Optional[Components]

    def __init__(
        self,
        phrase: LiteralString,
        components: Optional[Components],
    ):
        self.writing = Writing(phrase)
        self.components = components

    def deconstruct(self, j: Timeline):
        word = Jaini(self.writing.devanagari)
        word.points.next_to(ORIGIN, UP)

        j.play(Write(word))

        if self.components is not None:
            # Duplicate the phrase
            child = word.copy()
            child.generate_target()
            child.target.points.move_to(DOWN)
            j.play(MoveToTarget(child))

            # Create a group of the components
            devanagari = Group(
                *[
                    (lambda c: Jaini(c.writing.devanagari))(c)
                    for c in self.components.items
                ]
            )

            # Create a group of the joiners
            connectors = Jaini("$%s$" % self.components.delimiter) * (
                len(devanagari) - 1
            )

            # Create a group of the full equation
            equation = Group()
            for i in range(len(devanagari)):
                equation.add(devanagari[i])
                if i < len(connectors):
                    equation.add(connectors[i])

            equation.points.arrange()
            equation.points.move_to(child.target)

            j.forward(1)

            j.play(
                TransformMatchingShapes(child, devanagari),
            )
            j.play(
                FadeIn(connectors),
            )

            j.forward(3)

            j.play(
                AnimGroup(FadeOut(word), FadeOut(equation)),
                duration=1.0,
            )

            for component in self.components.items:
                if component.components is not None:
                    component.deconstruct(j)


class Sloka:
    padas: List[Node]

    def __init__(self, padas):
        self.padas = padas


def Jaini(text: LiteralString, scale: Optional[float] = 1.0):
    return TypstText('#text(font: "Jaini")[%s]' % text, scale=scale)


class SlokaTime(Timeline):
    def construct(self):
        node = Node(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati tasyAhaM na praNashyAmi sa ca me na praNashyati",
            Components(
                [
                    Node(
                        "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
                        Components(
                            [
                                Node("yo mAM pashyati sarvatra", None),
                                Node("sarvaM cha mayi pashyati", None),
                            ],
                            "+",
                        ),
                    ),
                    Node(
                        "tasyAhaM na praNashyAmi sa ca me na praNashyati",
                        Components(
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
            Components(
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
