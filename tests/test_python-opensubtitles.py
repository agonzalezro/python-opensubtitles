# Configuring the test environment

from os import path
class Test(object):
	username = 'doctest'
    password = 'doctest'
    # Remember to change the video path if you want to run the test!     
    name = 'Dark City'
    path = ('/home/alex/Videos/' 
    	    'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo/')
    video = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.mp4'
    subtitle = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.srt'

# First steps

from pythonopensubtitles.opensubtitles import OpenSubtitles
os = OpenSubtitles()

# Login

token = os.login('bad@mail.com', 'badpassword')
assert token == None
token = os.login(Test.username, Test.password)
assert type(token) == str

# Creating a video hash

from pythonopensubtitles.utils import File
f = File(path.join(Test.path, Test.video))
hash = f.get_hash()
assert type(hash) == str

# Getting video size

size = f.size
assert type(size) == str  # As str is easier to deal with long sizes
assert long(size)  # But even being a string, it can be casted

# Search subtitles

data = os.search_subtitles([{'sublanguageid': 'all', 'moviehash': hash, 'moviebytesize': size}])
assert type(data) == list

# Getting the IMDB id

imdb_id = int(data[0].get('IDMovieImdb'))
assert type(imdb_id) == int

# Search a movie at IMDB

data = os.search_movies_on_imdb(Test.name)
assert type(data) == dict

# Get MD5 from a subtitle

from pythonopensubtitles.utils import get_md5
md5 = get_md5(path.join(Test.path, Test.subtitle))
assert type(md5) == str


# Try to upload subtitles

params = [{'cd1': [{'submd5hash': md5,
                    'subfilename': Test.subtitle,
                    'moviehash': hash,
                    'moviebytesize': size}]}]
already_in_db = os.try_upload_subtitles(params)
assert type(already_in_db) == bool

# Upload subtitles

from pythonopensubtitles.utils import get_gzip_base64_encoded
if not already_in_db:
    params = {'baseinfo': {
                  'idmovieimdb': imdb_id},
              'cd1': {
                  'subhash': md5,
                  'subfilename': Test.subtitle,
                  'moviehash': hash,
                  'moviebytesize': size,
                  'moviefilename': Test.video,
                  'subcontent': get_gzip_base64_encoded(path.join(Test.path, Test.subtitle))}}
    url = os.upload_subtitles(params)
    assert type(url) == str

# Ping the server

os.no_operation()

# Auto update

data = os.auto_update('SubDownloader')
assert 'version' in data.keys()

# Logout

os.logout()
