"""
Parser for the sloka DSL.

File structure:
    === citation ===
    (abhinayadarpaNe 1) SANSKRIT

    === sanskrit ===
    --- line ---
    "node" @COLOR [GLOSS] +delay {
        "child"
    }

    --- line ---
    "next line node"

    === english ===
    --- line ---
    "translation node" @COLOR

Node syntax:
    "text" @COLOR [GLOSS.INFO] +delay {
        child_node
        child_node
    }

All node fields except text are optional and order-independent.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from models import Citation, Language, Node, Sloka

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

from janim.imports import (
    BLUE,
    DOWN,
    GREEN,
    ORANGE,
    ORIGIN,
    PINK,
    RED,
    UP,
    WHITE,
    YELLOW,
)

# ---------------------------------------------------------------------------
# Grammar
# ---------------------------------------------------------------------------

GRAMMAR = Grammar(r"""
    sloka            = ws citation_section sanskrit_section english_section ws

    citation_section = "=== citation ===" ws citation_body ws
    citation_body    = ~r"[^\n]+"

    sanskrit_section = "=== sanskrit ===" ws line+
    english_section  = "=== english ===" ws line+

    line             = "--- line ---" ws node+ ws

    node             = text attrs ws children?

    text             = ws quoted_str ws
    attrs            = attr*
    attr             = ws (color / gloss / delay)

    color            = "@" identifier
    gloss            = "[" gloss_content "]"
    gloss_content    = ~r"[^\]]+"
    delay            = "+" ~r"[0-9]+"

    children         = "{" ws node* ws "}" ws

    quoted_str       = '"' ~r'(?:[^"\\]|\\.)*' '"'
    identifier       = ~r"[A-Za-z_][A-Za-z0-9_.]*"
    ws               = ~r"\s*"
""")


# ---------------------------------------------------------------------------
# Visitor
# ---------------------------------------------------------------------------


class SlokaVisitor(NodeVisitor):
    # -- top level ----------------------------------------------------------

    def visit_sloka(self, node, visited_children):
        _, citation, sanskrit, english, _ = visited_children
        return Sloka(citation=citation, sanskrit=sanskrit, english=english)

    # -- citation -----------------------------------------------------------

    def visit_citation_section(self, node, visited_children):
        _, _, body, _ = visited_children
        return body

    def visit_citation_body(self, node, visited_children):
        raw = node.text.strip()
        parts = raw.rsplit(None, 1)
        if len(parts) == 2 and parts[1].isupper():
            lang = Language[parts[1]]  # "SANSKRIT" -> Language.SANSKRIT
            return Citation(text=parts[0].strip(), lang=lang)
        return Citation(text=raw, lang=Language.SANSKRIT)

    # -- sections -----------------------------------------------------------

    def visit_sanskrit_section(self, node, visited_children):
        _, _, lines = visited_children
        return lines

    def visit_english_section(self, node, visited_children):
        _, _, lines = visited_children
        return lines

    def visit_line(self, node, visited_children):
        _, _, nodes, _ = visited_children
        return nodes

    # -- nodes --------------------------------------------------------------

    def visit_node(self, node, visited_children):
        text, attrs, _, children_maybe = visited_children
        color = WHITE
        gloss = None
        delay = 0
        for kind, value in attrs:
            if kind == "color":
                color = value
            elif kind == "gloss":
                gloss = value
            elif kind == "delay":
                delay = value

        children = []
        if isinstance(children_maybe, list) and children_maybe:
            children = children_maybe[0]

        return Node(text=text, color=color, gloss=gloss, delay=delay, children=children)

    def visit_text(self, node, visited_children):
        _, quoted, _ = visited_children
        return quoted

    def visit_attrs(self, node, visited_children):
        return visited_children

    def visit_attr(self, node, visited_children):
        _, attr = visited_children
        return attr[0]

    def visit_color(self, node, visited_children):
        _, identifier = visited_children
        return ("color", identifier)

    def visit_gloss(self, node, visited_children):
        _, content, _ = visited_children
        return ("gloss", content)

    def visit_gloss_content(self, node, visited_children):
        return node.text

    def visit_delay(self, node, visited_children):
        _, digits = visited_children
        return ("delay", int(digits.text))

    def visit_children(self, node, visited_children):
        _, _, nodes, _, _, _ = visited_children
        return nodes

    def visit_quoted_str(self, node, visited_children):
        return node.text[1:-1].replace('\\"', '"').replace("\\\\", "\\")

    def visit_identifier(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse(source: str) -> Sloka:
    """Parse a sloka file string and return a Sloka object."""
    tree = GRAMMAR.parse(source)
    return SlokaVisitor().visit(tree)


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = r"""
=== citation ===
(abhinayadarpaNe 1) SANSKRIT

=== sanskrit ===
--- line ---
"A~NgikaM bhuvanaM yasya" {
    "A~Ngikam"  @ADJECTIVES +1
    "bhuvanam"  @OBJECTS +1
    "yasya"     @YOU +1
}
"vAchikaM sarvavA~Nmayam ." {
    "vAchikam"  @ADJECTIVES +3
    "sarvavA~Nmayam" {
        "sarva"     @YOU +2
        "vA~Nmayam" @ORANGE [COMP] {
            "vAc"   @YELLOW
            "mayam" @RED
        }
    }
    "."
}

--- line ---
"AhAryaM chandratArAdi" {
    "AhAryam"       @ADJECTIVES +2
    "chandratArAdi" {
        "chandra"   @YOU +1
        "tAra"      @OBJECTS +1
        "Adi"       @PARTICLES +1
    }
}
"taM numaH sAttvikaM shivam .." {
    "tam"       @YOU +1
    "numaH"     @VERB +1
    "sAttvikam" @ADJECTIVES +1
    "shivam"    @GOD +1
    ".."
}

=== english ===
--- line ---
"Whose bodily expression is the universe," {
    "Whose"             @YOU +2
    "bodily expression" @ADJECTIVES +2
    "is"
    "the universe"      @OBJECTS +2
    ","
}
"Whose verbal expression is all language," {
    "Whose"
    "verbal expression" @ADJECTIVES +4
    "is"
    "all"               @YOU +4
    "language"          @ORANGE [COMP] +2 {
        "language"  @ORANGE
        "made of"   @RED
        "speech"    @YELLOW
    }
    ","
}

--- line ---
"Whose ornamental expression is the moon, stars, etc." {
    "Whose"
    "ornamental expression" @ADJECTIVES +3
    "is"
    "the moon"  @YOU +3
    ","
    "stars"     @OBJECTS +3
    ","
    "etc."      @PARTICLES +3
}
"We verbally praise that pure lord shiva." {
    "We verbally praise"    @VERB +2
    "that"                  @YOU +2
    "pure"                  @ADJECTIVES +2
    "lord shiva"            @GOD +2
    "."
}
"""

    sloka = parse(sample)
    print(sloka)
