from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from operator import add
from tkinter import BOTTOM
from typing import List, LiteralString, Optional
from enum import Enum

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from janim.imports import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    ORANGE,
    # LEFT,
    ORIGIN,
    PINK,
    PURE_BLUE,
    PURE_GREEN,
    RED,
    RIGHT,
    # RIGHT,
    UP,
    WHITE,
    YELLOW,
    Aligned,
    AnimGroup,
    Color,
    Config,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Item,
    MoveToTarget,
    ShowSubitemsOneByOne,
    Succession,
    # Succession,
    Timeline,
    TransformMatchingShapes,
    Triangle,
    TypstText,
    Wait,
    Write,
)
from numpy.char import join

SCALE = 1.5


class Language(Enum):
    ENGLISH = 1
    SANSKRIT = 2
    TRANSLIT = 3


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

    # Get the typst code for the text
    def typst_code(self, language: Language):
        match language:
            case Language.ENGLISH:
                return Junicode(self.text, self.color)
            case Language.TRANSLIT:
                iast = transliterate(self.text, sanscript.ITRANS, sanscript.IAST)
                return Junicode(iast, self.color)
            case Language.SANSKRIT:
                deva = transliterate(self.text, sanscript.ITRANS, sanscript.DEVANAGARI)
                return Junicode(deva, self.color)

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

    def decompose(self, j: Timeline, language: Language):
        states = [
            (lambda s: TypstText(s, scale=SCALE))(s) for s in self.strings(language)
        ]

        current = states.pop(0)
        j.play(Write(current, duration=3.0))

        for state in states:
            j.play(TransformMatchingShapes(current, state, duration=1.0))
            current = state


class Sloka:
    lines: List[Node]

    def __init__(self, lines):
        self.lines = lines


def Junicode(text: str, color: str = WHITE):
    return f'#text(font: "Junicode", stroke: none, fill: rgb("{color}"))[{text}]'


def Jaini(text: str, color: str = WHITE):
    return f'#text(font: "Jaini", stroke: none, fill: rgb("{color}"))[{text}]'


def aft(a, b):
    if a == b:
        return None
    else:
        return a


class SlokaTime(Timeline):
    # CONFIG = Config(fps=60, background_color=Color(PURE_GREEN))

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

        # He who sees me everywhere and sees all things in me- to him I am not lost, nor is he lost to me

        # Node()
        # node1 = external_sandhi_v2(words)
        sa = Node(
            "tasyAhaM na praNashyAmi sa ca me na praNashyAmi",
            children=[
                Node("tasyAhaM", children=[Node("tasya", GREEN), Node("aham", BLUE)]),
                Node("na", children=[Node("na", RED)]),
                Node("praNashyAmi", children=[Node("praNashyAmi", PINK)]),
                Node("sa", children=[Node("sa", YELLOW)]),
                Node("ca", children=[Node("ca", ORANGE)]),
                Node("me", children=[Node("me", GREEN)]),
                Node("na", children=[Node("na", RED)]),
                Node("praNashyati", children=[Node("praNashyati", PINK)]),
            ],
        )

        en = Node(
            "to him, I am not liost, and he is not lost to me",
            children=[
                Node(
                    "to him, I",
                    children=[Node("to him", GREEN), Node(","), Node("I", BLUE)],
                ),
                Node("am", children=[Node("am")]),
                Node("not", children=[Node("not", RED)]),
                Node("lost", children=[Node("lost", PINK)]),
                Node(",", children=[Node(",")]),
                Node("and", children=[Node("and", ORANGE)]),
                Node("he", children=[Node("he", YELLOW)]),
                Node("is", children=[Node("is")]),
                Node("not", children=[Node("not", RED)]),
                Node("lost", children=[Node("lost", PINK)]),
                Node("to me", children=[Node("to me", GREEN)]),
            ],
        )
        text = Node(
            "nAvadhItamastu",
            children=[
                Node("nau"),
                Node(
                    "adhItamastu",
                    children=[
                        Node("adhItam"),
                        Node("astu"),
                    ],
                ),
            ],
        )

        print(*text.strings(Language.SANSKRIT), sep="\n\n")
        sa.decompose(self, Language.SANSKRIT)

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
