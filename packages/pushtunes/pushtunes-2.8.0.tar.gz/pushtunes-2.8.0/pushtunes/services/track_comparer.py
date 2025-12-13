from pushtunes.models.track import Track
from pushtunes.models.compare_status import CompareStatus
from pushtunes.utils.filters import TrackFilter
from pushtunes.utils.similarity import get_best_match
from pushtunes.utils.logging import get_logger
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrackCompareResult:
    track: Track
    status: CompareStatus
    message: str = ""
    matched_track: Track | None = None


@dataclass
class TrackComparer:
    tracks_source: list[Track]
    tracks_target: list[Track]
    filter: TrackFilter | None = None
    min_similarity: float = 0.8
    mappings: "MappingsManager | None" = None

    def compare_tracks(self) -> list[TrackCompareResult]:
        """Compare tracks between source and target

        Args:
            tracks_source: List of tracks from source
            tracks_target: List of tracks from target
            track_filter: Optional TrackFilter to filter which tracks to compare

        Returns:
            List of TrackCompareResult objects

        Raises:
            Exception: If comparison fails
        """

        log = get_logger()
        log.info(
            f"Comparing {len(self.tracks_source)} source tracks with {len(self.tracks_target)} target tracks"
        )

        compare_results: list[TrackCompareResult] = []
        matched_target_tracks = set()

        # First pass: check each source track against target
        for track in self.tracks_source:
            if self.filter and self.filter.matches(track):
                add_result(
                    compare_results,
                    TrackCompareResult(track=track, status=CompareStatus.filtered),
                )
                continue

            # Check if there's a mapping for this track
            search_track = track
            if self.mappings:
                mapped_track = self.mappings.get_track_mapping(
                    track, "target"
                )  # Generic target name
                if mapped_track:
                    log.info(
                        f"Using mapping for {track.artist} - {track.title} -> {mapped_track.artist} - {mapped_track.title}"
                    )
                    search_track = mapped_track

            # Try to find a match in target
            best_match, _ = get_best_match(
                source=search_track,
                candidates=self.tracks_target,
                min_similarity=self.min_similarity,
            )

            if best_match:
                matched_target_tracks.add(id(best_match))
                add_result(
                    compare_results,
                    TrackCompareResult(
                        track=track,
                        matched_track=best_match,
                        status=CompareStatus.in_both,
                    ),
                )
            else:
                add_result(
                    compare_results,
                    TrackCompareResult(track=track, status=CompareStatus.only_in_source),
                )

        # Second pass: find tracks only in target (not matched in first pass)
        for track in self.tracks_target:
            if id(track) not in matched_target_tracks:
                # Apply filter to target tracks too
                if self.filter and self.filter.matches(track):
                    # Don't report filtered target tracks
                    continue

                add_result(
                    compare_results,
                    TrackCompareResult(track=track, status=CompareStatus.only_in_target),
                )

        return compare_results


def pretty_print_result(result: TrackCompareResult):
    match result.status:
        case CompareStatus.only_in_source:
            return f"Only in source: {result.track.artist} - {result.track.title}"
        case CompareStatus.only_in_target:
            return f"Only in target: {result.track.artist} - {result.track.title}"
        case CompareStatus.in_both:
            return f"In both: {result.track.artist} - {result.track.title} <-> {result.matched_track.artist} - {result.matched_track.title}"
        case CompareStatus.filtered:
            return f"Filtered: {result.track.artist} - {result.track.title}"
        case CompareStatus.error:
            return f"Error comparing {result.track.artist} - {result.track.title}: {result.message}"
        case _:
            return f"Unknown status for {result.track.artist} - {result.track.title}"


def add_result(results: list[TrackCompareResult], result: TrackCompareResult) -> None:
    """Add a result and send it to the logger at the same time"""
    log = get_logger(__name__)
    results.append(result)
    if result.status == CompareStatus.error:
        log.error(pretty_print_result(result))
    else:
        log.info(pretty_print_result(result))
