import pathlib
from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README text
README = (HERE / "README.md").read_text()


setup(
    name='grassed',  
    version='0.0.0',
    license='GPLv3',
    author="Sam Vanderslink",
    author_email="sam@notis.net.au",
    description="Python logger handler that can send messages to a Slack channel.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SSlinky/SlackLogger",
    package_dir={'': 'src'},
    packages=['grassed'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Logging"
    ],
    install_requires=[
        'concurrent.futures',
        'logging',
        're',
        'requests',
        'time'
        ],
    keywords="slack, logging handler, logger handler, logger, handler, logging"
)
