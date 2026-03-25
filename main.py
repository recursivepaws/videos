import importlib
from janim.imports import Config, Timeline
import glob
import os

import typst
import janim.utils.typst_compile as tc
import parser

from parser import NiruktaFile, SutraFile, parse_sloka, SlokaFile, parse_sutra

importlib.reload(parser)

font_dir = os.path.join(os.path.dirname(__file__), "fonts")
tc._typst_fonts = typst.Fonts(True, True, [font_dir])


def is_nirukta_file(file: str):
    return ".sloka" in file or ".sutra" in file


def get_nirukta_file() -> str:
    cached = os.environ.get("JANIM_SLOKA_FILE")
    if cached:
        return cached

    prefix = "./blueprints"

    end_loop = False

    while not end_loop:
        nirukta_files = []
        nirukta_files += sorted(glob.glob(f"{prefix}/**/"))
        nirukta_files += sorted(glob.glob(f"{prefix}/*.sloka"))
        nirukta_files += sorted(glob.glob(f"{prefix}/*.sutra"))
        if not nirukta_files:
            print(f"No nirukta files found in {prefix}")
            exit(1)

        print("Select a sloka file or nested folder:")
        for i, path in enumerate(nirukta_files):
            name = os.path.basename(path)
            dir = os.path.dirname(path).removeprefix(prefix)
            print(f"  [{i + 1}] {name if is_nirukta_file(name) else dir}")

        selection = input("\nEnter number or filename: ").strip()

        if selection.isdigit():
            index = int(selection) - 1
            if not (0 <= index < len(nirukta_files)):
                print(f"Invalid selection: {selection}")
                exit(1)
            chosen = nirukta_files[index]
        else:
            raise ValueError("Select valid index")

        if is_nirukta_file(chosen):
            end_loop = True
        else:
            prefix = chosen

    os.environ["JANIM_SLOKA_FILE"] = chosen
    return chosen


chosen = get_nirukta_file()


print(f"Loading {chosen}...")

with open(chosen) as f:
    source = f.read()


if ".sutra" in chosen:
    nirukta = parse_sutra(source)
else:
    nirukta = parse_sloka(source)


class SlokaTime(Timeline):
    CONFIG = Config(fps=60)

    def construct(self):
        self.play(nirukta.teach())
        self.forward()
