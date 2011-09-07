from xmlrpclib import ServerProxy

from settings import Settings


class OpenSubtitles(object):
    """OpenSubtitles API wrapper.

    Please check the official API documentation at:
    http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC"""

    def __init__(self, language=None):
        self.xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER,
                                  allow_none=True)
        self.language = language or Settings.LANGUAGE

    def get_from_data_or_none(self, key):
        """Return the key getted from data if the status is 200,
        otherwise return None.
        """
        status, _ = self.data.get('status').split()
        return self.data.get(key) if '200' == status else None

    def login(self, username, password):
        """Returns token is login is ok, otherwise None."""
        self.data = self.xmlrpc.LogIn(username, password,
                                 self.language, Settings.USER_AGENT)
        return self.get_from_data_or_none('token')

    def logout(self, token):
        """Returns True is logout is ok, otherwise None."""
        data = self.xmlrpc.LogOut(token)
        return '200' in data.get('status')

    def search_subtitles(self, token, params):
        self.data = self.xmlrpc.SearchSubtitles(token, params)
        return self.get_from_data_or_none('data')

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

    def try_upload_subtitles(self):
        # array TryUploadSubtitles( $token, array('cd1' => array('subhash' => $submd5hash, 'subfilename' => $subfilename, 'moviehash' => $moviehash, 'moviebytesize' => $moviesize, 'movietimems' => $movietimems, 'movieframes' => $movieframes, 'moviefps' => $moviefps, 'moviefilename' => $moviefilename), 'cd2' => array(...) ) )
        raise NotImplementedError

    def upload_subitles(self):
        # array UploadSubtitles( $token,array( 'baseinfo' => array ( 'idmovieimdb' => $idmovieimdb, 'moviereleasename' => $scene_releasename, 'movieaka' => $aka_in_subtitle_language, 'sublanguageid' => $sublanguageid, 'subauthorcomment' => $author_comment, 'hearingimpaired' => $hearing_impaired, 'highdefinition' => $high_definition, 'automatictranslation' => $automatic_translation), 'cd1' => array( 'subhash' => $md5subhash, 'subfilename' => $subfilename, 'moviehash' => $moviehash, 'moviebytesize' => $moviebytesize, 'movietimems' => $movietimems, 'moviefps' => $moviefps, 'movieframes' => $movieframes, 'moviefilename' => $moviefilename, 'subcontent' => $subtitlecontent ), 'cd2' => array (...) ) )
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

    def search_movies_on_imdb(self):
        # array SearchMoviesOnIMDB( $token, $query )
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
