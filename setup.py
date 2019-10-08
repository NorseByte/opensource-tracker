import setuptools
from pathlib import Path

setuptools.setup(
    name="optracker",
    version="1.0.3",
    description=('scrapes medias, likes, followers from social media. Organize them in a database for more deeper analyze.'),
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['optracker']),
    license="MIT",
    maintainer="suxSx",
    author='suxSx',
    author_email='marcuscrazy@gmail.com',
    url='https://github.com/suxSx/openSource-tracker',
    entry_points={
        'console_scripts': [
            'optracker = optracker.optracker:main',
        ],
    },
    install_requires=[
        'igramscraper==0.3.2',
        'unicodecsv==0.14.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education :: Testing',
        "License :: OSI Approved :: MIT License"
    ],
)
