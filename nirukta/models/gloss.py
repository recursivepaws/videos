from dataclasses import dataclass
from typing import Set, Union

from nirukta.inflection import Case, SanskritInflection
from nirukta.strings import find_nth


@dataclass
class EnglishGloss:
    """A single English gloss attached to a Sanskrit token.

    etymological=False  ->  [] translation gloss, shown in animations
    etymological=True   ->  {} etymology gloss, hidden by default
    """

    text: str

    def find_reference(
        self, english: str, visited: Set[tuple[int, int]]
    ) -> tuple[int, int]:
        n = 1
        while True:
            gi = find_nth(english, self.text, n)

            assert gi >= 0, (
                "Gloss cannot reference text not contained in the english translation!\n"
                + f'Tried to find "{self.text}" in "{english}" but was unable.'
            )

            index = (gi, gi + len(self.text))

            assert english[index[0] : index[1]] == self.text, (
                "Invalid gloss index into english text"
            )

            # If we've already found this instance of the gloss text
            if index in visited:
                # Find the next one
                n += 1
            else:
                return index


type EtymGloss = Union[SanskritInflection, Case]
type Gloss = Union[EnglishGloss, EtymGloss]
