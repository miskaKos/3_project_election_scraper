# Engeto-pa-3-projekt
Election_scraper je třetím projektem do Engeto Online Python Akademie.

## Popis projektu
Tento projekt slouží k získání výsledků z parlamentních voleb uskutečněných v roce 2017, odkaz k nahlédnutí naleznete [zde](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103).

## Instalace knihoven
Knihovny, které jsou použité v kódu projektu, jsou uložené v souboru requirements.txt. 
Pro jejich instalaci je vhodné použít nové virtuální prostředí a s nainstalovaným manažerem spustit dle níže uvedeného postupu:

 > pip3 --version                             [overim verzi manazeru] <br>
 > pip3 install -r requirements.txt           [nainstalujeme knihovny]

## Spuštění projektu
Pro správné spuštění souboru election_scraper.py v příkazovém řádku jsou potřebné dva povinné argumenty, a to:

> python election_scraper.py <"odkaz-uzemniho-celku"> <"vysledny-soubor">

Následně budou staženy výsledky voleb zvolené obce jako "csv" soubor.

Pro správné otevření csv souboru v MS Excel byl použitý k zapisování dat do "csv" delimiter ";" (election_scraper.py řádek 153).

## Ukázka projektu
Výsledky hlasování pro okres Prostějov:
- je potřebné zadat dva povinné argumenty, a to:
1. argument: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
2. argument: vysledky_prostejov.csv


Spouštění programu: <br>
> python election_scraper.py  "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"  vysledky_prostejov.csv

Průběh stahování: <br>
> STAHUJI DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 <br>
> UKLADAM DO SOUBORU vysledky_prostejov.csv <br>
> UKONCUJI election_scraper

Částečný výstup: <br> 

> code;location;registred;envelopes;valid... <br>
> 506761;Alojzov;205;145;144;29;0;0;9;0;5;17;4;1;1;0;0;18;0;5;32;0;0;6;0;0;1;1;15;0 <br>
> 589268;Bedihošť;834;527;524;51;0;0;28;1;13;123;2;2;14;1;0;34;0;6;140;0;0;26;0;0;0;0;82;1 <br>
> 589276;Bílovice-Lutotín;431;279;275;13;0;0;32;0;8;40;1;0;4;0;0;30;0;3;83;0;0;22;0;0;0;1;38;0 <br>
...
