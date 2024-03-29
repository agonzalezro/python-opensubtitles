import struct
import os
import sys
import hashlib
import zlib
import base64
from platform import python_version_tuple
from warnings import warn

try:
    if int(python_version_tuple()[0]) < 3:
        raise ImportError
    from charset_normalizer import detect
except ImportError:
    try:
        from cchardet import detect
    except ImportError:
        try:
            from chardet import detect
            warn('python chardet is installed but could be unreliable, upgrade to python 3 and install '
                 'charset-normalizer or cchardet.')
        except ImportError:
            def detect(bytes_str):
                return None


def decompress(data, enable_encoding_guessing=True, encoding='utf-8'):
    """
    Convert a base64-compressed subtitles file back to a string.
    :param data: the compressed data
    :param bool enable_encoding_guessing:
    :param str decoding: if not enable_encoding_guessing you can specify the encoding here. e.g. "latin"
    """

    raw_subtitle = zlib.decompress(base64.b64decode(data), 16 + zlib.MAX_WBITS)
    encoding_detection = detect(raw_subtitle) if enable_encoding_guessing is True else None

    if encoding_detection is None:
        return raw_subtitle.decode(encoding, errors='ignore')

    try:
        my_decoded_str = raw_subtitle.decode(encoding_detection['encoding'])
    except UnicodeDecodeError as e:
        print(e)
        return

    return my_decoded_str


def get_gzip_base64_encoded(file_path):
    with open(file_path, mode="rb") as file:
        compressed_data = zlib.compress(file.read())
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 1:
            return base64.encodebytes(compressed_data).decode("utf-8")
        else:
            return base64.encodestring(compressed_data).decode("utf-8")


def get_md5(file_path):
    '''Return the md5 of a file.
    '''
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


class File(object):
    def __init__(self, path):
        self.path = path
        self.size = str(os.path.getsize(path))

    def get_hash(self):
        '''Original from: http://goo.gl/qqfM0
        '''
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        try:
            f = open(self.path, "rb")
        except(IOError):
            return "IOError"

        hash = int(self.size)

        if int(self.size) < 65536 * 2:
            return "SizeError"

        for _ in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, int(self.size) - 65536), 0)
        for _ in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        return str(returnedhash)
