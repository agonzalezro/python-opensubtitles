import struct
import os
import hashlib
import zlib
import base64


def decompress(data, encoding):
    """
    Convert a base64-compressed subtitles file back to a string.

    :param data: the compressed data
    :param encoding: the encoding of the original file (e.g. utf-8, latin1)
    """
    try:
        return zlib.decompress(base64.b64decode(data),
                               16 + zlib.MAX_WBITS).decode(encoding)
    except UnicodeDecodeError as e:
        print(e)
        return


def get_gzip_base64_encoded(file_path):
    handler = open(file_path, mode='rb').read()
    return base64.encodestring(zlib.compress(handler))


def get_md5(file_path):
    '''Return the md5 of a file.
    '''
    f = open(file_path, 'rb').read()
    return hashlib.md5(f).hexdigest()


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

        for x in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, int(self.size) - 65536), 0)
        for x in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        return str(returnedhash)
