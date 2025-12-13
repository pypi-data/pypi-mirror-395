from logging import getLogger

from api_deezer import API as API_Deezer
from api_deezer.exceptions.data import Error_Data_404 as Deezer_Error_Data_404

from api_spotify import API as API_Spotify

from .aliases import spo_playlist_2_dee_tracks


class Music_Link_Conv:
	logger = getLogger('MUSIC_LINK_CONV')


	def __init__(
		self,
		spotify_client_id: str,
		spotify_client_secret: str
	) -> None:

		self.__spotify_client_id = spotify_client_id
		self.__spotify_client_secret = spotify_client_secret
		self.__api_dee = API_Deezer()
		self.__api_spo = API_Spotify(self.__spotify_client_id, self.__spotify_client_secret)


	def conv_spo_track_2_dee_track(self, id_track: str) -> str | None:
		spotify_data = self.__api_spo.get_track(id_track)
		isrc = spotify_data.external_ids.isrc

		if not isrc:
			return

		try:
			deezer_data = self.__api_dee.get_track_by_isrc(isrc)
		except Deezer_Error_Data_404:
			return

		return deezer_data.link


	def conv_spo_album_2_dee_album(self, id_album: str) -> str | None:
		spotify_data = self.__api_spo.get_album(id_album)
		upc = spotify_data.external_ids.upc

		if not upc:
			return

		try:
			deezer_data = self.__api_dee.get_album_by_upc(upc)
		except Deezer_Error_Data_404:
			return

		return deezer_data.link


	def conv_spo_artist_2_dee_artist(self, id_artist: str) -> str | None:
		spotify_data = self.__api_spo.get_artist(id_artist)
		artist = spotify_data.name
		deezer_data = None

		search = self.__api_dee.search(f'artist:\'{artist}\'')

		for found in search.results:
			if found.artist.name == artist:
				deezer_data = found.artist
				return deezer_data.link


	def conv_spo_playlist_2_dee_tracks(self, id_playlist: str) -> spo_playlist_2_dee_tracks:
		spotify_data = self.__api_spo.get_playlist(id_playlist)
		tracks: spo_playlist_2_dee_tracks = []
		is_next = spotify_data.tracks

		while is_next:
			for data in is_next.items:
				deezer_link = None
				c_isrc = data.track.external_ids.isrc

				if c_isrc is not None:
					try:
						c_dee_track = self.__api_dee.get_track_by_isrc(c_isrc)
						deezer_link = c_dee_track.link
					except Deezer_Error_Data_404:
						pass

				tracks.append(
					(data.track, deezer_link)
				)


			is_next = is_next.get_next()

		return tracks
