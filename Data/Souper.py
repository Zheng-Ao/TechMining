
from bs4 import BeautifulSoup
import re

import pandas as pd


class Souper:

    def __init__(self, PN):

        self.PN = str(PN)
        self.dict = {
            'PN': self.PN,
            'REF': self.getSignals(),

            # 下面的皆通过getFeatures()函数进行更新
            # 把所有feature都单独写个函数太麻烦且不必要，仅针对不太鲁棒的几个特征单独写，其余的都写在getFeatures()中

            # 'IN': "inventor name",
            'ISD': "issue date",
            # 'IC': 'inventor city',
            'TTL': 'title',
            # 'IS': 'inventor state',
            'ABST': 'abstract',
            # 'ICN': 'inventor country',
            'ACLM': 'claims',
            # 'ACNM': 'applicant name',
            'CPC': '',
            'IPC': '',
            'b_cits': 'backward citations'
        }


    def getFeatures(self):

        path = "htmls/" + self.PN + ".html"
        with open(path, "r") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")
        body = soup.body
        tables = body.find_all('table', recursive=False)

        self.dict['ISD'] = tables[1].find_all(text = re.compile("\d{4}"))[0].text   # robust

        self.dict['TTL'] = body.find_all('font', size = "+1", recursive=False)[0].text  # robust

        self.dict['ABST'] = body.find_all('p', recursive=False)[0].text     # robust

        p = body.find_all('p', recursive=False)[1]
        p_tables = p.find_all('table', recursive = False)

        self.dict['CPC'] = p.find_all('td', align ="right", valign="top", width="70%")[1].text

        self.dict['IPC'] = p.find_all('td', align ="right", valign="top", width="70%")[2].text

        # backward citation list
        b_cits = []

        for item in p_tables[1].find_all('tr'):
            valid = item.find_all('td')
            if len(valid) == 3:
                pn = valid[0].text
                dt = valid[1].text
                b_cits.append([pn,dt])

        self.dict['b_cits'] = b_cits

        ass = p.text
        start = ass.find("Claims")+7
        end = ass.find("Description")
        self.dict['ACLM'] = ass[start:end]








    def getSignals(self):

        '''取Y标签，看起来好像没什么问题了'''

        signals = []
        
        path = "ref_htmls/" + self.PN + "_ref_1.html"
        with open(path, "r") as file:
            ref_html = file.read()

        soup = BeautifulSoup(ref_html, "html.parser")

        body = soup.body

        # ref = 1
        if body == None:
            signals.append(1)
            return signals
        
        # ref != 1
        n_str = body.find_all(text = re.compile('patents.'))[0].text
        start = n_str.find(':')
        end = n_str.find('p')
        n = int(n_str[start+2:end-1])
        n = int(n)
        signals.append(n)

        if n%50 == 0:
            n_page = int(n/50)
        else:
            n_page = int(n/50)+1

        for i in range(1, n_page+1):
            path = "ref_htmls/" + self.PN + "_ref_" + str(i) + '.html'
            with open(path, "r") as file:
                ref_html = file.read()
            soup = BeautifulSoup(ref_html, "html.parser")
            body = soup.body

            for item in body.find_all(text = re.compile("\d"), href = re.compile("Parser?")):
                if len(item.text) < 11:
                    cPN = item.text
                    signals.append(cPN)

        return signals




    


