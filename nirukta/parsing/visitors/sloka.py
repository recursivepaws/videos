import logging
import os
import traceback
from typing import Optional
from nirukta.inflection import Case, SanskritInflection
from nirukta.models import (
    CompoundToken,
    EnglishGloss,
    EtymGloss,
    Line,
    SimpleToken,
    Sloka,
    Utterance,
)
from nirukta.models import SlokaFile
from nirukta.parsing.grammars import SLOKA_GRAMMAR
from parsimonious.nodes import NodeVisitor


class SlokaVisitor(NodeVisitor):
    file: str
    dir: str
    source: str

    def __init__(self, file: str):
        NodeVisitor.__init__(self)

        print(f"Loading {file}...")

        with open(file) as f:
            self.source = f.read()

        self.file = file
        self.directory = os.path.dirname(self.file)

    def parse(self) -> SlokaFile:
        tree = SLOKA_GRAMMAR.parse(self.source)
        return self.visit(tree)


    # -- top level ----------------------------------------------------------

    def visit_sloka(self, _, visited_children):
        _, citation, _, lines, _ = visited_children
        return SlokaFile(citation=citation, sloka=Sloka(list(lines)))

    # -- citation -----------------------------------------------------------

    def visit_citation_line(self, _, visited_children):
        _, _, text, _, _ = visited_children
        return text

    def visit_citation_text(self, node, _):
        return node.text.strip()

    # -- line / verse line --------------------------------------------------

    def visit_line(self, _, visited_children):
        _, _, verse_lines = visited_children
        return Line(vAkyAni=list(verse_lines))

    def visit_verse_line(self, _, visited_children):
        # visited_children: [lookahead, token_seq, ws, first_quoted_str, rest_quoted_strs, ws]
        _, tokens, _, first, rest, _ = visited_children
        extra = [pair[1] for pair in rest]
        english = "#linebreak()".join([first] + extra)
        return Utterance(tokens=tokens, english=english)

    # -- token sequence -----------------------------------------------------

    def visit_token_seq(self, _, visited_children):
        first, rest = visited_children
        tokens = [first]
        for pair in rest:
            # pair = [ws_node, token_result] from the anonymous (ws token) sequence
            tokens.append(pair[1])
        return tokens

    def visit_token(self, _, visited_children):
        return visited_children[0]

    # -- compound (sandhi) tokens -------------------------------------------

    def visit_compound_token(self, _, visited_children):
        first_part, plus_parts, _, surface, gloss = visited_children
        etym_glosses = list(gloss)
        etym_gloss: Optional[EtymGloss] = (
            etym_glosses[0] if len(etym_glosses) > 0 else None
        )

        parts = [first_part] + list(plus_parts)

        return CompoundToken(
            parts=parts,
            slp1=surface,
            etym_gloss=etym_gloss,
        )

    def visit_plus_part(self, _, visited_children):
        _, part = visited_children
        return part

    def visit_comp_part(self, _, visited_children):
        return visited_children[0]

    def visit_paren_compound(self, _, visited_children):
        _, compound, _ = visited_children
        return compound

    # -- simple tokens & glosses --------------------------------------------

    def visit_simple_token(self, _, visited_children):
        slp1, glosses = visited_children
        return SimpleToken(slp1=slp1, glosses=glosses)

    def visit_gloss(self, _, visited_children):
        return visited_children[0]

    def visit_trans_gloss(self, _, visited_children):
        _, content, _ = visited_children
        return EnglishGloss(text=content)

    def visit_etym_gloss(self, _, visited_children):
        _, content, _ = visited_children
        try:
            inflection = SanskritInflection.parse(content)
            print(f"inflection: {inflection}")
            return inflection
        except Exception:
            try:
                case = Case.parse(content)
                print(f"case: {case}")
                return case
            except Exception:
                print(f'Error! invalid etymological glossing: "{content}"\n')
                logging.error(traceback.format_exc())
                return None

    def visit_trans_content(self, node, _):
        return node.text

    def visit_etym_content(self, node, _):
        return node.text

    # -- terminals ----------------------------------------------------------

    def visit_punct(self, node, _):
        return node.text

    def visit_slp1(self, node, _):
        return node.text

    def visit_quoted_str(self, node, _):
        return node.text[1:-1].replace('\\"', '"').replace("\\\\", "\\")

    def generic_visit(self, node, visited_children):
        return visited_children or node
