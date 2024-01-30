"""
project_3_election_scraper.py: treti projekt do Engeto Online Python Akademie

author: Michaela Kosova

email: kosova.m@outlook.cz

discord: miskaKos

"""

import os 
import sys
import argparse
import csv
import requests
import bs4 
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()

parser.add_argument('url', nargs='?', default=None, help='Odkaz na web')
parser.add_argument('csv_name', nargs='?', default=None, help='nazev csv')

def zpracuj_odpoved_serveru(url: str) -> bs:
    r = requests.get(url)
    return bs(r.text, features="html.parser")

# pomoci find nadefinovani parametru tabulky z webu
def najdi_tabulku(soup: bs) -> bs4.element.Tag:
    return soup.find("div", {"id": "inner"})
    
# pomoci find_all vytvoreni listu s cisly a nazvy obci
def najdi_nazvy_cisla_obci(obec_seznam: bs4.element.Tag) -> list:
    nazvy_obci = []
    cisla_obci = []

    nazvy_obci_podklad = obec_seznam.find_all("td", {"class": "overflow_name"})
    for i in nazvy_obci_podklad:
        nazvy_obci.append(i.text.strip())    

    cisla_obci_podklad = obec_seznam.find_all("td", {"class": "cislo"})
    for k in cisla_obci_podklad:
        cisla_obci.append(k.text.strip())
      
    return nazvy_obci, cisla_obci
    
# pomoci select vytvoreni odkazu na dalsi udaje o hlasovani k jednotlivym obcim
def vytvor_odkazy_obce_jednotlive(obec_seznam: bs4.element.Tag) -> list:
    podklady_odkazy = obec_seznam.select('.cislo a')
    return ["https://volby.cz/pls/ps2017nss/" + obec_seznam['href'] for obec_seznam in podklady_odkazy]

# vytvoreni listu s pocty volicu, vydanych obalek, odevzdanych obalek a platnych hlasu v jednotlivych obcich
def vytvor_pocty_seznam_list(r2: requests.models.Response) -> list:
    location_soup = bs(r2.text, features="html.parser")
    cisla_seznam = location_soup.find("table", {"id": "ps311_t1"})
    cisla_seznam_td = cisla_seznam.find_all("td")
    cisla_seznam_list = []
    for j in cisla_seznam_td:
        cisla_seznam_list.append(j.text.strip())
    cisla_seznam_list = [r.replace("\xa0", "") for r in cisla_seznam_list]
    return cisla_seznam_list

# pomoci find_all vytvoreni seznamu platnych hlasu dle politickych stran v jednotlivych obcich
def najdi_seznam_platne_hlasy(r2: requests.models.Response) -> list:
    location_soup = bs(r2.text, features="html.parser")
    strany_seznam = location_soup.find("div", {"id": "inner"})

    platne_hlasy_podklad_1 = strany_seznam.find_all("td", {"class":"cislo", "headers": ("t1sb3")})
    platne_hlasy_podklad_2 = strany_seznam.find_all("td", {"class":"cislo", "headers": ("t2sb3")})
    
    platne_hlasy_1 = []
    platne_hlasy_2 = []

    for i in platne_hlasy_podklad_1:
        platne_hlasy_1.append(i.text.strip())

    platne_hlasy_1 = [r.replace("\xa0", "") for r in platne_hlasy_1]
   
    for i in platne_hlasy_podklad_2:
        platne_hlasy_2.append(i.text.strip())

    platne_hlasy_2 = [r.replace("\xa0", "") for r in platne_hlasy_2]

    return platne_hlasy_1 + platne_hlasy_2   
 
# vytvoreni listu s nazvy vsech politickych stran
def najdi_seznam_pol_stran(r2: requests.models.Response) -> list:
    nazvy_stran_soup = bs(r2.text, features="html.parser")
    nazvy_stran_seznam = nazvy_stran_soup.find("div", {"id": "inner"})
    nazvy_stran = []

    nazvy_stran_podklad = nazvy_stran_seznam.find_all("td", {"class":"overflow_name"})

    for i in nazvy_stran_podklad:
        nazvy_stran.append(i.text.strip())
    
    return nazvy_stran

# vytvoreni prvni casti finalni tabulky pro export s obsahem: cisla obci, nazvy obci, volici v seznamu, odevzdane obalky, platne hlasy
def vytvor_list_fin_cast_1(cisla_obci, nazvy_obci, registred, envelopes, valid: list) -> list:
    fin_cast_1 = []
    for index in range(0, len(cisla_obci)):
        p = [cisla_obci[index], nazvy_obci[index], registred[index], envelopes[index], valid[index]]
        fin_cast_1.append(p)
    return fin_cast_1

# pripojeni hlasu dle politickych stran k tabulce fin_cast_1 --> vytvoreni finalni tabulky
def vytvor_list_fin_cast_2(fin_cast_1: list, platne_hlasy_strany: list) -> list:
    for index in range(0, len(fin_cast_1)):
        fin_cast_1[index].extend(platne_hlasy_strany[index])
    return fin_cast_1
     
def main():
    args = parser.parse_args()
 
    if args.url is None or args.csv_name is None:
        print("Pro spousteni chybi povinny argument.")
        sys.exit(1)    
    else:
        print(f"STAHUJI DATA Z VYBRANEHO URL: {args.url}")

    soup = zpracuj_odpoved_serveru(args.url) 
    obec_seznam = najdi_tabulku(soup)
    nazvy_obci, cisla_obci = najdi_nazvy_cisla_obci(obec_seznam)
    odkazy = vytvor_odkazy_obce_jednotlive(obec_seznam)
    nazvy_stran = najdi_seznam_pol_stran(requests.get(odkazy[0]))

    registred = []
    envelopes = []
    valid = []
    platne_hlasy_strany = []

    for odkaz in odkazy:
        r2 = requests.get(odkaz)
        cisla_seznam_list = vytvor_pocty_seznam_list(r2)
        registred.append(cisla_seznam_list[3])
        envelopes.append(cisla_seznam_list[4])
        valid.append(cisla_seznam_list[7])
        platne_hlasy_strany.append(najdi_seznam_platne_hlasy(r2))

    hlavicka = ['code', 'location', 'registred', 'envelopes', 'valid']
    hlavicka.extend(nazvy_stran)
    fin_cast_1 = vytvor_list_fin_cast_1(cisla_obci, nazvy_obci, registred, envelopes, valid)
    fin_cast_2 = vytvor_list_fin_cast_2(fin_cast_1, platne_hlasy_strany)
     
    with open(args.csv_name, "w", encoding='UTF-8-sig', newline='' ) as f:
        write = csv.writer(f, delimiter= ";")

        write.writerow(hlavicka)
        write.writerows(fin_cast_2)
        print(f"UKLADAM DO SOUBORU {args.csv_name}")

    with open(args.csv_name) as csv_soubor:
        csv_data = csv.reader(csv_soubor)
        print(f"UKONCUJI election_scraper")
     
                      
if __name__ == "__main__":
    main()