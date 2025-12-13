"""Jellyfin API client wrapper."""

import requests
from jellyfin_apiclient_python import JellyfinClient as JellyfinAPIClient


class JellyfinClient:
    """Wrapper around jellyfin-apiclient-python for easier use."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize Jellyfin client.

        Args:
            url: Jellyfin server URL
            username: Username for authentication
            password: Password for authentication
        """
        self.url = url
        self.username = username
        self.password = password

        self.client = JellyfinAPIClient()
        self.client.config.app("pushtunes", "0.6.0", "pushtunes-device", "pushtunes-1")

        # Initialize SSL config to avoid KeyError
        self.client.config.data['auth.ssl'] = True

        # Connect and authenticate
        self.client.auth.connect_to_address(self.url)
        result = self.client.auth.login(self.url, self.username, self.password)

        self.user_id = result["User"]["Id"]
        self.music_library_id = self._get_music_library_id()

    def _get_music_library_id(self) -> str | None:
        """Get the ID of the Music library.

        Returns:
            Music library ID or None if not found
        """
        folders_response = self.client.jellyfin.get_media_folders()

        if folders_response.get("Items"):
            for folder in folders_response["Items"]:
                if folder.get("CollectionType") == "music":
                    return folder.get("Id")

        return None

    def get_albums(self, limit: int | None = None) -> list[dict]:
        """Get all albums from the music library.

        Args:
            limit: Optional limit on number of albums to fetch

        Returns:
            List of album dictionaries
        """
        # Use the library's user_items() method with pagination
        all_albums = []
        start_index = 0
        batch_size = 100

        while True:
            params = {
                "IncludeItemTypes": "MusicAlbum",
                "Recursive": True,
                "StartIndex": start_index,
                "Limit": batch_size,
                "SortBy": "SortName",
            }

            response = self.client.jellyfin.user_items(params=params)

            items = response.get("Items", [])
            if not items:
                break

            all_albums.extend(items)

            # Check if we've fetched all albums
            total = response.get("TotalRecordCount", 0)
            if len(all_albums) >= total:
                break

            # Apply limit if specified and we've reached it
            if limit is not None and len(all_albums) >= limit:
                all_albums = all_albums[:limit]
                break

            start_index += batch_size

        return all_albums

    def get_tracks(self, limit: int | None = None) -> list[dict]:
        """Get favorite/starred tracks from the music library.

        Args:
            limit: Optional limit on number of tracks to fetch

        Returns:
            List of track dictionaries
        """
        # Use the library's user_items() method with pagination
        all_tracks = []
        start_index = 0
        batch_size = 100

        while True:
            params = {
                "IncludeItemTypes": "Audio",
                "Recursive": True,
                "Filters": "IsFavorite",
                "StartIndex": start_index,
                "Limit": batch_size,
            }

            response = self.client.jellyfin.user_items(params=params)

            items = response.get("Items", [])
            if not items:
                break

            all_tracks.extend(items)

            # Check if we've fetched all tracks
            total = response.get("TotalRecordCount", 0)
            if len(all_tracks) >= total:
                break

            # Apply limit if specified and we've reached it
            if limit is not None and len(all_tracks) >= limit:
                all_tracks = all_tracks[:limit]
                break

            start_index += batch_size

        return all_tracks

    def get_playlists(self) -> list[dict]:
        """Get all playlists.

        Returns:
            List of playlist dictionaries
        """
        response = self.client.jellyfin.get_items(
            {
                "UserId": self.user_id,
                "IncludeItemTypes": "Playlist",
                "Recursive": True,
            }
        )

        # Filter out non-music playlists if needed
        playlists = []
        for item in response.get("Items", []):
            # Skip library folders
            if item.get("Type") != "Playlist":
                continue
            playlists.append(item)

        return playlists

    def get_playlist_items(self, playlist_id: str) -> list[dict]:
        """Get tracks from a specific playlist.

        Args:
            playlist_id: ID of the playlist

        Returns:
            List of track dictionaries
        """
        # Use user_items with Recursive=True to get actual audio items
        # get_items returns library folders, which is not what we want
        response = self.client.jellyfin.user_items(params={
            "ParentId": playlist_id,
            "IncludeItemTypes": "Audio",
            "Recursive": True,
        })

        return response.get("Items", [])

    def create_playlist(self, name: str) -> str | None:
        """Create a new playlist.

        Args:
            name: Name of the playlist to create

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            # Create playlist using the Jellyfin HTTP API directly
            # The jellyfin-apiclient-python doesn't have a create_playlist method
            url = f"{self.url}/Playlists"
            headers = self.client.jellyfin.get_default_headers()
            headers["Content-Type"] = "application/json"

            response = requests.post(
                url,
                json={
                    "Name": name,
                    "UserId": self.user_id,
                    "MediaType": "Audio"
                },
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            return result.get("Id")
        except Exception as e:
            print(f"Error creating playlist '{name}': {e}")
            return None

    def add_items_to_playlist(self, playlist_id: str, item_ids: list[str]) -> bool:
        """Add items to a playlist.

        Args:
            playlist_id: ID of the playlist
            item_ids: List of item IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            # Use HTTP API directly - Jellyfin expects comma-separated IDs as query param
            ids_param = ",".join(item_ids)
            # Include userId parameter which is required by Jellyfin API
            url = f"{self.url}/Playlists/{playlist_id}/Items?userId={self.user_id}&ids={ids_param}"
            headers = self.client.jellyfin.get_default_headers()

            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error adding items to playlist {playlist_id}: {e}")
            return False

    def remove_from_playlist(self, playlist_id: str, entry_ids: list[str]) -> bool:
        """Remove specific entries from a playlist.

        Args:
            playlist_id: ID of the playlist
            entry_ids: List of entry IDs to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            # Use HTTP API directly - remove each entry individually via DELETE
            headers = self.client.jellyfin.get_default_headers()

            for entry_id in entry_ids:
                url = f"{self.url}/Playlists/{playlist_id}/Items?entryIds={entry_id}"
                response = requests.delete(url, headers=headers)
                response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error removing items from playlist {playlist_id}: {e}")
            return False
