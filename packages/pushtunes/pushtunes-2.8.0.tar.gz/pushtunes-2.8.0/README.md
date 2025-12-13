# Pushtunes

Pushtunes is a small tool to push your music from local sources (Subsonic-compatible server/Navidrome, Jellyfin, a CSV file, etc.) to music streaming services. It can also back up your music libraries to CSV files and restore them later. Currently Spotify, YouTube Music, and Tidal are supported. See "Music streaming services" below for more.

Documentation is also available in an easy-to-browse style on [Read the Docs](https://pushtunes.readthedocs.io/en/stable/), if you prefer.


## Installation

With any pip-like environment (pip, uv, etc.) it should be as easy as:

```
pip install pushtunes
```

See [Installation](docs/Installation.md) for more examples or how to install from source instead.


## Usage

Set your music service and source credentials (see [Getting Started](docs/Getting-Started.md) and, for example:

```bash
# Push albums from Subsonic to Spotify
pushtunes push albums --from subsonic --to spotify

# Push individual tracks (starred/favorites) from Subsonic to Spotify
pushtunes push tracks --from subsonic --to spotify

# Push playlists from Subsonic to Spotify, YouTube Music, or Tidal
pushtunes push playlist --from subsonic --playlist-name=myplaylist --to spotify
pushtunes push playlist --from subsonic --playlist-name=myplaylist --to ytm
pushtunes push playlist --from subsonic --playlist-name=myplaylist --to tidal

# Push from CSV file
pushtunes push tracks --from csv --csv-file=tracks.csv --to spotify
```

See `pushtunes --help`, `pushtunes push albums --help`, `pushtunes push tracks --help`, or `pushtunes push playlist --help` for more options.

There are many advanced features such as:

 * [Mapping items that can't be found](docs/Mappings.md)
 * [Filtering what gets skipped](docs/Filters.md)
 * [Deleting things that aren't in the source](docs/Deleting.md)
 * [Managing and syncing playlists from Subsonic/Jellyfin/CSV](docs/Playlists.md)
 * [Cross-Service Playlists](Cross-Service-Playlists.md) for direct syncing between YTM and Spotify without going through intermediary files
 * [Exporting problematic items to CSV for debugging and fixing](docs/Export-CSV.md)


## Music sources

* Subsonic (including Navidrome, Airsonic, etc.)
* Jellyfin
* CSV files

## Music streaming services

* Spotify
* YouTube Music
* Tidal

The streaming service market is in a very sad state of affairs regarding APIs. Spotify and Tidal have good ones, YouTube Music is almost unusable and working with it is only possible thanks to the people who maintain the unofficial ytmusicapi library. Deezer and Qobuz don't allow anyone to use their API anymore, requests for API keys go unanswered, documentation is being deleted and no up to date libraries exist.

Your main choices are Spotify, YouTube Music, and Tidal.

## More documentation

[Head over to our Read The Docs page](https://pushtunes.readthedocs.io/en/stable/).
