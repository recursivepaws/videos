from nirukta.models import Sloka, SutraFile
from nirukta.parsing.visitors.sloka import SlokaVisitor


class SutraVisitor(SlokaVisitor):
    def visit_sutra(self, _, visited_children):
        [citation, first], rest, _ = visited_children
        slokas = [first, *rest]

        print(f"slokas: {len(slokas)}")
        # for sloka in slokas:
        #     assert isinstance(sloka, Sloka), f"not a sloka: {sloka}"

        return SutraFile(citation, slokas)

    def visit_inline_sloka(self, _, visited_children):
        _, _, _, lines, _ = visited_children
        return Sloka(list(lines))

    def visit_sloka(self, _, visited_children):
        _, citation, _, lines, _ = visited_children
        return [citation, Sloka(list(lines))]
