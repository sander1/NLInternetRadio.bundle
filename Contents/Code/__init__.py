NAME = 'NL Internet Radio'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = 0

####################################################################################################
@handler('/music/nlinternetradio', NAME, thumb=ICON, art=ART)
def MainMenu():

	oc = ObjectContainer()
	json_obj = JSON.ObjectFromString(Resource.Load('radio.json'))

	for station in json_obj:

		if station['ext'] not in ('aac', 'mp3'):
			continue

		if 'thumb' in station:
			thumb = station['thumb']
		else:
			thumb = ''

		oc.add(CreateTrackObject(
			title = station['title'],
			url = station['url'],
			ext = station['ext'],
			thumb = thumb
		))

	return oc

####################################################################################################
@route('/music/nlinternetradio/track')
def CreateTrackObject(title, url, ext, thumb, include_container=False):

	if ext == 'aac':
		container = 'aac'
		audio_codec = AudioCodec.AAC
	else:
		container = 'mp3'
		audio_codec = AudioCodec.MP3

	track_obj = TrackObject(
		key = Callback(CreateTrackObject, title=title, url=url, ext=ext, thumb=thumb, include_container=True),
		rating_key = url,
		title = title,
		thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON),
		items = [
			MediaObject(
				parts = [
					PartObject(key=Callback(Play, url=url, extension=ext))
				],
				container = container,
				audio_codec = audio_codec,
				audio_channels = 2
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_obj])
	else:
		return track_obj

####################################################################################################
@route('/music/nlinternetradio/play.{extension}')
def Play(url, extension):

	return Redirect(url)
