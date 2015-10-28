python-opensubtitles
===

Simple module to access to the [OpenSubtitles.org](http://opensubtitles.org)
subtitles database. This class is a wrapper to the common methods at OS.

# Installing Notes

If you are installing this using `pip`, please use the following format:
`pip install -e git+https://github.com/agonzalezro/python-opensubtitles#egg=python-opensubtitles`

# Configuring the test environment

Before start to running the test (if you are only reading the documentation,
of course, you don't need to do it :D) you must provide a correct video path
and subtitle path.

    >>> from os import path
    >>> class Test(object):
    ...     username = 'doctest'
    ...     password = 'doctest'
    ...     # Remember to change the video path if you want to run the test!
    ...     name = 'Dark City'
    ...     path = ('/home/alex/Videos/'
    ...             'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo/')
    ...     video = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.mp4'
    ...     subtitle = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.srt'

# First steps

Typicall import and creation of the OpenSubitles wrapper.

    >>> from pythonopensubtitles.opensubtitles import OpenSubtitles
    >>> os = OpenSubtitles()

# Login

To most of the OpenSubtitles methods you must send a token, this token is given
to you by the api after the use of the login method.

    >>> token = os.login('bad@mail.com', 'badpassword')
    >>> assert token == None
    >>> token = os.login(Test.username, Test.password)
    >>> assert type(token) == str

This token will be saved as an attrib of the OpenSubtitle class, so you don't
need to send it always to the methods.

# Creating a video hash

To search subtitles, upload subtitles... a video hash token must be provided.
You can find a generator under this module utils.

    >>> from pythonopensubtitles.utils import File
    >>> f = File(path.join(Test.path, Test.video))
    >>> hash = f.get_hash()
    >>> assert type(hash) == str

# Getting video size

    >>> size = f.size
    >>> assert type(size) == str  # As str is easier to deal with long sizes
    >>> assert long(size)  # But even being a string, it can be casted

# Search subtitles

If you search for a subtitle you will receive a list of all the subtitles saved
at server.

    >>> data = os.search_subtitles([{'sublanguageid': 'all', 'moviehash': hash, 'moviebytesize': size}])
    >>> assert type(data) == list

# Getting the IMDB id

The info that you got on the method above provides you a imdb id, you must get
it to try to upload subtitles.

    >>> imdb_id = int(data[0].get('IDMovieImdb'))
    >>> assert type(imdb_id) == int

# Search a movie at IMDB

If you don't know the imdb (perhaps the film is very new and it doesn't have
subtitles yet), you can search it providing the film name.

    >>> data = os.search_movies_on_imdb(Test.name)
    >>> assert type(data) == dict

# Get MD5 from a subtitle

To know if the subtitle was uploaded correctly, a md5 of the file must be
provided.

    >>> from pythonopensubtitles.utils import get_md5
    >>> md5 = get_md5(path.join(Test.path, Test.subtitle))
    >>> assert type(md5) == str

# Try to upload subtitles

Before upload a subtitle you always need to check if it exists on the database:

    >>> params = [{'cd1': [{'submd5hash': md5,
    ...                     'subfilename': Test.subtitle,
    ...                     'moviehash': hash,
    ...                     'moviebytesize': size}]}]
    >>> already_in_db = os.try_upload_subtitles(params)
    >>> assert type(already_in_db) == bool

# Upload subtitles

If the subtitle isn't on the database yet, you can upload it with the method
``upload_subtitles``.

You can take the ``cd1`` params from the method above, but for the documentation
is more clear do it this way:

    >>> from pythonopensubtitles.utils import get_gzip_base64_encoded
    >>> if not already_in_db:
    ...     params = {'baseinfo': {
    ...                   'idmovieimdb': imdb_id},
    ...               'cd1': {
    ...                   'subhash': md5,
    ...                   'subfilename': Test.subtitle,
    ...                   'moviehash': hash,
    ...                   'moviebytesize': size,
    ...                   'moviefilename': Test.video,
    ...                   'subcontent': get_gzip_base64_encoded(path.join(Test.path, Test.subtitle))}}
    ...     url = os.upload_subtitles(params)
    ...     assert type(url) == str

# Ping the server

Each 15 minutes you need to ping the server to show that you are alive. To do
it use the metho no\_operation:

    >>> os.no_operation()
    True

# Auto update

Get info of the last version of one of the porgrams at OpenSubtitiles DB.

    >>> data = os.auto_update('SubDownloader')
    >>> assert 'version' in data.keys()

# Logout

You can remove your session token with this method:

    >>> os.logout()
    True
