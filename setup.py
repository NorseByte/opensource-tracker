import setuptools
from pathlib import Path

setuptools.setup(
    name="optracker",
    version="0.1.0",
    description=('scrapes medias, likes, followers from social media. Organize them in a database for more deeper analyze.'),
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="MIT",
    maintainer="suxSx",
    author='suxSx',
    url='https://github.com/suxSx/openSource-tracker',
    install_requires=[
        'igramscraper==0.3.2'
    ],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        "License :: OSI Approved :: MIT License"
    ],
)
