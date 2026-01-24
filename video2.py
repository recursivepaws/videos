from __future__ import annotations
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


class Writing:
    text: str
    # english: Optional[LiteralString]
    # devanagari: Optional[LiteralString]
    # iast: Optional[LiteralString]
    color: str

    def __init__(self, text: str, color: str = WHITE):
        self.text = text
        self.color = color
        # if language == Language.ENGLISH:
        #     self.english = text
        # else:
        #     self.devanagari = transliterate(
        #         text, sanscript.ITRANS, sanscript.DEVANAGARI
        #     )
        # self.iast = transliterate(text, sanscript.ITRANS, sanscript.IAST)

    def render(self, language: Language, direction=DOWN):
        group = None
        if language == Language.ENGLISH:
            group = Group(Junicode(self.text, self.color))
        if language == Language.TRANSLIT:
            iast = transliterate(self.text, sanscript.ITRANS, sanscript.IAST)
            group = Group(Junicode(iast, self.color))
        if language == language.SANSKRIT:
            iast = transliterate(self.text, sanscript.ITRANS, sanscript.DEVANAGARI)
            group = Group(Jaini(iast, self.color))

        if group is not None:
            # group.points.arrange(direction)
            return group
        else:
            return Group[TypstText]()


class Children:
    nodes: List[Node]
    delimiter: LiteralString

    def __init__(self, nodes: List[Node], delimiter: LiteralString = ""):
        self.nodes = nodes
        self.delimiter = delimiter


class Node:
    language: Language
    before: Writing
    children: Optional[Children]
    after: Optional[Writing]

    bg: Group[TypstText]
    ag: Optional[Group[TypstText]]

    def __init__(
        self,
        language: Language,
        before: Writing,
        children: Optional[Children] = None,
        after: Optional[Writing] = None,
    ):
        self.language = language
        self.before = before
        self.children = children

        if after is None:
            self.after = after
            self.ag = None
        else:
            self.after = after
            self.ag = self.after.render(self.language)

        self.bg = self.before.render(self.language)

    # def initialize(self, j: Timeline):
    #     word = self.before.render()
    #     self.group = word
    def morph(self):
        if self.bg is not None and self.ag is not None:
            # self.bg.points.move_to(self.ag)
            # self.ag.points.align_to(self.bg, DOWN)
            return TransformMatchingShapes(self.bg, self.ag, duration=1.0)

    def safe_ag(self):
        if self.ag is None:
            return self.bg
        else:
            return self.ag

    def children_as_node(self):
        new = []
        if self.children is not None:
            for child in self.children.nodes:
                new.append(Node(self.language, child.before, child.children))

        # return (language, )

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

    def deconstruct_in_place(self, j: Timeline):
        # Render the parent if required
        if self.children is not None:
            self.bg.generate_target()
            # Create a group of the components
            # before_children = [
            #     (lambda child: child.bg)(node) for node in self.children.nodes
            # ]
            # for b of befo
            before_children = Group()
            after_children = Group()
            for node in self.children.nodes:
                for item in node.bg:
                    before_children.add(item)
                for item in node.safe_ag():
                    after_children.add(item)

            # before_children = reduce(add, before_children, [])

            # after_children = Group()
            #     *[
            #         (lambda child: child.safe_ag())(node)
            #         for node in self.children.nodes
            #     ],
            # )
            # for node in self.children.

            # Create a group of the full equation
            equation = Group()

            for i in range(len(after_children)):
                bg = before_children[i]
                ag = after_children[i]

                # for t in ag:
                #     t.
                # ag.points.move_to_by_indicator(bg, ag)

                if ag is not None:
                    # ag.points.align_to(self.bg, DOWN)
                    # ag.points.move_to(self.bg)
                    equation.add(ag)
                else:
                    # bg.points.align_to(self.bg, DOWN)
                    # bg.points.move_to(self.bg)
                    equation.add(bg)

            # equation.points.match_pattern()
            equation.points.arrange(direction=RIGHT, center=True, aligned_edge=DOWN)
            # equation.points.arrange(aligned_edge=DOWN)
            # equation.points.arrange_in_grid(
            #     n_rows=1, aligned_edge=DOWN, h_buff=1, by_center_point=True
            # )
            equation.points.move_to(self.bg.target)

            # Precreate the morph animations
            animations = []
            for node in self.children.nodes:
                if node.ag is not None:
                    animations.append(node.morph())

            # animation = Aligned(*animations)
            # if len(animations) > 0:
            #     animation = Aligned(*animations)
            # else:
            #     animation = None)
            # j.play(
            # )
            animation = TransformMatchingShapes(self.bg, before_children, duration=1.0)
            # animation = Write(before_children)

            # Determine if any of the nodes in the components also have children
            children_exist = reduce(
                lambda x, y: x or y,
                [(lambda c: c.children is not None)(n) for n in self.children.nodes],
            )

            child_animations = []
            if children_exist:
                # Recurse
                for component in self.children.nodes:
                    if component.children is not None:
                        child_animations.append(component.deconstruct_in_place(j))

            if len(child_animations) > 0:
                return Succession(
                    AnimGroup(animation, Aligned(*child_animations), offset=1.0)
                )
            else:
                return animation
        else:
            # Empty anim
            return AnimGroup()
            # else:
            #     # Otherwise fade out
            #     j.play(
            #         AnimGroup(FadeOut(self.bg), FadeOut(equation)),
            #     )


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
    before: Writing
    children: List[Writing]

    def __init__(self, before: Writing, children: List[Writing] = []):
        self.before = before
        self.children = children

    # def safe_after(self):
    #     if self.after is None:
    #         return self.before
    #     else:
    #         return self.after


