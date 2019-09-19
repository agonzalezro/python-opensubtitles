from setuptools import setup, find_packages
from platform import python_version_tuple
import sys, os

version = '0.2'

setup(
    name='python-opensubtitles',
    version=version,
    description="Wrapper to use the OpenSubtitles API easily",
    keywords='opensubtitles python api',
    author='\xc3\x81lex Gonz\xc3\xa1lez',
    author_email='agonzalezro@gmail.com',
    url='http://twitter.com/agonzalezro',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'Support for encoding detection on downloaded subtitle':
            [
                'charset_normalizer' if int(python_version_tuple()[0]) >= 3 else 'chardet'
            ],
    }
)
