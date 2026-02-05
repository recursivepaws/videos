from __future__ import annotations

import importlib
from enum import StrEnum

# Import the necessary modules from indic_transliteration
from janim.imports import (
    BLUE,
    GREEN,
    ORANGE,
    PINK,
    RED,
    TEAL,
    YELLOW,
    Config,
    Timeline,
)

import framework

importlib.reload(framework)

from framework import Node, Sloka, translit  # noqa: E402


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
                [Node("OM", LC.GOD, delay=1)],
                [
                    Node(
                        "saha nAvavatu .",
                        children=[
                            Node(
                                "saha",
                                LC.PARTICLES,
                                delay=2,
                            ),
                            Node(
                                "nAvavatu",
                                children=[
                                    Node("nau", LC.YOU, delay=1),
                                    Node("avatu", LC.VERB, delay=1),
                                ],
                            ),
                            Node("."),
                        ],
                    ),
                    Node(
                        "saha nau bhunaktu .",
                        children=[
                            Node("saha", LC.PARTICLES, delay=1),
                            Node("nau", LC.YOU, delay=1),
                            Node("bhunaktu", LC.VERB, delay=1),
                            Node("."),
                        ],
                    ),
                    Node(
                        "saha vIryaM karavAvahai .",
                        children=[
                            Node("saha", color=LC.PARTICLES, delay=1),
                            Node("vIryam", color=LC.ADJECTIVES, delay=1),
                            Node("karavAvahai", color=LC.VERB, delay=1),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        "tejasvi nAvadhItamastu mA vidviShAvahai ..",
                        children=[
                            Node("tejasvi", LC.ADJECTIVES, delay=2),
                            Node(
                                "nAvadhItamastu",
                                children=[
                                    Node("nau", LC.YOU, delay=1),
                                    Node("adhItam", LC.OBJECTS, delay=1),
                                    Node("astu", LC.VERB, delay=1),
                                ],
                            ),
                            Node(";"),
                            Node("mA", LC.PARTICLES, delay=2),
                            Node("vidviShAvahai", LC.VERB, delay=2),
                            Node(".."),
                        ],
                    ),
                ],
                [
                    Node(
                        "OM shAntishshAntishshAntiH ..",
                        children=[
                            Node("OM", LC.GOD, delay=2),
                            Node(
                                "shAntish",
                                children=[Node("shAntiH", LC.OBJECTS, delay=1)],
                            ),
                            Node(
                                "shAntish",
                                children=[Node("shAntiH", LC.OBJECTS, delay=1)],
                            ),
                            Node("shAntiH", LC.OBJECTS, delay=2),
                            Node(".."),
                        ],
                    )
                ],
            ],
            # jagataH pitarau vande pArvatIparameshvarau..
            english=[
                [Node(translit("OM"), LC.GOD, delay=1)],
                [
                    Node(
                        "May we both be protected together.",
                        children=[
                            Node("May", LC.VERB, delay=2),
                            Node("we both", LC.YOU, delay=2),
                            Node("be protected", LC.VERB, delay=2),
                            Node("together", LC.PARTICLES, delay=2),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May we both be nourished together.",
                        children=[
                            Node("May", LC.VERB, delay=1),
                            Node("we both", LC.YOU, delay=1),
                            Node("be nourished", LC.VERB, delay=1),
                            Node("together", LC.PARTICLES, delay=1),
                            Node("."),
                        ],
                    ),
                    Node(
                        "May we both work vigorously together.",
                        children=[
                            Node("May we both work", LC.VERB, delay=1),
                            Node("vigorously", LC.ADJECTIVES, delay=1),
                            Node("together", LC.PARTICLES, delay=1),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        "May both our study be brilliant;#linebreak()may we both not be hateful.",
                        children=[
                            Node("May", LC.VERB, delay=2),
                            Node("both our", LC.YOU, delay=2),
                            Node("study", LC.OBJECTS, delay=2),
                            Node("be", LC.VERB, delay=2),
                            Node("brilliant", LC.ADJECTIVES, delay=2),
                            Node(";#linebreak()"),
                            Node("may we both", LC.VERB, delay=2),
                            Node("not", LC.PARTICLES, delay=2),
                            Node("be hateful", LC.VERB, delay=2),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        f"{translit('OM')}, peace, peace, peace.",
                        children=[
                            Node(f"{translit('OM')}", LC.GOD, delay=2),
                            Node(","),
                            Node("peace", LC.OBJECTS, delay=2),
                            Node(","),
                            Node("peace", LC.OBJECTS, delay=2),
                            Node(","),
                            Node("peace", LC.OBJECTS, delay=2),
                            Node("."),
                        ],
                    ),
                ],
            ],
        )

        self.play(sloka.teach())
