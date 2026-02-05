from __future__ import annotations
from enum import StrEnum

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from janim.imports import (
    BLUE,
    GREEN,
    ORANGE,
    PINK,
    PURPLE,
    RED,
    TEAL,
    YELLOW,
    Config,
    Timeline,
)

from framework import Declension, Node, Sloka, translit


class LC(StrEnum):
    GOD = BLUE
    VERB = PINK
    YOU = GREEN
    PARTICLES = ORANGE
    NEGATION = RED
    OBJECTS = YELLOW
    ADJECTIVES = TEAL


# saha nAvavatu . saha nau bhunaktu . saha vIryaM karavAvahai . tejasvi nAvadhItamastu mA vidviShAvahai ..
# OM shAntiH shAntiH shAntiH ..


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            "",
            sanskrit=[
                [Node("OM")],
                [
                    Node(
                        "saha nAvavatu .",
                        children=[
                            Node("saha", color=LC.PARTICLES),
                            Node(
                                "nAvavatu",
                                children=[
                                    Node("nau", color=LC.YOU),
                                    Node("avatu", color=LC.VERB),
                                ],
                            ),
                            Node("."),
                        ],
                    ),
                    Node(
                        "saha nau bhunaktu .",
                        children=[
                            Node("saha", color=LC.PARTICLES),
                            Node("nau", color=LC.YOU),
                            Node("bhunaktu", color=LC.VERB),
                            Node("."),
                        ],
                    ),
                    Node(
                        "saha vIryaM karavAvahai .",
                        children=[
                            Node("saha", color=LC.PARTICLES),
                            Node("vIryam", color=LC.ADJECTIVES),
                            Node("karavAvahai", color=LC.VERB),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        "tejasvi nAvadhItamastu mA vidviShAvahai ..",
                        children=[
                            Node("tejasvi", LC.ADJECTIVES),
                            Node(
                                "nAvadhItamastu",
                                children=[
                                    Node("nau", LC.YOU),
                                    Node("adhItam", LC.OBJECTS),
                                    Node("astu", LC.VERB),
                                ],
                            ),
                            Node(";"),
                            Node("mA", LC.PARTICLES),
                            Node("vidviShAvahai", LC.VERB),
                            Node(".."),
                        ],
                    ),
                ],
                [
                    Node(
                        "OM shAntishshAntishshAntiH ..",
                        children=[
                            Node("OM"),
                            Node("shAntish", children=[Node("shAntiH")]),
                            Node("shAntish", children=[Node("shAntiH")]),
                            Node("shAntiH"),
                            Node(".."),
                        ],
                    )
                ],
            ],
            # jagataH pitarau vande pArvatIparameshvarau..
            english=[
                [Node(translit("OM"))],
                [
                    Node(
                        "May we both be protected together.",
                        children=[
                            Node("May", color=LC.VERB),
                            Node("we both", color=LC.YOU),
                            Node("be protected", color=LC.VERB),
                            Node("together", color=LC.PARTICLES),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May we both be nourished together.",
                        children=[
                            Node("May", color=LC.VERB),
                            Node("we both", color=LC.YOU),
                            Node("be nourished", color=LC.VERB),
                            Node("together", color=LC.PARTICLES),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May we both work vigorously together.",
                        children=[
                            Node("May we both work", color=LC.VERB),
                            Node("vigorously", color=LC.ADJECTIVES),
                            Node("together", color=LC.PARTICLES),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        "May both our study be brilliant;#linebreak()may we both not be hateful.",
                        children=[
                            Node("May", LC.VERB),
                            Node("both our", LC.YOU),
                            Node("study", LC.OBJECTS),
                            Node("be", LC.VERB),
                            Node("brilliant", LC.ADJECTIVES),
                            Node(";#linebreak()"),
                            Node("may we both", LC.VERB),
                            Node("not", LC.PARTICLES),
                            Node("be hateful", LC.VERB),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May our study be brilliant.",
                        children=[],
                    ),
                ],
                [
                    Node(
                        f"{translit('OM')}, peace, peace, peace.",
                        children=[
                            Node(f"{translit('OM')}"),
                            Node(","),
                            Node("peace"),
                            Node(","),
                            Node("peace"),
                            Node(","),
                            Node("peace"),
                            Node("."),
                        ],
                    ),
                ],
            ],
        )

        self.play(sloka.teach())
