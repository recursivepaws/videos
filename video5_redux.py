from janim.imports import Config, Timeline
from parser import parse, Sloka

with open("video5.sloka") as f:
    source = f.read()

sloka: Sloka = parse(source)
print(sloka)


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        self.play(sloka.teach())
