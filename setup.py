import setuptools
from pathlib import Path

setuptools.setup(
    name="optracker",
    version="1.2.4",
    description=('Scrapes medias, likes, followers from social media. Organize them in a database for more deeper analyze.'),
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="MIT",
    maintainer="suxSx",
    author='suxSx',
    author_email='marcuscrazy@gmail.com',
    keywords='scraper media social network mapper tracker instagram scrape like follow analyze',
    url='https://github.com/suxSx/openSource-tracker',
    entry_points={
        'console_scripts': [
            'optracker = optracker.optracker:run',
        ],
    },
    install_requires=[
        'python-slugify==3.0.2',
        'unicodecsv==0.14.1',
        'mysql-connector-python==8.0.18',
        'networkx==2.4'
        'matplotlib==3.1.1'
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
