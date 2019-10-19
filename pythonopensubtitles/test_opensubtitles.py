from pythonopensubtitles.opensubtitles import *

import base64
import json
import os
import tempfile
import unittest
import zlib


class MockServerProxy:
    pass

class TestOpenSubtitles(unittest.TestCase):
    def setUp(self):
        self.mock = MockServerProxy()
        self.ost = OpenSubtitles()
        self.ost.xmlrpc = self.mock

    def test_login(self):
        self.mock.LogIn = lambda *_: {
            'status': '403',
        }
        assert self.ost.login('good@mail.com', 'goodpassword') is None

        self.mock.LogIn = lambda *_: {
            'status': '200 OK',
            'token': 'token',
        }
        assert self.ost.login('good@mail.com', 'goodpassword') == 'token'
        
    def test_search_subtitles(self):
        self.mock.SearchSubtitles = lambda *_: fixture('search_subtitles')
        
        data = self.ost.search_subtitles([])
        
        assert len(data) == 1
        assert data[0].get('IDSubtitle') == '7783633'
        assert data[0].get('IDSubtitleFile') == '1956355942'
        assert data[0].get('IDSubMovieFile') == '19353776'

    def test_search_imdb(self):
        self.mock.SearchMoviesOnIMDB = lambda *_: {
            'status': '200 OK',
            'data': [
                {
                    'IDMovieImdb': 'id',
                }
            ]
        }

        # TODO: not sure if these are the right params. I am just keeping the test because it was on the README
        data = self.ost.search_movies_on_imdb([])
        assert data[0].get('IDMovieImdb') == 'id'

    def test_no_operation(self):
        self.mock.NoOperation = lambda *_: {'status': '200 OK'}
        assert self.ost.no_operation()

    def test_logout(self):
        self.mock.LogOut = lambda *_: {'status': '403'}
        assert not self.ost.logout()

        self.mock.LogOut = lambda *_: {'status': '200 OK'}
        assert self.ost.logout()

    def test_auto_update(self):
        self.mock.AutoUpdate = lambda *_: {
            'status': '200 OK',
            'version': 'something',
        }
        data = self.ost.auto_update('SubDownloader')
        assert 'version' in data.keys()

    def test_already_exists(self):
        self.mock.TryUploadSubtitles = lambda *_: {
            'status': '403',
        }
        # TODO: The error here is unauthorized and not that the subtitle wasn't found,
        # however, for not breaking compatibility we will keep it this way for now.
        assert not self.ost.try_upload_subtitles([])

        self.mock.TryUploadSubtitles = lambda *_: {
            'status': '200 OK',
            'alreadyindb': 1,
        }
        assert self.ost.try_upload_subtitles([])

    def test_upload_subtitles(self):
        self.mock.UploadSubtitles = lambda *_: {
            'status': '200 OK',
            'data': {
                'url': 'http://example.com',
            },
        }
        data = self.ost.upload_subtitles([])
        assert 'url' in data.keys()

    def test_check_subtitle_hash(self):
        self.mock.CheckSubHash = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        data = self.ost.check_subtitle_hash([])
        assert data == {}
    
    def test_check_movie_hash(self):
        self.mock.CheckMovieHash = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        data = self.ost.check_movie_hash([])
        assert data == {}

    def test_insert_movie_hash(self):
        self.mock.InsertMovieHash = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        data = self.ost.insert_movie_hash([])
        assert data == {}

    def test_report_wrong_movie_hash(self):
        self.mock.ReportWrongMovieHash = lambda *_: {
            'status': '419',
        }
        assert not self.ost.report_wrong_movie_hash([])

        self.mock.ReportWrongMovieHash = lambda *_: {
            'status': '200 OK',
        }
        assert self.ost.report_wrong_movie_hash([])

    def test_report_wrong_movie_hash(self):
        self.mock.ReportWrongMovieHash = lambda *_: {
            'status': '404',
        }
        assert not self.ost.report_wrong_movie_hash('hash')

        self.mock.ReportWrongMovieHash = lambda *_: {
            'status': '200 OK',
        }
        assert self.ost.report_wrong_movie_hash('hash')

    def test_get_subtitle_languages(self):
        self.mock.GetSubLanguages = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        assert self.ost.get_subtitle_languages() == {}

    def test_get_available_translations(self):
        self.mock.GetAvailableTranslations = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        assert self.ost.get_available_translations('SubDownloader') == {}

    def test_subtitles_votes(self):
        self.mock.SubtitlesVote = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        assert self.ost.subtitles_votes({}) == {}

    def test_get_comments(self):
        self.mock.GetComments = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        assert self.ost.get_comments([]) == {}

    def test_add_comment(self):
        self.mock.AddComment = lambda *_: {
            'status': '403',
        }
        assert not self.ost.add_comment({})

        self.mock.AddComment = lambda *_: {
            'status': '200 OK',
        }
        assert self.ost.add_comment({})

    def test_add_request(self):
        self.mock.AddRequest = lambda *_: {
            'status': '200 OK',
            'data': {},
        }
        assert self.ost.add_request({}) == {}

    def test_download_subtitles(self):
        self.mock.DownloadSubtitles = lambda *_: fixture('download_subtitles')
        with tempfile.TemporaryDirectory() as tmpdirname:
            data = self.ost.download_subtitles(['id'], output_directory=tmpdirname)
        
        assert data, data

def fixture(name):
    fullpath = os.path.join(os.path.dirname(__file__), 'fixtures', name+'.json')
    with open(fullpath) as f:
        return json.load(f)