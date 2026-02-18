from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import List

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from janim.imports import (
    BLUE,
    DOWN,
    GREEN,
    ORANGE,
    ORIGIN,
    PINK,
    RED,
    UP,
    WHITE,
    YELLOW,
    Aligned,
    FadeOut,
    Group,
    GrowFromCenter,
    ShrinkToCenter,
    Succession,
    TransformMatchingDiff,
    TypstText,
    Wait,
    Write,
)

SCALE = 2.0


class Language(Enum):
    ENGLISH = 1
    SANSKRIT = 2
    TRANSLIT = 3


class LangColor(StrEnum):
    GOD = BLUE
    VERB = PINK
    YOU = GREEN
    PARTICLES = ORANGE
    NEGATION = RED
    OBJECTS = YELLOW


class Declension(Enum):
    NOP = 0
    NOM = 1
    ACC = 2
    INS = 3
    DAT = 4
    ABL = 5
    GEN = 6
    LOC = 7
    VOC = 8


@dataclass
class Node:
    text: str
    label: str
    color: str

    children: List[Node]

    def __init__(
        self,
        text: str,
        color: str = WHITE,
        declension: Declension = Declension.NOP,
        children: List[Node] = [],
        delay: int = 0,
    ):
        if delay > 0:
            if len(children) > 0:
                raise ValueError("cannot add color delay when there are children")
            node = Node(text, color, children=[])
            for i in range(delay):
                node = Node(text, children=[node])

            self.text = node.text
            self.color = node.color
            self.children = node.children
            self.label = node.label
        else:
            splits = text.split(" ")
            # If there are spaces
            if len(splits) > 1 and len(splits) == len(children):
                print(splits)
                new_children = []
                for i in range(len(splits)):
                    new_children.append(Node(splits[i], color, children=[children[i]]))

                self.text = text
                self.color = color
                self.children = new_children
                self.label = f"label{abs(hash(text)) % (10**8)}"
            else:
                self.text = text
                self.color = color
                self.children = children
                self.label = f"label{abs(hash(text)) % (10**8)}"

    # Get the typst code for the text
    def typst_code(self, language: Language):
        match language:
            case Language.ENGLISH:
                return Junicode(self.text, self.color, self.label)
            case Language.TRANSLIT:
                iast = transliterate(self.text, sanscript.ITRANS, sanscript.IAST)
                return Junicode(iast, self.color, self.label)
            case Language.SANSKRIT:
                deva = transliterate(self.text, sanscript.ITRANS, sanscript.DEVANAGARI)
                return Jaini(deva, self.color, self.label)

    def strings(self, language: Language):
        strings = [self.typst_code(language)]
        child_strings = []
        depth = 0

        if len(self.children) > 0:
            for child in self.children:
                cs = child.strings(language)
                if len(cs) > depth:
                    depth = len(cs)
                child_strings.append(cs)

        roots = []
        # each depth should have its own string
        for i in range(depth):
            root = []
            for cs in child_strings:
                if len(cs) > i:
                    root.append(cs[i])
                else:
                    root.append(cs[len(cs) - 1])
            roots.append(str(" ").join(root))

        return strings + roots

    def states(self, language: Language):
        return [
            (lambda s: TypstText(s, scale=SCALE))(s) for s in self.strings(language)
        ]

    def decompose_states(self, states: List[TypstText]):
        animations = []
        animations.append(Write(states[0], duration=1.0))

        for i in range(len(states) - 1):
            animations.append(
                TransformMatchingDiff(
                    states[i],
                    states[i + 1],
                    duration=0.5,
                    mismatch=(  # type: ignore[arg-type]
                        lambda item, p, **kwargs: ShrinkToCenter(item, **kwargs),
                        lambda item, p, **kwargs: GrowFromCenter(item, **kwargs),
                    ),
                )
            )
            animations.append(Wait(0.2))

        return Succession(
            *animations,
            Wait(1.2),
            FadeOut(states[len(states) - 1], duration=0.5),
        )


def translit(value: str):
    return transliterate(value, sanscript.ITRANS, sanscript.IAST)


class Question:
    question: Node

    def __init__(
        self,
        question: str,
    ):
        self.question = Node(question)

    def ask(self):
        typst = TypstText(self.question.typst_code(Language.ENGLISH), scale=SCALE)
        return Succession(
            Write(typst, duration=0.5), Wait(3.0), FadeOut(typst, duration=1.0)
        )


class Citation:
    text: Node
    lang: Language

    def __init__(self, text: str, lang: Language):
        self.text = Node(text)
        self.lang = lang


class Sloka:
    citation: Citation
    sanskrit: List[List[Node]]
    english: List[List[Node]]

    def __init__(
        self,
        citation: Citation,
        sanskrit: List[List[Node]],
        english: List[List[Node]],
    ):
        self.citation = citation
        self.sanskrit = sanskrit
        self.english = english

    def teach(self):
        sloka = []

        for i in range(len(self.sanskrit)):
            line = ""
            for sentence in self.sanskrit[i]:
                line += sentence.typst_code(Language.SANSKRIT)

            sloka.append(TypstText(line, scale=SCALE))

        sloka = Group(*sloka)
        sloka.points.arrange(DOWN)

        animations = []

        for line in sloka:
            animations.append(Write(line, duration=6.0))

        citation = TypstText(
            self.citation.text.typst_code(self.citation.lang), scale=SCALE
        )
        citation.points.next_to(sloka, DOWN)

        animations.append(
            Succession(
                Wait(2.0),
                Write(citation, duration=0.5),
                Wait(0.5),
                FadeOut(Group(sloka, citation)),
            )
        )

        for i in range(len(self.sanskrit)):
            for j in range(len(self.sanskrit[i])):
                sa = self.sanskrit[i][j].states(Language.SANSKRIT)
                ia = self.sanskrit[i][j].states(Language.TRANSLIT)
                en = self.english[i][j].states(Language.ENGLISH)

                for xi in range(len(sa)):
                    ia_ref = ia[min(xi, len(ia) - 1)]
                    ia_ref.points.move_to(ORIGIN)
                    sa[min(xi, len(sa) - 1)].points.next_to(ia_ref, UP / SCALE * 4.0)
                    en[min(xi, len(en) - 1)].points.next_to(ia_ref, DOWN / SCALE * 4.0)
                    # Language.SANSKRIT, ORIGIN + UP / SCALE * 2.0

                animations.append(
                    Aligned(
                        self.sanskrit[i][j].decompose_states(sa),
                        self.sanskrit[i][j].decompose_states(ia),
                        self.english[i][j].decompose_states(en),
                    )
                )

        return Succession(*animations)


def Junicode(text: str, color: str, label: str):
    return (
        f'#text(font: "Junicode", stroke: none, fill: rgb("{color}"))[{text}] <{label}>'
    )


def Jaini(text: str, color: str, label: str):
    return f'#text(font: "Jaini", stroke: none, fill: rgb("{color}"))[{text}] <{label}>'
