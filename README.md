# Elections Scraper Project

Můj třetí projekt pro kurz Engeto


## Popis

Tento projekt stahuje data z webové stránky volby.cz a ukládá je do CSV souboru.

Tento scraper je navržen pro extrakci dat z webového zdroje a uložení těchto dat do CSV souboru. Projekt využívá následující knihovny:

- `csv`: Slouží pro práci s CSV soubory.
- `sys`: Poskytuje přístup k některým proměnným a funkcím souvisejícím se systémem.
- `typing.List`: Definuje typ seznamu.
- `requests`: Používá se k provedení HTTP požadavků na webové stránky.
- `bs4 (BeautifulSoup)`: Slouží pro extrakci dat z HTML stránky.

## Instalace

1. Naklonujte tento repozitář na svůj počítač.
2. Nainstalujte potřebné knihovny pomocí příkazu `pip install .


## Použití

1. Zadejte do terminálu s kódem adresu webu a název výstupního souboru jako argumenty při spuštění programu. Například:
   python scraper.py <adresa_webu> <nazev_souboru.csv>

   Příklad: python Elections_Scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110" vysledky.csv

2. Program stáhne data z webové stránky a uloží je do CSV souboru.

3. Následně můžeme otevřít csv soubor, kde uvidíme stažené a uložené výsledky voleb ze zadaného okrsku.
