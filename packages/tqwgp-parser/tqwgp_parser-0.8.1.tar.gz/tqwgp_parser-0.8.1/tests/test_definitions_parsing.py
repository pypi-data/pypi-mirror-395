# -*- coding: utf-8 -*-
"""
tests.test_definitions_parsing
~~~~~~~~~~~~~~~~~~~~~
Ensures definitions are well-parsed and that the format is normalized.
:copyright: (c) 2017-2021 Yoan Tournade.
"""
import codecs
import yaml
import os
import copy
import pprint
from tqwgp_parser import parse_quote, parse_invoices

SAMPLE_DIR = os.getcwd() + "/tests/samples/"


def load_definition_from_file(path):
    with codecs.open(path, "r", "utf-8") as f:
        content = f.read()
        return yaml.load(content, Loader=yaml.SafeLoader)


# ------------------------------------------------------------------------------
# Quotes.
# ------------------------------------------------------------------------------

TESLA_16_01_QUOTE = load_definition_from_file(SAMPLE_DIR + "16-TESLA-01/quote.yml")
TESLA_SECTIONS_QUOTE = load_definition_from_file(
    SAMPLE_DIR + "TESLA-SECTIONS/quote.yml"
)
TESLA_BATCHES_QUOTE = load_definition_from_file(SAMPLE_DIR + "TESLA-BATCHES/quote.yml")
TESLA_QUANTITIES_QUOTE = load_definition_from_file(
    SAMPLE_DIR + "TESLA-QUANTITIES/quote.yml"
)
COMMERCE_NESTED_OPTIONAL_QUOTE = load_definition_from_file(
    SAMPLE_DIR + "NESTED-OPTIONAL/quote.yml"
)

# TODO Make an universal data validation framework.
QUOTE_MANDATORY_ENTRIES = [
    "prestations",
    "all_prestations",
    "sections",
    "title",
    "date",
    "place",
    "sect",
    "legal",
    "client",
    "object",
    "batches",
    "optional_prestations",
    "price",
    "optional_price",
    "documents",
]
PRESTATION_MANDATORY_ENTRIES = [
    "title",
    "price",
    "description",
    "batch",
    "section",
    "optional",
]
SECTION_MANDATORY_ENTRIES = ["title", "price", "description", "prestations", "optional"]
BATCH_MANDATORY_ENTRIES = ["name", "price", "prestations"]
SECT_MANDATORY_ENTRIES = ["name", "email", "logo"]


def checkQuote(quote):
    for mandatoryEntry in QUOTE_MANDATORY_ENTRIES:
        assert mandatoryEntry in quote
    for sectEntry in SECT_MANDATORY_ENTRIES:
        assert sectEntry in quote["sect"]
    for prestation in quote["prestations"]:
        if "prestations" in prestation:
            # This is a section.
            for mandatoryEntry in SECTION_MANDATORY_ENTRIES:
                assert mandatoryEntry in prestation
                # TODO Make it recursive. One level max.
            for prestation in prestation["prestations"]:
                for mandatoryEntry in PRESTATION_MANDATORY_ENTRIES:
                    assert mandatoryEntry in prestation
        else:
            for mandatoryEntry in PRESTATION_MANDATORY_ENTRIES:
                assert mandatoryEntry in prestation
    for section in quote["sections"]:
        for mandatoryEntry in SECTION_MANDATORY_ENTRIES:
            assert mandatoryEntry in section
        for prestation in section["prestations"]:
            for mandatoryEntry in PRESTATION_MANDATORY_ENTRIES:
                assert mandatoryEntry in prestation
    for batch in quote["batches"]:
        for mandatoryEntry in BATCH_MANDATORY_ENTRIES:
            assert mandatoryEntry in batch
        for prestation in batch["prestations"]:
            for mandatoryEntry in PRESTATION_MANDATORY_ENTRIES:
                assert mandatoryEntry in prestation