class WordOld:
    before: LiteralString
    after: Optional[LiteralString]
    color: str

    def __init__(self, before, after=None, color=WHITE):
        self.before = before
        self.after = after
        self.color = color

    def safe_after(self):
        if self.after is None:
            return self.before
        else:
            return self.after


def Junicode(text: str, color: str = WHITE, scale: Optional[float] = SCALE):
    return TypstText(
        f'#text(font: "Junicode", stroke: none, fill: rgb("{color}"))[{text}]',
        scale=scale,
    )


def Jaini(text: str, color: str = WHITE, scale: Optional[float] = SCALE):
    return TypstText(
        f'#text(font: "Jaini", stroke: none, fill: rgb("{color}"))[{text}]', scale=scale
    )

    # c = a == true then 5 else 4


def aft(a, b):
    if a == b:
        return None
    else:
        return a


def color_revealer(language: Language, words: List[WordOld]):
    before = " ".join([(lambda w: w.before)(w) for w in words])
    colored_children = [
        (lambda w: Node(language, before=Writing(w.before, w.color)))(w) for w in words
    ]

    return Node(language, before=Writing(before), children=Children(colored_children))


def color_revealerV2(language: Language, words: List[Word]):
    def word_to_node(word: Word):
        if len(word.children) > 0:
            children = Children(
                [
                    (lambda c: word_to_node(Word(Writing(c.text, c.color))))(c)
                    for c in word.children
                ]
            )
            return Node(language, word.before, children)
        else:
            return Node(language, word.before)

    before = str(" ").join([(lambda w: w.before.text)(w) for w in words])

    return Node(
        language,
        Writing(before),
        Children([(lambda w: word_to_node(w))(w) for w in words]),
    )


""" def external_sandhi_v2(words: List[Word]):
    before = " ".join([(lambda w: w.before)(w) for w in words])
    after = " ".join([(lambda w: w.safe_after())(w) for w in words])
    return external_sandhi(before, after) """


