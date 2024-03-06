# JobSifter

## Overview

JobSifter is a simple CLI tool to help you sift through the thousands of
job postings online. I found that most job boards have some terrible sorting and
filtering options, so I wanted to make a tool that would allow me to get the job
postings in a format that I could easily filter and sort through.

## Features

- **Supports multiple job boards**: Currently supports Indeed and ZipRecruiter,
  with plans to add more.
- **Filtering**: Allows you to provide excluded keywords to filter out job
  titles that you are not interested in.
- **Location**: Allows you to specify the location of the job postings. The
  default is "remote".
- **Pagination**: Allows you to specify the number of pages to search. The
  default is 2, and the maximum is 10.
- **Sorting**: Tries to sort by latest postings first, so you can see the most
  recent job postings. This is not perfect, as some job boards don't have the
  date of the posting, but it's better than nothing.
- **Output**: Outputs the job postings in a CSV file, so you can easily filter
  and sort the postings in Excel or Google Sheets.

## Installation

Python 3.12.2

### Clone the repository

```bash
git clone https://github.com/nronzel/job-sifter.git
cd job-sifter
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

Use the `--help` flag to see the available options.

```bash
python main.py --help
```

This will show the following output:

```
usage: main.py [-h] [-t TITLE] [-e EXCLUDE [EXCLUDE ...]] [-p PAGES] [-l LOCATION]

Grab job data from job boards.

options:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        Job title to search for.
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        OPTIONAL - Keywords to exclude from job title - space separated.
  -p PAGES, --pages PAGES
                        OPTIONAL - Number of pages to search. Default: 2, Max: 10.
  -l LOCATION, --location LOCATION
                        OPTIONAL - Location to search for jobs. Default: remote.
```

### Example

To search for software engineer jobs, excluding junior and intern positions,
and searching the first 5 pages, you would run the following:

```bash
python main.py -t "software engineer" -e "jr" "junior" "intern" -p 5
```

After running this command, it will show some console output and create a CSV
file in the project directory called `software-engineer.csv`.

## Potential Improvements

- Add more job boards.
- Add more output options.
- Filter based on keywords in job description.

## Contributing

If you would like to contribute, please open an issue or a pull request. I would
love to hear your feedback and ideas for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