def test_parse_simple_quote():
    """
    Parse a simple quote definition.
    """
    quote = parse_quote(TESLA_16_01_QUOTE)
    checkQuote(quote)
    assert quote["title"] == "Configurateur de Tesla Model 3"
    assert quote["sect"]["logo"]["path"] == "tests/samples/tesla_logo.png"
    assert quote["sect"]["logo"]["file"] == "tests/samples/tesla_logo.png"
    assert quote["price"]["total_vat_excl"] == 40000
    assert len(quote["prestations"]) == 4
    assert quote["optional_price"]["total_vat_excl"] == 14000
    assert len(quote["all_prestations"]) == 4
    assert len(quote["optional_prestations"]) == 1
    assert quote["has_quantities"] is False
    assert quote["prestations"][0]["title"] == "Création des configurations sur le CPQ"
    assert quote["prestations"][0]["price"] == 5000
    assert quote["prestations"][0]["optional"] is False
    assert quote["prestations"][2]["title"] == "Growth-hacking après mise en ligne"
    assert quote["prestations"][2]["price"] == 14000
    assert quote["prestations"][2]["optional"] is True
    assert (
        quote["optional_prestations"][0]["title"]
        == "Growth-hacking après mise en ligne"
    )
    assert quote["optional_prestations"][0]["price"] == 14000
    assert quote["optional_prestations"][0]["optional"] is True


def test_parse_quote_with_sections():
    """
    Parse a quote definition with prestation sections (recursive prestations).
    """
    quote = parse_quote(TESLA_SECTIONS_QUOTE)
    checkQuote(quote)
    assert quote["title"] == "Configurateur de Tesla Model 3"
    assert quote["sect"]["logo"] is None
    # Must always return a prestation list, flattened.
    assert len(quote["all_prestations"]) == 5
    # The not flattened representation.
    assert len(quote["prestations"]) == 3
    assert len(quote["sections"]) == 2
    assert len(quote["optional_prestations"]) == 0
    assert quote["price"]["total_vat_excl"] == 46300
    assert quote["optional_price"]["total_vat_excl"] == None
    assert (
        quote["all_prestations"][0]["title"] == "Création des configurations sur le CPQ"
    )
    assert quote["all_prestations"][0]["price"] == 5000
    assert (
        quote["all_prestations"][0]["section"] == "Développement du Nouveau CPQ Tesla"
    )
    assert quote["sections"][0]["title"] == "Développement du Nouveau CPQ Tesla"
    assert quote["sections"][0]["price"]["total_vat_excl"] == 15000
    assert quote["sections"][0]["optional_price"]["total_vat_excl"] == 15000
    assert (
        quote["sections"][1]["title"] == "Intégration e-commerce du CPQ sur tesla.com"
    )
    assert quote["sections"][1]["price"]["total_vat_excl"] == 6300
    assert quote["sections"][1]["optional_price"]["total_vat_excl"] == 6300


def test_parse_quote_with_batches():
    """
    Parse a quote definition with prestation batches (and sections).
    """
    quote = parse_quote(TESLA_BATCHES_QUOTE)
    checkQuote(quote)
    assert quote["sect"]["logo"] is None
    assert len(quote["all_prestations"]) == 5
    assert len(quote["prestations"]) == 3
    assert len(quote["sections"]) == 2
    assert len(quote["batches"]) == 3
    assert quote["price"]["total_vat_excl"] == 46300
    assert (
        quote["all_prestations"][0]["title"] == "Création des configurations sur le CPQ"
    )
    assert quote["all_prestations"][0]["price"] == 5000
    assert quote["batches"][0]["name"] == "1"
    assert quote["batches"][0]["price"] == 17000
    assert quote["batches"][1]["name"] == "2"
    assert quote["batches"][1]["price"] == 4300
    assert quote["batches"][2]["name"] == "3"
    assert quote["batches"][2]["price"] == 25000
    assert quote["all_prestations"][0]["batch"] == "1"
    assert quote["all_prestations"][1]["batch"] == "1"
    assert quote["all_prestations"][2]["batch"] == "1"
    assert quote["all_prestations"][3]["batch"] == "2"
    assert quote["all_prestations"][4]["batch"] == "3"
    assert quote["prestations"][0]["prestations"][0]["batch"] == "1"
    assert quote["prestations"][0]["prestations"][1]["batch"] == "1"
    assert quote["prestations"][1]["prestations"][0]["batch"] == "1"
    assert quote["prestations"][1]["prestations"][1]["batch"] == "2"
    assert quote["prestations"][2]["batch"] == "3"


