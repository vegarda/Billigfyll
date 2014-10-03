# -*- coding: utf-8 -*-
import threading
from urllib import request, error
import lxml.html
import lxml.etree
import html.parser
import re
import time

class Vinmonopolet(threading.Thread):
    link = "http"
    lagttil = 0
    antall = 0
    varenavn = "NULL"
    pris = "NULL"
    volum = "NULL"
    varenummer = "NULL"
    varetype = "NULL"
    undervaretype = "NULL"
    produktutvalg = "NULL"
    farge = "NULL"
    lukt = "NULL"
    smak = "NULL"
    land = "NULL"
    prosent = "NULL"
    alkohol = "NULL"
    aargang = "NULL"
    metode = "NULL"
    raastoff = "NULL"
    produsent = "NULL"
    url = "NULL"
    starttime = 0.0

    def __init__(self, link, varetype):
        super(Vinmonopolet, self).__init__()
        self.link = link
        self.varetype = varetype
        #self.starttime = time.time()
        #print(self.starttime)

        self.site = 'http://www.vinmonopolet.no'
        #vareutvalg = self.urlopen2(self.site + '/vareutvalg/').read()
        #vareutvalgDOM = lxml.html.fromstring(vareutvalg)

        #self.antall = int(re.sub(r'\D', '', vareutvalgDOM.xpath('//div[@id="selectView"]/p/strong')[0].text))
        #print(self.antall)

        #self.file = open('database.sql', 'w', encoding='utf-8')
        #self.file.write("CREATE TABLE vareliste(varenavn VARCHAR(255), pris decimal(6,2), volum int, varenummer int, varetype VARCHAR(255), undervaretype VARCHAR(255), produktutvalg VARCHAR(255), farge VARCHAR(255), lukt VARCHAR(255), smak VARCHAR(255), land  VARCHAR(255), prosent decimal(10,2), alkohol float(10,6), aargang int, metode VARCHAR(255), raastoff VARCHAR(255), produsent VARCHAR(255), url VARCHAR(2047));\n\n")

        self.htmlparser = html.parser.HTMLParser()
    
    def urlopen2(self, url):
        try:
            req = request.Request(url)
            return request.urlopen(req)
        except error.URLError:
            self.urlopen2(url)
        
    def run(self):
        vareutvalglink = self.link
        lagttil = self.lagttil
        varenavn = self.varenavn
        pris = self.pris
        volum = self.volum
        varenummer = self.varenummer
        varetype = self.varetype
        undervaretype = self.undervaretype
        produktutvalg = self.produktutvalg
        farge = self.farge
        lukt = self.lukt
        smak = self.smak
        land = self.land
        prosent = self.prosent
        alkohol = self.alkohol
        aargang = self.aargang
        metode = self.metode
        raastoff = self.raastoff
        produsent = self.produsent
        url = self.url

        print(vareutvalglink.text)
        vareHTML = self.urlopen2(self.site + vareutvalglink.attrib['href']).read()
        self.file = open(vareutvalglink.text + '.sql', 'w', encoding='utf-8')
        vareDOM = lxml.html.document_fromstring(vareHTML)
        vareLinks = vareDOM.xpath('//tbody/tr/td/h3/a')
        
        neste = 1
        url = self.site + vareutvalglink.attrib['href']
        while(neste == 1):
            varedataHTML = self.urlopen2(url).read()
            varedataDOM = lxml.html.fromstring(varedataHTML)
            vareLinks = varedataDOM.xpath('//tbody/tr/td/h3/a')      
            for vareLink in vareLinks:
                varenavn = self.htmlparser.unescape(vareLink.text).encode('utf-8')
                varenavn = re.sub(r"\"", "\\\"", varenavn.decode())
                varenavn = '"' + varenavn + '"'
                url =  re.sub(r";.+=", "", vareLink.attrib['href'])
                vare = self.urlopen2(url).read()
                vareDOM = lxml.html.fromstring(vare)
                volum = vareDOM.xpath('//h3/em[1]')[0].text
                volum = re.findall(r"[-+]?\d*\.\d+|\d+", volum)[0]
                volum = '"' + volum + '"'
                pris = vareDOM.xpath('//h3/strong[1]')[0].text
                pris = re.sub(r"Kr. ", "", pris)
                pris = re.sub(r"\.", "", pris)
                pris = re.sub(r",-", "", pris)
                pris = re.sub(r"\r\n", "", pris)
                pris = re.sub(r",", ".", pris)
                pris = '"' + pris + '"'

                vareData = vareDOM.xpath('//div[@class=\'productData\']/ul/li')
                for data in vareData:
                    data = self.htmlparser.unescape(lxml.etree.tostring(data).decode())
                    data = re.sub(r"<[^>]*>", "", data)
                    data = re.sub(r"\n+", "", data)
                    data = re.sub(r"  ", "", data)
                           
                    if "Varenummer" in data:
                        varenummer = re.sub(r"Varenummer: ", "", data)
                        varenummer = '"' + varenummer + '"'

                    if "Varetype" in data:
                        undervaretype = re.sub(r"Varetype: ", "", data)
                        undervaretype = '"' + undervaretype + '"'
                       
                    if "Produktutvalg" in data:
                        produktutvalg = re.sub(r"Produktutvalg: ", "", data)
                        produktutvalg = '"' + produktutvalg + '"'

                    if "Farge" in data:
                        farge = re.sub(r"Farge: ", "", data)
                        farge = '"' + farge + '"'

                    if "Lukt" in data:
                        lukt = re.sub(r"Lukt: ", "", data)
                        lukt = '"' + lukt + '"'

                    if "Smak" in data:
                        smak = re.sub(r"Smak: ", "", data)
                        smak = re.sub(r"\"", "\\\"", smak)
                        smak = '"' + smak + '"'

                    if "Land" in data:
                        land = re.sub(r"Land/distrikt:", "", data)
                        land = '"' + land + '"'

                    if "Innhold" in data:
                        prosent = re.sub(r"Innhold: Alkohol ", "", data)
                        prosent = re.sub(r"%.+", "", prosent)
                        prosent = re.sub(r",", ".", prosent)
                        prosent = '"' + prosent + '"'
                        alkohol = float(re.sub(r"\"", "", prosent))*float(re.sub(r"\"", "", re.sub(r"\"", "", volum)))/float(re.sub(r"\"", "", pris))/float(10)
                        round(alkohol,6)

                    if "Årgang" in data:
                        aargang = re.sub(r"Årgang: ", "", data)
                        aargang = '"' + aargang + '"'

                    if "Metode" in data:
                        metode = re.sub(r"Metode: ", "", data)
                        metode = re.sub(r"\"", "\\\"", metode)
                        metode = '"' + metode + '"'

                    if "Råstoff" in data:
                        raastoff = re.sub(r"Råstoff:", "", data)
                        raastoff = re.sub(r"\"", "\\\"", raastoff)
                        raastoff = '"' + raastoff + '"'

                    if "Produsent" in data:
                        produsent = re.sub(r"Produsent: ", "", data)
                        produsent = re.sub(r"\"", "\\\"", produsent)
                        produsent = '"' + produsent + '"'

                q = "INSERT INTO billigfyll.vareliste VALUES (" + varenavn + ", " + pris + ", " + volum + ", " + varenummer + ", \"" + varetype + "\", " + undervaretype + ", " + produktutvalg + ", " + farge + ", " + lukt + ", " + smak + ", " + land + ", " + prosent + ", " + str(alkohol) + ", " + aargang + ", " + metode + ", " + raastoff + ", " + produsent + ", \"" + url + "\");"
                self.file.write(q + "\n")
                
                varenavn = "NULL"
                pris = "NULL"
                volum = "NULL"
                varenummer = "NULL"
                undervaretype = "NULL"
                produktutvalg = "NULL"
                farge = "NULL"
                lukt = "NULL"
                smak = "NULL"
                land = "NULL"
                prosent = "NULL"
                alkohol = "NULL"
                aargang = "NULL"
                metode = "NULL"
                raastoff = "NULL"
                produsent = "NULL"
                url = "NULL"
                
                #timer
                self.lagttil = self.lagttil + 1
                #currenttime = time.time()
                #est = (self.antall - lagttil)*(currenttime - self.starttime)/lagttil
                #print(est)
            #if page contains next
            varetypeNeste = varedataDOM.xpath('//td/a[starts-with(text(), \'Neste\')]')
            if len(varetypeNeste) > 0:
                url = self.site + varetypeNeste[0].attrib['href']
            if len(varetypeNeste) == 0:
                neste = 0
 
def urlopen2(url):
    try:
        req = request.Request(url)
        return request.urlopen(req)
    except error.URLError:
        self.urlopen2(url)

def main():
    site = 'http://www.vinmonopolet.no'
    vareutvalg = urlopen2(site + '/vareutvalg/').read()
    vareutvalgDOM = lxml.html.fromstring(vareutvalg)
    vareutvalgLinks = vareutvalgDOM.xpath("//div[@class='sitemap']/div[@class='row'][position()<4]/div[@class='facet'][position()<4]/h3[@class='title']/a")
    workers = []
    i = 1
    for vareutvalglink in vareutvalgLinks:
        worker = Vinmonopolet(vareutvalglink, vareutvalglink.text)
        worker.setName(vareutvalglink.text)
        worker.daemon = True
        worker.start()
        workers.append(worker)
        i = i+1
    for worker in workers:
        worker.join()
        print("join")

if __name__ == '__main__':
    main()
        
        
