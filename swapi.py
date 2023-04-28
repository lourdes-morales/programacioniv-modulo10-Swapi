import requests
import json

def fetch_resource(resource):
    base_url = f"https://swapi.dev/api/{resource}/"
    results = []
    next_url = base_url

    while next_url:
        response = requests.get(next_url)
        data = json.loads(response.text)

        results.extend(data["results"])
        next_url = data["next"]

    return results

def is_wookiee(character):
    for species_url in character["species"]:
        response = requests.get(species_url)
        species_data = json.loads(response.text)
        if species_data["name"] == "Wookie":
            return True
    return False

def main():
    films = fetch_resource("films")
    planets = fetch_resource("planets")
    characters = fetch_resource("people")
    starships = fetch_resource("starships")

    # 1. ¿En cuántas películas hay planetas con climas áridos?
    arid_planets = [planet for planet in planets if "arid" in planet["climate"]]
    arid_planet_films = set()
    for planet in arid_planets:
        arid_planet_films.update(planet["films"])

    print(f"1. Hay {len(arid_planet_films)} películas con planetas de climas áridos.")

    # 2. ¿Cuántos Wookies aparecen en la sexta película?
    episode_6_characters = films[5]["characters"]
    wookies_in_episode_6 = [character for character in characters if character["url"] in episode_6_characters and is_wookiee(character)]

    print(f"2. Hay {len(wookies_in_episode_6)} Wookies en la sexta película.")

    # 3. ¿Cuál es el nombre de la aeronave más grande en toda la saga?
    largest_starship = max(starships, key=lambda x: float(x["length"].replace(",", "")) if x["length"] != "unknown" else 0)

    print(f"3. El nombre de la aeronave más grande en toda la saga es {largest_starship['name']}.")

if __name__ == "__main__":
    main()