def test_parse_quote_price_none():
    """
    A prestation price can be set to None (not specified).
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["prestations"][0]["price"] = None
    quote = parse_quote(definition)
    checkQuote(quote)
    assert quote["price"]["total_vat_excl"] == 35000
    assert len(quote["prestations"]) == 4
    assert quote["prestations"][0]["price"] == None


def test_parse_quote_price_string():
    """
    A prestation price can be set to a string.
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["prestations"][0]["price"] = "(inclus)"
    quote = parse_quote(definition)
    checkQuote(quote)
    assert quote["price"]["total_vat_excl"] == 35000
    assert len(quote["prestations"]) == 4
    assert quote["prestations"][0]["price"] == "(inclus)"


def test_parse_quote_price_all_none_or_string():
    """
    All prestation prices can be set to None or String. Then the total must be None.
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["prestations"][0]["price"] = None
    definition["prestations"][1]["price"] = "à définir"
    definition["prestations"][3]["price"] = "à définir"
    quote = parse_quote(definition)
    checkQuote(quote)
    assert quote["price"]["total_vat_excl"] == None
    assert quote["optional_price"]["total_vat_excl"] == 14000
    assert len(quote["prestations"]) == 4
    assert quote["prestations"][0]["price"] == None
    assert quote["prestations"][1]["price"] == "à définir"
    assert quote["prestations"][2]["price"] == 14000
    assert quote["prestations"][2]["optional"] is True


def test_parse_simple_quote_tva():
    """
    A prestation price can include VAT.
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["vat_rate"] = 20
    quote = parse_quote(definition)
    checkQuote(quote)
    assert len(quote["prestations"]) == 4
    assert quote["vat_rate"] == 20
    assert quote["price"]["total_vat_excl"] == 40000
    assert quote["price"]["vat"] == 8000
    assert quote["price"]["total_vat_incl"] == 48000


def test_parse_simple_quote_rounding():
    """
    Prestation prices are rounded by default.
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["vat_rate"] = 20
    definition["prestations"][0]["price"] = 2329.33
    quote = parse_quote(definition)
    checkQuote(quote)
    assert len(quote["prestations"]) == 4
    assert quote["vat_rate"] == 20
    assert quote["prestations"][0]["price"] == 2329.33
    assert quote["price"]["total_vat_excl"] == 37329.33
    assert quote["price"]["vat"] == 7465.87
    assert quote["price"]["total_vat_incl"] == 44795.2


def test_parse_simple_quote_with_formula():
    """
    Prestation prices can include formulas. (opt-in)
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["options"] = {
        **definition.get("options", {}),
        "price_formula": {"enabled": True},
    }
    definition["prestations"][0]["price"] = "=1000*0.3"
    definition["prestations"][1]["price"] = ""
    quote = parse_quote(definition)
    checkQuote(quote)
    assert len(quote["prestations"]) == 4
    assert quote["prestations"][0]["total"] == 300
    assert quote["prestations"][0]["price"] == 300
    assert quote["prestations"][1]["price"] == ""
    assert quote["prestations"][1]["total"] is None
    assert quote["price"]["total_vat_excl"] == 25300.0


def test_parse_simple_quote_no_optional_tva():
    """
    Parse a simple quote definition which include VAT but no optional.
    """
    definition = copy.deepcopy(TESLA_SECTIONS_QUOTE)
    definition["vat_rate"] = 20
    quote = parse_quote(definition)
    checkQuote(quote)
    assert quote["vat_rate"] == 20
    assert quote["title"] == "Configurateur de Tesla Model 3"
    assert len(quote["all_prestations"]) == 5
    assert len(quote["prestations"]) == 3
    assert len(quote["sections"]) == 2
    assert len(quote["optional_prestations"]) == 0
    assert quote["price"]["total_vat_excl"] == 46300
    assert quote["optional_price"]["total_vat_excl"] == None


