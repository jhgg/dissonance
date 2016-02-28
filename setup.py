import os
import dissonance
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="dissonance",
    version=dissonance.version.split('-')[0] + 'b0',
    author="Jacob Heinz",
    author_email="me@jh.gg",
    description="Discord python client & bot framework.",
    license="MIT",
    keywords="chat discord bot irc jeev",
    url="https://github.com/jhgg/dissonance",
    packages=find_packages(exclude=['modules']),
    install_requires=[
        'certifi==14.5.14',
        'coloredlogs==1.0.1',
        'Flask==0.10.1',
        'gevent==1.1rc5',
        'greenlet==0.4.9',
        'requests==2.9.1',
        'six==1.10.0',
        'websocket-client==0.35.0',
        'wheel==0.24.0',
    ],
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/dissonance'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
)