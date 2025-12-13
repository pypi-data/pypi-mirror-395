# Plexutil

CLI tool with helpful functions to manage a Plex server.


> [!NOTE]
> Installation is supported only for the following: 
> - Windows
> - Linux

> [!NOTE]
> Development requires a fully configured [Dotfiles](https://github.com/florez-carlos/dotfiles) dev environment <br>

## Table of Contents

* [Installation](#installation)
* [Configuration](#configuration)
  * [Required](#required)
  * [Optional](#optional)
    * [TV Series Language Override](#tv-series-language-override)
    * [Library Preferences](#library-preferences)
    * [Server Setting Preferences](#server-setting-preferences)
* [Usage](#usage)
  * [Creating a media library](#creating-a-media-library)
  * [Deleting a media library](#deleting-a-media-library)
  * [Creating a Playlist](#creating-a-playlist)
  * [Deleting a Playlist](#deleting-a-playlist)
  * [Adding songs to a Playlist](#adding-songs-to-a-playlist)
  * [Exporting/Importing Music Playlists](#exportingimporting-music-playlists)
* [Development](#development)
* [Config Location](#config-location)
* [Log Location](#log-location)


## Installation

```bash
pip install plexutil
```

## Configuration
### Required
Set the host, port, token of your plex server
```bash
plexutil config -host <PLEX_SERVER_HOST> -port <PLEX_SERVER_PORT> -token <PLEX_SERVER_TOKEN>
```
### Optional
#### TV Series Language Override
To override the language of tv series, modify the tv_language_manifest.json file found in: [Config Location](#config-location) <br >
The file can be modified like such:
```bash
{
  "es-ES": [327417,396583,388477,292262,282670,274522],
  "en-US": []
}
```
Where the key is the language and the list contains the [TVDB](https://www.thetvdb.com/) ids of the desired series to be overriden <br >
For a list of supported languages: [Language](./src/plexutil/enums/language.py)

---

#### Library Preferences
Libraries of type:
- Movie
- Music
- TV

Can have their preferences set in the following files:

- movie_library_preferences.json
- music_library_preferences.json
- tv_library_preferences.json

These files can be found here: [Config Location](#config-location) <br >
These Preferences are set at library creation time <br >
The files already include default preferences that can be removed/modified/added based on your needs <br >

---

#### Server Setting Preferences
These preferences modify the behavior of the server

- plex_server_setting_preferences.json

The file can be found here: [Config Location](#config-location) <br >
For example:
```json
"ButlerStartHour": 23,
```
Starts scheduled tasks at 11:00PM local time, to modify this time to 1:00AM
```json
"ButlerStartHour": 1,
```
These modifications need to be set by doing:
```bash
plexutil set_server_settings
```
The file already includes default preferences that can be removed/modified/added based on your needs <br >

---

## Usage
### Creating a media library:
> [!NOTE]
> If language is not supplied, the default is en-US
```bash
plexutil create_movie_library -libn <NAME_OF_THE_LIBRARY> -loc </PATH/TO/MEDIA/LOCATION> -l <LANGUAGE>
```
---

### Deleting a media library:
```bash
plexutil delete_movie_library -libn <NAME_OF_THE_LIBRARY>
```
---

### Creating a Playlist
> [!NOTE]
> Only Music Playlists are currently supported
```bash
plexutil create_music_playlist -libn <LIBRARY_NAME_WHERE_PLAYLIST_IS> -pn <NAME_OF_THE_PLAYLIST> -s /path/to/song.mp3 /path/to/another-song.mp3
```
> [!NOTE]
> The paths passed to -s must match the location of the library <br >
> Therefore, if the library has for location /media/music these song paths must be in /media/music/song.mp3

---

### Deleting a Playlist
> [!NOTE]
> Only Music Playlists are currently supported
```bash
plexutil delete_music_playlist -libn <LIBRARY_NAME_WHERE_PLAYLIST_IS> -pn <NAME_OF_THE_PLAYLIST>
```

---

### Adding songs to a Playlist

```bash
plexutil add_songs_to_music_playlist -libn <LIBRARY_NAME_WHERE_PLAYLIST_IS> -pn <NAME_OF_THE_PLAYLIST> -s /path/to/song.mp3 /path/to/another-song.mp3
```
> [!NOTE]
> The paths passed to -s must match the location of the library <br >
> Therefore, if the library has for location /media/music these song paths must be in /media/music/song.mp3

---

### Exporting/Importing Music Playlists
Music Playlists can be exported to a playlists.db file, this file can later be imported to another Plex server with plexutil
```bash
plexutil export_music_playlist -libn <LIBRARY_NAME_WHERE_PLAYLISTS_ARE>
```
This action will create a playlists.db file here: [Config Location](#config-location) <br >
This file can then be used to recreate the playlists in another Plex Server with plexutil by doing
```bash
plexutil import_music_playlist -libn <LIBRARY_NAME_WHERE_PLAYLISTS_ARE>
```
> [!NOTE]
> The songs in the Music Library of the importing server must match the songs in the exporting server

---

## Development
```bash
source init.sh
```
## Config Location
The config directory of Plexutil is located:
> [!NOTE]
> Replace <YOUR_USER> with your Windows UserName
- Windows
```bash
C:\Users\<YOUR_USER>\Documents\plexutil\config\
```
- Linux
```bash
$HOME/plexutil/config/tv_language_manifest.json
```

## Log Location
The log directory of Plexutil is located:
> [!NOTE]
> Replace <YOUR_USER> with your Windows UserName
- Windows
```bash
C:\Users\<YOUR_USER>\Documents\plexutil\log
```
- Linux
```bash
$HOME/plexutil/log
```
> [!NOTE]
> Log files are archived based on date, such as yyyy-mm-dd.log

## License
[MIT](https://choosealicense.com/licenses/mit/)

