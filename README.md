# PyLibGen
A python3 script to download books from libgen.io

### Install

You need python3 to run the script. 
To install the required dependencies:

``pip install -r requirements.txt``

### Usage

```
usage: pylibgen.py [-h] [-t | -a | -p | -y] search

positional arguments:
  search           search term

optional arguments:
  -h, --help       show this help message and exit
  -t, --title      get books from the specified title
  -a, --author     get books from the specified author
  -p, --publisher  get books from the specified publisher
  -y, --year       get books from the specified year
```

### Settings

You can easily tweak some stuff about the display changing the variables in ``settings.py``, like the number of authors showed, maximum lenght of different columns, etc.

**Happy Reading!**
