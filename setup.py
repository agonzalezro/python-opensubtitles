from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='python-opensubtitles',
      version=version,
      description="Wrapper to use the OpenSubtitles API easily",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='opensubtitles python api',
      author='\xc3\x81lex Gonz\xc3\xa1lez',
      author_email='agonzalezro@gmail.com',
      url='http://twitter.com/agonzalezro',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
