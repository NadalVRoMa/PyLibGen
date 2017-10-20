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

The default download path for the books is set to the directory from where you run the script. You can easily tweak this and some other options changing the variable's values in ``settings.py``.

**Happy Reading!**
