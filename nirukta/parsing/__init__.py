from nirukta.models import SlokaFile, SutraFile
from nirukta.parsing.visitors import SlokaVisitor, SutraVisitor
from nirukta.parsing.grammars import SLOKA_GRAMMAR, SUTRA_GRAMMAR


def parse_sutra(source: str) -> SutraFile:
    """Parse a sutra source string and return a Sutra object."""
    tree = SUTRA_GRAMMAR.parse(source)
    return SutraVisitor().visit(tree)


def parse_sloka(source: str) -> SlokaFile:
    """Parse a sloka source string and return a Sloka object."""
    tree = SLOKA_GRAMMAR.parse(source)
    return SlokaVisitor().visit(tree)
