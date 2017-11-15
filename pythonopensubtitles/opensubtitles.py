from __future__ import print_function
from .utils import decompress
import os
import os.path
import sys

try:                    #Python 2
    from xmlrpclib import ServerProxy, Transport
    from settings import Settings
except ImportError:     #Python 3
    from xmlrpc.client import ServerProxy, Transport
    from .settings import Settings


class OpenSubtitles(object):
    '''OpenSubtitles API wrapper.

    Please check the official API documentation at:
    http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
    '''

    def __init__(self, language=None, user_agent=None):
        """
        Initialize the OpenSubtitles client
        
        :param language: language for login
        :param user_agent: User Agent to include with requests.
            Can be specified here, via the OS_USER_AGENT environment variable,
            or via Settings.USER_AGENT (default)
            
            For more information: http://trac.opensubtitles.org/projects/opensubtitles/wiki/DevReadFirst#Howtorequestanewuseragent 
        """
        self.language = language or Settings.LANGUAGE
        self.token = None
        self.user_agent = user_agent or os.getenv('OS_USER_AGENT') or Settings.USER_AGENT

        transport = Transport()
        transport.user_agent = self.user_agent

        self.xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER,
                                  allow_none=True, transport=transport)


    def _get_from_data_or_none(self, key):
        '''Return the key getted from data if the status is 200,
        otherwise return None.
        '''
        status = self.data.get('status').split()[0]
        return self.data.get(key) if '200' == status else None

    def login(self, username, password):
        '''Returns token is login is ok, otherwise None.
        '''
        self.data = self.xmlrpc.LogIn(username, password,
                                 self.language, self.user_agent)
        token = self._get_from_data_or_none('token')
        if token:
            self.token = token
        return token

    def logout(self):
        '''Returns True is logout is ok, otherwise None.
        '''
        data = self.xmlrpc.LogOut(self.token)
        return '200' in data.get('status')

    def search_subtitles(self, params):
        '''Returns a list with the subtitles info.
        '''
        self.data = self.xmlrpc.SearchSubtitles(self.token, params)
        return self._get_from_data_or_none('data')

    def try_upload_subtitles(self, params):
        '''Return True if the subtitle is on database, False if not.
        '''
        self.data = self.xmlrpc.TryUploadSubtitles(self.token, params)
        return self._get_from_data_or_none('alreadyindb') == 1

    def upload_subtitles(self, params):
        '''Returns the URL of the subtitle in case that the upload is OK,
        other case returns None.
        '''
        self.data = self.xmlrpc.UploadSubtitles(self.token, params)
        return self._get_from_data_or_none('data')

    def no_operation(self):
        '''Return True if the session is actived, False othercase.

        .. note:: this method should be called 15 minutes after last request to
                  the xmlrpc server.
        '''
        data = self.xmlrpc.NoOperation(self.token)
        return '200' in data.get('status')

    def auto_update(self, program):
        '''Returns info of the program: last_version, url, comments...
        '''
        data = self.xmlrpc.AutoUpdate(program)
        return data if '200' in data.get('status') else None

    def search_movies_on_imdb(self, params):
        self.data = self.xmlrpc.SearchMoviesOnIMDB(self.token, params)
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

    def download_subtitles(self, ids, override_filenames=None,
                           output_directory='.', extension='srt'):
        """
        Returns a dictionary with max. 20 IDs of and paths to all
        successfully downloaded subtitle files, otherwise None.

        Be aware that if you provide an override_filenames dictionary
        containing duplicate values (the same file name for different
        subtitle IDs), you will end up with only one subtitle file with
        that file name as each new download overrides any already
        existing file with the same name. I.e. the total of downloaded
        files will be smaller than the number of submitted IDs.

        :param ids: list of ids of subtitle files to download
        :param override_filenames: optional dictionary with preferred file
                names; for keys use subtitle file IDs (as strings),
                for values use file names (incl. file extensions)
        :param extension: one of: srt, sub, txt, ssa, smi, mpi, tmp;
                only applicable if only subtitle file IDs are provided
        :param output_directory: path to directory to which to write files
                (defaults to directory the script is run in)
        """
        override_filenames = override_filenames or {}
        successful = {}

        # OpenSubtitles will accept a maximum of 20 IDs for download
        if len(ids) > 20:
            print("Cannot download more than 20 files at once.",
                  file=sys.stderr)
            ids = ids[:20]

        self.data = self.xmlrpc.DownloadSubtitles(self.token, ids)
        encoded_data = self._get_from_data_or_none('data')

        if not encoded_data:
            return

        for item in encoded_data:
            subfile_id = item['idsubtitlefile']

            decoded_data = (decompress(item['data'], 'utf-8')
                            or decompress(item['data'], 'latin1'))

            if not decoded_data:
                print("An error occurred while decoding subtitle "
                      "file ID {}.".format(subfile_id), file=sys.stderr)
            else:
                fname = override_filenames.get(subfile_id,
                                               subfile_id + '.' + extension)
                fpath = os.path.join(output_directory, fname)

                try:
                    with open(fpath, 'w') as f:
                        f.write(decoded_data)
                    successful[subfile_id] = fpath
                except IOError as e:
                    print("There was an error writing file {}.".format(fpath),
                          file=sys.stderr)
                    print(e)

        return successful or None

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
