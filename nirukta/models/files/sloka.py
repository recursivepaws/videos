from dataclasses import dataclass
from nirukta.models.presentation import Sloka


@dataclass
class SlokaFile:
    citation: str
    sloka: Sloka
