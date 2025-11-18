from datetime import datetime, timedelta
import random
from logic import *

rain = Symbol("rain")
wet_grass = Symbol("wet_grass")
umbrella = Symbol("umbrella")

knowledge = And(
    Implication(rain, wet_grass),    # Als het regent, wordt het gras nat
    Implication(wet_grass, umbrella) # Als het gras nat is, heb je een paraplu nodig
)


def generate_weather_data_with_dates():
    """
    Genereert weersgegevens voor 10 dagen vanaf de huidige datum.
    voobeeld genereet data:
    {'2025-01-25': {'name': 'Mark', 'rain': False}, '2025-01-26': {'name': 'Jan', 'rain': False}, '2025-01-27': {'name': 'Lisa', 'rain': False}, '2025-01-28': {'name': 'Anna', 'rain': False}, '2025-01-29': {'name': 'Jan', 'rain': False}, '2025-01-30': {'name': 'Sophie', 'rain': False}, '2025-01-31': {'name': 'Lisa', 'rain': False}, '2025-02-01': {'name': 'Anna', 'rain': False}, '2025-02-02': {'name': 'Sophie', 'rain': False}, '2025-02-03': {'name': 'Lisa', 'rain': False}}
    """
    data = {}
    today = datetime.now()
    names = ["Jan", "Anna", "Sophie", "Mark", "Lisa"] 
    
    for i in range(10):
        day_date = today + timedelta(days=i)
        is_raining = random.random() < 0.3  # 30% kans op regen
        person = random.choice(names)  # random persoon

        # Data per dag opslaan
        data[day_date.strftime("%Y-%m-%d")] = {
            "name": person,
            "rain": is_raining
        }
    return data

def generate_recommendations(data):
    """
    Gebruikt de dataset en kennisbasis om aanbevelingen te genereren.
    """
    print("Weeradvies voor de komende 10 dagen:\n")
    for date, info in data.items():
        person = info["name"]
        is_raining = info["rain"]

        model = And(
            rain if is_raining else Not(rain)
        )

        if model_check(And(knowledge, model), umbrella):
            print(f"{date}: Hallo {person}, het regent vandaag. Vergeet je paraplu niet!")
        else:
            print(f"{date}: Hallo {person}, geen regen vandaag. Een paraplu is niet nodig.")

if __name__ == "__main__":
    weather_data = generate_weather_data_with_dates()

    print("Weeradvies AI\n----------------")
    generate_recommendations(weather_data)
