from typing import List

from janim.imports import YELLOW, Succession, Timeline
from nirukta.models import Line
from nirukta.timelines.line import LineTimeline


class ExplainSloka(Timeline):
    lines: List[Line]

    def __init__(self, lines: List[Line]):
        super().__init__()
        self.lines = lines

    @property
    def gui_color(self) -> str:
        return YELLOW

    def construct(self):
        animations = []
        for line in self.lines:
            line_timeline = LineTimeline(line).build().to_item()
            line_timeline.show()
            self.forward_to(line_timeline.end)
        self.play(Succession(*animations))
