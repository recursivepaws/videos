from __future__ import annotations

# Import the necessary modules from indic_transliteration
from indic_transliteration import sanscript
from janim.imports import (
    BLUE,
    PURPLE,
    RED,
    Config,
    Timeline,
)

from framework import Citation, Declension, LangColor, Language, Node, Sloka, translit

# vAgarthAviva saMpR^iktau vAgarthapratipattaye.
# jagataH pitarau vande pArvatIparameshvarau..


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            Citation("", Language.ENGLISH),
            sanskrit=[
                [
                    Node(
                        "vAgarthAviva saMpR^iktau vAgarthapratipattaye",
                        children=[
                            Node(
                                "vAgarthAviva",
                                children=[
                                    Node(
                                        "vAgarthau",
                                        children=[Node("vAk"), Node("artha")],
                                    ),
                                    Node("iva"),
                                ],
                            ),
                            Node("saMpR^iktau"),
                            Node(
                                "vAgarthapratipattaye",
                                children=[Node("vAgartha"), Node("pratipattaye")],
                            ),
                        ],
                    ),
                ],
                [
                    Node(
                        "jagataH pitarau vande pArvatIparameshvarau",
                        children=[
                            Node("jagataH"),
                            Node("pitarau"),
                            Node("vande"),
                            Node(
                                "pArvaItparameshvarau",
                                children=[Node("pArvatI"), Node("parameshvara")],
                            ),
                        ],
                    )
                ],
            ],
            # jagataH pitarau vande pArvatIparameshvarau..
            english=[
                [
                    Node(
                        "like a word joined with its meaning, to attain "
                        "vAgarthAviva saMpR^iktau vAgarthapratipattaye",
                        children=[
                            Node(
                                "vAgarthAviva",
                                children=[
                                    Node(
                                        "vAgarthau",
                                        children=[Node("vAk"), Node("artha")],
                                    ),
                                    Node("iva"),
                                ],
                            ),
                            Node("saMpR^iktau"),
                            Node(
                                "vAgarthapratipattaye",
                                children=[Node("vAgartha"), Node("pratipattaye")],
                            ),
                        ],
                    ),
                ],
                [
                    Node(
                        f"I bow to the two parents of the world, {translit('pArvatI')} and {translit('shiva')}",
                        children=[
                            Node("I bow"),
                            Node("to"),
                            Node("the two parents", declension=Declension.ACC),
                            Node("of the world"),
                            Node("vande"),
                            Node(
                                f"{translit('pArvatI')} and {translit('shiva')}",
                                children=[
                                    Node(translit("pArvatI"), color=RED),
                                    Node(translit("shiva"), color=BLUE),
                                ],
                                color=PURPLE,
                            ),
                        ],
                    )
                ],
            ],
        )

        self.play(sloka.teach())
