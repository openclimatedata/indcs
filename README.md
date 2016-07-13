Files with Intended Nationally Determined Contributions (INDCs) and submission
dates as provided by the
[UNFCCC secreteriat](http://unfccc.int/focus/indc_portal/items/8766.php).


## Data

INDCs are downloaded from the
[INDC portal](http://www4.unfccc.int/submissions/indc/Submission%20Pages/submissions.aspx).


## Preparation

Click forward and back in the INDC portal to get a full list of submitted INDCs.
The saved HTML file is scraped to generate a JSON file with links and submissions
dates and to download all INDCs and accompanying files.

Python3 and the libraries in `scripts/requirements.txt` are used.

Run

    make

to download and generate a `indcs.json` file or

    make process

to only process the list of INDCs.


## Notes

Please refer to the
[INDC portal](http://www4.unfccc.int/submissions/indc/Submission%20Pages/submissions.aspx)
for updates of submissions.


## License
The Python files in `scripts` are released under an
[CC0 Public Dedication License](https://creativecommons.org/publicdomain/zero/1.0/).
