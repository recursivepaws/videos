from dataclasses import dataclass
from typing import List

from nirukta.models import Line, Utterance

from janim.imports import GREEN, Timeline
from nirukta.timelines.utterance import UtteranceTimeline


@dataclass
class LineTimeline(Timeline):
    vAkyAni: List[Utterance]

    def __init__(self, line: Line):
        super().__init__()
        self.vAkyAni = line.vAkyAni

    @property
    def gui_name(self) -> str:
        return " | ".join(vAkya.english for vAkya in self.vAkyAni)

    @property
    def gui_color(self) -> str:
        return GREEN

    def construct(self):
        # When doing translation pages we do an utterance at a time rather
        # than a line at a time.
        for vAkya in self.vAkyAni:
            vt = UtteranceTimeline(vAkya).build().to_item().show()
            self.forward_to(vt.end)
