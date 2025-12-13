from pushtunes.models.track import Track
from pushtunes.models.album import Album
from pushtunes.models.push_status import PushStatus
from pushtunes.services.music_service import MusicService
from pushtunes.utils.filters import TrackFilter, AlbumFilter
from pushtunes.utils.similarity import get_best_match
from pushtunes.utils.logging import get_logger
from dataclasses import dataclass
from typing import TypeVar, Generic, Literal


T = TypeVar('T', Album, Track)


@dataclass(frozen=True, slots=True)
class PushResult(Generic[T]):
    item: T
    status: PushStatus
    message: str = ""
    found_item: T | None = None


@dataclass
class Pusher(Generic[T]):
    items: list[T]
    service: MusicService
    item_type: Literal["album", "track"]
    filter: AlbumFilter | TrackFilter | None = None
    min_similarity: float = 0.8
    mappings: "MappingsManager | None" = None

    def push(self) -> list[PushResult[T]]:
        """Push items (albums or tracks) from a music source to a service

        Args:
            items: List of Album or Track objects to push
            service: The music service to sync to
            item_type: Either "album" or "track"
            filter: Optional filter to exclude certain items
            min_similarity: Minimum similarity threshold for matching
            mappings: Optional mappings manager for manual overrides

        Returns:
            List of PushResult objects with status for each item

        Raises:
            Exception: If authentication or cache loading fails
        """

        log = get_logger()
        log.info(f"Got {len(self.items)} {self.item_type}s to push")

        results: list[PushResult[T]] = []
        for item in self.items:
            if self.filter and self.filter.should_filter_out(item):
                add_result(
                    results, PushResult(item=item, status=PushStatus.filtered)
                )
                continue

            # This uses the cache to discard perfect matches before we even send a search query
            # If authentication fails, this will raise an exception and abort the entire operation
            try:
                is_in_library_method = getattr(self.service, f"is_{self.item_type}_in_library")
                is_in_library = is_in_library_method(item)
            except Exception as e:
                log.error(
                    f"Failed to check library for {self.item_type} {item.artist} - {item.title}: {e}"
                )
                log.error(
                    f"Authentication or library access failed. Aborting {self.item_type} push operation."
                )
                raise

            if is_in_library:
                add_result(
                    results,
                    PushResult(item, status=PushStatus.already_in_library),
                )
                continue

            # Check if item has a service ID for the target service in extra_data (from CSV)
            best_match = None
            if item.extra_data:
                service_id_key = f"{self.service.service_name}_id"
                service_id = item.extra_data.get(service_id_key)
                if service_id:
                    # Create an item object with the service ID
                    if self.item_type == "album":
                        best_match = Album(
                            artists=item.artists,
                            title=item.title,
                            year=item.year,
                            service_id=service_id,
                            service_name=self.service.service_name,
                        )
                    else:  # track
                        best_match = Track(
                            artists=item.artists,
                            title=item.title,
                            album=item.album,
                            year=item.year,
                            service_id=service_id,
                            service_name=self.service.service_name,
                        )
                    log.info(
                        f"Using CSV service_id for {item.artist} - {item.title} -> {self.service.service_name} ID {service_id}"
                    )

            # Check if there's a mapping for this item (if no service ID from CSV)
            if not best_match and self.mappings:
                # Get Spotify client for ID type detection (if service is Spotify)
                service_client = None
                if self.service.service_name == "spotify" and hasattr(self.service, 'sp'):
                    service_client = self.service.sp

                get_mapping_method = getattr(self.mappings, f"get_{self.item_type}_mapping")
                mapped_result = get_mapping_method(
                    item, self.service.service_name, service_client
                )

                if mapped_result:
                    # Check if this is a cross-type mapping
                    if self.item_type == "album" and isinstance(mapped_result, Track):
                        # Album mapped to track - add as track instead
                        log.info(
                            f"Cross-type mapping: album {item.artist} - {item.title} mapped to track"
                        )
                        try:
                            # Check if track already in library
                            is_track_in_library = self.service.is_track_in_library(mapped_result)
                            if is_track_in_library:
                                add_result(
                                    results,
                                    PushResult(
                                        item,
                                        found_item=None,
                                        status=PushStatus.already_in_library,
                                        message="Mapped track already in library"
                                    ),
                                )
                            else:
                                # Add the track
                                success = self.service.add_track(mapped_result)
                                if success:
                                    add_result(
                                        results,
                                        PushResult(
                                            item,
                                            found_item=None,
                                            status=PushStatus.added,
                                            message="Added as track (album→track mapping)"
                                        ),
                                    )
                                else:
                                    add_result(
                                        results,
                                        PushResult(item, status=PushStatus.error),
                                    )
                        except Exception as e:
                            log.error(f"Error adding mapped track: {e}")
                            add_result(
                                results,
                                PushResult(item, status=PushStatus.error),
                            )
                        continue

                    elif self.item_type == "track" and isinstance(mapped_result, Album):
                        # Track mapped to album - add as album instead
                        log.info(
                            f"Cross-type mapping: track {item.artist} - {item.title} mapped to album"
                        )
                        try:
                            # Check if album already in library
                            is_album_in_library = self.service.is_album_in_library(mapped_result)
                            if is_album_in_library:
                                add_result(
                                    results,
                                    PushResult(
                                        item,
                                        found_item=None,
                                        status=PushStatus.already_in_library,
                                        message="Mapped album already in library"
                                    ),
                                )
                            else:
                                # Add the album
                                success = self.service.add_album(mapped_result)
                                if success:
                                    add_result(
                                        results,
                                        PushResult(
                                            item,
                                            found_item=None,
                                            status=PushStatus.added,
                                            message="Added as album (track→album mapping)"
                                        ),
                                    )
                                else:
                                    add_result(
                                        results,
                                        PushResult(item, status=PushStatus.error),
                                    )
                        except Exception as e:
                            log.error(f"Error adding mapped album: {e}")
                            add_result(
                                results,
                                PushResult(item, status=PushStatus.error),
                            )
                        continue

                    # Normal mapping (same type)
                    mapped_item = mapped_result
                    # If the mapping has a service_id, use it directly
                    if mapped_item.service_id:
                        best_match = mapped_item
                        log.info(
                            f"Using mapping for {item.artist} - {item.title} -> ID {mapped_item.service_id}"
                        )
                    else:
                        # If the mapping has metadata, search for it
                        log.info(
                            f"Using mapping for {item.artist} - {item.title} -> {mapped_item.artist} - {mapped_item.title}"
                        )
                        search_method = getattr(self.service, f"search_{self.item_type}s")
                        search_results = search_method(mapped_item)
                        if search_results:
                            best_match, _ = get_best_match(
                                source=mapped_item,
                                candidates=search_results,
                                min_similarity=self.min_similarity,
                            )

            # If no service ID or mapping, do normal search
            if not best_match:
                search_method = getattr(self.service, f"search_{self.item_type}s")
                search_results = search_method(item)
                if not search_results:
                    add_result(
                        results, PushResult(item=item, status=PushStatus.not_found)
                    )
                    continue

                best_match, _ = get_best_match(
                    source=item,
                    candidates=search_results,
                    min_similarity=self.min_similarity,
                )

            if best_match:
                # A suitable match was found on the target service.
                # The is_in_library check should have already caught this,
                # but we'll double-check here just in case.
                try:
                    is_in_library_method = getattr(self.service, f"is_{self.item_type}_in_library")
                    is_best_match_in_library = is_in_library_method(best_match)
                except Exception as e:
                    log.error(
                        f"Failed to check library for best match {best_match.artist} - {best_match.title}: {e}"
                    )
                    log.error(
                        f"Authentication or library access failed. Aborting {self.item_type} push operation."
                    )
                    raise

                if is_best_match_in_library:
                    add_result(
                        results,
                        PushResult(
                            item,
                            found_item=best_match,
                            status=PushStatus.already_in_library,
                        ),
                    )
                else:
                    # It's a good match and it's not in the library, so add it.
                    add_method = getattr(self.service, f"add_{self.item_type}")
                    success = add_method(best_match)
                    if success:
                        add_result(
                            results,
                            PushResult(
                                item,
                                found_item=best_match,
                                status=PushStatus.added,
                            ),
                        )
                    else:
                        add_result(
                            results,
                            PushResult(
                                item,
                                found_item=best_match,
                                status=PushStatus.error,
                            ),
                        )
            else:  # No suitable match was found in the search results.
                add_result(
                    results,
                    PushResult(
                        item,
                        found_item=None,
                        status=PushStatus.similarity_too_low,
                    ),
                )
        return results


