from dataclasses import dataclass


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class TVEpisodeDTO:
    name: str = ""
    first_aired_year: int = 0
    season: int = 0
    episode: int = 0

    def __str__(self) -> str:
        return (
            self.name + " "
            f"({self.first_aired_year}): "
            f"S{self.season:02}E{self.episode:02}"
        )
