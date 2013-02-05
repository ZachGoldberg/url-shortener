from setuptools import setup, find_packages

import url_shortener
import os
import urllib

def setup_distribute():
    """
    This will download and install Distribute.
    """
    try:
        import distribute_setup
    except:
        # Make sure we have Distribute
        if not os.path.exists('distribute_setup'):
            urllib.urlretrieve('http://nightly.ziade.org/distribute_setup.py',
                               './distribute_setup.py')
        distribute_setup = __import__('distribute_setup')
    distribute_setup.use_setuptools()

def get_reqs(reqs=[]):
    # optparse is included with Python <= 2.7, but has been deprecated in favor
    # of argparse.  We try to import argparse and if we can't, then we'll add
    # it to the requirements
    try:
        import argparse
    except ImportError:
        reqs.append("argparse>=1.1")
    return reqs

# Make sure we have Distribute installed
setup_distribute()

setup(
    name = "url_shortener",
    packages = find_packages(),
    package_data = {
        '': [],
        'url_shortener/': ['templates/*.*'],
    },
    author = "Nilesh D Kapadia",
    author_email = "Unknown",
    description = "",
    license = "Free",
    url = "http://nileshk.com/2009/06/02/url-shortener-web-app-using-django.html",
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = get_reqs(["Django>=1.0"]),
)
