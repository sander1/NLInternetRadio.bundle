NAME = 'NL Internet Radio'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
FEED = 'https://raw.github.com/sander1/NLInternetRadio.bundle/master/Contents/Resources/radio.xml'

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
	xml = XML.ElementFromURL(FEED)

	for item in xml.xpath('//item'):
		ext = item.xpath('./ext/text()')[0].lower()

		if ext not in ('aac', 'mp3'):
			continue

		title = item.xpath('./title/text()')[0]
		url = item.xpath('./url/text()')[0]

		try: thumb = item.xpath('./thumb/text()')[0]
		except: thumb = ''

		oc.add(CreateTrackObject(
			title = title,
			url = url,
			ext = ext,
			thumb = thumb
		))

	return oc

####################################################################################################
@route('/music/nlinternetradio/track')
def CreateTrackObject(title, url, ext, thumb, include_container=False):

	if ext == 'aac':
		container = Container.MP4
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
					PartObject(key=url)
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
