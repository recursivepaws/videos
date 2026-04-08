import os
import glob
from janim.imports import WHITE
from aksharamukha import transliterate

from nirukta.models.enums import Language
from nirukta.parsing import parse_sloka, parse_sutra
from nirukta.constants import SCALE, TYPST_CMD_RE
from nirukta.timelines import SlokaFileTimeline, SutraFileTimeline


def is_nirukta_file(file: str):
    return ".sloka" in file or ".sutra" in file


def choose_nirukta_file() -> str:
    cached = os.environ.get("NIRUKTA_FILE")
    if cached:
        return cached

    prefix = "./library"

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

    os.environ["NIRUKTA_FILE"] = chosen
    return chosen


def file_to_timeline(chosen: str):
    print(f"Loading {chosen}...")

    with open(chosen) as f:
        source = f.read()

    if ".sutra" in chosen:
        return SutraFileTimeline(parse_sutra(source))
    else:
        return SlokaFileTimeline(parse_sloka(source))