def test_parse_quote_with_optional_sections():
    """
    Parse a quote definition with prestation optional sections.
    """
    definition = copy.deepcopy(TESLA_SECTIONS_QUOTE)
    definition["prestations"][1]["optional"] = True
    quote = parse_quote(definition)
    # import pprint
    # pprint.pprint(quote)
    checkQuote(quote)
    assert quote["title"] == "Configurateur de Tesla Model 3"
    # Must always return a prestation list, flattened.
    assert len(quote["all_prestations"]) == 5
    # The not flattened representation.
    assert len(quote["prestations"]) == 3
    assert len(quote["sections"]) == 2
    pprint.pprint(quote["optional_prestations"])
    assert len(quote["optional_prestations"]) == 2
    assert len(quote["optional_sections"]) == 1
    assert quote["price"]["total_vat_excl"] == 40000
    assert quote["optional_price"]["total_vat_excl"] == 6300
    assert quote["all_prestations"][2]["title"] == "Intégration Javascript"
    assert quote["all_prestations"][2]["price"] == 2000
    assert quote["all_prestations"][2]["optional"] == True
    assert quote["all_prestations"][3]["title"] == "Intégration CSS"
    assert quote["all_prestations"][3]["price"] == 4300
    assert quote["all_prestations"][3]["optional"] == True
    assert (
        quote["sections"][1]["title"] == "Intégration e-commerce du CPQ sur tesla.com"
    )
    assert quote["sections"][1]["price"]["total_vat_excl"] == None
    assert quote["sections"][1]["optional_price"]["total_vat_excl"] == 6300
    assert quote["sections"][1]["optional"] == True


def test_parse_quote_with_quantities():
    """
    Parse a quote definition including quantities.
    """
    quote = parse_quote(TESLA_QUANTITIES_QUOTE)
    checkQuote(quote)
    assert quote["title"] == "Configurateur de Tesla Model 3"
    assert quote["sect"]["logo"]["path"] == "tests/samples/tesla_logo.png"
    assert quote["sect"]["logo"]["file"] == "tests/samples/tesla_logo.png"
    assert quote["has_quantities"] is True
    assert quote["price"]["total_vat_excl"] == 35000
    assert len(quote["prestations"]) == 2
    assert len(quote["all_prestations"]) == 2
    assert len(quote["optional_prestations"]) == 0
    assert quote["prestations"][0]["title"] == "Création des configurations sur le CPQ"
    assert quote["prestations"][0]["price"] == 5000
    assert quote["prestations"][0]["total"] == 5000
    assert quote["prestations"][0]["optional"] is False
    assert quote["prestations"][0]["quantity"] == 1
    assert quote["prestations"][1]["title"] == "Intégration de l'UI"
    assert quote["prestations"][1]["price"] == 10000
    assert quote["prestations"][1]["total"] == 30000
    assert quote["prestations"][1]["optional"] is False
    assert quote["prestations"][1]["quantity"] == 3


def test_parse_nested_section_quote_with_optional():
    """
    Parse a quote definition with nested (in section) optional prestations.
    """
    quote = parse_quote(COMMERCE_NESTED_OPTIONAL_QUOTE)
    checkQuote(quote)
    assert quote["title"] == "Configurateur de Tesla Model 3"
    assert quote["price"]["total_vat_excl"] == 23940
    assert len(quote["prestations"]) == 2
    assert quote["optional_price"]["total_vat_excl"] == 400
    assert len(quote["all_prestations"]) == 5
    assert len(quote["optional_prestations"]) == 2
    assert quote["has_quantities"] is True
    assert quote["all_prestations"][2]["title"] == "Fonction spécial optionnelle n°1"
    assert quote["all_prestations"][2]["total"] == 320
    assert quote["all_prestations"][2]["optional"] is True
    assert (
        quote["optional_prestations"][0]["title"] == "Fonction spécial optionnelle n°1"
    )
    assert quote["optional_prestations"][0]["price"] == 80
    assert quote["optional_prestations"][0]["optional"] is True
    assert quote["sections"][0]["price"]["total_vat_excl"] == 19540
    assert quote["sections"][0]["optional_price"]["total_vat_excl"] == 19940
    assert quote["sections"][0]["optional"] == False
    assert quote["sections"][1]["price"]["total_vat_excl"] == 4400
    assert quote["sections"][1]["optional_price"]["total_vat_excl"] == 4400
    assert quote["sections"][1]["optional"] == False


