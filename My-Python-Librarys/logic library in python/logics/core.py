# core.py

from typing import Dict, Set, List, Union
from .data import VERBAND_CATEGORIEEN
from nltk.corpus import stopwords 
from typing import Optional, Set
import re
import nltk
import json




class VerbandExtractor:
    def __init__(self, verwijswoorden: List[str]):
        self.verwijswoorden = verwijswoorden
        self.verwijscategorisatie = self._map_woorden_naar_categorie()

    def _map_woorden_naar_categorie(self) -> Dict[str, str]:
        mapping = {}
        for categorie, woorden in VERBAND_CATEGORIEEN.items():
            for woord in woorden:
                mapping[woord.lower()] = categorie
        return mapping

    def extract_structuur(self, text: str, thema: str = "onbekend") -> Dict:
        text = re.sub(r"\n+", "\n", text.strip())
        zinnen = re.split(r"[.!?]\s+|\n", text)

        structuur = []

        for zin in zinnen:
            zin_lc = zin.lower()
            for woord in self.verwijswoorden:
                if woord in zin_lc:
                    verband = self.verwijscategorisatie.get(woord.lower())
                    if verband:
                        structuur.append({
                            "verband": verband,
                            "signaalwoord": woord,
                            "inhoud": zin.strip()
                        })
                        break  # voorkom dubbele extractie binnen 1 zin

        return {
            "thema": thema,
            "structuur": structuur
        }



class EvaluationException(Exception):
    """Raised when a variable is not found in the model."""
    pass


class Sentence:
    def evaluate(self, model: Dict[str, bool]) -> bool:
        raise Exception("Cannot evaluate abstract sentence")

    def formula(self) -> str:
        return ""

    def symbols(self) -> Set[str]:
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("Must be a logical sentence")

    @classmethod
    def parenthesize(cls, s: str) -> str:
        def balanced(s: str) -> bool:
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if not s or s.isalpha() or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])):
            return s
        return f"({s})"


class Symbol(Sentence):
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description or None

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name, self.description))

    def __repr__(self):
        return self.name

    def evaluate(self, model: Dict[str, bool]) -> bool:
        try:
            return bool(model[self.name])
        except KeyError:
            raise EvaluationException(f"Variable '{self.name}' not in model")

    def formula(self) -> str:
        return self.name

    def symbols(self) -> Set[str]:
        return {self.name}


class LiteralTrue(Sentence):
    def evaluate(self, model: Dict[str, bool]) -> bool:
        return True

    def formula(self) -> str:
        return "⊤"

    def symbols(self) -> Set[str]:
        return set()


class LiteralFalse(Sentence):
    def evaluate(self, model: Dict[str, bool]) -> bool:
        return False

    def formula(self) -> str:
        return "⊥"

    def symbols(self) -> Set[str]:
        return set()


class Not(Sentence):
    def __init__(self, operand: Sentence):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return not self.operand.evaluate(model)

    def formula(self) -> str:
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self) -> Set[str]:
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *disjuncts: Sentence):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)
        
    def __eq__(self, other):
        return isinstance(other, And) and self.disjuncts == other.conjuncts

    def __hash__(self):
        return hash(("and", tuple(hash(c) for c in self.disjuncts)))

    def __repr__(self):
        return f"And({', '.join(map(str, self.disjuncts))})"
    
    def add(self, disjunct):
        Sentence.validate(disjunct)
        self.disjuncts.append(disjunct)

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return all(c.evaluate(model) for c in self.disjuncts)

    def formula(self) -> str:
        return " ∧ ".join(Sentence.parenthesize(c.formula()) for c in self.disjuncts)

    def symbols(self) -> Set[str]:
        return set.union(*(c.symbols() for c in self.disjuncts))


class Or(Sentence):
    def __init__(self, *disjuncts: Sentence):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(("or", tuple(hash(d) for d in self.disjuncts)))

    def __repr__(self):
        return f"Or({', '.join(map(str, self.disjuncts))})"
    
    def add(self, disjunct):
        Sentence.validate(disjunct)
        self.disjuncts.append(disjunct)

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return any(d.evaluate(model) for d in self.disjuncts)

    def formula(self) -> str:
        return " ∨ ".join(Sentence.parenthesize(d.formula()) for d in self.disjuncts)

    def symbols(self) -> Set[str]:
        return set.union(*(d.symbols() for d in self.disjuncts))


class Xor(Sentence):
    def __init__(self, left: Sentence, right: Sentence):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return self.left.evaluate(model) != self.right.evaluate(model)

    def formula(self) -> str:
        return f"{Sentence.parenthesize(self.left.formula())} ⊕ {Sentence.parenthesize(self.right.formula())}"

    def symbols(self) -> Set[str]:
        return self.left.symbols() | self.right.symbols()

    def __repr__(self):
        return f"Xor({self.left}, {self.right})"

    def __eq__(self, other):
        return isinstance(other, Xor) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(("xor", hash(self.left), hash(self.right)))

class Implication(Sentence):
    def __init__(self, antecedent: Sentence, consequent: Sentence):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return not self.antecedent.evaluate(model) or self.consequent.evaluate(model)

    def formula(self) -> str:
        return f"{Sentence.parenthesize(self.antecedent.formula())} ⇒ {Sentence.parenthesize(self.consequent.formula())}"

    def symbols(self) -> Set[str]:
        return self.antecedent.symbols() | self.consequent.symbols()

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def __eq__(self, other):
        return isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent

    def __hash__(self):
        return hash(("implication", hash(self.antecedent), hash(self.consequent)))


