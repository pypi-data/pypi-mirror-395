from __future__ import annotations

from enum import Enum


class Agent(Enum):
    MUSIC = "tv.plex.agents.music"
    TV = "tv.plex.agents.series"
    MOVIE = "tv.plex.agents.movie"

    @staticmethod
    def get_all() -> list[Agent]:
        return [Agent.MUSIC, Agent.TV, Agent.MOVIE]

    @staticmethod
    def get_from_str(candidate: str) -> Agent:
        for agent in Agent.get_all():
            if candidate.lower() == agent.value:
                return agent

        description = f"Agent not supported: {candidate}"
        raise ValueError(description)
