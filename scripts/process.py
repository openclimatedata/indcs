# encoding: UTF-8

# Written in 2016 - 2017 by Robert Gieseke <robert.gieseke@pik-potsdam.de>
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

import os
import re
import urllib.request

from collections import OrderedDict
from shutil import copyfile
from urllib.parse import quote, unquote

import countrynames
import delegator
import pandas as pd
import pycld2 as cld2
import textract

from bs4 import BeautifulSoup
from normality import normalize
from pathlib import Path
from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage

root = Path(__file__).parents[1]
indc_table = root / "archive/INDC - Submissions.html"
data_dir = root / "data"
pdfs_dir = root / "pdfs"
cache_dir = root / "cache"

if not cache_dir.exists():
    cache_dir.mkdir()

if not pdfs_dir.exists():
    pdfs_dir.exists()

soup = BeautifulSoup(open(str(indc_table), "r"), "lxml")

rows = soup.findAll("tr", {"class": "soby_griddatarow"})

indcs = []

for row in rows:
    cells = row.findAll("td")
    # Links to INDCs are embedded as another table in our row so we skip those.
    # < row >< party >< submission data >< table with links >< row >
    if len(cells) == 1:
        continue
    party = cells[0].text.strip().replace(u"\u200b", "")
    if " - " in party:
        name = party.split(" - ")[0].strip()
    elif " The " in party:
        name = party.split(" The ")[0].strip()
    elif "on behalf" in party:
        name = party.split(" on behalf")[0].strip()
    else:
        name = party
    code = countrynames.to_alpha_3(name, fuzzy=True)
    if "Latvia" in party:
        name = "European Union"
        code = "EUU"
    elif "East Timor" in party:
        name = "Timor-Leste"

    submission_date = cells[1].text.strip()
    submissions = cells[2].findAll("a")
    files = []
    for submission in submissions:
        url = "http://www4.unfccc.int" + quote(submission.attrs['href'])
        # unquote for Algerie accent, remove multiple spaces
        filename = re.sub(
            " +",
            " ",
            unquote(url.split("/")[-1])
        )
        files.append(OrderedDict([
            ("filename", filename),
            ("url", url)
        ]))
        if not (cache_dir / filename).exists():
            print("Fetching: ", filename)
            urllib.request.urlretrieve(url, os.path.join(cache_dir, filename))

    # Some languages could not be detected automatically.
    mappings = {
        "Belarus": "English",  # cover letter
        "Bolivia": "Spanish",
        "Cameroon": "French",
        "Central African Republic": "French",
        "Haiti": "French",
        "Indonesia": "English",
        "Liberia": "English",
        "Malawi": "English",
        "Maldives": "English",
        "Oman": "English",  # also contains Arabic version
        "Panama": "Spanish",
        "Philippines": "English",
        "Rwanda": "English",
        "Serbia": "English",
        "The former Yugoslav Republic of Macedonia": "English",
        "Timor-Leste": "English",
        "Togo": "French"
    }

    for f in files:
        filename = f["filename"]
        url = f["url"]
        filepath = cache_dir / filename
        language = None
        try:
            text = textract.process(str(filepath))
            lang = Detector(text.decode("UTF-8"))
            if lang:
                language = lang.language.name
        except (cld2.error, UnicodeDecodeError, UnknownLanguage) as e:
            if any(sub in filename for sub in ('english', '_EN', 'Eng')):
                language = "English"
            elif "_Rus_" in filename:
                language = "Russian"
            elif name in mappings:
                language = mappings[name]
            else:
                print(" '{}' ::: not detected'".format(name))
                print(name, " - language not detected")
        except textract.exceptions.ExtensionNotSupported as e:
            if name == "Sri Lanka":  # in .xps format
                language = "English"

        # Detect kind of document.
        addendums = ("lettre", "letter", "executive summary", "addendum",
                     "verbal_note")
        translations = ("translation", "english version", "english_version")
        if any(sub in filename.lower() for sub in addendums):
            file_type = "Addendum"
        elif any(sub in filename.lower() for sub in translations):
            file_type = "Translation"
        elif filename == "Belarus.pdf":
            file_type = "Addendum"
        elif filename == "Liberia_INDC Submission.002.pdf":
            file_type = "Addendum"
        elif filename.startswith("Sierra Leone INDC Submission to UNFCCC"):
            file_type = "Addendum"
        else:
            file_type = "INDC"
        print("{} : {} ({}) : {}".format(name, file_type, language, filename))

        clean_filename = "{}_{}_{}_{}.pdf".format(
            code,
            normalize(name, lowercase=False).replace(" ", "-"),
            file_type,
            language
        )
        if file_type == "Translation":
            clean_filename = clean_filename.replace(
                "Translation", "INDC_Translation")
        elif file_type == "Addendum":
            clean_filename = clean_filename.replace(
                "Addendum", "INDC_Addendum")

        clean_filepath = pdfs_dir / clean_filename

        indcs.append(OrderedDict([
            ("Code", code),
            ("Party", name),
            ("FileType", file_type),
            ("Language", language),
            ("Filename", clean_filename),
            ("SubmissionDate", submission_date),
            ("EncodedAbsUrl", url),
            ("OriginalFilename", filename),
        ]))

        if not clean_filepath.exists():
            if filename.suffix == ".pdf":
                copyfile(str(cache_dir / filename), str(clean_filepath))
            elif (filename.suffix == ".doc") or (filename.suffix == ".docx"):
                command = ("libreoffice --convert-to 'pdf' " +
                           "--nolockcheck " +
                           "--headless " +
                           "--outdir {} " +
                           "'{}'").format(
                    cache_dir, str(cache_dir / filename))
                print(command)
                c = delegator.run(command)
                print(c.out)
                pdf_version = filename.stem + ".pdf"
                copyfile(str(cache_dir / pdf_version), str(clean_filepath))
            elif filename.suffix == ".xps":
                pdf_version = filename.stem + ".pdf"
                command = "xpstopdf '{}' '{}'".format(
                    str(cache_dir / filename),
                    str(cache_dir / pdf_version)
                )
                print(command)
                c = delegator.run(command)
                print(c.out)
                copyfile(os.path.join(cache_dir, pdf_version), clean_filepath)
        print("=>", clean_filename)
    print("====")

df = pd.DataFrame(indcs)
df = df.sort_values(["Party", "FileType"])

assert(len(df.Filename.unique()) == len(df.Filename))
df.to_csv(str(data_dir / "indcs.csv"), index=False)
