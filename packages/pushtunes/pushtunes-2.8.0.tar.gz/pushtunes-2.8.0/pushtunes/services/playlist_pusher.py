"""Playlist pusher service for pushing playlists from one service to another."""

from pushtunes.models.playlist import Playlist
from pushtunes.models.push_status import PushStatus
from pushtunes.models.track import Track
from pushtunes.services.music_service import MusicService
from pushtunes.utils.similarity import get_best_match
from pushtunes.utils.logging import get_logger
from dataclasses import dataclass, field
from enum import Enum, auto


class ConflictMode(Enum):
    """How to handle conflicts when a playlist with the same name exists."""
    abort = auto()      # Show differences and abort
    replace = auto()    # Replace entire playlist
    append = auto()      # Add missing tracks in same positions
    sync = auto()       # Add missing, remove extras


@dataclass(frozen=True, slots=True)
class TrackMatchResult:
    """Result of matching a single track in a playlist."""
    source_track: Track
    status: PushStatus
    matched_track: Track | None = None
    message: str = ""


@dataclass(frozen=True, slots=True)
class PlaylistConflict:
    """Information about a playlist conflict."""
    existing_playlist_id: str
    existing_track_count: int
    source_track_count: int
    tracks_to_add: list[Track] = field(default_factory=list)
    tracks_to_remove: list[Track] = field(default_factory=list)
    tracks_in_common: list[Track] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class PlaylistResult:
    """Result of pushing an entire playlist."""
    playlist: Playlist
    success: bool
    playlist_id: str | None = None
    track_results: list[TrackMatchResult] = None
    conflict: PlaylistConflict | None = None
    message: str = ""


