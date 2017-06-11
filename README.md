Files with Intended Nationally Determined Contributions (INDCs) and submission
dates as provided by the
[UNFCCC secreteriat](http://unfccc.int/focus/indc_portal/items/8766.php).


## Data

INDCs are downloaded from the
[INDC portal](http://www4.unfccc.int/submissions/indc/Submission%20Pages/submissions.aspx).


## Preparation

Click forward and back in the INDC portal to get a full list of submitted INDCs.
The resulting full table needs to be manually saved from the Developer Tools.
The saved HTML file is parsed to generate a CSV file with links and submissions
dates. For convenience all INDCs and accompanying files are downloaded, converted
to PDF (for .doc, .docx and .xps files) and renamed in the `pdfs` directory..

Python3 and the libraries in `scripts/requirements.txt` are used. It is
recommended to use a Virtualenv.

Run

    make

to download and generate a `indcs.csv` file and download the INDC files.


## Requirements

A couple of Python libraries have further dependencies.

MacOS:

    brew antiword icu4c libgxps

`icu4c` may require explicit linking:

    brew link icu4c --force


To run LibreOffice from the command line a simple bash wrapper is required:

```
#!/bin/bash

~/Applications/LibreOffice.app/Contents/MacOS/soffice "$@"
```

On Debian/Ubuntu systems:

sudo apt-get install libgxps-utils


## Notes

Please refer to the
[INDC portal](http://www4.unfccc.int/submissions/indc/Submission%20Pages/submissions.aspx)
for updates of submissions.


## License
The Python files in `scripts` are released under an
[CC0 Public Dedication License](https://creativecommons.org/publicdomain/zero/1.0/).
