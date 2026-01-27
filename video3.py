from __future__ import annotations

# Import the necessary modules from indic_transliteration
from janim.imports import (
    Config,
    Timeline,
)

from framework import LangColor, Node, Sloka

# vAgarthAviva sampruktau vAgarthapratipattaye
# jagataH pitarau vande pArvatIparameshvarau

# vAgarthAviva saMpR^iktau vAgarthapratipattaye.
# jagataH pitarau vande pArvatIparameshvarau..


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        sloka = Sloka(
            [
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
            [
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
        )
        sloka.teach(self)
