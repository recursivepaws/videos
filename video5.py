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

from framework import Citation, Language, Node, Sloka, translit  # noqa: E402


class LC(StrEnum):
    GOD = BLUE
    VERB = PINK
    YOU = GREEN
    PARTICLES = ORANGE
    NEGATION = RED
    OBJECTS = YELLOW
    ADJECTIVES = TEAL


# A~NgikaM bhuvanaM yasya vAchikaM sarvavA~Nmayam .
# AhAryaM chandratArAdi taM numaH sAttvikaM shivam ..

# abhinayadarpaNe 1


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            Citation("(abhinayadarpaNe 1)", Language.SANSKRIT),
            sanskrit=[
                [
                    Node(
                        "A~NgikaM bhuvanaM yasya",
                        children=[
                            Node("A~Ngikam", LC.ADJECTIVES, delay=1),
                            Node("bhuvanam", LC.OBJECTS, delay=1),
                            Node("yasya", LC.YOU, delay=1),
                        ],
                    ),
                    Node(
                        "vAchikaM sarvavA~Nmayam .",
                        children=[
                            Node("vAchikam", LC.ADJECTIVES, delay=2),
                            Node(
                                "sarvavA~Nmayam",
                                children=[
                                    Node("sarva", LC.YOU, delay=1),
                                    Node("vAc", LC.PARTICLES, delay=1),
                                    Node("mayam", LC.OBJECTS, delay=1),
                                ],
                            ),
                            Node("."),
                        ],
                    ),
                ],
                [
                    Node(
                        "AhAryaM chandratArAdi",
                        children=[
                            Node("AhAryam", LC.ADJECTIVES, delay=2),
                            Node(
                                "chandratArAdi",
                                children=[
                                    Node("chandra", LC.YOU, delay=1),
                                    Node("tArA", LC.OBJECTS, delay=1),
                                    Node("Adi", LC.PARTICLES, delay=1),
                                ],
                            ),
                        ],
                    ),
                    Node(
                        "taM numaH sAttvikaM shivam ..",
                        children=[
                            Node("tam", LC.YOU, delay=1),
                            Node("numaH", LC.VERB, delay=1),
                            Node("sAttvikam", LC.ADJECTIVES, delay=1),
                            Node("shivam", LC.GOD, delay=1),
                            Node(".."),
                        ],
                    ),
                ],
            ],
            english=[
                [
                    Node(
                        "Whose bodily expression is#linebreak()the universe,",
                        children=[
                            Node("Whose", LC.YOU, delay=2),
                            Node("bodily expression", LC.ADJECTIVES, delay=2),
                            Node("is"),
                            Node("#linebreak()"),
                            Node("the universe", LC.OBJECTS, delay=2),
                            Node(","),
                        ],
                    ),
                    Node(
                        "Whose verbal expression is#linebreak()everything made of speech,",
                        children=[
                            Node("Whose"),
                            Node("verbal expression", LC.ADJECTIVES, delay=3),
                            Node("is"),
                            Node("#linebreak()"),
                            Node("everything", LC.YOU, delay=3),
                            Node("made of", LC.PARTICLES, delay=3),
                            Node("speech", LC.OBJECTS, delay=3),
                            Node(","),
                        ],
                    ),
                ],
                [
                    Node(
                        "Whose ornamental expression is#linebreak()the moon, the stars, etc.",
                        children=[
                            Node("Whose"),
                            Node("ornamental expression", LC.ADJECTIVES, delay=3),
                            Node("is"),
                            Node("#linebreak()"),
                            Node("the moon", LC.YOU, delay=3),
                            Node(","),
                            Node("the stars", LC.OBJECTS, delay=3),
                            Node(","),
                            Node("etc.", LC.PARTICLES, delay=3),
                        ],
                    ),
                    Node(
                        f"We bow to that pure lord {translit('shiva')}.",
                        children=[
                            Node("We bow", LC.VERB, delay=2),
                            Node("to", delay=2),
                            Node("that", LC.YOU, delay=2),
                            Node("pure", LC.ADJECTIVES, delay=2),
                            Node(f"lord {translit('shiva')}", LC.GOD, delay=2),
                            Node("."),
                        ],
                    ),
                ],
            ],
        )

        self.play(sloka.teach())
