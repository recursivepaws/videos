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
    Config,
    FadeOut,
    Group,
    Succession,
    Timeline,
    TransformMatchingDiff,
    TypstText,
    Vect,
    Wait,
    Write,
)

SCALE = 1.5


class Language(Enum):
    ENGLISH = 1
    SANSKRIT = 2
    TRANSLIT = 3


class LangColor(StrEnum):
    GOD = BLUE
    VERB = PINK
    YOU = GREEN
    PARTICLES = ORANGE
    OBJECTS = YELLOW


test_json = """
{
  "text": "nAvadhItamastu",
  "children": [
    { "text": "nau", "children": [] },
    {
      "text": "adhItamastu",
      "children": [
        { "text": "adhItam", "children": [] },
        { "text": "astu", "children": [] }
      ]
    }
  ]
}
"""


@dataclass
class Node:
    # language: Language

    text: str
    label: str
    color: str

    children: List[Node]

    def __init__(
        self,
        text: str,
        color: str = WHITE,
        children: List[Node] = [],
    ):
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

    def decompose(self, language: Language, position: Vect):
        states = [
            (lambda s: TypstText(s, scale=SCALE))(s) for s in self.strings(language)
        ]
        for i in range(len(states)):
            states[i].points.move_to(position)

        animations = []
        animations.append(Write(states[0], duration=3.0))
        for i in range(len(states) - 1):
            animations.append(
                TransformMatchingDiff(states[i], states[i + 1], duration=1.0)
            )
            animations.append(Wait(1.0))

        return Succession(*animations, Wait(1.0), FadeOut(states[len(states) - 1]))

        # current = states.pop(0)
        #
        # j.play(Write(current, duration=1.0))
        #
        # for state in states:
        #     j.play(TransformMatchingDiff(current, state, duration=1.0))
        #     current = state


class Sloka:
    sanskrit: List[List[Node]]
    english: List[List[Node]]

    def __init__(self, sanskrit, english):
        self.sanskrit = sanskrit
        self.english = english

    def teach(self, t: Timeline):
        sloka = []

        for i in range(len(self.sanskrit)):
            line = ""
            for sentence in self.sanskrit[i]:
                line += sentence.typst_code(Language.SANSKRIT)

            for i in range(i + 1):
                line += "।"

            sloka.append(TypstText(line, scale=SCALE))

        sloka = Group(*sloka)
        sloka.points.arrange(DOWN)

        for line in sloka:
            t.play(Write(line, duration=6.0))

        t.play(FadeOut(sloka))

        for i in range(len(self.sanskrit)):
            for j in range(len(self.sanskrit[i])):
                t.play(
                    Aligned(
                        self.sanskrit[i][j].decompose(
                            Language.SANSKRIT, ORIGIN + UP / SCALE * 1.5
                        ),
                        self.sanskrit[i][j].decompose(Language.TRANSLIT, ORIGIN),
                        self.english[i][j].decompose(
                            Language.ENGLISH, ORIGIN + DOWN / SCALE * 1.5
                        ),
                    )
                )

        # (lambda line: line.text)(x) for line in self.sanskrit


def Junicode(text: str, color: str, label: str):
    return (
        f'#text(font: "Junicode", stroke: none, fill: rgb("{color}"))[{text}] <{label}>'
    )


def Jaini(text: str, color: str, label: str):
    return f'#text(font: "Jaini", stroke: none, fill: rgb("{color}"))[{text}] <{label}>'


class SlokaTime(Timeline):
    # CONFIG = Config(fps=60, background_color=Color(PURE_GREEN))
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            [
                [
                    Node(
                        "yo mAM pashyati sarvatra",
                        children=[
                            Node("yo", children=[Node("yo", LangColor.YOU)]),
                            Node("mAM", children=[Node("mAm", LangColor.GOD)]),
                            Node(
                                "pashyati", children=[Node("pashyati", LangColor.VERB)]
                            ),
                            Node(
                                "sarvatra",
                                children=[Node("sarvatra", LangColor.OBJECTS)],
                            ),
                        ],
                    ),
                    Node(
                        "sarvaM cha mayi pashyati",
                        children=[
                            Node(
                                "sarvaM", children=[Node("sarvam", LangColor.OBJECTS)]
                            ),
                            Node("cha", children=[Node("cha", LangColor.PARTICLES)]),
                            Node("mayi", children=[Node("mayi", LangColor.GOD)]),
                            Node(
                                "pashyati", children=[Node("pashyati", LangColor.VERB)]
                            ),
                        ],
                    ),
                ],
                [
                    Node(
                        "tasyAhaM na praNashyAmi",
                        children=[
                            Node(
                                "tasyAhaM",
                                children=[
                                    Node("tasya", LangColor.YOU),
                                    Node("aham", LangColor.GOD),
                                ],
                            ),
                            Node("na", children=[Node("na", LangColor.PARTICLES)]),
                            Node(
                                "praNashyAmi",
                                children=[Node("praNashyAmi", LangColor.VERB)],
                            ),
                        ],
                    ),
                    Node(
                        "sa cha me na praNashyati",
                        children=[
                            Node("sa", children=[Node("sa", LangColor.YOU)]),
                            Node("ca", children=[Node("ca", LangColor.PARTICLES)]),
                            Node("me", children=[Node("me", LangColor.GOD)]),
                            Node("na", children=[Node("na", LangColor.PARTICLES)]),
                            Node(
                                "praNashyati",
                                children=[Node("praNashyati", LangColor.VERB)],
                            ),
                        ],
                    ),
                ],
            ],
            [
                [
                    Node(
                        "He who sees me everywhere",
                        children=[
                            Node(
                                "He who",
                                children=[Node("He who", LangColor.YOU)],
                            ),
                            Node("sees", children=[Node("sees", LangColor.VERB)]),
                            Node("me", children=[Node("me", LangColor.GOD)]),
                            Node(
                                "everywhere",
                                children=[Node("everywhere", LangColor.OBJECTS)],
                            ),
                        ],
                    ),
                    Node(
                        "and sees all things in me",
                        children=[
                            Node("and", children=[Node("and", LangColor.PARTICLES)]),
                            Node("sees", children=[Node("sees", LangColor.VERB)]),
                            Node(
                                "all things",
                                children=[Node("all things", LangColor.OBJECTS)],
                            ),
                            Node("in me", children=[Node("in me", LangColor.GOD)]),
                        ],
                    ),
                ],
                [
                    Node(
                        "to him, I am not lost,",
                        children=[
                            Node(
                                "to him, I",
                                children=[
                                    Node("to him", LangColor.YOU),
                                    Node(","),
                                    Node("I", LangColor.GOD),
                                ],
                            ),
                            Node("am", children=[Node("am")]),
                            Node("not", children=[Node("not", LangColor.PARTICLES)]),
                            Node("lost", children=[Node("lost", LangColor.VERB)]),
                        ],
                    ),
                    Node(
                        "and he is not lost to me",
                        children=[
                            Node("and", children=[Node("and", LangColor.PARTICLES)]),
                            Node("he", children=[Node("he", LangColor.YOU)]),
                            Node("is", children=[Node("is")]),
                            Node("not", children=[Node("not", LangColor.PARTICLES)]),
                            Node("lost", children=[Node("lost", LangColor.VERB)]),
                            Node("to me", children=[Node("to me", LangColor.GOD)]),
                        ],
                    ),
                ],
            ],
        )
        sloka.teach(self)
