import argparse
import re
import os
from urllib import request
from urllib.parse import urlencode
from tabulate import tabulate
from bs4 import BeautifulSoup
from settings import *


def getSearchResults(term, page, column):
    params = urlencode({'req': term, 'column': column, 'page': page})
    url = 'http://libgen.io/search.php?&%s' %params

    source = request.urlopen(url)
    soup = BeautifulSoup(source, 'lxml')
    if page == 1:
        books_found = re.search(r'(\d+) books found', str(soup))
        print(books_found.group().upper())
        if int(books_found.groups()[0]) == 0:
            return(False)

    page_books = soup.find_all('tr')
    page_books = page_books[3:-1]  # Ignore 3 first and the last <tr> label.
    books = page_books
    return(books)


def formatBooks(books, page, n_authors, mc_authors, mc_title, mc_publisher):
    # TODO: Add support for multiple choices
    fmt_books = []
    books_mirrors = []  # List of dics with complete titles and mirrors

    for i, rawbook in enumerate(books):
        i += (page - 1) * 25

        book_attrs = rawbook.find_all('td')

        authors = [a.text for a in book_attrs[1].find_all('a')]
        author = ', '.join(authors[:n_authors])
        author = author[:mc_authors]

        title = book_attrs[2].find(title=True).text
        tinytitle = title[:mc_title]

        publisher = book_attrs[3].text[:mc_publisher]
        year = book_attrs[4].text
        lang = book_attrs[6].text[:2]  # Show only 2 first characters
        size = book_attrs[7].text
        ext = book_attrs[8].text
        io_mirror = book_attrs[9].a.attrs['href']

        book = (str(i + 1), author, tinytitle, publisher,
                year, lang, ext, size)  # Start at 1

        book_mirrors = {'title': title, 'io': io_mirror}
        books_mirrors.append(book_mirrors)

        fmt_books.append(book)

    return(fmt_books, books_mirrors)


def selectBook(books, mirrors, page, down_path, end=False):
    headers = ['#', 'Author', 'Title', 'Publisher',
               'Year', 'Lang', 'Ext', 'Size']

    if end:
        print('Sorry, no more matches.')
    else:
        print(tabulate(books[(page - 1) * 25:page * 25], headers))

    while True:
        elec = input(
            '\n Type # of book to download, q to quit or just press Enter to see more matches: ')

        if elec.isnumeric():
            choice = int(elec) - 1
            if choice < len(books):  # Selection
                title = '{}.{}'.format(
                    mirrors[choice]['title'], books[choice][-2])
                downloadBook(mirrors[choice]['io'], title, down_path)
                return(False)
            else:
                print("Too big of a number.")
                continue

        elif elec == 'q' or elec == 'Q':  # Quit
            return(False)

        elif not elec:  # See more matches
            return(True)

        else:
            print('Not a valid option.')


def downloadBook(link, filename, down_path):
    source = request.urlopen(link)
    soup = BeautifulSoup(source, 'lxml')

    for a in soup.find_all('a'):
        if a.text == 'GET':
            download_url = a.attrs['href']
            break

    if os.path.exists(down_path) and os.path.isdir(down_path):
        print('Downloading...')
        path = '{}/{}'.format(down_path, filename)
        request.urlretrieve(download_url, filename=path)
        print('Book downloaded to {}'.format(os.path.abspath(path)))
    elif os.path.isfile(down_path):
        print('The download path is not a directory. Change it in settings.py')
    else:
        print('The download path does not exist. Change it in settings.py')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    column = parser.add_mutually_exclusive_group()
    parser.add_argument('search', nargs='+', help='search term')
    column.add_argument('-t', '--title', action='store_true',
                        help='get books from the specified title')
    column.add_argument('-a', '--author', action='store_true',
                        help='get books from the specified author')
    column.add_argument('-p', '--publisher', action='store_true',
                        help='get books from the specified publisher')
    column.add_argument('-y', '--year', action='store_true',
                        help='get books from the specified year')

    args = parser.parse_args()
    
    search_term = ' '.join(args.search)
    search_arguments = [(args.title, 'title'),
                        (args.author, 'author'),
                        (args.publisher, 'publisher'),
                        (args.year, 'year')]

    sel_column = 'def'
    for arg in search_arguments:
        if arg[0]:
            sel_column = arg[1]

    books = []
    mirrors = []
    page = 1
    get_next_page = True

    while get_next_page:
        raw_books = getSearchResults(search_term, page, sel_column)
        if raw_books:
            new_books, new_mirrors = formatBooks(
                raw_books, page, N_AUTHORS, MAX_CHARS_AUTHORS, MAX_CHARS_TITLE, MAX_CHARS_PUBLISHER)
            books += new_books
            mirrors += new_mirrors
            get_next_page = selectBook(books, mirrors, page, DOWNLOAD_PATH)
            page += 1
        elif raw_books == []:  # 0 matches in the last page
            get_next_page = selectBook(
                books, mirrors, page - 1, DOWNLOAD_PATH, end=True)
        else:  # 0 matches total
            get_next_page = False