def test_parse_simple_quote_discount_amount():
    """
    A prestation price can define a discount (amount).
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["vat_rate"] = 20
    definition["discount"] = 500
    quote = parse_quote(definition)
    checkQuote(quote)
    assert len(quote["prestations"]) == 4
    assert quote["discount"]["mode"] == "amount"
    assert quote["discount"]["value"] == 500
    assert quote["discount"]["title"] == None
    assert quote["price"]["gross_vat_excl"] == 40000
    assert quote["price"]["discount_vat_excl"] == 500
    assert quote["price"]["total_vat_excl"] == 39500
    assert quote["price"]["vat"] == 7900
    assert quote["price"]["total_vat_incl"] == 47400


def test_parse_simple_quote_discount_percent():
    """
    A prestation price can define a discount (percent).
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["vat_rate"] = 20
    definition["discount"] = "5%"
    quote = parse_quote(definition)
    checkQuote(quote)
    assert len(quote["prestations"]) == 4
    assert quote["discount"]["mode"] == "percent"
    assert quote["discount"]["value"] == 5
    assert quote["discount"]["title"] == None
    assert quote["price"]["gross_vat_excl"] == 40000
    assert quote["price"]["total_vat_excl"] == 38000
    assert quote["price"]["discount_vat_excl"] == 2000
    assert quote["price"]["vat"] == 7600
    assert quote["price"]["total_vat_incl"] == 45600


def test_parse_simple_quote_discount_spec():
    """
    A prestation price can define a discount (spec).
    """
    definition = copy.deepcopy(TESLA_16_01_QUOTE)
    definition["vat_rate"] = 20
    definition["discount"] = {
        "mode": "percent",
        "value": 5,
        "title": "Remise commerciale",
    }
    quote = parse_quote(definition)
    checkQuote(quote)
    assert len(quote["prestations"]) == 4
    assert quote["discount"]["mode"] == "percent"
    assert quote["discount"]["value"] == 5
    assert quote["discount"]["title"] == "Remise commerciale"
    assert quote["price"]["gross_vat_excl"] == 40000
    assert quote["price"]["total_vat_excl"] == 38000
    assert quote["price"]["discount_vat_excl"] == 2000
    assert quote["price"]["vat"] == 7600
    assert quote["price"]["total_vat_incl"] == 45600


# ------------------------------------------------------------------------------
# Invoices.
# ------------------------------------------------------------------------------

TESLA_16_01_INVOICE = load_definition_from_file(SAMPLE_DIR + "16-TESLA-01/invoices.yml")
TESLA_20_01_INVOICE = load_definition_from_file(
    SAMPLE_DIR + "TESLA-QUANTITIES/invoices.yml"
)

INVOICE_CLIENT_GENERAL = {
    "name": "General Internet",
    "legal": {
        "siret": None,
        "address": {
            "line1": "Rue du parc",
            "line2": "Tannerie",
            "zip": "93240",
            "city": "Montreuil",
            "country": "France",
        },
        "contact": {
            "civility": "M.",
            "name": "Gilbert du Motier de La Fayette",
            "role": "général",
            "sason": "son",
        },
    },
}

# TODO Make an universal data validation framework.
INVOICES_MANDATORY_ENTRIES = ["invoices"]
INVOICE_MANDATORY_ENTRIES = [
    "date",
    "sect",
    "legal",
    "client",
    "lines",
    "number",
    "price",
]
LINE_MANDATORY_ENTRIES = ["title", "price", "description"]
SECT_MANDATORY_ENTRIES = ["name", "email", "logo"]


def checkInvoices(invoices):
    for mandatoryEntry in INVOICES_MANDATORY_ENTRIES:
        assert mandatoryEntry in invoices
    for invoice in invoices["invoices"]:
        for mandatoryEntry in INVOICE_MANDATORY_ENTRIES:
            assert mandatoryEntry in invoice
        for sectEntry in SECT_MANDATORY_ENTRIES:
            assert sectEntry in invoice["sect"]
        for line in invoice["lines"]:
            for mandatoryEntry in LINE_MANDATORY_ENTRIES:
                assert mandatoryEntry in line


def test_parse_simple_invoices():
    """
    Parse simple invoices definition.
    """
    invoices = parse_invoices(TESLA_16_01_INVOICE)
    checkInvoices(invoices)
    assert len(invoices["invoices"]) == 3
    assert invoices["invoices"][0]["price"]["total_vat_incl"] == 12000
    assert invoices["invoices"][0]["number"] == "17001"
    assert invoices["invoices"][0]["sect"]["logo"] is None
    assert invoices["invoices"][0]["vat_rate"] is None
    assert invoices["invoices"][0]["display_project_reference"] is True
    assert invoices["invoices"][0]["title"] is None
    assert invoices["invoices"][0]["has_quantities"] is False
    assert "closing_note" in invoices["invoices"][0]
    assert len(invoices["invoices"][0]["lines"]) == 1
    assert invoices["invoices"][0]["lines"][0]["title"] == "Acompte devis 16-TESLA-01"
    assert invoices["invoices"][2]["title"] == "Solde du projet"


