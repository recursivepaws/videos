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
    YELLOW,
    Config,
    Timeline,
)

from framework import Declension, Node, Sloka, translit


class LangColor(StrEnum):
    GOD = BLUE
    VERB = PINK
    YOU = GREEN
    PARTICLES = ORANGE
    NEGATION = RED
    OBJECTS = YELLOW


# saha nAvavatu . saha nau bhunaktu . saha vIryaM karavAvahai . tejasvi nAvadhItamastu mA vidviShAvahai ..
# OM shAntiH shAntiH shAntiH ..


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            "",
            sanskrit=[
                [
                    Node(
                        "OM saha nAvavatu .",
                        children=[
                            Node("OM"),
                            Node("saha", color=LangColor.PARTICLES),
                            Node(
                                "nAvavatu",
                                children=[
                                    Node("nau", color=LangColor.YOU),
                                    Node("avatu", color=LangColor.VERB),
                                ],
                            ),
                            Node("."),
                        ],
                    ),
                    Node(
                        "saha nau bhunaktu .",
                        children=[
                            Node(
                                "saha",
                            ),
                            Node("nau", color=BLUE),
                            Node("bhunaktu"),
                            Node("."),
                        ],
                    ),
                    Node(
                        "saha vIryaM karavAvahai .",
                        children=[
                            Node("saha"),
                            Node("vIryaM"),
                            Node("karavAvahai"),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        "tejasvi nAvadhItamastu mA vidviShAvahai ..",
                        children=[
                            Node("tejasvi"),
                            Node(
                                "nAvadhItamastu",
                                children=[
                                    Node("nau"),
                                    Node("adhItam"),
                                    Node("astu"),
                                ],
                            ),
                            Node("mA"),
                            Node("vidviShAvahai"),
                            Node(".."),
                        ],
                    ),
                ],
                [
                    Node(
                        "OM shAntiH shAntiH shAntiH ..",
                        children=[
                            Node("OM"),
                            Node("shAntiH"),
                            Node("shAntiH"),
                            Node("shAntiH"),
                            Node(".."),
                        ],
                    )
                ],
            ],
            # jagataH pitarau vande pArvatIparameshvarau..
            english=[
                [
                    Node(
                        f"{translit('OM')}; May [it] protect us both together.",
                        children=[
                            Node(translit("OM")),
                            Node(";"),
                            Node("May", color=LangColor.VERB),
                            Node("[it]", color=LangColor.GOD),
                            Node("protect", color=LangColor.VERB),
                            Node("us both", color=LangColor.YOU),
                            Node("together", color=LangColor.PARTICLES),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May the both of us be nourished together.",
                        children=[
                            Node("May", color=LangColor.VERB),
                            Node("the both of us", color=LangColor.YOU),
                            Node("be nourished", color=LangColor.VERB),
                            Node("together", color=LangColor.PARTICLES),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May we work vigorously together.",
                        children=[],
                    ),
                ],
                [
                    Node(
                        "May our study be brilliant.",
                        children=[],
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
                            Node("peace,"),
                            Node("peace,"),
                            Node("peace,"),
                        ],
                    ),
                ],
            ],
        )

        self.play(sloka.teach())
