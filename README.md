python-opensubtitles
===

Simple module to access to the [OpenSubtitles.org](http://opensubtitles.org)
subtitles database. This class is a wrapper to the common methods at OS.

# Configuring the test environment
    >>> class Test(object):
    ...     username = 'doctest'
    ...     password = 'doctest'
    ...     # Remember to change the video path if you want to run the test!
    ...     video = ('/home/alex/Videos/'
    ...              'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo/'
    ...              'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.mp4')

# First steps

    >>> from pythonopensubtitles.opensubtitles import OpenSubtitles
    >>> os = OpenSubtitles()

# Login

    >>> token = os.login('bad@mail.com', 'badpassword')
    >>> token
    >>> token = os.login(Test.username, Test.password)
    >>> assert type(token) == str

# Logout

    >>> os.logout(token)
    True

# Creating a video hash

    >>> from pythonopensubtitles.utils import File
    >>> f = File(Test.video)
    >>> hash = f.get_hash()
    >>> assert type(hash) == str

# Getting video size

    >>> size = f.size
    >>> assert type(size) == long

# Search subtitles

    >>> data = os.search_subtitles(token, [{'sublanguageid': 'all', 'moviehash': hash, 'moviebytesize': size}])
    >>> assert ('200' in data.get('status')) == True
    >>> assert type(data) == dict
