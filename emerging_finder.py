from bs4 import BeautifulSoup
import requests as req


class Webpage:
    #     def __init__(self, url):
    #         self.url = url
    #         self.request = req.get(url)
    #         self.soup = BeautifulSoup(request)
    def wikify(link):
        return "https://en.wikipedia.org"+link

    def find_link(tag):
        return tag.find('a')['href']


class TechList:
    def __init__(self, cont):
        self.contents = cont
        self.title = ""
        self.tbtag = ""
        self.techlist = []
        self.set_title_tb()
        self.get_tech_list()

    def set_title_tb(self):
        span = self.contents.find['span']
        self.title = span.text

        ttag = self.contents.next_sibling()
        self.tbtag = ttag.find('tbody')

    def citationslist(self, tr):
        links = []
        for i in tr.findall('sup'):
            text = i.text
            text = text[1:-1]
            num = int(text)
            cit = self.citefinder(self, num)
            links.append(cit)
        return links

    def citefinder(self, no):
        block = self.soup.find("li", {'id': f"cite_note-{no}"})
        atags = block.find_all('a')
        link = []
        for i in atags[1:]:
            link.append(i['href'])
        return link

    def get_tech_list(self):
        for i in self.tbtag.find_all('tr'):
            self.techlist.append(Tech(i, self.citationslist(i)))

    def create_file(title, tbtag):
        trs = tbtag.find_all('tr')
        with open(f"{title}.txt", 'w') as f:
            for i in trs:
                tds = i.find_all('td')


class Tech(Webpage):
    def __init__(self, tr, citations):
        self.tds = tr.find_all('td')
        self.titlelink = wikify(find_link(tds[0]))
        self.title = tds[0].text
        self.development = [td[1].text, td[3].text]
        self.citelinks = citations
        self.contents = ""

        # def brief_wiki_contents(self):
        # req.get(self.titlelink)
