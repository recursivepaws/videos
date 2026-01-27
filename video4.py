from __future__ import annotations

# Import the necessary modules from indic_transliteration
from janim.imports import (
    DOWN,
    ORIGIN,
    UP,
    Aligned,
    Config,
    FadeOut,
    Timeline,
    TypstText,
    Wait,
    Write,
)

from framework import SCALE, Language, Node


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        node = Node(
            "sarvaM",
            children=[
                Node(
                    "sarvam",
                ),
            ],
        )

        n = Node("Where can I find God?")
        t = TypstText(n.typst_code(Language.ENGLISH), scale=SCALE)
        self.play(Write(t, duration=0.5))
        self.play(Wait(3.0))
        self.play(FadeOut(t, duration=1.0))
        # self.play(
        #     Aligned(
        #         node.decompose(Language.SANSKRIT, ORIGIN + UP),
        #         node.decompose(Language.TRANSLIT, ORIGIN + DOWN),
        #     )
        # )
