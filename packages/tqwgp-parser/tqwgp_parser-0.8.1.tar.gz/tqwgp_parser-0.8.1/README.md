# Talk Quote Work Get-Paid (aka TQWGP) proposal and invoice parser

[![Build Status](https://travis-ci.org/YtoTech/talk-quote-work-getpaid-parser.svg?branch=master)](https://travis-ci.org/YtoTech/talk-quote-work-getpaid-parser) [![PyPI version](https://badge.fury.io/py/tqwgp-parser.svg)](https://pypi.python.org/pypi/tqwgp-parser/)

> Your text base sales and accounting toolkit, especially designed for freelancers, by freelancers

# Installing

```sh
pip install tqwgp-parser
```

# Usage

## Parsing proposals

First, declare your quote data:

```python
my_proposal = {
    "title": "Tesla Model 3 Configurator",
    "date": "29 novembre 2016",
    "place": "Philadelphie",
    "version": "v1",
    "sect": {
        "email": "bf@bf-printer.com",
        "logo": "tests/samples/tesla_logo.png",
        "name": "BF Printer \\& Co",
    },
    "legal": {
        "address": {
            "city": "Philadelphie",
            "line1": "E Thompson Saint",
            "zip": "19125",
        },
        "siret": "999999999 00099",
    },
    "author": {
        "civility": "M.",
        "mobile": "07.73.35.51.00",
        "name": "Benjamin Franklin",
        "role": "membre",
    },
    "client": {
        "contact": {
            "civility": "M.",
            "name": "Elon Musk",
            "role": "CEO",
            "sason": "son",
        },
        "legal": {
            "address": {
                "city": "Chambourcy",
                "line1": "103 Route de Mantes",
                "zip": "78240",
            },
            "siret": "524335262 00084",
        },
        "name": "Tesla",
    },
    "object": "The current proposal includes ...\n",
    "prestations": [
        {
            "description": "Files for describing the steps of product configuration, their prices, etc.",
            "price": 5000,
            "title": "Definition of configurations",
        }
    ],
}
```

> Note: your can look at more complete and various samples in [`tests/samples`](tests/samples).

You can then process this proposal data using `tqwgp_parser.parse_quote`:

```python
import pprint
from tqwgp_parser import parse_quote

my_parsed_proposal = parse_quote(my_proposal)
pprint.pprint(my_parsed_proposal)
```

> Pro-tip: the data can be declared in flat files, for eg. using Yaml or Json formats. It could also be loaded from a database: this is your choice!

## Parsing invoices

Declare your invoices data:

```python
my_invoices = {
    "sect": {"email": "bf@bf-printer.com", "name": "BF Printer \\& Co"},
    "legal": {
        "address": {
            "city": "Philadelphie",
            "line1": "E Thompson Saint",
            "zip": "19125",
        },
        "siret": "999999999 00099",
    },
    "author": {
        "civility": "M.",
        "mobile": "07.73.35.51.00",
        "name": "Benjamin Franklin",
        "role": "membre",
    },
    "client": {
        "contact": {
            "civility": "M.",
            "name": "Elon Musk",
            "role": "CEO",
            "sason": "son",
        },
        "legal": {
            "address": {
                "city": "Chambourcy",
                "line1": "103 Route de Mantes",
                "zip": "78240",
            },
            "siret": "524335262 00084",
        },
        "name": "Tesla",
    },
    "invoices": [
        {
            "date": "5 janvier 2017",
            "lines": [{"price": 12000, "title": "Acompte devis 16-TESLA-01"}],
            "number": "17001",
            "vat_rate": 20,
        }
    ],
}
```

And process it with the help of `tqwgp_parser.parse_invoices`:

```python
import pprint
from tqwgp_parser import parse_invoices

my_parsed_invoices = parse_invoices(my_invoices)
pprint.pprint(my_parsed_invoices)
```

## Going further

You could then feed the processed data to your own document edition toolchain to create PDFs from it. This could include using Pandoc and LaTeX to edit the PDF (see for eg. [mrzool's invoice-boilerplate](https://github.com/mrzool/invoice-boilerplate/) setup) ; or sending it to an online PDF compiler with your own template (for eg. with a LaTeX template and [LaTeX-on-HTTP](https://github.com/YtoTech/latex-on-http)), or using HTML/CSS based template (with tooks like [WeasyPrint](https://github.com/Kozea/WeasyPrint/tree/gh-pages/samples/invoice) or [ReLaXed](https://github.com/RelaxedJS/ReLaXed)).

You may also use the parsed data in a web application.

-------------------

# TQWGP text-base documents specification

The format of the TQWGP text-base documents is not finalized.

We'll use this repository as a working specification, through the [samples](tests/samples) and [tests](tests).


-------------------

# Contributing

## Tests

To contribute to the parser and specification, please wrote test samples for your modifications.

The tests are written for being runned with `pytest`:

```sh
pipenv run pytest -vv
```