@dataclass
class PlaylistPusher:
    """Service for pushing playlists from one music service to another."""

    playlist: Playlist
    service: MusicService
    min_similarity: float = 0.8
    conflict_mode: ConflictMode = ConflictMode.abort
    target_playlist_id: str | None = None  # Specific playlist ID to target (for Spotify)
    mappings: "MappingsManager | None" = None
    require_all_tracks: bool = False  # If True, fail if any track can't be matched

    def push_playlist(self) -> PlaylistResult:
        """Push a playlist to the target service, matching tracks in order.

        Returns:
            PlaylistResult with success status and track matching details
        """
        log = get_logger()
        log.info(f"Pushing playlist '{self.playlist.name}' with {len(self.playlist.tracks)} tracks")

        # Check if playlist already exists
        existing_playlist = None

        if self.target_playlist_id:
            # Use the specific playlist ID provided
            log.info(f"Using target playlist ID: {self.target_playlist_id}")
            existing_playlist = {
                "id": self.target_playlist_id,
                "name": self.playlist.name,  # We'll get the actual name when we fetch tracks
                "track_count": 0  # Will be updated when we fetch tracks
            }
        else:
            # Look up by name
            existing_playlists = self.service.get_user_playlists()
            for pl in existing_playlists:
                if pl["name"].lower() == self.playlist.name.lower():
                    existing_playlist = pl
                    break

        # Match all tracks first
        track_results: list[TrackMatchResult] = []
        for track in self.playlist.tracks:
            match_result = self._match_track(track)
            track_results.append(match_result)

        # Count successful matches
        matched_tracks = [r for r in track_results if r.status == PushStatus.matched]
        log.info(f"Successfully matched {len(matched_tracks)}/{len(self.playlist.tracks)} tracks")

        if len(matched_tracks) == 0:
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                track_results=track_results,
                message="No tracks could be matched"
            )

        # If require_all_tracks is enabled, fail if not all tracks matched
        if self.require_all_tracks and len(matched_tracks) < len(self.playlist.tracks):
            unmatched_count = len(self.playlist.tracks) - len(matched_tracks)
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                track_results=track_results,
                message=f"Only {len(matched_tracks)}/{len(self.playlist.tracks)} tracks matched. {unmatched_count} track(s) could not be matched. Use --mappings-file to provide manual mappings or lower --similarity threshold."
            )

        # Get matched track IDs in order
        matched_track_ids = [r.matched_track.service_id for r in track_results if r.status == PushStatus.matched]

        # Handle conflict if playlist exists
        if existing_playlist:
            return self._handle_conflict(
                existing_playlist=existing_playlist,
                track_results=track_results,
                matched_track_ids=matched_track_ids
            )

        # No conflict - create new playlist
        return self._create_new_playlist(track_results, matched_track_ids)

    def _create_new_playlist(
        self,
        track_results: list[TrackMatchResult],
        matched_track_ids: list[str]
    ) -> PlaylistResult:
        """Create a new playlist with matched tracks."""
        log = get_logger()

        playlist_id = self.service.create_playlist(
            name=self.playlist.name,
            description=f"Imported playlist with {len(matched_track_ids)} tracks"
        )

        if not playlist_id:
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                track_results=track_results,
                message="Failed to create playlist"
            )

        success = self.service.add_tracks_to_playlist(playlist_id, matched_track_ids)

        if not success:
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                playlist_id=playlist_id,
                track_results=track_results,
                message="Failed to add tracks to playlist"
            )

        return PlaylistResult(
            playlist=self.playlist,
            success=True,
            playlist_id=playlist_id,
            track_results=track_results,
            message=f"Successfully created playlist with {len(matched_track_ids)} tracks"
        )

    def _handle_conflict(
        self,
        existing_playlist: dict,
        track_results: list[TrackMatchResult],
        matched_track_ids: list[str]
    ) -> PlaylistResult:
        """Handle conflict when playlist already exists."""
        log = get_logger()
        playlist_id = existing_playlist["id"]

        # Get existing tracks
        existing_tracks = self.service.get_playlist_tracks(playlist_id)

        # Build conflict information
        conflict = self._analyze_conflict(existing_tracks, track_results)

        if self.conflict_mode == ConflictMode.abort:
            return self._handle_abort(playlist_id, track_results, conflict)
        elif self.conflict_mode == ConflictMode.replace:
            return self._handle_replace(playlist_id, track_results, matched_track_ids, conflict)
        elif self.conflict_mode == ConflictMode.append:
            return self._handle_append(playlist_id, track_results, existing_tracks, conflict)
        elif self.conflict_mode == ConflictMode.sync:
            return self._handle_sync(playlist_id, track_results, matched_track_ids, existing_tracks, conflict)

    def _analyze_conflict(
        self,
        existing_tracks: list[Track],
        track_results: list[TrackMatchResult]
    ) -> PlaylistConflict:
        """Analyze differences between existing and source playlists."""
        # Build sets for comparison using similarity matching
        matched_results = [r for r in track_results if r.status == PushStatus.matched]
        source_tracks = [r.matched_track for r in matched_results]

        tracks_in_common = []
        tracks_to_add = []

        for source_track in source_tracks:
            found, _ = get_best_match(source_track, existing_tracks, self.min_similarity)
            if found:
                tracks_in_common.append(source_track)
            else:
                tracks_to_add.append(source_track)

        # Find tracks to remove (in existing but not in source)
        tracks_to_remove = []
        for existing_track in existing_tracks:
            found, _ = get_best_match(existing_track, source_tracks, self.min_similarity)
            if not found:
                tracks_to_remove.append(existing_track)

        return PlaylistConflict(
            existing_playlist_id="",
            existing_track_count=len(existing_tracks),
            source_track_count=len(source_tracks),
            tracks_to_add=tracks_to_add,
            tracks_to_remove=tracks_to_remove,
            tracks_in_common=tracks_in_common
        )

    def _handle_abort(
        self,
        playlist_id: str,
        track_results: list[TrackMatchResult],
        conflict: PlaylistConflict
    ) -> PlaylistResult:
        """Handle abort mode - show differences and abort."""
        return PlaylistResult(
            playlist=self.playlist,
            success=False,
            playlist_id=playlist_id,
            track_results=track_results,
            conflict=conflict,
            message=f"Playlist '{self.playlist.name}' already exists (use --on-conflict to handle)"
        )

    def _handle_replace(
        self,
        playlist_id: str,
        track_results: list[TrackMatchResult],
        matched_track_ids: list[str],
        conflict: PlaylistConflict
    ) -> PlaylistResult:
        """Handle replace mode - replace entire playlist."""
        log = get_logger()

        success = self.service.replace_playlist_tracks(playlist_id, matched_track_ids)

        if not success:
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                playlist_id=playlist_id,
                track_results=track_results,
                conflict=conflict,
                message="Failed to replace playlist tracks"
            )

        return PlaylistResult(
            playlist=self.playlist,
            success=True,
            playlist_id=playlist_id,
            track_results=track_results,
            conflict=conflict,
            message=f"Successfully replaced playlist with {len(matched_track_ids)} tracks"
        )

    def _handle_append(
        self,
        playlist_id: str,
        track_results: list[TrackMatchResult],
        existing_tracks: list[Track],
        conflict: PlaylistConflict
    ) -> PlaylistResult:
        """Handle append mode - add missing tracks at the end."""
        log = get_logger()

        if not conflict.tracks_to_add:
            return PlaylistResult(
                playlist=self.playlist,
                success=True,
                playlist_id=playlist_id,
                track_results=track_results,
                conflict=conflict,
                message="No new tracks to add (playlist already contains all tracks)"
            )

        # Add only the missing tracks
        track_ids_to_add = [t.service_id for t in conflict.tracks_to_add]
        success = self.service.add_tracks_to_playlist(playlist_id, track_ids_to_add)

        if not success:
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                playlist_id=playlist_id,
                track_results=track_results,
                conflict=conflict,
                message="Failed to add tracks to playlist"
            )

        return PlaylistResult(
            playlist=self.playlist,
            success=True,
            playlist_id=playlist_id,
            track_results=track_results,
            conflict=conflict,
            message=f"Successfully appended {len(track_ids_to_add)} new tracks into playlist"
        )

    def _handle_sync(
        self,
        playlist_id: str,
        track_results: list[TrackMatchResult],
        matched_track_ids: list[str],
        existing_tracks: list[Track],
        conflict: PlaylistConflict
    ) -> PlaylistResult:
        """Handle sync mode - add missing and remove extras."""
        log = get_logger()

        # Remove tracks that aren't in source
        if conflict.tracks_to_remove:
            track_ids_to_remove = [t.service_id for t in conflict.tracks_to_remove]
            remove_success = self.service.remove_tracks_from_playlist(playlist_id, track_ids_to_remove)
            if not remove_success:
                log.warning("Failed to remove some tracks during sync")

        # Replace with source tracks to maintain order
        success = self.service.replace_playlist_tracks(playlist_id, matched_track_ids)

        if not success:
            return PlaylistResult(
                playlist=self.playlist,
                success=False,
                playlist_id=playlist_id,
                track_results=track_results,
                conflict=conflict,
                message="Failed to sync playlist"
            )

        return PlaylistResult(
            playlist=self.playlist,
            success=True,
            playlist_id=playlist_id,
            track_results=track_results,
            conflict=conflict,
            message=f"Successfully synced playlist (added {len(conflict.tracks_to_add)}, removed {len(conflict.tracks_to_remove)})"
        )

    def _match_track(self, track: Track) -> TrackMatchResult:
        """Match a single track on the target service.

        Args:
            track: Source track to match

        Returns:
            TrackMatchResult with matching status and found track
        """
        log = get_logger()

        # Check if there's a mapping for this track
        best_match = None
        if self.mappings:
            mapped_track = self.mappings.get_track_mapping(
                track, self.service.service_name
            )
            if mapped_track:
                # If the mapping has a service_id, use it directly
                if mapped_track.service_id:
                    best_match = mapped_track
                    log.info(
                        f"Using mapping for {track.artist} - {track.title} -> ID {mapped_track.service_id}"
                    )
                else:
                    # If the mapping has metadata, search for it
                    log.info(
                        f"Using mapping for {track.artist} - {track.title} -> {mapped_track.artist} - {mapped_track.title}"
                    )
                    search_results = self.service.search_tracks(mapped_track)
                    if search_results:
                        best_match, _ = get_best_match(
                            source=mapped_track,
                            candidates=search_results,
                            min_similarity=self.min_similarity,
                        )

        # If no mapping or mapping didn't find a match, do normal search
        if not best_match:
            # Search for the track
            search_results = self.service.search_tracks(track)

            if not search_results:
                log.warning(f"No search results for {track.artist} - {track.title}")
                return TrackMatchResult(
                    source_track=track,
                    status=PushStatus.not_found,
                    message="No search results found"
                )

            # Find best match using similarity matching
            best_match, _ = get_best_match(
                source=track,
                candidates=search_results,
                min_similarity=self.min_similarity
            )

            if not best_match:
                log.warning(f"Similarity too low for {track.artist} - {track.title}")
                return TrackMatchResult(
                    source_track=track,
                    status=PushStatus.similarity_too_low,
                    message="No sufficiently similar match found"
                )

        log.info(f"Matched {track.artist} - {track.title} -> {best_match.artist} - {best_match.title}")
        return TrackMatchResult(
            source_track=track,
            status=PushStatus.matched,
            matched_track=best_match
        )


def pretty_print_track_result(result: TrackMatchResult) -> str:
    """Format a track match result for display."""
    match result.status:
        case PushStatus.not_found:
            return f"Could not find: {result.source_track.artist} - {result.source_track.title}"
        case PushStatus.similarity_too_low:
            return f"Similarity too low: {result.source_track.artist} - {result.source_track.title}"
        case PushStatus.error:
            return f"Error matching: {result.source_track.artist} - {result.source_track.title}"
        case PushStatus.matched:
            return f"Matched: {result.source_track.artist} - {result.source_track.title}"
        case _:
            return f"Unknown status for: {result.source_track.artist} - {result.source_track.title}"
