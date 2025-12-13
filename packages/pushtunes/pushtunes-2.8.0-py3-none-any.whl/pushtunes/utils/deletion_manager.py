"""Deletion manager for handling safe deletion of albums and tracks with backup."""

import os
from datetime import datetime
from dataclasses import dataclass
from typing import TypeVar, Generic
from platformdirs import user_data_dir

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.utils.csv_manager import CsvManager
from pushtunes.utils.logging import get_logger

T = TypeVar('T', Album, Track)


@dataclass
class DeletionCandidate(Generic[T]):
    """Represents an item that could be deleted."""
    item: T  # The item in the target library
    source_match: T | None  # The matching item from source (if found)
    similarity_score: float  # Similarity score if match was found
    will_be_deleted: bool  # Whether this will be deleted with current settings


@dataclass
class DeletionPreview:
    """Preview of what would be deleted."""
    total_target_items: int
    items_to_delete: list[DeletionCandidate]
    items_preserved: list[DeletionCandidate]


class DeletionManager:
    """Manages safe deletion of albums/tracks with backup and preview."""

    def __init__(self, backup_dir: str | None = None):
        """Initialize deletion manager.

        Args:
            backup_dir: Directory to store backup CSV files. If None, uses platformdirs user_data_dir
        """
        if backup_dir is None:
            # Use platform-appropriate data directory
            app_data_dir = user_data_dir("pushtunes", "pushtunes")
            self.backup_dir = os.path.join(app_data_dir, "backups")
        else:
            self.backup_dir = backup_dir

        self.log = get_logger(__name__)

        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, exist_ok=True)
            self.log.info(f"Created backup directory: {self.backup_dir}")

    def backup_albums(self, albums: list[Album], operation_name: str = "deletion") -> str:
        """Backup albums to CSV before deletion.

        Args:
            albums: List of albums to backup
            operation_name: Name of the operation (for filename)

        Returns:
            Path to the backup file
        """
        if not albums:
            self.log.warning("No albums to backup")
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            self.backup_dir,
            f"albums_{operation_name}_backup_{timestamp}.csv"
        )

        CsvManager.export_albums(albums, backup_file)
        self.log.info(f"Backed up {len(albums)} albums to {backup_file}")

        return backup_file

    def backup_tracks(self, tracks: list[Track], operation_name: str = "deletion") -> str:
        """Backup tracks to CSV before deletion.

        Args:
            tracks: List of tracks to backup
            operation_name: Name of the operation (for filename)

        Returns:
            Path to the backup file
        """
        if not tracks:
            self.log.warning("No tracks to backup")
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            self.backup_dir,
            f"tracks_{operation_name}_backup_{timestamp}.csv"
        )

        CsvManager.export_tracks(tracks, backup_file)
        self.log.info(f"Backed up {len(tracks)} tracks to {backup_file}")

        return backup_file

    def generate_deletion_preview(
        self,
        target_items: list[T],
        source_items: list[T],
        min_similarity: float,
        mappings=None,
        service_name: str | None = None,
    ) -> DeletionPreview:
        """Generate a preview of what would be deleted.

        Args:
            target_items: Items in the target library
            source_items: Items in the source
            min_similarity: Minimum similarity threshold for matching
            mappings: Optional MappingsManager for checking mapped items
            service_name: Service name ('spotify' or 'ytm') required if using mappings

        Returns:
            DeletionPreview with analysis of what would be deleted
        """
        from pushtunes.utils.similarity import get_best_match

        items_to_delete: list[DeletionCandidate[T]] = []
        items_preserved: list[DeletionCandidate[T]] = []

        # Build a list of mapped target items if mappings are provided
        mapped_target_items: list[T] = []
        if mappings and service_name:
            for source_item in source_items:
                if isinstance(source_item, Album):
                    mapped_item = mappings.get_album_mapping(source_item, service_name)
                elif isinstance(source_item, Track):
                    mapped_item = mappings.get_track_mapping(source_item, service_name)
                else:
                    continue

                # Only include if the mapping is the same type (album→album or track→track)
                if mapped_item and type(mapped_item) == type(source_item):
                    mapped_target_items.append(mapped_item)

        # For each item in target, check if it has a match in source
        for target_item in target_items:
            # First, check direct similarity match with source items
            best_match, similarity_score = get_best_match(target_item, source_items, min_similarity)

            # If no direct match, check if this target item is a mapped version of a source item
            is_mapped = False
            if not best_match and mapped_target_items:
                # Check if target_item matches any mapped target item
                mapped_match, mapped_similarity = get_best_match(target_item, mapped_target_items, min_similarity)
                if mapped_match:
                    is_mapped = True
                    similarity_score = mapped_similarity
                    self.log.info(
                        f"Preserving mapped item: {target_item.artist} - {target_item.title} "
                        f"(matches mapping with similarity {similarity_score:.2f})"
                    )

            if best_match or is_mapped:
                # Use the similarity score returned from get_best_match
                candidate = DeletionCandidate(
                    item=target_item,
                    source_match=best_match,
                    similarity_score=similarity_score,
                    will_be_deleted=False
                )
                items_preserved.append(candidate)
            else:
                # No match found - this item would be deleted
                candidate = DeletionCandidate(
                    item=target_item,
                    source_match=None,
                    similarity_score=0.0,
                    will_be_deleted=True
                )
                items_to_delete.append(candidate)

        return DeletionPreview(
            total_target_items=len(target_items),
            items_to_delete=items_to_delete,
            items_preserved=items_preserved,
        )