def test_parse_invoice_overriding():
    """
    Ensure common invoices attributes can be overriden on each invoice.
    """
    definitions = copy.deepcopy(TESLA_16_01_INVOICE)
    common_client = definitions["client"]
    definitions["invoices"][1]["client"] = INVOICE_CLIENT_GENERAL
    invoices = parse_invoices(definitions)
    checkInvoices(invoices)
    assert len(invoices["invoices"]) == 3
    assert invoices["invoices"][0]["client"] == common_client
    assert invoices["invoices"][1]["client"] == INVOICE_CLIENT_GENERAL
    assert invoices["invoices"][1]["sect"]["logo"]["path"] == "__logo.png"
    assert (
        invoices["invoices"][1]["sect"]["logo"]["url"]
        == "https://www.ytotech.com/static/images/ytotech_logo.png"
    )
    assert invoices["invoices"][2]["client"] == common_client


def test_parse_invoice_tva():
    """
    Parse invoices definition with VAT support.
    """
    definitions = copy.deepcopy(TESLA_16_01_INVOICE)
    definitions["invoices"][1]["vat_rate"] = 20
    definitions["invoices"][1]["display_project_reference"] = False
    invoices = parse_invoices(definitions)
    checkInvoices(invoices)
    assert len(invoices["invoices"]) == 3
    assert invoices["invoices"][0]["number"] == "17001"
    assert invoices["invoices"][0]["vat_rate"] == None
    assert invoices["invoices"][0]["display_project_reference"] == True
    assert invoices["invoices"][0]["price"]["vat"] == None
    assert invoices["invoices"][0]["price"]["total_vat_incl"] == 12000
    assert invoices["invoices"][0]["price"]["total_vat_excl"] == 12000
    # Check total with vat.
    assert invoices["invoices"][1]["number"] == "17002"
    assert invoices["invoices"][1]["vat_rate"] == 20
    assert invoices["invoices"][1]["display_project_reference"] == False
    assert invoices["invoices"][1]["price"]["total_vat_excl"] == 18000
    assert invoices["invoices"][1]["price"]["vat"] == 3600
    assert invoices["invoices"][1]["price"]["total_vat_incl"] == 21600
    assert invoices["invoices"][2]["number"] == "17003"
    assert invoices["invoices"][2]["price"]["vat"] == None
    assert invoices["invoices"][2]["price"]["total_vat_incl"] == 10000
    assert invoices["invoices"][2]["price"]["total_vat_excl"] == 10000


def test_parse_invoice_display_project_reference_true():
    """
    Check true is accepted for display_project_reference.
    """
    definitions = copy.deepcopy(TESLA_16_01_INVOICE)
    definitions["invoices"][0]["display_project_reference"] = True
    invoices = parse_invoices(definitions)
    checkInvoices(invoices)
    assert len(invoices["invoices"]) == 3
    assert invoices["invoices"][0]["number"] == "17001"
    assert invoices["invoices"][0]["display_project_reference"] == True


def test_parse_invoice_quantities():
    """
    Parse invoices definition with quantities support.
    """
    definitions = copy.deepcopy(TESLA_20_01_INVOICE)
    invoices = parse_invoices(definitions)
    checkInvoices(invoices)
    pprint.pprint(invoices["invoices"][0]["lines"])
    assert len(invoices["invoices"]) == 1
    assert invoices["invoices"][0]["number"] == "20001"
    assert invoices["invoices"][0]["vat_rate"] is None
    assert invoices["invoices"][0]["has_quantities"] is True
    assert invoices["invoices"][0]["price"]["total_vat_incl"] == 15000
    assert invoices["invoices"][0]["price"]["total_vat_excl"] == 15000
    # Check quantities of prestations.
    assert invoices["invoices"][0]["lines"][0]["quantity"] == 3
    assert invoices["invoices"][0]["lines"][0]["price"] == 1000
    assert invoices["invoices"][0]["lines"][0]["total"] == 3000
    assert invoices["invoices"][0]["lines"][1]["quantity"] == 1
    assert invoices["invoices"][0]["lines"][1]["price"] == 12000
    assert invoices["invoices"][0]["lines"][1]["total"] == 12000
