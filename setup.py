from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()


setup(
    name='grassed',  
    version='0.1.0',
    author="Sam Vanderslink",
    author_email="sam@notis.net.au",
    description="Python logging handler that can send messages to a Slack channel.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/SSlinky/SlackLogger",
    package_dir={'': 'grassed'}
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Logging"
    ],
    keywords="slack, logging handler"
)