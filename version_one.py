from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from math import ceil

pageHistories = []

prevAccepts = ['prev', 'precedent']
nextAccepts = ['next', 'suivant']


def wikiRequest(query: str = None):
    """
    :param query:
    :return:
    """
    # https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard
    webpage = urlopen('https://fr.wikipedia.org/wiki/%s' % (query if query else 'Sp%C3%A9cial:Page_au_hasard')).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup


def getPageTitle(wikiRequest: BeautifulSoup):
    """
    :param wikiRequest:
    :return:
    """
    title = wikiRequest.find('title').getText()
    title = title.split('—')[0].strip()
    return title


def getHyperLinks(page: BeautifulSoup):
    """
    :param page:
    :return:
    """
    return page.findAll('a', attrs={'href': re.compile("^/wiki/[^:]+$"), 'title': re.compile("[\S\s]+[\S]+.*(?<!c])$")})


def pagination(lists, page, maxItems):
    """
    :param lists:
    :param page:
    :param maxItems:
    :return:
    """
    return {
        "items": lists[slice(maxItems * (page - 1), page * maxItems)],
        "lastItem": lists[len(lists) - 1],
        "prev": False if page == 1 else True,
        "next": False if (page * maxItems) >= len(lists) else True,
        "page": page,
        "maxPage": ceil(len(lists) / maxItems)
    }


def startGame(startPage: BeautifulSoup, endPage: BeautifulSoup, page=1, currentPage: BeautifulSoup = None, round=1):
    """
    :param startPage:
    :param endPage:
    :param page:
    :param currentPage:
    :param round:
    :return:
    """
    startTitlePage = getPageTitle(startPage)
    if not currentPage: currentPage = startPage

    print('************************ Tour %s ************************' % round)
    print('Départ: %s' % startTitlePage)
    print('Cible: %s' % getPageTitle(endPage))
    print('Actuellement : %s' % getPageTitle(currentPage), end='\n\n')
    lists = [(idx + 1, page.get('title')) for idx, page in enumerate(getHyperLinks(currentPage))]
    listIds = [str(_[0]) for _ in lists]

    error = False
    while getPageTitle(currentPage) != getPageTitle(endPage):
        try:
            paginate = pagination(lists, page, 10)
            for items in (paginate['items'] + [paginate['lastItem']]):
                listId = items[0]
                country = items[1]
                print('{} - {}'.format(('0' + str(listId) if listId < 10 else listId), country))

            print('Page actuel: {} | Dernière page: {}'.format(paginate['page'], paginate['maxPage']))
            pageParameters = prevAccepts + nextAccepts
            listInputAccepts = pageParameters + listIds

            if error: print(error, end='')
            userInput = str(input("Entrer le numéro de la ligne ou Precedent/Suivant pour changer de page: ")).lower()
            assert userInput in listInputAccepts

            if userInput not in pageParameters:
                nextPage = wikiRequest(parse.quote(lists[int(userInput) - 1][1]))
                pageHistories.append(getPageTitle(nextPage))
                return startGame(startPage, endPage, 1, nextPage, round + 1)
            elif userInput in prevAccepts:
                if not paginate['prev']:
                    raise Exception('prev')
                return startGame(startPage, endPage, page - 1, None, round)
            elif userInput in nextAccepts:
                if not paginate['next']:
                    raise Exception('next')
                return startGame(startPage, endPage, page + 1, None, round)
            error = False
        except AssertionError:
            error = 'La valeur entrée est invalid. '
        except Exception as e:
            if str(e) == 'next':
                error = 'Vous ne pouvez pas aller plus haut dans la pagination'
            if str(e) == 'prev':
                error = 'Vous ne pouvez pas aller plus bas dans la pagination'

    print('Gagné en {} coups amen'.format(round))


# startPage = wikiRequest()
# endPage = wikiRequest()

print('************************ WikiGame ************************')
# startGame(startPage, endPage)
