from pythonopensubtitles.utils import File, get_md5, decompress

import os
import tempfile
import unittest
import unittest.mock as mock

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(delete=False)
        self.temp.write(('x'*65536*2).encode())
        self.temp.close()

    def tearDown(self):
        os.remove(self.temp.name)

    def test_hash(self):
        f = File(self.temp.name)
        assert f.get_hash() == '1e1e1e1e1e200000'

    def test_md5(self):
        assert get_md5(self.temp.name) == '3832e28c8feea48397f30d70b43d7987'

    def test_size(self):
        assert File(self.temp.name).size == "131072"

    @mock.patch('pythonopensubtitles.utils.zlib')
    @mock.patch('pythonopensubtitles.utils.detect')
    @mock.patch('pythonopensubtitles.utils.base64')
    def test_decompress(self, mock_base64, mock_detect, mock_zlib):
        mock_raw_data = mock.MagicMock()
        mock_zlib.decompress.return_value = mock_raw_data
        mock_detect.return_value = None
        decompress('test_base64data',enable_encoding_guessing=True,encoding='test_encoding')
        mock_raw_data.decode.assert_called_with('test_encoding', errors='ignore')
