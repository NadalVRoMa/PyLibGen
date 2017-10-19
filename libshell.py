import argparse
import urllib.request as req
import bs4
import os
from tabulate import tabulate


def getSearchResults(term, column='def'):
    page = 1
    url = 'http://libgen.io/search.php?&req={}&column={}&page={}'.format(
        term, column, str(page))
    # URGENT : ESCAPE SYMBOLS!!

    source = req.urlopen(url)
    soup = bs4.BeautifulSoup(source, 'lxml')
    page_books = soup.find_all('tr')
    page_books = page_books[3:-1]  # Ignore 3 first and the last <tr> label.
    books = page_books

    # TODO: Add functionality to get first results if there are too many.

    while len(page_books) == 25:  # The max number of books in a page is 25.
        page += 1
        url = 'http://libgen.io/search.php?&req={}&column={}&page={}'.format(
            term, column, str(page))

        source = req.urlopen(url)
        soup = bs4.BeautifulSoup(source, 'lxml')
        page_books = soup.find_all('tr')
        page_books = page_books[3:-1]
        books += page_books

    return(books)


def displayBooks(books):
    # TODO: Add support for multiple choices
    fmt_books = []
    titles = []
    for i, rawbook in enumerate(books):
        book_attrs = rawbook.find_all('td')
        author = book_attrs[1].a.text  # only first author
        title = book_attrs[2].find(title=True).text
        tinytitle = title[:100]
        publisher = book_attrs[3].text
        year = book_attrs[4].text
        lang = book_attrs[6].text[:2]  # Show only 2 first characters
        size = book_attrs[7].text
        ext = book_attrs[8].text
        book = [str(i + 1), author, tinytitle, publisher,
                year, lang, ext, size]  # Start at 1
        titles.append(title)
        fmt_books.append(book)

    headers = ['#', 'Author', 'Title', 'Publisher',
               'Year', 'Lang', 'Ext', 'Size']

    cont = True
    i = 0
    while cont:
        print(tabulate(fmt_books[i * 25:(i + 1) * 25], headers))
        while True:
            print('\n Type the number of your choice to start the download.')
            elec = input('Press Enter to see more matches or type q to quit: ')

            if elec.isnumeric():
                choice = int(elec)
                if choice <= (i + 1) * 25:  # Selection
                    return([choice, titles[choice], fmt_books[choice][6]])
                else:
                    print("Too big of a number.")
                    continue

            elif elec == 'q' or elec == 'Q':  # Quit
                return(False)

            elif not elec:  # See more matches
                if (i + 1) * 25 >= len(books):
                    print("There aren't more matches")
                    continue
                else:
                    i += 1
                    break


def downloadBook(book, filename):
    io_mirror = book.find_all('td')[-5]
    link = io_mirror.a.attrs['href']
    source = req.urlopen(link)
    soup = bs4.BeautifulSoup(source, 'lxml')

    for a in soup.find_all('a'):
        if a.text == 'GET':
            download_url = a.attrs['href']
            break

    print('Downloading...')
    req.urlretrieve(download_url, filename=filename)
    path = '{}/{}'.format(os.getcwd(), filename)
    print('Book downloaded to {}'.format(path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', required=True, dest='search_term')
    args = parser.parse_args()

    books = getSearchResults(args.search_term)
    if books:
        ch_book = displayBooks(books)
        if ch_book:
            book = books[ch_book[0]]
            title = '{}.{}'.format(ch_book[1], ch_book[2])
            downloadBook(book, title)
    else:
        print('Sorry, no matches found.')