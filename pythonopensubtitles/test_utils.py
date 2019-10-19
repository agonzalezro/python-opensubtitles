from pythonopensubtitles.utils import File, get_md5

import os
import tempfile
import unittest


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
