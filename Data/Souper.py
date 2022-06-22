
from bs4 import BeautifulSoup
import re

import pandas as pd


class Souper:

    def __init__(self, PN):
        self.PN = str(PN)


    def getFeatures(self):

        features = []

        path = "htmls/" + self.PN + ".html"
        with open(path, "r") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")
        body = soup.body
        tables = body.find_all('table', recursive=False)

        _ISD = tables[1].find_all(text = re.compile("\d{4}"))[0].text   # robust

        _TTL = body.find_all('font', size = "+1", recursive=False)[0].text  # robust

        _ABST = body.find_all('p', recursive=False)[0].text     # robust

        p = body.find_all('p', recursive=False)[1]
        p_tables = p.find_all('table', recursive = False)

        _CPC = p.find_all('td', align ="right", valign="top", width="70%")[1].text

        _IPC = p.find_all('td', align ="right", valign="top", width="70%")[2].text

        # backward citation list
        b_cits = []

        for item in p_tables[1].find_all('tr'):
            valid = item.find_all('td')
            if len(valid) == 3:
                pn = valid[0].text
                dt = valid[1].text
                b_cits.append([pn,dt])

        ass = p.text
        start = ass.find("Claims")+7
        end = ass.find("Description")
        _ACLM = ass[start:end]


        features.extend([self.PN, _ISD, _TTL, _ABST, _CPC, _IPC, b_cits, _ACLM])     # num_features = 7
        return features








    def getSignals(self):

        signals = []
        
        path = "ref_htmls/" + self.PN + "_ref.html"
        with open(path, "r") as file:
            ref_html = file.read()

        soup = BeautifulSoup(ref_html, "html.parser")

        body = soup.body

        if body == None:
            signals.append(1)
            return signals

        n_str = body.find_all(text = re.compile('patents.'))[0].text
        start = n_str.find(':')
        end = n_str.find('p')
        n = int(n_str[start+2:end-1])
        n_page = int(n/50)+1

        signals.append(n)

        for i in range(1, n_page+1):
            url = url_p  + PN + "&p=" + str(i)
            _request = request.Request(url, headers= config._headers)
            _response = request.urlopen(_request)
            _html = _response.read()
            soup = BeautifulSoup(_html, "html.parser")
            body = soup.body

            for item in body.find_all(text = re.compile("\d"), href = re.compile("Parser?")):
                if len(item.text) < 11:
                    cPN = item.text
                    signals.append(cPN)

        return signals



def getFcits(PN):
    '''
    Arguments:
        PN
    Return:
        A list contains forward citations.
        and the number of citations.
    '''

    signals = []

    url_p = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2Fsearch-adv.htm&r=0&f=S&l=50&d=PALL&Query=ref/'
    url = url_p + PN + '&p=1'

    _request = request.Request(url, headers= config._headers)
    _response = request.urlopen(_request)
    _html = _response.read()
    soup = BeautifulSoup(_html, "html.parser")
    body = soup.body

    if body == None:
        signals.append(1)
        return signals

    n_str = body.find_all(text = re.compile('patents.'))[0].text
    start = n_str.find(':')
    end = n_str.find('p')
    n = int(n_str[start+2:end-1])
    n_page = int(n/50)+1

    signals.append(n)

    for i in range(1, n_page+1):
        url = url_p  + PN + "&p=" + str(i)
        _request = request.Request(url, headers= config._headers)
        _response = request.urlopen(_request)
        _html = _response.read()
        soup = BeautifulSoup(_html, "html.parser")
        body = soup.body

        for item in body.find_all(text = re.compile("\d"), href = re.compile("Parser?")):
            if len(item.text) < 11:
                cPN = item.text
                signals.append(cPN)

    return signals






