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
    VERB = RED
    YOU = GREEN
    PARTICLES = PINK
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
        for i in range(len(states) - 1):
            if i == 0:
                animations.append(Write(states[i], duration=3.0))

            animations.append(
                TransformMatchingDiff(states[i], states[i + 1], duration=1.0)
            )
            animations.append(Wait(1.0))

        return Succession(*animations, Wait(2.0), FadeOut(states[len(states) - 1]))

        # current = states.pop(0)
        #
        # j.play(Write(current, duration=1.0))
        #
        # for state in states:
        #     j.play(TransformMatchingDiff(current, state, duration=1.0))
        #     current = state


class Sloka:
    lines: List[Node]

    def __init__(self, lines):
        self.lines = lines


def Junicode(text: str, color: str, label: str):
    return (
        f'#text(font: "Junicode", stroke: none, fill: rgb("{color}"))[{text}] <{label}>'
    )


def Jaini(text: str, color: str, label: str):
    return f'#text(font: "Jaini", stroke: none, fill: rgb("{color}"))[{text}] <{label}>'


class SlokaTime(Timeline):
    # CONFIG = Config(fps=60, background_color=Color(PURE_GREEN))

    def construct(self):
        sa = Node(
            "yo mAM pashyati sarvatra sarvaM cha mayi pashyati",
            children=[
                Node("yo", children=[Node("yo", LangColor.YOU)]),
                Node("mAM", children=[Node("mAm", LangColor.GOD)]),
                Node("pashyati", children=[Node("pashyati", LangColor.VERB)]),
                Node("sarvatra", children=[Node("sarvatra", LangColor.OBJECTS)]),
                Node("sarvaM", children=[Node("sarvam", LangColor.OBJECTS)]),
                Node("cha", children=[Node("cha", LangColor.PARTICLES)]),
                Node("mayi", children=[Node("mayi", LangColor.GOD)]),
                Node("pashyati", children=[Node("pashyati", LangColor.VERB)]),
            ],
        )
        en = Node(
            "He who sees me everywhere and sees all things in me-",
            children=[
                Node(
                    "He who",
                    children=[Node("He who", LangColor.YOU)],
                ),
                Node("sees", children=[Node("sees", LangColor.VERB)]),
                Node("me", children=[Node("me", LangColor.GOD)]),
                Node("everywhere", children=[Node("everywhere", LangColor.OBJECTS)]),
                # Node(",", children=[Node(",")]),
                Node("and", children=[Node("and", LangColor.PARTICLES)]),
                Node("sees", children=[Node("sees", LangColor.VERB)]),
                Node("all things", children=[Node("all things", LangColor.OBJECTS)]),
                Node("in me", children=[Node("in me", LangColor.GOD)]),
            ],
        )

        self.play(
            Aligned(
                sa.decompose(Language.SANSKRIT, ORIGIN + UP / SCALE * 1.5),
                sa.decompose(Language.TRANSLIT, ORIGIN),
                en.decompose(Language.ENGLISH, ORIGIN + DOWN / SCALE * 1.5),
            )
        )

        sa = Node(
            "tasyAhaM na praNashyAmi sa ca me na praNashyati",
            children=[
                Node(
                    "tasyAhaM",
                    children=[
                        Node("tasya", LangColor.YOU),
                        Node("aham", LangColor.GOD),
                    ],
                ),
                Node("na", children=[Node("na", LangColor.PARTICLES)]),
                Node("praNashyAmi", children=[Node("praNashyAmi", LangColor.VERB)]),
                Node("sa", children=[Node("sa", LangColor.YOU)]),
                Node("ca", children=[Node("ca", LangColor.PARTICLES)]),
                Node("me", children=[Node("me", LangColor.GOD)]),
                Node("na", children=[Node("na", LangColor.PARTICLES)]),
                Node("praNashyati", children=[Node("praNashyati", LangColor.VERB)]),
            ],
        )

        en = Node(
            "to him, I am not lost, and he is not lost to me",
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
                Node(",", children=[Node(",")]),
                Node("and", children=[Node("and", LangColor.PARTICLES)]),
                Node("he", children=[Node("he", LangColor.YOU)]),
                Node("is", children=[Node("is")]),
                Node("not", children=[Node("not", LangColor.PARTICLES)]),
                Node("lost", children=[Node("lost", LangColor.VERB)]),
                Node("to me", children=[Node("to me", LangColor.GOD)]),
            ],
        )

        # text = Node(
        #     "nAvadhItamastu",
        #     children=[
        #         Node("nau"),
        #         Node(
        #             "adhItamastu",
        #             children=[
        #                 Node("adhItam"),
        #                 Node("astu"),
        #             ],
        #         ),
        #     ],
        # )

        # print(*text.strings(Language.SANSKRIT), sep="\n\n")
        # print(*text.typsts(Language.SANSKRIT), sep="\n\n")

        self.play(
            Aligned(
                sa.decompose(Language.SANSKRIT, ORIGIN + UP / SCALE * 1.5),
                sa.decompose(Language.TRANSLIT, ORIGIN),
                en.decompose(Language.ENGLISH, ORIGIN + DOWN / SCALE * 1.5),
            )
        )

        # .decompose(self, Language.SANSKRIT)

        # node1 = color_revealerV2(Language.SANSKRIT, sa)
        # node2 = color_revealerV2(Language.TRANSLIT, sa)
        # node3 = color_revealerV2(Language.ENGLISH, en)

        # node =

        # node1.bg.points.move_to(ORIGIN + UP / SCALE * 1.5)
        # node2.bg.points.move_to(ORIGIN)
        # node3.bg.points.move_to(ORIGIN + DOWN / SCALE * 1.5)
        # print("styles: " + str(node1.bg.get_available_styles()))
        # node1.bg[0].scale_descendants_stroke_radius(2)
        # gold1 = Group(*node1.bg.copy())
        # gold1 = Group(*node1.bg.copy(), color=PURE_GREEN)
        # gold1[0].scale_descendants_stroke_radius(2.0)

        # self.play(
        #     Aligned(
        #         # Write(node1.bg, at=1.0, duration=6.0),
        #         Write(node1.bg, duration=3.0),
        #         Write(node2.bg, duration=3.0),
        #         Write(node3.bg, duration=3.0),
        #     )
        # )
        # self.play(
        #     Write(node1.bg, duration=3.0),
        # )
        # n1a = node1.deconstruct_in_place()
        # n2a = node2.deconstruct_in_place(self)
        # n3a = node3.deconstruct_in_place(self)

        # self.play(Aligned(AnimGroup(n1a, n2a, n3a)))
        # self.play(Aligned(AnimGroup(n1a)))

        # self.play(Write(node1.bg, duration=6.0))
        # # self.play(Write(node1.bg))
        # self.play(Write(node2.bg, duration=6.0))
        # node.deconstruct(self)
