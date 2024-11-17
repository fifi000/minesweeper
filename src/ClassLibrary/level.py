import enum


class Levels(enum.Enum):
    Easy = 1
    Medium = 2
    Hard = 3
    Custom = 4


class Level:
    def __init__(
        self,
        rows: int,
        cols: int,
        mines_percent: float,
        name: str = 'CUSTOM',
        level=Levels.Custom,
    ):
        self.level = level
        self.name = name
        self.rows = rows
        self.cols = min(cols, 2 * self.rows)
        self.mines_percent = mines_percent

    @classmethod
    def easy(cls):
        return cls(level=Levels.Easy, rows=10, cols=10, mines_percent=0.15625)

    @classmethod
    def medium(cls):
        return cls(level=Levels.Medium, rows=14, cols=18, mines_percent=0.15873)

    @classmethod
    def hard(cls):
        return cls(level=Levels.Hard, rows=16, cols=30, mines_percent=0.209)