class Biconditional(Sentence):
    def __init__(self, left: Sentence, right: Sentence):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return self.left.evaluate(model) == self.right.evaluate(model)

    def formula(self) -> str:
        return f"{Sentence.parenthesize(self.left.formula())} ⇔ {Sentence.parenthesize(self.right.formula())}"

    def symbols(self) -> Set[str]:
        return self.left.symbols() | self.right.symbols()

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def __eq__(self, other):
        return isinstance(other, Biconditional) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))


class Color:
    def __init__(self, r, g, b):
        self.r = self._clamp(r)
        self.g = self._clamp(g)
        self.b = self._clamp(b)

    def _clamp(self, val):
        return max(0, min(255, int(val)))

    def to_rgb(self):
        return (self.r, self.g, self.b)

    def to_hex(self):
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)

    def to_ansi(self, text="Color Sample"):
        return f"\033[38;2;{self.r};{self.g};{self.b}m{text}\033[0m"

    def darken(self, amount):
        return Color(self.r - amount, self.g - amount, self.b - amount)

    def lighten(self, amount):
        return Color(self.r + amount, self.g + amount, self.b + amount)

    def __repr__(self):
        return f"Color(RGB={self.to_rgb()}, HEX='{self.to_hex()}')"


class settings:
    def __init__(self, language:str):
        self.lang = language

    def ensure_nltk_stopwords_downloaded(self) -> bool:
        """Controleer of de NLTK stopwoorden gedownload zijn, anders downloaden."""
        try:
            stopwords.words(self.lang)
            return True
        except LookupError:
            print("📦 Downloading NLTK stopwords...")
            nltk.download("stopwords")


    def export_stopwords_to_file(self, of: Optional[str]="stopwoorden.txt") -> dict:
        """Exporteer stopwoorden van de opgegeven taal naar een tekstbestand.
        of: output file
        
        """
        try:
            stopwoorden = stopwords.words(self.lang)
        except LookupError:
            print("📦 Downloading NLTK stopwords...")
            nltk.download("stopwords")
            stopwoorden = stopwords.words(self.lang)

        with open(of, "w", encoding="utf-8") as f:
            for woord in sorted(stopwoorden):
                f.write(woord + "\n")

        return stopwoorden

    def load_stopwords_from_file(self, fp: Optional[str]=None) -> dict:
        if fp is None:
            return None
        with open(fp, "r", encoding="utf-8") as f:
            stopwoorden = {line.strip() for line in f if line.strip()}
        return stopwoorden

    def load_conversations_json(self, fp: Optional[str] = None) -> dict:
        """Laad JSON data uit bestand als pad is opgegeven, anders None."""
        if fp is None:
            return None
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f)

class LogicaOptions:
    def __init__(self, rules: Dict[str, str], logic_connectors: Dict[str, str], stopwords: Dict[str, str],
                 verwijswoorden: Optional[List[str]] = None, TEKENS: Optional[List[str]] = None):
        self.rules = rules
        self.logic_connectors = logic_connectors
        self.stopwords = stopwords or {}
        self.verwijswoorden = verwijswoorden or []
        self.tokens = TEKENS or []

    @staticmethod
    def model_check(knowledge, query) -> bool:
        """Check if knowledge entails query using truth-table enumeration."""
        def check_all(knowledge, query, symbols, model):
            if not symbols:
                if knowledge.evaluate(model):
                    return query.evaluate(model)
                return True
            else:
                remaining = symbols.copy()
                p = remaining.pop()
                return (
                    check_all(knowledge, query, remaining, {**model, p: True}) and
                    check_all(knowledge, query, remaining, {**model, p: False})
                )

        all_symbols = knowledge.symbols() | query.symbols()
        return check_all(knowledge, query, all_symbols, {})

    def grammar(self, input_text: str) -> tuple[str, dict]:
        """
        Verwacht input in format 'variabele: logische expressie'
        Zet Nederlandse logische termen om en haalt verwijsteksten op.
        """
        if ":" in input_text:
            var, expr = input_text.split(":", 1)
        else:
            var = "result"
            expr = input_text

        var = var.strip()
        expr = expr.strip().lower()

        expr = self.replace_logic_phrases(expr)
        expr = self.replace_connectors(expr)

        woorden = expr.split()
        verwijzingen = {}
        resultaat_woorden = []

        i = 0
        while i < len(woorden):
            woord = woorden[i]
            if woord in self.verwijswoorden:
                verwijzing = []
                i += 1
                while i < len(woorden) and woorden[i] not in self.tokens:
                    verwijzing.append(woorden[i])
                    i += 1
                verwijzingen[woord] = " ".join(verwijzing)
            else:
                resultaat_woorden.append(woord)
                i += 1

        resultaat_expr = f"{var} = {' '.join(resultaat_woorden)}"
        return resultaat_expr, verwijzingen


    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s:=<>!]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        woorden = text.split()
        gefilterd = [woord for woord in woorden if woord not in self.stopwords]

        return " ".join(gefilterd)

    def replace_logic_phrases(self, text: str) -> str:
        # Vervang eerst langere zinnen, daarom sorteren op lengte aflopend
        for phrase, symbol in sorted(self.rules.items(), key=lambda x: -len(x[0])):
            text = text.replace(phrase, f" {symbol} ")
        return text

    def replace_connectors(self, text: str) -> str:
        for nl_word, py_word in self.logic_connectors.items():
            text = re.sub(fr"\b{nl_word}\b", py_word, text)
        return text
