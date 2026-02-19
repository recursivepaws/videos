from janim.constants.colors import *  # noqa: F403  # pyright: ignore[reportWildcardImportFromLibrary]

GOD = BLUE  # noqa: F405
VERB = PINK  # noqa: F405
YOU = GREEN  # noqa: F405
PARTICLES = ORANGE  # noqa: F405
NEGATION = RED  # noqa: F405
OBJECTS = YELLOW  # noqa: F405
ADJECTIVES = TEAL  # noqa: F405

COLORS = {
    k: v
    for k, v in globals().items()
    if k.isupper() and isinstance(v, str) and v.startswith("#")
}
