# python-opensubtitles

Simple module to access to the [OpenSubtitles.org](http://opensubtitles.org)
subtitles database. This class is a wrapper for the common methods used by the OpenSubtitles API.

## Install Notes

If you are installing this module with `pip`, please use the following path to use the latest version:
```
pip install -e git+https://github.com/agonzalezro/python-opensubtitles#egg=python-opensubtitles
```

## Configuring the test environment

Before you start running tests (if you are only reading the documentation, of course, you don't need to do it :D), you must provide a correct video path and subtitle path.

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

## First steps

Example for a typical import and creation of the OpenSubitles wrapper:

    >>> from pythonopensubtitles.opensubtitles import OpenSubtitles
    >>> ost = OpenSubtitles()

## Login

For most OpenSubtitles methods you must send a token. This token is given to you by the API after the use of the login method.

    >>> token = ost.login('bad@mail.com', 'badpassword')
    >>> assert token == None
    >>> token = ost.login(Test.username, Test.password)
    >>> assert type(token) == str

The token will be saved as an attribute of the OpenSubtitle class, so you don't need to send it again when using other methods.

## Creating a video hash

To search for subtitles for a specific file, a hash token for this file must be provided. You can find a file hash generator in this module's `utils`.

    >>> from pythonopensubtitles.utils import File
    >>> f = File(path.join(Test.path, Test.video))
    >>> hash = f.get_hash()
    >>> assert type(hash) == str

## Getting video size

    >>> size = f.size
    >>> assert type(size) == str  # As str is easier to deal with long sizes
    >>> assert long(size)  # But even being a string, it can be casted

## Search for subtitles

If you do a simple search for a subtitle, you will receive a list of all matching subtitles saved on the server.

    >>> data = ost.search_subtitles([{'sublanguageid': 'all', 'moviehash': hash, 'moviebytesize': size}])
    >>> id_subtitle = data[0].get('IDSubtitle')
    >>> id_subtitle_file = data[0].get('IDSubtitleFile')
    >>> id_sub_movie_file = data[0].get('IDSubMovieFile')
    >>> assert type(data) == list

## Getting the IMDb ID

The info you received with the search method also includes an IMDb ID, which you need if you want to try to upload subtitles.

    >>> imdb_id = int(data[0].get('IDMovieImdb'))
    >>> assert type(imdb_id) == int

## Search for a movie on IMDb

If you don't know the IMDb ID and cannot get it through opensubtitles.org – perhaps the film is very new and no-one has uploaded any subtitles for it yet –, you can search for it directly in IMDb's database by providing the film's name.

    >>> data = ost.search_movies_on_imdb(Test.name) # doctest: +SKIP
    >>> assert type(data) == dict # doctest: +SKIP


## Get MD5 for a subtitle file

To make sure a subtitle was uploaded correctly, an MD5 hash of the file must be provided.

    >>> from pythonopensubtitles.utils import get_md5
    >>> md5 = get_md5(path.join(Test.path, Test.subtitle))
    >>> assert type(md5) == str

## Upload of subtitles

### Check for existence of subtitle first

Before uploading a subtitle, you always need to check if it already exists on opensubtitles.org:

    >>> params = [{'cd1': [{'submd5hash': md5,
    ...                     'subfilename': Test.subtitle,
    ...                     'moviehash': hash,
    ...                     'moviebytesize': size}]}]
    >>> already_in_db = ost.try_upload_subtitles(params)
    >>> assert type(already_in_db) == bool

### Actual file upload

If the subtitle does not yet exist on opensubtitles.org, you can upload it with the method ``upload_subtitles``. For this, you can take the ``cd1`` parameters from the method for checking for the existence of a subtitle.

For documentation purposes, it is more clear to do it this way:

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
    ...     url = ost.upload_subtitles(params)
    ...     assert type(url) == str


## Download of subtitles

Download subtitles from opensubtitles.org:

    >>> data = ost.download_subtitles([id_subtitle_file], override_filenames={id_subtitle_file: 'output_filename.srt'}, output_directory='PATH/TO/DIR', extension='srt')
    >>> assert type(data) == dict

The only required parameter is a list of IDs of subtitle files.

The optional parameters include an option to override the original file names of the subtitle files, the provision of a specific download directory and the subtitle type in the form of the file extension (if the original file names are kept).

Note that OpenSubtitles restricts downloads of subtitle files to 20 at a time.


## Check if subtitle hash exists.

Check if multiple subtitles exist on opensubtitles.org at once by passing the MD5 hash of all subtitle files as parameter.

    >>> data = ost.check_subtitle_hash([md5])
    >>> assert type(data) == dict


## Check Movie Hash

Get movie information by using the hash of movie file.

    >>> data = ost.check_movie_hash([hash])
    >>> assert type(data) == dict


## Insert Movie hash

Insert or update movie data on opensubtitles.org.
moviehash,moviebytesize,and imdbid are required prameters rest are
optional.

    >>> data = ost.insert_movie_hash([{'moviehash':hash,'moviebytesize':size,'imdbid':imdb_id}])
    >>> assert type(data) == dict

## Report wrong movie hash

If you find that the movie hash of subtitle file data is incorrect or is for some other release or version use this method to report it.Once enough people report, hash will be deleted from opensubtitles.org.

    >>> ost.report_wrong_movie_hash(id_sub_movie_file)
    True


## Get subtitle languages

Get all subtitle languages supported by opensubtitles.org.
Returns language name, sub language id and iso639 code.

    >>> data = ost.get_subtitle_languages()
    >>> assert type(data) == list


## Available translations

Get all the available translations for a program.

    >>> data = ost.get_available_translations('SubDownloader')
    >>> assert type(data) == dict


## Search Movie information from IMDB

This method can be used to retrive movie information available on IMDB.
Opensubtitles.org uses external program for retrieving info for every query.
Overuse of this function can result in UserAgent being disabled, instead use some 3rd party library for retrieving info from IMDB.

    >>> data = ost.get_imdb_movie_details(imdb_id) # doctest: +SKIP
    >>> assert type(data) == dict # doctest: +SKIP


## Rate subtitle

Allows logged in users to vote subtitles.
Score must be between 1 to 10.

    >>> data = ost.subtitles_votes({'idsubtitle':id_subtitle,'score':'5'})
    >>> assert type(data) == dict


## Get Comments

Retrive comments about subtitles using subtitle id.

    >>> data = ost.get_comments([id_subtitle])
    >>> assert type(data) == dict


## Add a comment

Allows logged in users to comment on subtitles.
Optional 'badsubtitles' field can be set to 1 to flag subtitle as bad.

    >>> ost.add_comment({'idsubtitle':id_subtitle,'comment':'Thanks'})
    True


## Request for new subtitle

You can request for a new subtitle in case it doesn't exit on opensubtitles.org
Use this method only if subtitle was not found for a given IMDB not moviehash.
Optional 'comment' can be passed in dictionary to indicate movie release name.

    >>> data = ost.add_request({'sublanguageid':'eng','idmovieimdb':imdb_id})
    >>> assert type(data) == dict


## Pinging the server

Every 15 minutes, you need to ping the server to show that you are alive. To do this, use the method `no_operation`:

    >>> ost.no_operation()
    True


## Get info for OpenSubtitles software

Get info for the latest version of one of the programs listed on opensubtitles.org.

    >>> data = ost.auto_update('SubDownloader')
    >>> assert 'version' in data.keys()

## Logout

You can remove your session token with this method:

    >>> ost.logout()
    True
