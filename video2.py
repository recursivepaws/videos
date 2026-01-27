from __future__ import annotations

# Import the necessary modules from indic_transliteration
from janim.imports import (
    Config,
    Timeline,
)

from framework import LangColor, Node, Sloka


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            "BG 6.30",
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
                            Node("na", children=[Node("na", LangColor.NEGATION)]),
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
                            Node("na", children=[Node("na", LangColor.NEGATION)]),
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
                        "to him, I am not lost",
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
                            Node("not", children=[Node("not", LangColor.NEGATION)]),
                            Node("lost", children=[Node("lost", LangColor.VERB)]),
                        ],
                    ),
                    Node(
                        "and he is not lost to me",
                        children=[
                            Node("and", children=[Node("and", LangColor.PARTICLES)]),
                            Node("he", children=[Node("he", LangColor.YOU)]),
                            Node("is", children=[Node("is")]),
                            Node("not", children=[Node("not", LangColor.NEGATION)]),
                            Node("lost", children=[Node("lost", LangColor.VERB)]),
                            Node("to me", children=[Node("to me", LangColor.GOD)]),
                        ],
                    ),
                ],
            ],
        )
        sloka.teach(self)
