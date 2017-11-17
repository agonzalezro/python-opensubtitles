import pytest
from os import path


class TestPythonOpenSubtitles(object):
    @staticmethod
    @pytest.fixture
    def data():
        class Data:
            username = 'doctest'
            password = 'doctest'
            name = 'Dark City'
            path = '/home/alex/Videos/Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo/'
            video = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.mp4'
            subtitle = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.srt'
        return Data

    @staticmethod
    @pytest.fixture
    def os():
        from pythonopensubtitles.opensubtitles import OpenSubtitles
        return OpenSubtitles()

    @staticmethod
    @pytest.fixture
    def file(data):
        from pythonopensubtitles.utils import File
        return File(path.join(data.path, data.video))

    # Login
    @staticmethod
    def test_login(data, os):
        token = os.login('bad@mail.com', 'badpassword')
        assert token is None
        token = os.login(data.username, data.password)
        assert type(token) == str

    # Creating a video hash
    @staticmethod
    def test_video_hash(file):
        hash = file.get_hash()
        assert type(hash) == str

    # Getting video size
    @staticmethod
    def test_video_size(file):
        size = file.size
        assert type(size) == str  # As str is easier to deal with long sizes
        assert int(size)  # But even being a string, it can be casted
        return size

    # Search subtitles
    def test_search_subtitles(self, file, os):
        size = self.test_video_size(file)
        data = os.search_subtitles([{'sublanguageid': 'all', 'moviehash': hash, 'moviebytesize': size}])
        assert type(data) == list
        return data

    # Getting the IMDB id
    def test_imdb_id(self, file, os):
        data = self.test_search_subtitles(file, os)
        imdb_id = int(data[0].get('IDMovieImdb'))
        assert type(imdb_id) == int
        return imdb_id

    # Search a movie at IMDB
    @staticmethod
    def search_movie_imdb(os, data):
        data = os.search_movies_on_imdb(data.name)
        assert type(data) == dict

    # Get MD5 from a subtitle
    @staticmethod
    def test_subtitle_md5(data):
        from pythonopensubtitles.utils import get_md5

        md5 = get_md5(path.join(data.path, data.subtitle))
        assert type(md5) == str
        return md5

    # Upload subtitles
    def test_upload_subtitles(self, os, data, file):
        md5 = self.test_subtitle_md5(data)
        size = self.test_video_size(file)

        params = [{'cd1': [{'submd5hash': md5,
                            'subfilename': data.subtitle,
                            'moviehash': hash,
                            'moviebytesize': size}]}]
        already_in_db = os.try_upload_subtitles(params)
        assert type(already_in_db) == bool

        # Upload subtitles
        if not already_in_db:
            from pythonopensubtitles.utils import get_gzip_base64_encoded

            imdb_id = self.test_imdb_id(file, os)
            params = {'baseinfo': {
                          'idmovieimdb': imdb_id},
                      'cd1': {
                          'subhash': md5,
                          'subfilename': data.subtitle,
                          'moviehash': hash,
                          'moviebytesize': size,
                          'moviefilename': data.video,
                          'subcontent': get_gzip_base64_encoded(path.join(data.path, data.subtitle))}}
            url = os.upload_subtitles(params)
            assert type(url) == str

    # Ping the server
    @staticmethod
    def test_ping_server(os):
        os.no_operation()

    # Auto update
    @staticmethod
    def test_auto_update(os):
        data = os.auto_update('SubDownloader')
        assert 'version' in data.keys()

    # Logout
    @staticmethod
    def test_logout(os):
        os.logout()
