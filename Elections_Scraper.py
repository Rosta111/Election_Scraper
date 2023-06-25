import csv
import sys
from typing import List
import requests
from bs4 import BeautifulSoup


class Election_Scraper:
    def __init__(self, url: str):
        self.url = url

    def scrape(self, file_name: str) -> None:
        html = self._get_html()
        rows = self._extract_data(html)
        header = self._get_header(rows)
        parties = self._get_parties()
        self._save_data(file_name, header, rows, parties)

    def _get_html(self) -> BeautifulSoup:
        response = requests.get(self.url)
        html = BeautifulSoup(response.text, "html.parser")
        print(f"STAHUJI DATA Z URL: {self.url}")
        return html

    def _extract_data(self, html: BeautifulSoup) -> List[List[str]]:
        rows = []
        municipalities = self._get_municipalities(html)
        ids = self._get_municipality_ids(html)
        votes = self._get_votes(html)
        zipped = zip(ids, municipalities, votes["registered_voters"], votes["envelopes_issued"], votes["valid_votes"])
        parties = self._get_parties()
        for i, m, rv, ei, vv in zipped:
            row = [i, m, rv, ei, vv]
            for party in parties:
                row.append(votes["party_votes"][party].get(i, ""))
            rows.append(row)
        return rows

    def _get_municipalities(self, html: BeautifulSoup) -> List[str]:
        municipalities_search = html.find_all("td", "overflow_name")
        municipalities = [m.text for m in municipalities_search]
        return municipalities

    def _get_municipality_ids(self, html: BeautifulSoup) -> List[str]:
        ids = html.find_all("td", "cislo")
        municipality_ids = [i.text for i in ids]
        return municipality_ids

    def _get_parties(self) -> List[str]:
        html = self._get_html()
        municipality_link = self._get_municipality_links(html)
        html_villages = BeautifulSoup(requests.get(municipality_link[0]).text, "html.parser")
        parties_search = html_villages.find_all("td", "overflow_name")
        parties = [p.text for p in parties_search]
        return parties

    def _get_municipality_links(self, html: BeautifulSoup) -> List[str]:
        link_search = html.find_all("td", "cislo", "href")
        municipality_links = [f"https://volby.cz/pls/ps2017nss/{link_municipality.a['href']}" for link_municipality in link_search]
        return municipality_links

    def _get_votes(self, html: BeautifulSoup) -> dict:
        votes = {"registered_voters": [], "envelopes_issued": [], "valid_votes": [], "party_votes": {}}
        links = self._get_municipality_links(html)
        for link in links:
            html_village = self._get_html_village(link)
            self._extract_voter_data(html_village, votes)
            self._extract_party_votes(html_village, votes)
        return votes


    def _get_html_village(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        html_village = BeautifulSoup(response.text, "html.parser")
        return html_village

    def _extract_voter_data(self, html: BeautifulSoup, votes: dict) -> None:
        voters_search = html.find_all("td", headers="sa2")
        envelopes_search = html.find_all("td", headers="sa3")
        valid_votes_search = html.find_all("td", headers="sa6")
        voters = [v.text.replace('\xa0', ' ').replace(',', '') for v in voters_search]
        envelopes = [e.text.replace('\xa0', ' ').replace(',', '') for e in envelopes_search]
        valid_votes = [vv.text.replace('\xa0', ' ').replace(',', '') for vv in valid_votes_search]
        votes["registered_voters"].extend(voters)
        votes["envelopes_issued"].extend(envelopes)
        votes["valid_votes"].extend(valid_votes)

    def _extract_party_votes(self, html: BeautifulSoup, votes: dict) -> None:
        parties_search = html.find_all("td", "overflow_name")
        parties = [p.text for p in parties_search]
        if not votes["party_votes"]:
            votes["party_votes"] = {p: {} for p in parties}
        votes_search = html.find_all("td", "cislo", headers=["t1sb4", "t2sb4"])
        party_votes = {p: {} for p in parties}
        for i, vote_search in enumerate(votes_search):
            party_votes[parties[i]][html.find("td", headers="t1sb3").text.strip()] = vote_search.text + " %"
        for p, votes_dict in party_votes.items():
            votes["party_votes"][p].update(votes_dict)

    def _get_header(self, rows: List[List[str]]) -> List[str]:
        header = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
        parties = self._get_parties()
        header.extend(parties)
        return header

    def _save_data(self, file_name: str, header: List[str], rows: List[List[str]], parties: List[str]) -> None:
        print(f"UKLÁDÁM DATA DO SOUBORU: {file_name}")
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"UKONČUJI: {sys.argv[0]}")


def election_results(url: str, file: str) -> None:
    try:
        scraper = Election_Scraper(url)
        scraper.scrape(file)
    except IndexError:
        print("Nastala chyba. Nejspíš máte špatný odkaz nebo jste jej zapomněli dát do uvozovek.")
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Nesprávný počet argumentů. Zadejte prosím správný odkaz a název souboru.")
        sys.exit()
    address = sys.argv[1]
    file_name = sys.argv[2]
    election_results(address, file_name)

    
