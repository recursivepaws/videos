from __future__ import annotations
from functools import reduce
from typing import List, LiteralString, Optional

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from janim.imports import (
    BLUE,
    DOWN,
    GREEN,
    # LEFT,
    ORIGIN,
    PURE_BLUE,
    PURE_GREEN,
    # RIGHT,
    UP,
    WHITE,
    Aligned,
    AnimGroup,
    Color,
    Config,
    FadeIn,
    FadeOut,
    Group,
    MoveToTarget,
    ShowSubitemsOneByOne,
    # Succession,
    Timeline,
    TransformMatchingShapes,
    TypstText,
    Wait,
    Write,
)
from numpy.char import join

SCALE = 2.0


class Writing:
    devanagari: LiteralString
    iast: LiteralString
    color: str

    def __init__(self, itrans: LiteralString, color: str = WHITE):
        self.devanagari = transliterate(itrans, sanscript.ITRANS, sanscript.DEVANAGARI)
        self.iast = transliterate(itrans, sanscript.ITRANS, sanscript.IAST)
        self.color = color

    def render(self, direction=DOWN):
        devanagari = Jaini(self.devanagari, self.color)
        iast = Jaini(self.iast, self.color)
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
        before: Writing,
        children: Optional[Children] = None,
        after: Optional[LiteralString] = None,
    ):
        self.before = before
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


def Jaini(text: LiteralString, color: str = WHITE, scale: Optional[float] = SCALE):
    return TypstText(
        f'#text(font: "Jaini", stroke: none, fill: rgb("{color}"))[{text}]', scale=scale
    )

    # c = a == true then 5 else 4


def aft(a, b):
    if a == b:
        return None
    else:
        return a


def color_revealer(words: List[Word]):
    before = " ".join([(lambda w: w.before)(w) for w in words])
    colored_children = [
        (lambda w: Node(before=Writing(w.before, w.color)))(w) for w in words
    ]

    return Node(before=Writing(before), children=Children(colored_children, "-"))

    after = " ".join([(lambda w: w.before)(w) for w in words])
    return external_sandhi(before, after)


def external_sandhi_v2(words: List[Word]):
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
        before=Writing(before),
        children=Children(
            [
                (lambda b, a: Node(before=Writing(b), after=aft(a, b)))(b, a)
                for (b, a) in list(zip(before.split(" "), after.split(" ")))
            ],
            "-",
        ),
        after=None,
    )


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

        words = [
            Word("tasyAhaM", "tasyAham"),
            Word("na", color=BLUE),
            Word("praNashyAmi"),
            Word("sa"),
            Word("ca"),
            Word("me"),
            Word("na"),
            Word("praNashyati"),
        ]
        # Node()
        # node1 = external_sandhi_v2(words)
        node1 = color_revealer(words)

        # node =

        node1.bg.points.move_to(ORIGIN + UP / 2.0)
        print("styles: " + str(node1.bg.get_available_styles()))
        # node1.bg[0].scale_descendants_stroke_radius(2)
        # gold1 = Group(*node1.bg.copy())
        # gold1 = Group(*node1.bg.copy(), color=PURE_GREEN)
        # gold1[0].scale_descendants_stroke_radius(2.0)

        self.play(
            Aligned(
                # Write(node1.bg, at=1.0, duration=6.0),
                Write(node1.bg, duration=6.0),
            )
        )

        self.play()

        node1.deconstruct(self)

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
