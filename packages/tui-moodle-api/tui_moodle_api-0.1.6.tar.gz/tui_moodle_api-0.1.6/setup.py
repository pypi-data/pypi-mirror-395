from setuptools import setup, find_packages

VERSION = '0.1.6'

setup(
    name='tui-moodle-api',
    version=VERSION,
    author='Eric Tröbs',
    author_email='eric.troebs@tu-ilmenau.de',
    description='scraper for moodle',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://dbgit.prakinf.tu-ilmenau.de/ertr8623/moodle-api',
    project_urls={
        'Bug Tracker': 'https://dbgit.prakinf.tu-ilmenau.de/ertr8623/moodle-api/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.10',
    install_requires=[
        'aiohttp~=3.11.16',
        'beautifulsoup4~=4.13.3',
        'pyyaml~=6.0.2'
    ],
)
