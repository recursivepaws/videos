from __future__ import annotations

import sys

from typing import Union

from parser import CompoundToken, Gloss, Line, SimpleToken, SlokaFile, VerseLine, parse

TokenType = Union[SimpleToken, CompoundToken, str]

# ---------------------------------------------------------------------------
# Serialiser
# ---------------------------------------------------------------------------


def fmt_gloss(g: Gloss) -> str:
    return ("{" + g.text + "}") if g.etymological else ("[" + g.text + "]")


def fmt_simple(token: SimpleToken) -> str:
    return token.slp1 + "".join(fmt_gloss(g) for g in token.glosses)


def fmt_comp_part(token: TokenType) -> str:
    if isinstance(token, CompoundToken):
        return "(" + fmt_compound(token) + ")"
    elif isinstance(token, SimpleToken):
        return fmt_simple(token)
    else:
        return token


def fmt_compound(token: CompoundToken) -> str:
    parts = "+".join(fmt_comp_part(p) for p in token.parts)
    return f"{parts}={token.slp1}"


def fmt_token(token: TokenType) -> str:
    if isinstance(token, str):
        return token
    elif isinstance(token, SimpleToken):
        return fmt_simple(token)
    else:
        return fmt_compound(token)


def fmt_verse_line(vline: VerseLine) -> str:
    # Every token (including punctuation) is separated by a single space.
    # The first token has no leading space; all subsequent ones do.
    parts: list[str] = []
    for tok in vline.tokens:
        serialised = fmt_token(tok)
        parts.append(serialised if not parts else " " + serialised)

    token_line = "".join(parts)

    # Multiple quoted strings are stored joined by "#linebreak()" — split back.
    english_parts = vline.english.split("#linebreak()")
    quoted_lines = "\n".join(f'"{p}"' for p in english_parts)

    return token_line + "\n" + quoted_lines


def fmt_line(line: Line) -> str:
    # Blank line between vākyāni; no trailing blank line.
    body = "\n\n".join(fmt_verse_line(v) for v in line.vAkyAni)
    return "\n--- line ---\n" + body


def fmt_sloka(sloka: SlokaFile) -> str:
    header = f"=== {sloka.citation} ==="
    lines = "\n".join(fmt_line(ln) for ln in sloka.lines)
    return header + "\n" + lines + "\n"


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) == 2:
        path = sys.argv[1]
        with open(path, "r", encoding="utf-8") as fh:
            source = fh.read()
        result = fmt_sloka(parse(source))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(result)
    else:
        source = sys.stdin.read()
        sys.stdout.write(fmt_sloka(parse(source)))


if __name__ == "__main__":
    main()
