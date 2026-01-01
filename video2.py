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


class Node:
    writing: Writing
    components: Optional[List[Node]]

    def __init__(self, phrase: LiteralString, components):
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
                *[(lambda c: Jaini(c.writing.devanagari))(c) for c in self.components]
            )

            # Create a group of the joiners
            connectors = Jaini("$+$") * (len(devanagari) - 1)

            # Create a group of the full equation
            equation = Group()
            for i in range(len(devanagari)):
                equation.add(devanagari[i])
                if i < len(connectors):
                    equation.add(connectors[i])
            # So they can be arranged
            equation.points.arrange()

            j.forward(1)

            j.play(
                AnimGroup(
                    FadeIn(connectors),
                    TransformMatchingShapes(child, devanagari),
                ),
                duration=1.0,
            )

            j.forward(3)


class Sloka:
    padas: List[Node]

    def __init__(self, padas):
        self.padas = padas


def Jaini(text: LiteralString, scale: Optional[float] = 2.0):
    return TypstText('#text(font: "Jaini")[%s]' % text, scale=scale)


class SlokaTime(Timeline):
    def construct(self):
        node = Node(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
            [
                Node("yo mAM pashyati sarvatra", None),
                Node("sarvaM cha mayi pashyati", None),
            ],
        )
        node.deconstruct(self)
