# python-opensubtitles

![CircleCI](https://img.shields.io/circleci/build/github/agonzalezro/python-opensubtitles?style=flat-square)

Simple module to access to the [OpenSubtitles.org](http://opensubtitles.org)
subtitles database. This class is a wrapper for the common methods used by the OpenSubtitles API.

## Install

### Released version

The package is released in pypi, you can simply install it with:

    $ pip install python-opensubtitles

### Dev version

If you want to install the latest version from this repo:

    $ pip install -e git+https://github.com/agonzalezro/python-opensubtitles#egg=python-opensubtitles

## Test

If you want to run the tests:

    $ python -m unittest

Note: I am using python 3, previous versions might not catch all the tests.

## Simple usage

**TL;DR;** version to download a subtitle:

```python
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

ost = OpenSubtitles() 
ost.login('xxx', 'xxx')

f = File('/full/path/to/the/movie')

data = ost.search_subtitles([{'sublanguageid': 'all', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])
id_subtitle_file = data[0].get('IDSubtitleFile')

ost.download_subtitles([id_subtitle_file], output_directory='/tmp', extension='srt')
```

If you want to see more info you can take a look to the old `doctest`s on the
[APPENDIX.md file](https://github.com/agonzalezro/python-opensubtitles/blob/master/APPENDIX.md).

## Release a new version

Probably you will not need to run this, but just FTR:

```bash
$ # Edit setup.py to change the version
$ pip install twine
$ python3 setup.py sdist bdist_wheel
$ python3 -m twine upload dist/*
```

The previous command will upload a release to PyPI.
