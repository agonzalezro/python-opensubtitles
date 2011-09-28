from xmlrpclib import ServerProxy

from settings import Settings


class OpenSubtitles(object):
    '''OpenSubtitles API wrapper.

    Please check the official API documentation at:
    http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
    '''

    def __init__(self, language=None):
        self.xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER,
                                  allow_none=True)
        self.language = language or Settings.LANGUAGE

    def get_from_data_or_none(self, key):
        '''Return the key getted from data if the status is 200,
        otherwise return None.
        '''
        status = self.data.get('status').split()[0]
        return self.data.get(key) if '200' == status else None

    def login(self, username, password):
        '''Returns token is login is ok, otherwise None.
        '''
        self.data = self.xmlrpc.LogIn(username, password,
                                 self.language, Settings.USER_AGENT)
        return self.get_from_data_or_none('token')

    def logout(self, token):
        '''Returns True is logout is ok, otherwise None.
        '''
        data = self.xmlrpc.LogOut(token)
        return '200' in data.get('status')

    def search_subtitles(self, token, params):
        '''Returns a list with the subtitles info.
        '''
        self.data = self.xmlrpc.SearchSubtitles(token, params)
        return self.get_from_data_or_none('data')

    def try_upload_subtitles(self, token, params):
        '''Return True if the subtitle is on database, False if not.
        '''
        self.data = self.xmlrpc.TryUploadSubtitles(token, params)
        return self.get_from_data_or_none('alreadyindb') == 1

    def upload_subtitles(self, token, params):
        '''Returns the URL of the subtitle in case that the upload is OK,
        other case returns None.
        '''
        self.data = self.xmlrpc.UploadSubtitles(token, params)
        return self.get_from_data_or_none('data')

    def search_movies_on_imdb(self, token, params):
        self.data = self.xmlrpc.SearchMoviesOnIMDB(token, params)
        return self.data

    def search_to_mail(self):
        # array SearchToMail( $token, array( $sublanguageid, $sublanguageid, ...), array( array( 'moviehash' => $moviehash, 'moviesize' => $moviesize), array( 'moviehash' => $moviehash, 'moviesize' => $moviesize), ...) )'
        raise NotImplementedError

    def check_subtitle_hash(self):
        # array CheckSubHash( $token, array($subhash, $subhash, ...) )
        raise NotImplementedError

    def check_movie_hash(self):
        # array CheckMovieHash( $token, array($moviehash, $moviehash, ...) )
        raise NotImplementedError

    def check_movie_hash_2(self):
        # array CheckMovieHash2( $token, array($moviehash, $moviehash, ...) )
        raise NotImplementedError

    def insert_movie_hash(self):
        # array InsertMovieHash( $token, array( array('moviehash' => $moviehash, 'moviebytesize' => $moviebytesize, 'imdbid' => $imdbid, 'movietimems' => $movietimems, 'moviefps' => $moviefps, 'moviefilename' => $moviefilename), array(...) ) )
        raise NotImplementedError

    def detect_language(self):
        # array DetectLanguage( $token, array($text, $text, ...) )
        raise NotImplementedError

    def download_subtitles(self):
        # array DownloadSubtitles( $token, array($IDSubtitleFile, $IDSubtitleFile,...) )
        raise NotImplementedError

    def report_wrong_movie_hash(self):
        # array ReportWrongMovieHash( $token, $IDSubMovieFile )
        raise NotImplementedError

    def get_subtitle_languages(self):
        # array GetSubLanguages( $language = 'en' )
        raise NotImplementedError

    def get_available_translations(self):
        # array GetAvailableTranslations( $token, $program )
        raise NotImplementedError

    def get_translation(self):
        # array GetTranslation( $token, $iso639, $format, $program )
        raise NotImplementedError

    def get_imdb_movie_details(self):
        # array GetIMDBMovieDetails( $token, $imdbid )
        raise NotImplementedError

    def insert_movie(self):
        # array InsertMovie( $token, array('moviename' => $moviename, 'movieyear' => $movieyear) )
        raise NotImplementedError

    def subtitles_vote(self):
        # array SubtitlesVote( $token, array('idsubtitle' => $idsubtitle, 'score' => $score) )
        raise NotImplementedError

    def get_comments(self):
        # array GetComments( $token, array($idsubtitle, $idsubtitle, ...))
        raise NotImplementedError

    def add_comment(self):
        # array AddComment( $token, array('idsubtitle' => $idsubtitle, 'comment' => $comment, 'badsubtitle' => $int) )
        raise NotImplementedError

    def add_request(self):
        # array AddRequest( $token, array('sublanguageid' => $sublanguageid, 'idmovieimdb' => $idmovieimdb, 'comment' => $comment ) )
        raise NotImplementedError

    def auto_update(self):
        # array AutoUpdate ( $program_name )
        raise NotImplementedError

    def no_operation(self):
        # array NoOperation( $token )
        raise NotImplementedError
