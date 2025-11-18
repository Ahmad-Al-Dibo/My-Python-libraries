"""
Logische Uitdrukking Analyse:

De logische uitdrukking die je hebt gegeven kan worden opgesplitst en stap voor stap worden uitgelegd. De uitdrukking is:

((¬rain) => hagrid) ∧ (hagrid ∨ dumbledore) ∧ (¬(hagrid ∧ dumbledore)) ∧ dumbledore

---

1. ((¬rain) ⇒ hagrid)
- Dit is een implicatie:
  - "Als het niet regent (¬rain), dan geldt dat Hagrid waar moet zijn (hagrid)."
- Waarheidswaarden:
  - Deze implicatie is niet waar alleen als:
    - ¬rain waar is en hagrid onwaar is.
  - In andere gevallen is de implicatie waar.

---

2. (hagrid ∨ dumbledore)
- Dit is een disjunctie (of):
  - "Hagrid of Dumbledore moet waar zijn, of beide."
- Waarheidswaarden:
  - Deze uitspraak is waar als ten minste één van hagrid of dumbledore waar is.
  - Alleen als beiden onwaar zijn, is dit vals.

---

3. ¬(hagrid ∧ dumbledore)
- Dit is een negatie van een conjunctie:
  - "Het is niet zo dat zowel Hagrid als Dumbledore waar zijn."
- Waarheidswaarden:
  - Deze uitspraak is waar als:
    - Ofwel hagrid onwaar is, of
    - dumbledore onwaar is, of
    - Beiden onwaar zijn.
  - Het is alleen vals als zowel hagrid als dumbledore tegelijk waar zijn.

---

4. dumbledore
- Deze term stelt dat dumbledore waar is.

---

Gecombineerde Uitleg:
De volledige uitdrukking combineert de bovenstaande onderdelen met en (∧):

1. Als het niet regent, moet Hagrid waar zijn.
2. Hagrid of Dumbledore (of beiden) moet waar zijn.
3. Het is niet mogelijk dat zowel Hagrid als Dumbledore waar zijn.
4. Dumbledore moet waar zijn.

---

Conclusie:
1. Omdat dumbledore expliciet waar moet zijn, voldoet dit aan onderdeel 2 (hagrid ∨ dumbledore).
2. Onderdeel 3 (¬(hagrid ∧ dumbledore)) dwingt ons te concluderen dat hagrid niet waar kan zijn tegelijk met dumbledore.
3. Onderdeel 1 ((¬rain) ⇒ hagrid) speelt alleen een rol als het niet regent. Maar omdat hagrid niet tegelijk waar kan zijn met dumbledore, lijkt dit geen directe impact te hebben zolang dumbledore waar is.

Mogelijke interpretatie:
- dumbledore is waar.
- hagrid moet onwaar zijn.
- Of het regent (rain) of niet, heeft geen directe invloed zolang bovenstaande waar is.
"""

from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")


knowledge = And(
    Implication(Not(rain), hagrid),  # Als het niet regent, dan hagrid
    Or(hagrid, dumbledore),         # Hagrid of Dumbledore moet waar zijn
    Not(And(hagrid, dumbledore)),   # Hagrid en Dumbledore kunnen niet beide waar zijn
    dumbledore                      # Dumbledore is waar
)

# Resultaten tonen
print("Is het logisch dat het regent?")
print(f"Rain: {model_check(knowledge, rain)}")
print("\nIs Hagrid waar volgens de kennisbasis?")
print(f"Hagrid: {model_check(knowledge, hagrid)}")
print("\nIs Dumbledore waar volgens de kennisbasis?")
print(f"Dumbledore: {model_check(knowledge, dumbledore)}")
