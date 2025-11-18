# Logical rules in NL
LOGIC_CONNECTORS = {
    "en": "∧",
    "of": "∨",
    "niet": "¬",
    "als ... dan": "→",
    "als en slechts als": "↔"
}

# Common stopwords in NL
STOPWORDS = {
    "de", "het", "een", "en", "of", "maar", "want", "om", "te", "dat", "die",
    "dit", "wat", "wie", "waar", "waarom", "hoe", "als", "dan", "toen",
    "nu", "daarom", "dus", "niet", "geen", "alleen", "ook", "nog",
    "bijvoorbeeld", "zoals", "namelijk", "immers",
}

# Simple logic connectives in NL
VERBAND_CATEGORIEEN = {
    "tijd": [
        "voordat", "vroeger", "aanvankelijk", "eerst", "eerder", "nadat", "daarna",
        "later", "wanneer", "intussen", "tegelijkertijd", "tijdens",
    ],
    "opsomming": [
        "ook", "verder", "ten eerste", "ten tweede", "eerste plaats",
        "in de tweede plaats", "daarnaast", "bovendien", "vervolgens",
        "ten slotte", "als laatste", "niet alleen", "zowel",
        "een ander argument", "er is nog een reden waarom",
    ],
    "tegenstelling": [
        "maar", "echter", "toch", "niettemin", "desalniettemin", "desondanks",
        "daarentegen", "enerzijds", "anderzijds", "hoewel", "ofschoon",
        "integendeel", "daar staat tegenover", "behalve als", "weliswaar…. maar",
    ],
    "vergelijking": [
        "net zoals", "hetzelfde als", "evenals", "evenzeer", "overeenkomstig",
        "lijkt op", "is vergelijkbaar met",
    ],
    "voorbeeld": [
        "bijvoorbeeld", "een voorbeeld", "zo", "ter illustratie", "dat wil zeggen",
        "zoals", "onder andere", "te denken valt aan", "je moet daarbij denken aan",
    ],
    "oorzaak-gevolg": [
        "want", "doordat", "daardoor", "waardoor", "dat komt door",
        "dat heeft alles te maken met", "door", "door dit alles", "op grond van",
        "ten gevolge van", "als gevolg van",
    ],
    "doel-middel": [
        "om te", "opdat", "door middel van", "daarmee",
        "is erop gericht", "daartoe",
    ],
    "reden": [
        "omdat", "namelijk", "daarom", "aangezien", "immers", "om die reden",
    ],
    "voorwaarde": [
        "als", "indien", "tenzij", "mits", "aangenomen dat", "gesteld dat",
    ],
    "samenvatting": [
        "samengevat", "kortom", "al met al", "terugblikkend", "zoals gezegd",
        "ofwel", "oftewel", "anders gezegd", "het komt erop neer dat",
    ],
    "conclusie": [
        "dus", "concluderend", "daaruit", "hieruit volgt", "vandaar dat",
        "uit dit alles blijkt"
    ]
}

# Punctuation marks to consider
TEKENS = {".", ",", "!", "?", ";", ":", "-", "(", ")", "[", "]", "{", "}", "\"", "'"}