""" def external_sandhi(before: LiteralString, after: LiteralString):
    def aft(a, b):
        if a == b:
            return None
        else:
            return a

    return Node(
        before=Writing(before),
        children=Children(
            [
                (lambda b, a: Node(before=Writing(b), after=aft(a, b)))(b, a)
                for (b, a) in list(zip(before.split(" "), after.split(" ")))
            ],
            "-",
        ),
        after=None,
    ) """


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

        # node1 = external_sandhi(
        #     "yo mAM pashyati sarvatra sarvaM cha mayi pashyati ।",
        #     "yo mAm pashyati sarvatra sarvam cha mayi pashyati",
        # )
        # node2 = external_sandhi(
        #     "tasyAhaM na praNashyAmi sa ca me na praNashyati ।।",
        #     "tasyAham na praNashyAmi sa ca me na praNashyati",
        # )

        sloka = [
            [
                WordOld("yo"),
                WordOld("mAM", "mAm"),
                WordOld("pashyati"),
                WordOld("sarvatra"),
                WordOld("sarvaM", "sarvam"),
                WordOld("cha"),
                WordOld("mayi"),
                WordOld("pashyati"),
            ],
            [
                WordOld("tasyAhaM", "tasya-aham"),
                WordOld("na", color=BLUE),
                WordOld("praNashyAmi"),
                WordOld("sa"),
                WordOld("ca"),
                WordOld("me"),
                WordOld("na"),
                WordOld("praNashyati"),
            ],
        ]

        """ sloka = [
            [
                Word("He who"),
                Word("sees"),
                Word("me"),
                Word("everywhere"),
                Word("and"),
                Word("sees"),
                Word("all things"),
                Word("in me;"),
            ],
            [
                Word("to him"),
                Word("I am", color=BLUE),
                Word("not"),
                Word("lost"),
                Word("ca"),
                Word("me"),
                Word("na"),
                Word("praNashyati"),
            ],
        ] """

        # He who sees me everywhere and sees all things in me- to him I am not lost, nor is he lost to me

        # verbs: pink
        # pronouns:

        # Node()
        # node1 = external_sandhi_v2(words)
        sa = [
            Word(Writing("tasyAhaM"), [Writing("tasya", GREEN), Writing("aham", BLUE)]),
            Word(Writing("na"), [Writing("na", RED)]),
            Word(Writing("praNashyAmi"), [Writing("praNashyAmi", PINK)]),
            Word(Writing("sa"), [Writing("sa", YELLOW)]),
            Word(Writing("ca"), [Writing("ca", ORANGE)]),
            Word(Writing("me"), [Writing("me", GREEN)]),
            Word(Writing("na"), [Writing("na", RED)]),
            Word(Writing("praNashyati"), [Writing("praNashyati", PINK)]),
        ]

        en = [
            Word(
                Writing("to him, I"),
                [Writing("to him", GREEN), Writing(","), Writing("I", BLUE)],
            ),
            Word(Writing("am"), [Writing("am")]),
            Word(Writing("not"), [Writing("not", RED)]),
            Word(Writing("lost"), [Writing("lost", PINK)]),
            Word(Writing(","), [Writing(",")]),
            Word(Writing("and"), [Writing("and", ORANGE)]),
            Word(Writing("he"), [Writing("he", YELLOW)]),
            Word(Writing("is"), [Writing("is")]),
            Word(Writing("not"), [Writing("not", RED)]),
            Word(Writing("lost"), [Writing("lost", PINK)]),
            Word(Writing("to me"), [Writing("to me", GREEN)]),
        ]

        node1 = color_revealerV2(Language.SANSKRIT, sa)
        node2 = color_revealerV2(Language.TRANSLIT, sa)
        node3 = color_revealerV2(Language.ENGLISH, en)

        # node =

        node1.bg.points.move_to(ORIGIN + UP / SCALE * 1.5)
        node2.bg.points.move_to(ORIGIN)
        node3.bg.points.move_to(ORIGIN + DOWN / SCALE * 1.5)
        print("styles: " + str(node1.bg.get_available_styles()))
        # node1.bg[0].scale_descendants_stroke_radius(2)
        # gold1 = Group(*node1.bg.copy())
        # gold1 = Group(*node1.bg.copy(), color=PURE_GREEN)
        # gold1[0].scale_descendants_stroke_radius(2.0)

        self.play(
            Aligned(
                # Write(node1.bg, at=1.0, duration=6.0),
                Write(node1.bg, duration=3.0),
                Write(node2.bg, duration=3.0),
                Write(node3.bg, duration=3.0),
            )
        )

        n1a = node1.deconstruct_in_place(self)
        n2a = node2.deconstruct_in_place(self)
        n3a = node3.deconstruct_in_place(self)

        self.play(Aligned(AnimGroup(n1a, n2a, n3a)))

        """ node2.bg.points.move_to(ORIGIN + DOWN / 2.0)
        # gold2 = Group(*node2.bg.copy(), color=PURE_GREEN)
        gold2 = Group(*node2.bg.copy())
        # gold2[0].scale_descendants_stroke_radius(2.0)

        self.play(
            Aligned(
                # Write(node2.bg, at=1.0, duration=6.0),
                Write(gold2, duration=6.0),
            )
        )

        self.play(Wait(duration=10.0)) """

        # self.play(Write(node1.bg, duration=6.0))
        # # self.play(Write(node1.bg))
        # self.play(Write(node2.bg, duration=6.0))
        # node.deconstruct(self)
