import json
from logic import Symbol, And, Or, Not, Implication

# Dataset laden
with open("Game-AI/data/animals.json", "r") as f:
    dataset = json.load(f)["animals"]

# Symbolen en eigenschappen definiëren
has_fur = Symbol("has_fur")
can_fly = Symbol("can_fly")
lives_in_water = Symbol("lives_in_water")
is_domestic = Symbol("is_domestic")
size_small = Symbol("size_small")
size_medium = Symbol("size_medium")
size_large = Symbol("size_large")

# Kennisbasis opstellen
knowledge = And(
    Implication(has_fur, Not(lives_in_water)),  # Dieren met vacht leven niet in water
    Implication(can_fly, Not(lives_in_water)),  # Vliegende dieren leven niet in water
    Implication(size_large, Not(size_small)),   # Groot en klein zijn exclusief
    Implication(size_medium, Not(size_large)),  # Middelgroot en groot zijn exclusief
)

# Functie om overeenkomsten te berekenen
def calculate_similarity(animal, answers):
    """
    Bereken hoe goed een dier overeenkomt met de antwoorden.
    :param animal: Een dier uit de dataset (dictionary).
    :param answers: De antwoorden van de speler (dictionary).
    :return: Percentage overeenkomst (0-100).
    """
    total_questions = len(answers)
    matching_answers = 0

    # Controleer elk antwoord
    for key, answer in answers.items():
        if key in animal and animal[key] == answer:
            matching_answers += 1

    # Bereken percentage overeenkomst
    return (matching_answers / total_questions) * 100

# Vragen stellen en antwoorden verzamelen
def ask_questions():
    """
    Stelt vragen en verzamelt antwoorden van de speler.
    :return: Een dictionary met de antwoorden van de speler.
    """
    answers = {}

    questions = {
        "has_fur": "Heeft het dier vacht?",
        "can_fly": "Kan het dier vliegen?",
        "lives_in_water": "Leeft het dier in water?",
        "is_domestic": "Is het dier gedomesticeerd?",
        "size_small": "Is het dier klein van formaat?",
        "size_medium": "Is het dier middelgroot?",
        "size_large": "Is het dier groot van formaat?"
    }

    for key, question in questions.items():
        while True:
            try:
                print(knowledge.formula())
                response = input(f"{question} (ja/nee): ").strip().lower()
                if response == "ja":
                    answers[key] = True
                    knowledge.add(Symbol(key))  # Voeg kennis toe
                    break
                elif response == "nee":
                    answers[key] = False
                    knowledge.add(Not(Symbol(key)))  # Voeg kennis toe
                    break
                else:
                    print("Ongeldig antwoord. Voer 'ja' of 'nee' in.")
            except Exception as e:
                print(f"Er ging iets fout: {e}")
                continue

    print(knowledge.formula())

    return answers

# Hoofdprogramma
def main():
    print("Raad het Dier - AI Game met Kennisbasis")
    print("---------------------------------------")
    
    # Antwoorden ophalen
    answers = ask_questions()
    
    # Zoek dieren met overeenkomsten
    best_match = None
    highest_similarity = 0
    threshold = 60  # Minimale overeenkomst in procenten

    for animal in dataset:
        # Creëer een model van het dier
        model = {
            Symbol("has_fur"): animal["has_fur"],
            Symbol("can_fly"): animal["can_fly"],
            Symbol("lives_in_water"): animal["lives_in_water"],
            Symbol("is_domestic"): animal["is_domestic"],
            Symbol("size_small"): animal["size"] == "small",
            Symbol("size_medium"): animal["size"] == "medium",
            Symbol("size_large"): animal["size"] == "large"
        }
        
        # Controleer of kennisbasis klopt met het dier
        if knowledge.evaluate(model):
            similarity = calculate_similarity(animal, answers)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = animal

    # Resultaat tonen
    if best_match and highest_similarity >= threshold:
        print(f"Ik denk dat het dier een {best_match['name']} is! ({highest_similarity:.2f}% overeenstemming)")
    elif best_match:
        print(f"Ik weet het niet zeker, maar het lijkt het meest op een {best_match['name']} ({highest_similarity:.2f}% overeenstemming)")
    else:
        print("Ik kon geen dier vinden dat overeenkomt met de antwoorden.")

if __name__ == "__main__":
    main()


"""

"""