def pretty_print_result(result: PushResult) -> str:
    """Format a push result for display."""
    item = result.item
    match result.status:
        case PushStatus.error:
            return f"Failed to add {item.artist} - {item.title}"
        case PushStatus.not_found:
            return f"Could not find a match for {item.artist} - {item.title}"
        case PushStatus.already_in_library:
            msg = f"Skipping {item.artist} - {item.title} (already in library)"
            if result.message:
                msg += f" - {result.message}"
            return msg
        case PushStatus.filtered:
            return f"Skipping {item.artist} - {item.title} (filtered)"
        case PushStatus.similarity_too_low:
            return f"Skipping {item.artist} - {item.title} (similarity too low)"
        case PushStatus.mapped:
            return f"Added {item.artist} - {item.title} -> Mapped to {result.found_item.artist} - {result.found_item.title}"
        case PushStatus.added:
            if result.message:
                # Cross-type mapping message
                return f"Added {item.artist} - {item.title} -> {result.message}"
            elif result.found_item:
                return f"Added {item.artist} - {item.title} -> Found {result.found_item.artist} - {result.found_item.title}"
            else:
                return f"Added {item.artist} - {item.title}"
        case PushStatus.deleted:
            return f"Deleted {item.artist} - {item.title} from target library"
        case _:
            return f"Something unknown happened while adding {item.artist} - {item.title}"


def add_result(results: list[PushResult], result: PushResult) -> None:
    """Add a result and send it to the logger at the same time"""
    log = get_logger(__name__)
    results.append(result)
    if result.status == PushStatus.error:
        log.error(pretty_print_result(result))
    else:
        log.info(pretty_print_result(result))
