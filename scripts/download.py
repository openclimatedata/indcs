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
import urllib


path = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(path, "../data/")
indcs = os.path.join(data_dir, "indcs.json")

indcs = json.load(open(indcs, "r"))

for submission in indcs:
    directory = os.path.join(data_dir, submission["party"])
    if not os.path.exists(directory):
        os.makedirs(directory)
    for item in submission["files"]:
        filename = item["filename"]
        url = item["url"]
        print "Fetching", filename
        urllib.urlretrieve(url, os.path.join(directory, filename))
