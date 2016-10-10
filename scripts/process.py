# encoding: UTF-8

# Written in 2016 by Robert Gieseke <robert.gieseke@pik-potsdam.de>
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

import json
import os
import re

from urllib.parse import quote, unquote

import pandas as pd

from bs4 import BeautifulSoup

path = os.path.dirname(os.path.realpath(__file__))
indc_table = os.path.join(path, "../archive/INDC - Submissions.html")
datapackage_json = os.path.join(path, "../datapackage.json")
data_dir = os.path.join(path, "../data/")
output = os.path.join(data_dir, "indcs.json")

soup = BeautifulSoup(open(indc_table), "lxml")

rows = soup.findAll("tr", {"class": "soby_griddatarow"})

indcs = []

url = ("https://raw.githubusercontent.com/" +
       "datasets/country-codes/master/data/country-codes.csv")

country_codes = pd.read_csv(
    url,
    index_col="official_name_en",
    usecols=["ISO3166-1-Alpha-3", "official_name_en"],
    encoding="UTF-8"
)
country_codes = country_codes.reset_index().dropna().set_index(
    'official_name_en')

country_codes = country_codes.rename(
    columns={"ISO3166-1-Alpha-3": "country_code"}
)

# Add country code for European Union and drop Latvia to filter for EU later.
country_codes.loc["European Union"] = 'EU28'
country_codes = country_codes.drop("Latvia")

for row in rows:
    cells = row.findAll("td")
    # Links to INDCs are embedded as another table in our row so we skip those.
    # < row >< party >< submission data >< table with links >< row >
    if len(cells) == 1:
        continue
    party = cells[0].text.strip()
    try:
        code = country_codes.loc[party].values[0]
    except KeyError:
        for value in country_codes.index:
            if value in party or party in value:
                code = country_codes.loc[value].values[0]
                break
        if party == "Saint Vincent and Grenadines":
            code = "VCT"
        if party == "Bosnia-Herzegovina":
            code = "BIH"
    print(party, code)
    name = country_codes[country_codes.country_code == code].index.values[0]
    submission_date = cells[1].text.strip()
    submissions = cells[2].findAll("a")
    files = []
    for submission in submissions:
        url = "http://www4.unfccc.int" + quote(submission.attrs['href'])
        print(url)
        # unquote for Algerie accent, remove multiple spaces
        filename = re.sub(
            " +",
            " ",
            unquote(url.split("/")[-1])
        )
        files.append({
            "filename": filename,
            "url": url
        })
    indcs.append({
      "party": name,
      "code": code,
      "submission_date": submission_date,
      "files": files
    })

resources = [{
    "name": "INDCs",
    "path": "data/indcs.json",
    "format": "json",
    "mediatype": "text/json"
}]
for indc in indcs:
    for item in indc["files"]:
        resources.append({
            "name": item["filename"],
            "path": "data/" + indc["party"] + "/" + item["filename"],
            "format": item["filename"].split(".")[-1]
        })

datapackage = json.load(open(datapackage_json, "r"))
datapackage["resources"] = resources

json.dump(datapackage, open(datapackage_json, "w"), indent=2,
          ensure_ascii=False)

json.dump(indcs, open(output, "w"), indent=2, ensure_ascii=False)
