from bs4 import BeautifulSoup
import requests as req
import re


def concat(listofstrs):
    final = ""
    for i in listofstrs:
        final += i
    return final


class Webpage:
    #     def __init__(self, url):
    #         self.url = url
    #         self.request = req.get(url)
    #         self.soup = BeautifulSoup(request)
    @staticmethod
    def wikify(link):
        return "https://en.wikipedia.org"+link

    @staticmethod
    def find_link(tag):
        return tag.find('a')['href']


class TechCategory(Webpage):
    def __init__(self, title, techlist):
        self.title = title
        self.techlist = techlist

    @classmethod
    def via_handtbl(cls, h, tbl):
        title = cls.set_title_tb(h)
        techlist = cls.get_tech_list(tbl)
        return(TechCategory(title, techlist))

    @staticmethod
    def set_title_tb(h):
        span = h.find('span')
        title = span.text
        return title
        # ttag = self.contents.next_sibling()
        # self.tbtag = ttag.find('tbody')

    @ staticmethod
    def get_tech_list(table):
        techlist = []
        for i in table.find_all('tr')[1:]:
            techlist.append(Tech.via_tr(i))
        return techlist

    def printall(self):
        print(self.title)
        for i in self.techlist:
            i.prettyprint()


class Tech(Webpage):
    def __init__(self, title, titlelink, develop, citations):
        self.title = title.strip()
        self.titlelink = titlelink.strip()
        self.develop = develop.strip()
        self.citations = citations

    @ classmethod
    def via_tr(cls, tr):
        tds = tr.find_all('td')
        title = cls.getridofbrackets(tds[0].text)
        titlelink = cls.wikify(cls.find_link(tds[0]))
        articles = cls.getridofbrackets(tds[-1].text)
        cit = cls.citationslist(tr)
        return cls(title, titlelink, articles, cit)

    @ staticmethod
    def getridofbrackets(st):
        sp = re.split(r"\[.*\]", st)
        return concat(sp)

    def citationslist(tr):
        links = []
        reseted = Tech.reset(tr)
        for i in tr.find_all('sup'):
            text = i.text
            text = text[1:-1]
            if text.isnumeric():
                num = int(text)
                cit = Tech.citefinder(reseted, num)
                links.append(cit)
        return links

    def citefinder(body, no):
        block = body.find("li", {'id': f"cite_note-{no}"})
        if block != None:
            atags = block.find_all('a')
            link = ''
            if len(atags) >= 2:
                link = atags[1]['href']
            return link
        else:
            return ''

    @ staticmethod
    def reset(tr):
        i = tr.parent
        while i.name != 'body':
            i = i.parent
        return i

    def create_file(title, tbtag):
        trs = tbtag.find_all('tr')
        with open(f"{title}.txt", 'w') as f:
            for i in trs:
                tds = i.find_all('td')
        # def brief_wiki_contents(self):
        # req.get(self.titlelink)

    def prettyprint(self):
        print('\t'+self.title)
        print('\t'+self.titlelink)
        print('\t'+self.develop)
        print(self.citations)
        print(2*'\n')


htm = req.get(
    "https://en.wikipedia.org/wiki/List_of_emerging_technologies").text
soup = BeautifulSoup(htm, 'html.parser')
# tr = ((soup.find_all(
#     'table', {'class': "wikitable sortable"})[1]).find_all('tr'))[1]

table = soup.find_all('table', {'class': 'wikitable sortable'})[3]
h = table.previous_sibling.previous_sibling

agr = TechCategory.via_handtbl(h, table)
agr.printall()
