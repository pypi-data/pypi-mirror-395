from pushtunes.models.playlist import Playlist
from pushtunes.models.track import Track
from pushtunes.models.compare_status import CompareStatus
from pushtunes.utils.similarity import get_best_match
from pushtunes.utils.logging import get_logger
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TrackCompareResult:
    """Result of comparing a single track in a playlist."""

    track: Track
    status: CompareStatus
    matched_track: Track | None = None
    message: str = ""


@dataclass(frozen=True, slots=True)
class PlaylistCompareResult:
    """Result of comparing two playlists."""

    playlist_name: str
    source_track_count: int
    target_track_count: int
    tracks_only_in_source: list[Track] = field(default_factory=list)
    tracks_only_in_target: list[Track] = field(default_factory=list)
    tracks_in_both: list[tuple[Track, Track]] = field(
        default_factory=list
    )  # (source, target) pairs
    message: str = ""


@dataclass
class PlaylistComparer:
    """Service for comparing playlists between source and target."""

    playlist_source: Playlist
    playlist_target: Playlist
    min_similarity: float = 0.8

    def compare_playlists(self) -> PlaylistCompareResult:
        """Compare tracks between source and target playlists.

        Returns:
            PlaylistCompareResult with detailed comparison information
        """
        log = get_logger()
        log.info(
            f"Comparing playlist '{self.playlist_source.name}' ({len(self.playlist_source.tracks)} tracks) "
            f"with '{self.playlist_target.name}' ({len(self.playlist_target.tracks)} tracks)"
        )

        matched_target_tracks = set()
        tracks_in_both = []
        tracks_only_in_source = []

        # First pass: check each source track against target
        for track in self.playlist_source.tracks:
            best_match, _ = get_best_match(
                source=track,
                candidates=self.playlist_target.tracks,
                min_similarity=self.min_similarity,
            )

            if best_match:
                matched_target_tracks.add(id(best_match))
                tracks_in_both.append((track, best_match))
                log.info(
                    f"Match found: {track.artist} - {track.title} <-> {best_match.artist} - {best_match.title}"
                )
            else:
                tracks_only_in_source.append(track)
                log.info(
                    f"Only in source: {track.artist} - {track.title}"
                )

        # Second pass: find tracks only in target (not matched in first pass)
        tracks_only_in_target = [
            track
            for track in self.playlist_target.tracks
            if id(track) not in matched_target_tracks
        ]

        for track in tracks_only_in_target:
            log.info(f"Only in target: {track.artist} - {track.title}")

        return PlaylistCompareResult(
            playlist_name=self.playlist_source.name,
            source_track_count=len(self.playlist_source.tracks),
            target_track_count=len(self.playlist_target.tracks),
            tracks_only_in_source=tracks_only_in_source,
            tracks_only_in_target=tracks_only_in_target,
            tracks_in_both=tracks_in_both,
        )


def pretty_print_result(result: PlaylistCompareResult) -> str:
    """Generate a human-readable summary of the playlist comparison."""
    lines = [
        f"\nPlaylist Comparison: {result.playlist_name}",
        f"Source tracks: {result.source_track_count}",
        f"Target tracks: {result.target_track_count}",
        f"Tracks in both: {len(result.tracks_in_both)}",
        f"Only in source: {len(result.tracks_only_in_source)}",
        f"Only in target: {len(result.tracks_only_in_target)}",
    ]

    if result.tracks_only_in_source:
        lines.append("\nTracks only in source:")
        for track in result.tracks_only_in_source:
            lines.append(f"  - {track.artist} - {track.title}")

    if result.tracks_only_in_target:
        lines.append("\nTracks only in target:")
        for track in result.tracks_only_in_target:
            lines.append(f"  - {track.artist} - {track.title}")

    return "\n".join(lines)
