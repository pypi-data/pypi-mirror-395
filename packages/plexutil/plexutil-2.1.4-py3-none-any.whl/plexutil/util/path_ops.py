from __future__ import annotations

import re
from pathlib import Path

from plexutil.dto.movie_dto import MovieDTO
from plexutil.dto.song_dto import SongDTO
from plexutil.dto.tv_episode_dto import TVEpisodeDTO
from plexutil.dto.tv_series_dto import TVSeriesDTO
from plexutil.enums.file_type import FileType
from plexutil.exception.unexpected_naming_pattern_error import (
    UnexpectedNamingPatternError,
)
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.static import Static


class PathOps(Static):
    @staticmethod
    def get_path_from_str(
        path_candidate: str,
        is_dir_expected: bool = False,
        is_file_expected: bool = False,
    ) -> Path:
        """
        Get pathlib.Path from a str

        Args:
            path_candidate (str): The likely Path
            is_dir_expected (bool): Is the path expected to be a dir?
            is_file_expected (bool): Is the path expected to be a file?

        Returns:
            A pathlib.Path

        Raises:
            ValueError: If path_candidate is not supplied or path doesn't exist
            or path does not meet is_dir_expected/is_file_expected condition
        """
        if not path_candidate:
            description = "Expected a path candidate but none supplied "
            raise ValueError(description)

        path = Path(path_candidate)

        if not path.exists():
            description = f"Path candidate ({path_candidate}) does not exist"
            raise ValueError(description)

        if is_dir_expected and not path.is_dir():
            description = (
                f"Expected a dir for ({path_candidate}) but this is not a dir"
            )
            raise ValueError(description)

        if is_file_expected and not path.is_file():
            description = (
                f"Expected a file for ({path_candidate}) but path not a file"
                f"candidate is not a file {path_candidate}"
            )
            raise ValueError(description)

        return path

    @staticmethod
    def __walk_tv_structure(
        show_name: str, first_aired_year: int, path: Path
    ) -> tuple[list[TVEpisodeDTO], list[str]]:
        """
        *Private refer to PathOps.get_local_tv()
        Walks subdirectories in search of TV episodes
        A TV episode is expected to have a file name with a pattern
        of S##E##

        Args:
            show_name (str): The name of the TV show
            first_aired_year (int): The year of the TV show
            path (pathlib.Path): The parent directory of the TV show

        Returns:
            A tuple of:
            1) [TVEpisodeDTO] for each file found and understood as an episode
            2) [str] The name of the files encountered that were not
            understood as episodes
        """
        episodes = []
        unknown = []

        children = path.rglob("*")
        for child in children:
            if child.is_dir():
                sub_episodes, sub_unknown = PathOps.__walk_tv_structure(
                    show_name, first_aired_year, child
                )
                episodes.extend(sub_episodes)
                unknown.extend(sub_unknown)
            elif child.is_file():
                try:
                    tv_episode_dto = PathOps.get_episode_from_str(
                        show_name=show_name,
                        first_aired_year=first_aired_year,
                        candidate=child.stem,
                    )
                    episodes.append(tv_episode_dto)
                except UnexpectedNamingPatternError:
                    unknown.append(child.stem)

        return episodes, unknown

    @staticmethod
    def __walk_music_structure(path: Path) -> tuple[list[SongDTO], list[Path]]:
        """
        *Private, refer to PathOps.get_local_songs()
        Walks subdirectories in search of songs

        Args:
            path (pathlib.Path): The parent directory of the TV show

        Returns:
            A tuple of:
            1) [SongDTO] for each file found
            2) [pathlib.Path] The path of the files encountered that were not
            understood as songs
        """
        songs = []
        unknown = []

        if path.is_file():
            try:
                extension = path.suffix.replace(".", "")
                FileType.get_musical_file_type_from_str(extension)
                song_dto = SongDTO(name=path.stem, location=path)
                songs.append(song_dto)
            except ValueError:
                unknown.append(path)
        elif path.is_dir():
            children = path.rglob("*")
            for child in children:
                sub_songs, sub_unknown = PathOps.__walk_music_structure(child)
                songs.extend(sub_songs)
                unknown.extend(sub_unknown)

        return songs, unknown

    @staticmethod
    def get_local_tv(paths: list[Path]) -> list[TVSeriesDTO]:
        """
        Scans local directories in search of TV Series
        Expects to find directories with a pattern of <series_name> (<year>)

        Expects to see:
        <series_name> (<year>) *directory
        <series_name> (<year>) *directory
        ...

        Args:
            paths (pathlib.Path): The directories to scan

        Returns:
            [TVSeriesDTO]: Found series
        """
        series = []
        unknown = []

        for path in paths:
            for tv_dir in path.iterdir():
                if not tv_dir.is_dir():
                    description = (
                        f"Found a file but expected a dir: {tv_dir} "
                        f"Proceeding with default TVSeriesDTO"
                    )
                    PlexUtilLogger.get_logger().debug(description)
                    series.append(TVSeriesDTO(location=tv_dir))
                    unknown.append(tv_dir)
                    continue

                try:
                    name, year = PathOps.get_show_name_and_year_from_str(
                        tv_dir.name
                    )
                    tv_series_dto = TVSeriesDTO(
                        name=name, year=year, location=tv_dir
                    )
                except UnexpectedNamingPatternError:
                    description = (
                        f"Could not extract name, year from series: {tv_dir} "
                        f"Proceeding with default TVSeriesDTO"
                    )
                    PlexUtilLogger.get_logger().debug(description)
                    tv_series_dto = TVSeriesDTO(location=tv_dir)
                    unknown.append(tv_dir)

                series.append(tv_series_dto)

        description = (
            f"Evaluated local TV.\n"
            f"Understood: {len(series) - len(unknown)!s}\n"
            f"Unknown: {len(unknown)!s}\n"
        )
        PlexUtilLogger.get_logger().debug(description)
        if unknown:
            description = (
                "WARNING: Plexutil failed to understand some path as series:\n"
            )
            for unk in unknown:
                description = description + f"-> {unk}\n"
            description = description + (
                "https://support.plex.tv/articles/"
                "naming-and-organizing-your-tv-show-files/"
            )

            PlexUtilLogger.get_logger().warning(description)

        return series

    @staticmethod
    def get_local_movies(paths: list[Path]) -> list[MovieDTO]:
        """
        Scans local directories in search of movies
        A movie is expected to have a file name or directory name
        with a pattern of name (year) -optional arbitrary text-

        Args:
            paths (pathlib.Path): The directories to scan

        Returns:
            [MovieDTO]: Found movies
        """
        movies = []
        unknown = []
        for path in paths:
            for child in path.iterdir():
                file_name = child.name if child.is_dir() else child.stem

                try:
                    name, year = PathOps.get_show_name_and_year_from_str(
                        file_name
                    )
                    movies.append(
                        MovieDTO(name=name, year=year, location=child)
                    )
                except UnexpectedNamingPatternError:
                    description = (
                        f"Could not extract name, year from a movie: {child} "
                        f"Proceeding with default MovieDTO"
                    )
                    unknown.append(child)
                    PlexUtilLogger.get_logger().debug(description)
                    movies.append(MovieDTO(location=child))

        description = (
            f"Evaluated local movies.\n"
            f"Understood: {len(movies) - len(unknown)!s}\n"
            f"Unknown: {len(unknown)!s}\n"
        )
        PlexUtilLogger.get_logger().debug(description)
        if unknown:
            description = (
                "WARNING: Plexutil failed to understand some path as movies:\n"
            )
            for unk in unknown:
                description = description + f"-> {unk}\n"
            description = description + (
                "https://support.plex.tv/articles/"
                "naming-and-organizing-your-movie-media-files/"
            )

            PlexUtilLogger.get_logger().warning(description)

        return movies

    @staticmethod
    def get_local_songs(paths: list[Path]) -> list[SongDTO]:
        """
        Scans local directories recursively in search of songs
        A warning will be logged for each unsupported file type
        see FileType.get_musical_file_type_from_str()

        Args:
            paths (pathlib.Path): The directories to scan

        Returns:
            [SongDTO]: Found songs

        """
        songs = []
        unknown = []

        for path in paths:
            known, unk = PathOps.__walk_music_structure(path)
            songs.extend(known)
            unknown.extend(unk)

        description = (
            f"Evaluated local songs.\n"
            f"Understood: {(len(songs) - len(unknown))!s}\n"
            f"Unknown: {len(unknown)!s}\n"
        )
        PlexUtilLogger.get_logger().debug(description)
        if unknown:
            for unk in unknown:
                description = "Not understood as song (ignored): " + f"{unk}\n"
                PlexUtilLogger.get_logger().debug(description)

        return songs

    @staticmethod
    def get_show_name_and_year_from_str(candidate: str) -> tuple[str, int]:
        """
        Extracts Show name and year from a str,
        expects to find <show_name> (<year>) pattern

        Args:
            candidate (str): The likely show_name,year

        Returns:
            A tuple of:
            1) show name
            2) year

        Raises:
            UnexpectedNamingPatternError: If candiate str does not match
            the expected parttern

        """
        pattern = r"([\w\s'’:\-.,·àáâäèéêëìíîïòóôöùúûüçñ]+?)\s*\((\d{4})\)"  # noqa: RUF001
        match = re.search(pattern, candidate)

        if match:
            show_name = match.group(1).strip()
            year = match.group(2)
        else:
            description = (
                f"Could not extract show name, year from: {candidate}\n"
                f"Expected to see a 'show_name (year)' pattern"
            )
            raise UnexpectedNamingPatternError(description)

        return show_name.lower(), int(year)

    @staticmethod
    def get_episode_from_str(
        show_name: str, first_aired_year: int, candidate: str
    ) -> TVEpisodeDTO:
        """
        Extracts season, episode numbers from a str,
        expects to find a S#E# pattern

        Args:
            show_name (str): The name of the TV show (case insensitive)
            first_aired_year (int): Year of first airing
            candidate (str): Episode info (case insensitive)

        Returns:
            TVEpisodeDTO: Poulated with the supplied name and season, episode

        Raises:
            ValueError: If S#E# naming pattern not present in candidate
        """

        match = re.search(r"s(\d{2})e(\d{2})", candidate, re.IGNORECASE)

        if match:
            season = int(match.group(1))
            episode = int(match.group(2))
            return TVEpisodeDTO(
                name=show_name,
                first_aired_year=first_aired_year,
                season=season,
                episode=episode,
            )

        else:
            description = f"Did not understand this as an episode: {candidate}"
            raise UnexpectedNamingPatternError(description)

    @staticmethod
    def get_project_root() -> Path:
        """
        Gets the root of this project

        Returns:
            pathlib.Path: The project's root
        """
        return Path(__file__).parent.parent.parent
