
# wat - wat are this?

<img align="right" alt="Video of a dog being held to various items, captioned with the question: 'wat are this?'. Image based on Jenna Marble's work featuring Kermit the dog." src="https://user-images.githubusercontent.com/560608/227779499-2a2624b6-e80d-454f-8c90-7309d2f2b77f.gif" style="margin-right: 1em;" />


`wat` helps you find out what all the things in your Linux system are. You can ask it for information on:

 * executables
 * services
 * bash built-ins
 * packages
 * files and folders (experimental)

To find out what something is, simply pass the name to `wat`:

```
> wat zeitgeist

zeitgeist (package): Zeitgeist is a service which logs the user's activities and 
events (files opened, websites visited, conversations held with other people, etc.) 
and makes the relevant information available to other applications.
```

## Installation

`wat` requires Python 3.10.

### From repository

1. Install requirements: `pip install -r requirements.txt`
2. Install `wat` as command line tools: `python3 setup.py install --user`

## Usage

```
usage: wat [-h] [--version] [--update] [--skip-empty-result] [name ...]

positional arguments:
  name                 name of the thing to lookup

options:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  --update, -u         update the page sources
  --skip-empty-result  if there is no result, don't print anything
```

## Acknowledgments!

The inital repository structure is based on [navdeep-G/samplemod](https://github.com/navdeep-G/samplemod).

The implementation internally uses the Python-client of [tldr](https://github.com/tldr-pages/tldr-python-client/).
