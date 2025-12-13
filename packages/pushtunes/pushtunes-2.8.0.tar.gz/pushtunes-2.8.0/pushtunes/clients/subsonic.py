import os
import sys
import libsonic

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn

from pushtunes.utils.logging import get_logger


class SubsonicClient:
    """Client for interacting with Subsonic music server"""

    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        port: int = 443,
    ):
        """Initialize Subsonic client with connection parameters

        Args:
            url: Subsonic server URL (defaults to SUBSONIC_URL env var)
            username: Username (defaults to SUBSONIC_USER env var)
            password: Password (defaults to SUBSONIC_PASS env var)
            port: Server port (defaults to 443)
        """
        self.url: str | None = url or os.getenv("SUBSONIC_URL")
        self.username: str | None = username or os.getenv("SUBSONIC_USER")
        self.password: str | None = password or os.getenv("SUBSONIC_PASS")
        self.port: int = port

        self.connection: libsonic.Connection = libsonic.Connection(
            self.url, self.username, self.password, port=self.port
        )

        self.log = get_logger()

    def get_albums(self, albums=None, offset=0, progress_bar=None, progress_task=None):
        """Fetch all albums from Subsonic server

        Args:
            albums: Existing list of albums to append to (for recursion)
            offset: Pagination offset
            progress_bar: Optional Progress object for displaying progress
            progress_task: Optional task ID for updating progress

        Returns:
            List of album dictionaries with 'artist', 'title', 'id', and 'year' keys
        """
        if albums is None:
            albums = []

        albumlist = self.connection.getAlbumList2(
            "alphabeticalByArtist", size=500, offset=offset
        )
        albumentries = albumlist["albumList2"]["album"]

        for entry in albumentries:
            if not (
                entry["name"] == "[Unknown Album]"
                or entry["artist"] == "[Unknown Artist]"
            ):
                album_id = entry["id"]
                album_year = None
                try:
                    # Fetch full album details to get the year
                    album_details = self.connection.getAlbum(album_id)
                    if "album" in album_details and "song" in album_details["album"]:
                        # Take the year from the first song
                        first_song = album_details["album"]["song"][0]
                        if "year" in first_song:
                            album_year = int(first_song["year"])
                except Exception as e:
                    self.log.warning(
                        f"Could not fetch year for album {entry['name']}: {e}"
                    )

                albums.append(
                    {
                        "id": album_id,
                        "artist": entry["artist"],
                        "title": entry["name"],
                        "year": album_year,
                    }
                )

                # Update progress if provided
                if progress_bar and progress_task is not None:
                    progress_bar.update(progress_task, advance=1)

        if len(albumentries) == 500:
            # Make a recursive call to fetch more albums
            additional_albums = self.get_albums(None, offset + 500, progress_bar, progress_task)
            albums.extend(additional_albums)

        return albums

    def get_tracks(self, tracks=None, offset=0):
        """Fetch all starred/favorite tracks from Subsonic server

        Args:
            tracks: Existing list of tracks to append to (for recursion)
            offset: Pagination offset

        Returns:
            List of track dictionaries with 'artist', 'title', 'album', 'year' keys
        """
        if tracks is None:
            tracks = []

        starred = self.connection.getStarred2()
        if "starred2" not in starred or "song" not in starred["starred2"]:
            return tracks

        song_entries = starred["starred2"]["song"]

        for entry in song_entries:
            self.log.info(
                f"Fetching Subsonic metadata for {entry.get('artist', 'Unknown')} - {entry.get('title', 'Unknown')}"
            )

            # Skip unknown tracks
            if (
                entry.get("title") == "[Unknown]"
                or entry.get("artist") == "[Unknown Artist]"
            ):
                continue

            track_year = None
            if "year" in entry:
                try:
                    track_year = int(entry["year"])
                except (ValueError, TypeError):
                    pass

            tracks.append(
                {
                    "artist": entry.get("artist", ""),
                    "title": entry.get("title", ""),
                    "album": entry.get("album"),
                    "year": track_year,
                }
            )

        return tracks

    def get_playlists(self):
        """Fetch all playlists from Subsonic server

        Returns:
            List of playlist dictionaries with 'id' and 'name' keys
        """
        result = self.connection.getPlaylists()
        if "playlists" not in result or "playlist" not in result["playlists"]:
            return []

        playlists = result["playlists"]["playlist"]
        # Handle case where there's only one playlist (returns dict instead of list)
        if isinstance(playlists, dict):
            playlists = [playlists]

        return playlists

    def get_playlist(self, playlist_id):
        """Fetch a specific playlist by ID

        Args:
            playlist_id: ID of the playlist to fetch

        Returns:
            Playlist dictionary with 'name' and 'entry' keys
        """
        result = self.connection.getPlaylist(playlist_id)
        if "playlist" not in result:
            return None

        playlist = result["playlist"]

        # Handle case where there are no entries in the playlist
        if "entry" not in playlist:
            playlist["entry"] = []
        # Handle case where there's only one entry (returns dict instead of list)
        elif isinstance(playlist["entry"], dict):
            playlist["entry"] = [playlist["entry"]]

        return playlist

    def create_playlist(self, name: str) -> str | None:
        """Create a new playlist.

        Args:
            name: Name of the playlist to create

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            result = self.connection.createPlaylist(name=name)
            if "playlist" in result:
                return result["playlist"].get("id")
            return None
        except Exception as e:
            self.log.error(f"Error creating playlist '{name}': {e}")
            return None

    def update_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace all tracks in a playlist with the provided track IDs.

        Args:
            playlist_id: ID of the playlist to update
            track_ids: List of track IDs to set as the playlist content

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current playlist to find number of tracks
            playlist = self.get_playlist(playlist_id)
            if not playlist:
                self.log.error(f"Playlist {playlist_id} not found")
                return False

            current_track_count = len(playlist.get("entry", []))

            # Remove all existing tracks by index (from end to start to avoid index shifting)
            if current_track_count > 0:
                indices_to_remove = list(range(current_track_count))
                self.connection.updatePlaylist(
                    lid=playlist_id,
                    songIndexesToRemove=indices_to_remove
                )

            # Add new tracks
            if track_ids:
                self.connection.updatePlaylist(lid=playlist_id, songIdsToAdd=track_ids)

            return True
        except Exception as e:
            self.log.error(f"Error updating playlist {playlist_id}: {e}")
            return False

    def add_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to the end of a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of track IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            self.connection.updatePlaylist(lid=playlist_id, songIdsToAdd=track_ids)
            return True
        except Exception as e:
            self.log.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False

    def remove_from_playlist(self, playlist_id: str, indices: list[int]) -> bool:
        """Remove tracks at specific indices from a playlist.

        Args:
            playlist_id: ID of the playlist
            indices: List of track indices to remove (0-based)

        Returns:
            True if successful, False otherwise
        """
        try:
            self.connection.updatePlaylist(
                lid=playlist_id,
                songIndexesToRemove=indices
            )
            return True
        except Exception as e:
            self.log.error(f"Error removing tracks from playlist {playlist_id}: {e}")
            return False

    def get_all_tracks(self, limit: int | None = None) -> list[dict]:
        """Fetch all tracks from the Subsonic server (not just starred).

        Args:
            limit: Optional limit on number of tracks to fetch

        Returns:
            List of track dictionaries
        """
        all_tracks = []

        try:
            # Get all albums first
            albums = self.get_albums()

            for album_info in albums:
                # Get album details with tracks
                try:
                    # Use the album ID from get_albums if available
                    # Otherwise we need to search for it
                    album_list = self.connection.getAlbumList2(
                        "alphabeticalByArtist",
                        size=1,
                        offset=0
                    )

                    # For now, use a simpler approach: get random albums and their songs
                    # This is a workaround since we need album IDs
                    random_albums = self.connection.getAlbumList2(
                        "random",
                        size=500
                    )

                    if "albumList2" in random_albums and "album" in random_albums["albumList2"]:
                        for album in random_albums["albumList2"]["album"]:
                            album_id = album["id"]
                            album_details = self.connection.getAlbum(album_id)

                            if "album" in album_details and "song" in album_details["album"]:
                                songs = album_details["album"]["song"]
                                if isinstance(songs, dict):
                                    songs = [songs]

                                all_tracks.extend(songs)

                                if limit and len(all_tracks) >= limit:
                                    return all_tracks[:limit]

                    break  # Just do one pass for now

                except Exception as e:
                    self.log.warning(f"Error fetching tracks: {e}")
                    continue

        except Exception as e:
            self.log.error(f"Error fetching all tracks: {e}")

        return all_tracks
