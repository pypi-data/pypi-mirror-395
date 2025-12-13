from pushtunes.models.album import Album
from pushtunes.models.compare_status import CompareStatus
from pushtunes.utils.filters import AlbumFilter
from pushtunes.utils.similarity import get_best_match
from pushtunes.utils.logging import get_logger
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlbumCompareResult:
    album: Album
    status: CompareStatus
    message: str = ""
    matched_album: Album | None = None


@dataclass
class AlbumComparer:
    albums_source: list[Album]
    albums_target: list[Album]
    filter: AlbumFilter | None = None
    min_similarity: float = 0.8
    mappings: "MappingsManager | None" = None

    def compare_albums(self) -> list[AlbumCompareResult]:
        """Compare albums between source and target

        Args:
            albums_source: List of albums from source
            albums_target: List of albums from target
            album_filter: Optional AlbumFilter to filter which albums to compare

        Returns:
            List of AlbumCompareResult objects

        Raises:
            Exception: If comparison fails
        """

        log = get_logger()
        log.info(
            f"Comparing {len(self.albums_source)} source albums with {len(self.albums_target)} target albums"
        )

        compare_results: list[AlbumCompareResult] = []
        matched_target_albums = set()

        # First pass: check each source album against target
        for album in self.albums_source:
            if self.filter and self.filter.matches(album):
                add_result(
                    compare_results,
                    AlbumCompareResult(album=album, status=CompareStatus.filtered),
                )
                continue

            # Check if there's a mapping for this album
            search_album = album
            if self.mappings:
                mapped_album = self.mappings.get_album_mapping(
                    album, "target"
                )  # Generic target name
                if mapped_album:
                    log.info(
                        f"Using mapping for {album.artist} - {album.title} -> {mapped_album.artist} - {mapped_album.title}"
                    )
                    search_album = mapped_album

            # Try to find a match in target
            best_match, _ = get_best_match(
                source=search_album,
                candidates=self.albums_target,
                min_similarity=self.min_similarity,
            )

            if best_match:
                matched_target_albums.add(id(best_match))
                add_result(
                    compare_results,
                    AlbumCompareResult(
                        album=album,
                        matched_album=best_match,
                        status=CompareStatus.in_both,
                    ),
                )
            else:
                add_result(
                    compare_results,
                    AlbumCompareResult(album=album, status=CompareStatus.only_in_source),
                )

        # Second pass: find albums only in target (not matched in first pass)
        for album in self.albums_target:
            if id(album) not in matched_target_albums:
                # Apply filter to target albums too
                if self.filter and self.filter.matches(album):
                    # Don't report filtered target albums
                    continue

                add_result(
                    compare_results,
                    AlbumCompareResult(album=album, status=CompareStatus.only_in_target),
                )

        return compare_results


def pretty_print_result(result: AlbumCompareResult):
    match result.status:
        case CompareStatus.only_in_source:
            return f"Only in source: {result.album.artist} - {result.album.title}"
        case CompareStatus.only_in_target:
            return f"Only in target: {result.album.artist} - {result.album.title}"
        case CompareStatus.in_both:
            return f"In both: {result.album.artist} - {result.album.title} <-> {result.matched_album.artist} - {result.matched_album.title}"
        case CompareStatus.filtered:
            return f"Filtered: {result.album.artist} - {result.album.title}"
        case CompareStatus.error:
            return f"Error comparing {result.album.artist} - {result.album.title}: {result.message}"
        case _:
            return f"Unknown status for {result.album.artist} - {result.album.title}"


def add_result(results: list[AlbumCompareResult], result: AlbumCompareResult) -> None:
    """Add a result and send it to the logger at the same time"""
    log = get_logger(__name__)
    results.append(result)
    if result.status == CompareStatus.error:
        log.error(pretty_print_result(result))
    else:
        log.info(pretty_print_result(result))
