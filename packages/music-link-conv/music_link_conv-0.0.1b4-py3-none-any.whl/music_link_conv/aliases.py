from api_spotify.types import Track


type spo_playlist_2_dee_tracks = list[
	tuple[Track, str | None]
]
